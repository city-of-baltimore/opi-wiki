"""Adversarial tests for the local preview port and bind contract."""

from __future__ import annotations

from pathlib import Path

import pytest
from scripts.repo_tools.browser_readiness_contract import (
    find_browser_readiness_contract_issues,
)
from scripts.repo_tools.dockerfile_source import (
    dockerfile_instructions,
    effective_dockerfile_environment,
)
from tests.browser_readiness_fixtures import write_runtime_sources

_VALID_CONSUMERS = (
    "def run(page):\n    return navigate_to_ready_page(page)\n",
    "def run(page):\n    return navigate_to_instant_page(page)\n",
)


def _replace(path: Path, old: str, new: str) -> None:
    """Replace one known fixture seam and fail if the fixture itself drifted."""

    source = path.read_text(encoding="utf-8")
    assert source.count(old) == 1
    path.write_text(source.replace(old, new), encoding="utf-8")


@pytest.mark.parametrize("unsafe_address", ("0.0.0.0:5208", "127.0.0.1:5209"))
def test_browser_readiness_contract_rejects_mkdocs_host_bind_drift(
    tmp_path: Path,
    unsafe_address: str,
) -> None:
    """Host-side MkDocs must remain loopback-only on the registered slot."""

    write_runtime_sources(tmp_path, _VALID_CONSUMERS)
    _replace(
        tmp_path / "mkdocs.yml",
        "'127.0.0.1:5208'",
        f"'{unsafe_address}'",
    )

    assert find_browser_readiness_contract_issues(tmp_path) == [
        "mkdocs.yml: dev_addr must remain !ENV [MKDOCS_DEV_ADDR, '127.0.0.1:5208']"
    ]


def test_browser_readiness_contract_rejects_a_duplicate_mkdocs_bind_decoy(
    tmp_path: Path,
) -> None:
    """An expected first value must not hide a later effective unsafe bind."""

    write_runtime_sources(tmp_path, _VALID_CONSUMERS)
    mkdocs_config = tmp_path / "mkdocs.yml"
    mkdocs_config.write_text(
        mkdocs_config.read_text(encoding="utf-8")
        + "dev_addr: !ENV [MKDOCS_DEV_ADDR, '0.0.0.0:5208']\n",
        encoding="utf-8",
    )

    assert find_browser_readiness_contract_issues(tmp_path) == [
        "mkdocs.yml: dev_addr must remain !ENV [MKDOCS_DEV_ADDR, '127.0.0.1:5208']"
    ]


@pytest.mark.parametrize(
    "unsafe_mapping",
    (
        "0.0.0.0:5208:8000",
        "5208:8000",
        "127.0.0.1:5209:8000",
        "127.0.0.1:5208:8001",
    ),
)
def test_browser_readiness_contract_rejects_compose_port_drift(
    tmp_path: Path,
    unsafe_mapping: str,
) -> None:
    """Compose must publish only container port 8000 to slot 8 on loopback."""

    write_runtime_sources(tmp_path, _VALID_CONSUMERS)
    _replace(
        tmp_path / "docker-compose.yml",
        "127.0.0.1:5208:8000",
        unsafe_mapping,
    )

    assert find_browser_readiness_contract_issues(tmp_path) == [
        "docker-compose.yml: services.wiki.ports must remain ['127.0.0.1:5208:8000']"
    ]


@pytest.mark.parametrize("unsafe_address", ("127.0.0.1:8000", "0.0.0.0:5208"))
def test_browser_readiness_contract_rejects_container_bind_drift(
    tmp_path: Path,
    unsafe_address: str,
) -> None:
    """The container must listen on its internal all-interface port."""

    write_runtime_sources(tmp_path, _VALID_CONSUMERS)
    _replace(
        tmp_path / "Dockerfile",
        "ENV MKDOCS_DEV_ADDR=0.0.0.0:8000",
        f"ENV MKDOCS_DEV_ADDR={unsafe_address}",
    )

    assert find_browser_readiness_contract_issues(tmp_path) == [
        "Dockerfile: MKDOCS_DEV_ADDR must remain '0.0.0.0:8000'"
    ]


def test_browser_readiness_contract_uses_the_effective_container_bind(
    tmp_path: Path,
) -> None:
    """A later Docker ENV must win so an expected-value decoy cannot pass."""

    write_runtime_sources(tmp_path, _VALID_CONSUMERS)
    _replace(
        tmp_path / "Dockerfile",
        "ENV MKDOCS_DEV_ADDR=0.0.0.0:8000",
        "ENV MKDOCS_DEV_ADDR=0.0.0.0:8000\nENV MKDOCS_DEV_ADDR=127.0.0.1:8000",
    )

    assert find_browser_readiness_contract_issues(tmp_path) == [
        "Dockerfile: MKDOCS_DEV_ADDR must remain '0.0.0.0:8000'"
    ]


def test_effective_dockerfile_environment_parses_modern_and_legacy_forms() -> None:
    """The semantic reader must support both Docker ENV forms and continuations."""

    source = "ENV FIRST=one \\\n    SECOND='two words'\nENV MKDOCS_DEV_ADDR 0.0.0.0:8000\n"

    assert effective_dockerfile_environment(source) == {
        "FIRST": "one",
        "SECOND": "two words",
        "MKDOCS_DEV_ADDR": "0.0.0.0:8000",
    }


