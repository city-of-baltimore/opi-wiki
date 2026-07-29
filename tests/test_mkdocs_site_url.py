"""Tests for the externally visible MkDocs preview URL hook."""

from __future__ import annotations

from io import StringIO
from pathlib import Path

import pytest
import yaml
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.utils.yaml import yaml_load
from scripts.mkdocs_site_url import on_config


def _runtime_config(site_url: str) -> MkDocsConfig:
    """Return a minimal MkDocs config at the URL rewritten by ``serve``."""

    config = MkDocsConfig()
    config.site_url = site_url
    return config


def test_site_url_hook_is_a_noop_without_an_explicit_override(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Ordinary builds and task-based serving should retain MkDocs's selected URL."""

    monkeypatch.delenv("OPI_SITE_URL", raising=False)
    config = _runtime_config("http://127.0.0.1:5208/opi-wiki/")

    assert on_config(config) is config
    assert config.site_url == "http://127.0.0.1:5208/opi-wiki/"


@pytest.mark.parametrize(
    ("requested_url", "expected_url"),
    (
        (
            "http://127.0.0.1:5208/opi-wiki",
            "http://127.0.0.1:5208/opi-wiki/",
        ),
        (
            "https://docs.example.test/opi-wiki/",
            "https://docs.example.test/opi-wiki/",
        ),
    ),
)
def test_site_url_hook_restores_a_valid_reader_visible_url(
    requested_url: str,
    expected_url: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The hook should restore a validated external origin without changing mount path."""

    monkeypatch.setenv("OPI_SITE_URL", requested_url)
    config = _runtime_config("http://0.0.0.0:8000/opi-wiki/")

    assert on_config(config) is config
    assert config.site_url == expected_url


@pytest.mark.parametrize(
    ("requested_url", "expected_error"),
    (
        (
            "http://docs.example.test/opi-wiki/",
            "plain HTTP only for a loopback host",
        ),
        (
            "http://127.0.0.1:5208/other/",
            "path '/other/' must match",
        ),
        (
            "http://127.0.0.1:5208/opi-wiki/?preview=true",
            "must not contain a query or fragment",
        ),
    ),
)
def test_site_url_hook_rejects_unsafe_or_mismatched_overrides(
    requested_url: str,
    expected_error: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A preview override must never weaken origin or mount-path identity."""

    monkeypatch.setenv("OPI_SITE_URL", requested_url)
    config = _runtime_config("http://0.0.0.0:8000/opi-wiki/")

    with pytest.raises(ValueError, match=expected_error):
        on_config(config)


def test_site_url_hook_and_compose_override_remain_wired_together() -> None:
    """Source configuration should keep the load-bearing hook and external URL."""

    mkdocs_config = yaml_load(StringIO(Path("mkdocs.yml").read_text(encoding="utf-8")))
    compose_config = yaml.safe_load(Path("docker-compose.yml").read_text(encoding="utf-8"))

    assert mkdocs_config["hooks"] == ["scripts/mkdocs_site_url.py"]
    assert compose_config["services"]["wiki"]["environment"] == {
        "OPI_SITE_URL": "http://127.0.0.1:5208/opi-wiki/"
    }
