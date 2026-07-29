"""Probe the Docker preview without following redirects."""

from __future__ import annotations

from http.client import HTTPConnection, HTTPException
from typing import Protocol

PREVIEW_HEALTH_HOST = "127.0.0.1"
PREVIEW_HEALTH_PORT = 8000
PREVIEW_HEALTH_PATH = "/opi-wiki/"
PREVIEW_HEALTH_TIMEOUT_SECONDS = 2.0


class PreviewHealthError(RuntimeError):
    """Report that the Docker preview did not return its canonical page."""


class HealthResponse(Protocol):
    """Response fields needed by the preview probe."""

    @property
    def status(self) -> int:
        """Return the HTTP status code."""

    @property
    def reason(self) -> str:
        """Return the HTTP reason phrase."""


class HealthConnection(Protocol):
    """HTTP connection operations needed by the preview probe."""

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str],
    ) -> None:
        """Send one request."""

    def getresponse(self) -> HealthResponse:
        """Return the server response without redirect handling."""

    def close(self) -> None:
        """Close the connection."""


def _preview_connection() -> HealthConnection:
    """Create the loopback connection used inside the preview container."""

    return HTTPConnection(
        PREVIEW_HEALTH_HOST,
        PREVIEW_HEALTH_PORT,
        timeout=PREVIEW_HEALTH_TIMEOUT_SECONDS,
    )


def require_preview_health(connection: HealthConnection | None = None) -> None:
    """Require an exact HTTP 200 from the canonical preview path.

    ``http.client`` deliberately has no redirect-following behavior. A redirect
    therefore reaches the explicit status check instead of making a different
    location appear healthy.
    """

    active_connection = connection if connection is not None else _preview_connection()
    try:
        active_connection.request(
            "GET",
            PREVIEW_HEALTH_PATH,
            headers={"Connection": "close"},
        )
        response = active_connection.getresponse()
    except (HTTPException, OSError) as error:
        raise PreviewHealthError("unable to request the canonical Docker preview page") from error
    finally:
        active_connection.close()

    if response.status != 200:
        raise PreviewHealthError(
            "canonical Docker preview page must return HTTP 200 without a redirect; "
            f"received {response.status} {response.reason}"
        )
