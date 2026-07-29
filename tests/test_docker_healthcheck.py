"""Tests for the Docker preview's exact HTTP health probe."""

from __future__ import annotations

from dataclasses import dataclass
from http.client import RemoteDisconnected

import pytest
import scripts.docker_healthcheck as health_cli
import scripts.repo_tools.docker_health as docker_health
from scripts.repo_tools.docker_health import (
    HealthResponse,
    PreviewHealthError,
    require_preview_health,
)


@dataclass(frozen=True)
class _Response:
    """Minimal HTTP response used by the probe tests."""

    status: int
    reason: str


class _Connection:
    """Record the exact request while returning a controlled response."""

    def __init__(
        self,
        response: _Response | None = None,
        *,
        error: OSError | RemoteDisconnected | None = None,
    ) -> None:
        self.response = response
        self.error = error
        self.requests: list[tuple[str, str, dict[str, str]]] = []
        self.closed = False

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str],
    ) -> None:
        """Record the request or raise the configured transport failure."""

        self.requests.append((method, url, headers))
        if self.error is not None:
            raise self.error

    def getresponse(self) -> HealthResponse:
        """Return the configured response."""

        assert self.response is not None
        return self.response

    def close(self) -> None:
        """Record that the IO boundary always closes its connection."""

        self.closed = True


def test_require_preview_health_accepts_only_the_canonical_http_200() -> None:
    """The probe must request the exact canonical path and accept HTTP 200."""

    connection = _Connection(_Response(status=200, reason="OK"))

    require_preview_health(connection)

    assert connection.requests == [("GET", "/opi-wiki/", {"Connection": "close"})]
    assert connection.closed


def test_require_preview_health_connects_to_the_exact_loopback_endpoint(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The default probe must pin the container's canonical host, port, and timeout."""

    connection = _Connection(_Response(status=200, reason="OK"))
    connection_arguments: list[tuple[str, int, float]] = []

    def connection_factory(
        host: str,
        port: int,
        *,
        timeout: float,
    ) -> _Connection:
        connection_arguments.append((host, port, timeout))
        return connection

    monkeypatch.setattr(docker_health, "HTTPConnection", connection_factory)

    require_preview_health()

    assert connection_arguments == [("127.0.0.1", 8000, 2.0)]
    assert connection.requests == [("GET", "/opi-wiki/", {"Connection": "close"})]


def test_require_preview_health_rejects_a_redirect_without_following_it() -> None:
    """A redirect must not make a different destination appear healthy."""

    connection = _Connection(_Response(status=302, reason="Found"))

    with pytest.raises(
        PreviewHealthError,
        match=r"must return HTTP 200 without a redirect; received 302 Found",
    ):
        require_preview_health(connection)

    assert connection.requests == [("GET", "/opi-wiki/", {"Connection": "close"})]
    assert connection.closed


def test_require_preview_health_wraps_transport_failures() -> None:
    """Connection failures must become a stable, actionable probe error."""

    connection = _Connection(error=ConnectionRefusedError("not listening"))

    with pytest.raises(
        PreviewHealthError,
        match="unable to request the canonical Docker preview page",
    ):
        require_preview_health(connection)

    assert connection.closed


def test_docker_healthcheck_cli_reports_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The runtime CLI must return zero after a healthy probe."""

    monkeypatch.setattr(health_cli, "require_preview_health", lambda: None)

    assert health_cli.main() == 0


def test_docker_healthcheck_cli_reports_failure(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The runtime CLI must expose the probe failure and return nonzero."""

    def fail() -> None:
        raise PreviewHealthError("received 302 Found")

    monkeypatch.setattr(health_cli, "require_preview_health", fail)

    assert health_cli.main() == 1
    assert capsys.readouterr().err == ("Docker preview is unhealthy: received 302 Found\n")
