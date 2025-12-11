"""Orchestrator for the Transrouter pipeline.

Responsibilities:
- Entrypoints for audio/text handling
- Wire ASR -> intent classification -> entity extraction -> routing
- Return RouterResponse
"""

import base64
import binascii
from pathlib import Path
from typing import Any, Callable, Dict, Optional

from . import intent_classifier, entity_extractor, domain_router, logging_utils
from .asr_adapter import ASRAdapter, get_asr_provider
from .schemas import (
    AudioRequest,
    EntityExtraction,
    IntentClassification,
    RouterResponse,
    TranscriptResult,
)

DEFAULT_CONFIG = {
    "asr": {"provider": "whisper", "language": "en", "timeout_seconds": 120, "whisper_model": "base"},
    "routing": {"default_domain": "payroll", "fallback_intent": "unknown"},
    "logging": {"level": "INFO"},
}


def load_default_config() -> Dict[str, Any]:
    """Load config from default.yaml if available, else use in-memory defaults."""
    config_path = Path(__file__).resolve().parent.parent / "config" / "default.yaml"
    if config_path.exists():
        try:
            import yaml  # type: ignore

            with config_path.open("r", encoding="utf-8") as f:
                loaded = yaml.safe_load(f) or {}
                return {**DEFAULT_CONFIG, **loaded}
        except Exception:
            # Fall back silently to defaults if PyYAML is missing or file malformed.
            return DEFAULT_CONFIG
    return DEFAULT_CONFIG


def _resolve_audio_bytes(audio_request: AudioRequest) -> bytes:
    if audio_request.audio_bytes:
        return audio_request.audio_bytes
    b64 = audio_request.audio_base64 or audio_request.meta.get("audio_base64")
    if not b64:
        raise ValueError("AudioRequest must include audio_bytes or audio_base64")
    try:
        return base64.b64decode(b64)
    except binascii.Error as exc:
        raise ValueError("Invalid base64 audio payload") from exc


def handle_audio_request(
    audio_request: AudioRequest,
    *,
    asr_provider: Optional[ASRAdapter] = None,
    classifier: Callable[[str, Dict[str, Any]], tuple] = intent_classifier.classify_intent,
    extractor: Callable[[str, Dict[str, Any]], tuple] = entity_extractor.extract_entities,
    router: Callable[[str, str, Dict[str, Any], Dict[str, Any]], RouterResponse] = domain_router.route_request,
    logger=None,
    config: Optional[Dict[str, Any]] = None,
) -> RouterResponse:
    """Main entry for audio requests: transcribe -> interpret -> route."""
    logger = logger or logging_utils.get_logger("transrouter.orchestrator")
    config = config or load_default_config()

    try:
        audio_bytes = _resolve_audio_bytes(audio_request)
    except Exception as exc:
        return RouterResponse(domain=None, intent=None, entities={}, payload=None, errors=[str(exc)])

    meta = dict(audio_request.meta)
    meta.update({"audio_format": audio_request.audio_format, "sample_rate_hz": audio_request.sample_rate_hz})

    provider = asr_provider or get_asr_provider(config)
    try:
        transcript_result: TranscriptResult = provider.transcribe(
            audio_bytes, audio_request.audio_format, audio_request.sample_rate_hz
        )
        logging_utils.log_event(logger, "asr.transcribed", {"confidence": transcript_result.confidence})
    except Exception as exc:
        return RouterResponse(domain=None, intent=None, entities={}, payload=None, errors=[f"ASR failed: {exc}"])

    return _handle_text_core(
        transcript_result.transcript,
        meta,
        classifier=classifier,
        extractor=extractor,
        router=router,
        logger=logger,
        transcript_result=transcript_result,
    )


def handle_text_request(
    transcript: str,
    meta: Dict[str, Any],
    *,
    classifier: Callable[[str, Dict[str, Any]], tuple] = intent_classifier.classify_intent,
    extractor: Callable[[str, Dict[str, Any]], tuple] = entity_extractor.extract_entities,
    router: Callable[[str, str, Dict[str, Any], Dict[str, Any]], RouterResponse] = domain_router.route_request,
    logger=None,
) -> RouterResponse:
    """Entry for pre-transcribed text: interpret -> route."""
    logger = logger or logging_utils.get_logger("transrouter.orchestrator")
    transcript_result = TranscriptResult(transcript=transcript)
    return _handle_text_core(
        transcript,
        meta,
        classifier=classifier,
        extractor=extractor,
        router=router,
        logger=logger,
        transcript_result=transcript_result,
    )


def _handle_text_core(
    transcript: str,
    meta: Dict[str, Any],
    *,
    classifier: Callable[[str, Dict[str, Any]], tuple],
    extractor: Callable[[str, Dict[str, Any]], tuple],
    router: Callable[[str, str, Dict[str, Any], Dict[str, Any]], RouterResponse],
    logger,
    transcript_result: TranscriptResult,
) -> RouterResponse:
    try:
        domain_agent, intent_type, intent_conf = classifier(transcript, meta)
        intent = IntentClassification(domain_agent=domain_agent, intent_type=intent_type, confidence=intent_conf)
        logging_utils.log_event(logger, "intent.classified", intent.__dict__)
    except Exception as exc:
        return RouterResponse(domain=None, intent=None, entities={}, payload=None, errors=[f"Intent failed: {exc}"])

    try:
        entities, ent_conf = extractor(transcript, meta)
        extraction = EntityExtraction(entities=entities, confidence=ent_conf)
        logging_utils.log_event(logger, "entities.extracted", extraction.__dict__)
    except Exception as exc:
        return RouterResponse(
            domain=intent.domain_agent,
            intent=intent.intent_type,
            entities={},
            payload=None,
            errors=[f"Entity extraction failed: {exc}"],
        )

    response = router(intent.domain_agent, intent.intent_type, extraction.entities, meta)
    response.transcript = transcript_result.transcript
    response.intent_confidence = intent.confidence
    response.entity_confidence = extraction.confidence
    response.decision_reason = f"rule_based:{intent.intent_type}"
    logging_utils.log_event(logger, "router.routed", response.__dict__)
    return response
