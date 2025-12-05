import asyncio
import importlib
import unittest
from unittest import mock
import os

from transcribe import app as transcribe_app


class DummyUploadFile:
    filename = "sample.wav"
    content_type = "audio/wav"

    async def read(self):
        return b"audio-bytes"


class DummyModel:
    def transcribe(self, *_args, **_kwargs):
        return {"text": " raw Whisper text ", "language": "en"}


class DummyCleanupClient:
    def __init__(self):
        self.seen = []

    def clean_text(self, raw_text: str) -> str:
        self.seen.append(raw_text)
        return f"cleaned {raw_text.strip()}"


class DummyResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


class CleanupFlowTest(unittest.TestCase):
    def setUp(self):
        self._engine_app = None

    def load_engine_app(self):
        """Reload payroll engine with BigQuery stubbed so tests stay offline."""

        if self._engine_app is None:
            with mock.patch("google.cloud.bigquery.Client") as client_mock:
                client_mock.return_value = mock.Mock()
                self._engine_app = importlib.reload(
                    importlib.import_module("engine.payroll_engine")
                )
        return self._engine_app

    def test_transcribe_runs_cleanup_before_returning(self):
        dummy_cleanup = DummyCleanupClient()
        original_cleanup_client = transcribe_app.cleanup_client
        original_load_model = transcribe_app.load_model

        # Swap in the dummy implementations so the test does not hit Whisper or the network.
        transcribe_app.cleanup_client = dummy_cleanup
        transcribe_app.load_model = lambda: DummyModel()

        try:
            result = asyncio.run(transcribe_app.transcribe(DummyUploadFile(), None))
        finally:
            transcribe_app.cleanup_client = original_cleanup_client
            transcribe_app.load_model = original_load_model

        self.assertEqual(result["raw_text"], "raw Whisper text")
        self.assertEqual(result["text"], "cleaned raw Whisper text")
        self.assertEqual(dummy_cleanup.seen, ["raw Whisper text"])

    def test_engine_prefers_cleaned_text_from_transcriber(self):
        engine_app = self.load_engine_app()
        original_post = engine_app.requests.post

        def fake_post(_url, _files=None, timeout=0, **_kwargs):
            assert timeout == 180
            return DummyResponse({"text": "cleaned transcript", "raw_text": " messy text "})

        engine_app.requests.post = fake_post

        try:
            cleaned = asyncio.run(engine_app.transcribe_audio(DummyUploadFile()))
        finally:
            engine_app.requests.post = original_post

        self.assertEqual(cleaned, "cleaned transcript")

    def test_cleanup_client_falls_back_to_raw_on_error(self):
        from transcribe.cleanup.llm_cleanup import LlmCleanupClient

        client = LlmCleanupClient(endpoint_url="https://cleanup.example.com")

        with mock.patch("transcribe.cleanup.llm_cleanup.requests.post") as post:
            post.side_effect = RuntimeError("network fail")

            cleaned = client.clean_text(" raw sample ")

        self.assertEqual(cleaned, "raw sample")
        post.assert_called_once()

    def test_cleanup_client_uses_configurable_timeout(self):
        from transcribe.cleanup.llm_cleanup import LlmCleanupClient

        client = LlmCleanupClient(endpoint_url="https://cleanup.example.com", timeout_seconds=5)

        with mock.patch("transcribe.cleanup.llm_cleanup.requests.post") as post:
            post.return_value = DummyResponse({"cleaned_text": "polished"})

            cleaned = client.clean_text("   text   ")

        self.assertEqual(cleaned, "polished")
        post.assert_called_once()
        _args, kwargs = post.call_args
        self.assertEqual(kwargs["timeout"], 5)

    def test_cleanup_client_respects_timeout_env(self):
        from transcribe.cleanup.llm_cleanup import LlmCleanupClient

        with mock.patch.dict(os.environ, {"TRANSCRIBE_CLEANUP_TIMEOUT_SECONDS": "7.5"}):
            client = LlmCleanupClient(endpoint_url="https://cleanup.example.com", timeout_seconds=None)

        self.assertEqual(client.timeout_seconds, 7.5)

    def test_cleanup_client_handles_invalid_timeout_env(self):
        from transcribe.cleanup.llm_cleanup import LlmCleanupClient

        with mock.patch.dict(os.environ, {"TRANSCRIBE_CLEANUP_TIMEOUT_SECONDS": "not-a-number"}):
            client = LlmCleanupClient(endpoint_url="https://cleanup.example.com", timeout_seconds=None)

        self.assertEqual(client.timeout_seconds, 30.0)


if __name__ == "__main__":
    unittest.main()
