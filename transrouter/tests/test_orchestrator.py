"""Stub tests for the Transrouter orchestrator."""

from transrouter.src import transrouter_orchestrator as orch


def test_handle_audio_request_not_implemented():
    """Placeholder to assert the orchestrator is still a stub."""
    try:
        orch.handle_audio_request(None)  # type: ignore[arg-type]
    except NotImplementedError:
        pass
    else:
        raise AssertionError("handle_audio_request should not be implemented yet")


def test_handle_text_request_not_implemented():
    """Placeholder to assert the orchestrator is still a stub."""
    try:
        orch.handle_text_request("", {})  # type: ignore[arg-type]
    except NotImplementedError:
        pass
    else:
        raise AssertionError("handle_text_request should not be implemented yet")