def test_effective_dockerfile_environment_fails_closed_on_malformed_env() -> None:
    """An incomplete Docker ENV must not silently look absent."""

    with pytest.raises(RuntimeError, match="Unable to parse Dockerfile ENV instruction"):
        effective_dockerfile_environment("ENV MKDOCS_DEV_ADDR\n")


def test_dockerfile_instructions_return_effective_source_lines() -> None:
    """The shared Docker parser must ignore comments and join continuations."""

    instructions = dockerfile_instructions(
        '# CMD ["not-effective"]\nENV FIRST=one \\\n    SECOND=two\nCMD ["true"]\n'
    )

    assert [(item.keyword, item.body, item.line_number) for item in instructions] == [
        ("env", "FIRST=one SECOND=two", 2),
        ("cmd", '["true"]', 4),
    ]


def test_dockerfile_instructions_fail_closed_on_unterminated_continuation() -> None:
    """An incomplete logical instruction must not be partially interpreted."""

    with pytest.raises(RuntimeError, match="unterminated continuation"):
        dockerfile_instructions("ENV FIRST=one \\\n")


@pytest.mark.parametrize("unsafe_address", ("0.0.0.0:5208", "127.0.0.1:5209"))
def test_browser_readiness_contract_rejects_task_serve_bind_drift(
    tmp_path: Path,
    unsafe_address: str,
) -> None:
    """The task entry point must retain the same loopback slot as MkDocs."""

    write_runtime_sources(tmp_path, _VALID_CONSUMERS)
    _replace(
        tmp_path / "Taskfile.yml",
        "127.0.0.1:5208",
        unsafe_address,
    )

    assert find_browser_readiness_contract_issues(tmp_path) == [
        "Taskfile.yml: task serve must run 'uv run python -m mkdocs serve -a "
        "127.0.0.1:5208' so the registered hook can import repository code"
    ]


@pytest.mark.parametrize(
    "unsafe_url",
    (
        "http://0.0.0.0:5208/opi-wiki/",
        "http://127.0.0.1:5209/opi-wiki/",
    ),
)
def test_browser_readiness_contract_rejects_canonical_preview_port_drift(
    tmp_path: Path,
    unsafe_url: str,
) -> None:
    """Compose canonical links must name the reader-visible loopback slot."""

    write_runtime_sources(tmp_path, _VALID_CONSUMERS)
    _replace(
        tmp_path / "docker-compose.yml",
        "http://127.0.0.1:5208/opi-wiki/",
        unsafe_url,
    )

    assert find_browser_readiness_contract_issues(tmp_path) == [
        "docker-compose.yml: services.wiki.environment must remain "
        "{'OPI_SITE_URL': 'http://127.0.0.1:5208/opi-wiki/'}"
    ]


@pytest.mark.parametrize(
    ("override_key", "override_value"),
    (
        ("command", '["false"]'),
        ("entrypoint", '["false"]'),
        ("healthcheck", "{disable: true}"),
    ),
)
def test_browser_readiness_contract_rejects_compose_runtime_overrides(
    tmp_path: Path,
    override_key: str,
    override_value: str,
) -> None:
    """Compose must not replace Docker's proven startup or health behavior."""

    write_runtime_sources(tmp_path, _VALID_CONSUMERS)
    compose = tmp_path / "docker-compose.yml"
    compose.write_text(
        compose.read_text(encoding="utf-8") + f"    {override_key}: {override_value}\n",
        encoding="utf-8",
    )

    found_keys = sorted(
        ["build", "environment", "ports", "volumes", override_key],
    )
    assert find_browser_readiness_contract_issues(tmp_path) == [
        "docker-compose.yml: services.wiki must define only "
        "['build', 'environment', 'ports', 'volumes']; "
        f"found {found_keys!r}"
    ]


@pytest.mark.parametrize(
    ("old", "new", "expected"),
    (
        (
            "build: .",
            "build: ./preview",
            "docker-compose.yml: services.wiki.build must remain '.'",
        ),
        (
            "      OPI_SITE_URL: http://127.0.0.1:5208/opi-wiki/",
            "      OPI_SITE_URL: http://127.0.0.1:5208/opi-wiki/\n      EXTRA: unsafe",
            "docker-compose.yml: services.wiki.environment must remain "
            "{'OPI_SITE_URL': 'http://127.0.0.1:5208/opi-wiki/'}",
        ),
        (
            "      - /app/site",
            "      - /tmp/site",
            "docker-compose.yml: services.wiki.volumes must remain "
            "['.:/app', '/app/.venv', '/app/site']",
        ),
    ),
)
def test_browser_readiness_contract_rejects_compose_service_drift(
    tmp_path: Path,
    old: str,
    new: str,
    expected: str,
) -> None:
    """Every allowed Compose service seam must retain its exact reviewed value."""

    write_runtime_sources(tmp_path, _VALID_CONSUMERS)
    _replace(tmp_path / "docker-compose.yml", old, new)

    assert find_browser_readiness_contract_issues(tmp_path) == [expected]
