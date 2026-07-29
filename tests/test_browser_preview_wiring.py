"""Tests for the live-preview configuration held by browser readiness."""

from pathlib import Path

import pytest
from scripts.repo_tools.browser_readiness_contract import (
    find_browser_readiness_contract_issues,
)
from tests.browser_readiness_fixtures import write_runtime_sources

_VALID_CONSUMERS = (
    "def run(page):\n    return navigate_to_ready_page(page)\n",
    "def run(page):\n    return navigate_to_instant_page(page)\n",
)


def test_browser_readiness_contract_rejects_preview_canonical_wiring_drift(
    tmp_path: Path,
) -> None:
    """Compose must not expose a container-origin canonical that disables instant navigation."""

    write_runtime_sources(tmp_path, _VALID_CONSUMERS)
    mkdocs_config = tmp_path / "mkdocs.yml"
    mkdocs_config.write_text(
        mkdocs_config.read_text(encoding="utf-8").replace(
            "hooks:\n  - scripts/mkdocs_site_url.py",
            "hooks: []",
        ),
        encoding="utf-8",
    )
    compose_config = tmp_path / "docker-compose.yml"
    compose_config.write_text(
        compose_config.read_text(encoding="utf-8").replace(
            "http://127.0.0.1:5208/opi-wiki/",
            "http://0.0.0.0:8000/opi-wiki/",
        ),
        encoding="utf-8",
    )

    assert find_browser_readiness_contract_issues(tmp_path) == [
        "docker-compose.yml: services.wiki.environment must remain "
        "{'OPI_SITE_URL': 'http://127.0.0.1:5208/opi-wiki/'}",
        "mkdocs.yml: must register scripts/mkdocs_site_url.py as its sole MkDocs hook",
    ]


def test_browser_readiness_contract_rejects_non_mapping_configuration(
    tmp_path: Path,
) -> None:
    """A parseable but structurally invalid config must fail with one boundary error."""

    write_runtime_sources(tmp_path, _VALID_CONSUMERS)
    (tmp_path / "mkdocs.yml").write_text("[]\n", encoding="utf-8")

    with pytest.raises(RuntimeError, match="roots must be YAML mappings"):
        find_browser_readiness_contract_issues(tmp_path)


def test_browser_readiness_contract_rejects_preview_startup_drift(
    tmp_path: Path,
) -> None:
    """Both preview commands must preserve hook imports and canonical health checks."""

    write_runtime_sources(tmp_path, _VALID_CONSUMERS)
    (tmp_path / "Dockerfile").write_text(
        'ENV MKDOCS_DEV_ADDR=0.0.0.0:8000\nCMD ["uv", "run", "--no-dev", "mkdocs", "serve"]\n',
        encoding="utf-8",
    )
    (tmp_path / "Taskfile.yml").write_text(
        "tasks:\n"
        "  build:\n"
        "    cmds:\n"
        "      - uv run mkdocs build --strict\n"
        "  serve:\n"
        "    cmds:\n"
        "      - uv run mkdocs serve\n",
        encoding="utf-8",
    )

    assert find_browser_readiness_contract_issues(tmp_path) == [
        "Dockerfile: must define exactly one effective HEALTHCHECK; found 0",
        'Dockerfile: sole preview command must be \'CMD ["uv", "run", "--no-dev", '
        '"python", "-m", "mkdocs", "serve"]\'',
        "Taskfile.yml: task build must run 'uv run python -m mkdocs build --strict' "
        "so the registered hook can import repository code",
        "Taskfile.yml: task serve must run 'uv run python -m mkdocs serve -a "
        "127.0.0.1:5208' so the registered hook can import repository code",
    ]


def test_browser_readiness_contract_parses_effective_docker_instructions(
    tmp_path: Path,
) -> None:
    """Comments and continuations must not make valid preview instructions disappear."""

    write_runtime_sources(tmp_path, _VALID_CONSUMERS)
    (tmp_path / "Dockerfile").write_text(
        "# A commented CMD is documentation, not an effective instruction.\n"
        '# CMD ["not", "effective"]\n'
        '# ENTRYPOINT ["not", "effective"]\n'
        "ENV MKDOCS_DEV_ADDR=0.0.0.0:8000\n"
        "HEALTHCHECK --timeout=3s --retries=3 \\\n"
        "    --interval=30s --start-period=10s \\\n"
        '    CMD ["python", "-m", "scripts.docker_healthcheck"]\n'
        'CMD ["uv", "run", "--no-dev", \\\n'
        '    "python", "-m", "mkdocs", "serve"]\n',
        encoding="utf-8",
    )

    assert find_browser_readiness_contract_issues(tmp_path) == []


def test_browser_readiness_contract_honors_docker_escape_directive(
    tmp_path: Path,
) -> None:
    """The Docker parser must use a declared backtick continuation character."""

    write_runtime_sources(tmp_path, _VALID_CONSUMERS)
    (tmp_path / "Dockerfile").write_text(
        "# escape=`\n"
        "ENV MKDOCS_DEV_ADDR=0.0.0.0:8000\n"
        "HEALTHCHECK --timeout=3s --retries=3 `\n"
        "    --interval=30s --start-period=10s `\n"
        '    CMD ["python", "-m", "scripts.docker_healthcheck"]\n'
        'CMD ["uv", "run", "--no-dev", `\n'
        '    "python", "-m", "mkdocs", "serve"]\n',
        encoding="utf-8",
    )

    assert find_browser_readiness_contract_issues(tmp_path) == []


def test_browser_readiness_contract_rejects_a_later_effective_docker_cmd(
    tmp_path: Path,
) -> None:
    """A second CMD must fail even when the first retains the expected text."""

    write_runtime_sources(tmp_path, _VALID_CONSUMERS)
    dockerfile = tmp_path / "Dockerfile"
    dockerfile.write_text(
        dockerfile.read_text(encoding="utf-8") + 'CMD ["python", "-m", "http.server"]\n',
        encoding="utf-8",
    )

    assert find_browser_readiness_contract_issues(tmp_path) == [
        "Dockerfile: must define exactly one effective preview CMD; found 2"
    ]


@pytest.mark.parametrize(
    "dockerfile_text",
    (
        (
            "# HEALTHCHECK CMD python -m scripts.docker_healthcheck\n"
            "ENV MKDOCS_DEV_ADDR=0.0.0.0:8000\n"
            'CMD ["uv", "run", "--no-dev", "python", "-m", "mkdocs", "serve"]\n'
        ),
        (
            "RUN python -m scripts.docker_healthcheck\n"
            "ENV MKDOCS_DEV_ADDR=0.0.0.0:8000\n"
            'CMD ["uv", "run", "--no-dev", "python", "-m", "mkdocs", "serve"]\n'
        ),
    ),
)
def test_browser_readiness_contract_rejects_a_dead_health_url(
    tmp_path: Path,
    dockerfile_text: str,
) -> None:
    """A URL in a comment or unrelated instruction must not satisfy health policy."""

    write_runtime_sources(tmp_path, _VALID_CONSUMERS)
    (tmp_path / "Dockerfile").write_text(dockerfile_text, encoding="utf-8")

    assert find_browser_readiness_contract_issues(tmp_path) == [
        "Dockerfile: must define exactly one effective HEALTHCHECK; found 0"
    ]


@pytest.mark.parametrize(
    "healthcheck",
    (
        ('HEALTHCHECK CMD ["true", "scripts.docker_healthcheck"]'),
        ('HEALTHCHECK CMD ["python", "-c", "print(\'scripts.docker_healthcheck\')"]'),
        ('HEALTHCHECK CMD ["python", "-c", "import scripts.docker_healthcheck"]'),
        "HEALTHCHECK CMD python -m scripts.docker_healthcheck",
        "HEALTHCHECK CMD false # scripts.docker_healthcheck",
    ),
)
def test_browser_readiness_contract_rejects_health_command_decoys(
    tmp_path: Path,
    healthcheck: str,
) -> None:
    """Only the exact JSON probe and health options may satisfy the contract."""

    write_runtime_sources(tmp_path, _VALID_CONSUMERS)
    (tmp_path / "Dockerfile").write_text(
        "ENV MKDOCS_DEV_ADDR=0.0.0.0:8000\n"
        f"{healthcheck}\n"
        'CMD ["uv", "run", "--no-dev", "python", "-m", "mkdocs", "serve"]\n',
        encoding="utf-8",
    )

    assert find_browser_readiness_contract_issues(tmp_path) == [
        "Dockerfile: sole health check must be HEALTHCHECK --interval=30s "
        "--timeout=3s --start-period=10s --retries=3 CMD "
        '["python", "-m", "scripts.docker_healthcheck"]'
    ]


@pytest.mark.parametrize(
    "options",
    (
        "--timeout=3s --start-period=10s --retries=3",
        "--interval=31s --timeout=3s --start-period=10s --retries=3",
        "--interval=30s --timeout=3s --start-period=10s --retries=3 --start-interval=1s",
        "--interval=30s --interval=30s --timeout=3s --start-period=10s --retries=3",
    ),
)
def test_browser_readiness_contract_rejects_health_option_drift(
    tmp_path: Path,
    options: str,
) -> None:
    """Missing, changed, extra, and duplicate health options must fail closed."""

    write_runtime_sources(tmp_path, _VALID_CONSUMERS)
    (tmp_path / "Dockerfile").write_text(
        "ENV MKDOCS_DEV_ADDR=0.0.0.0:8000\n"
        f"HEALTHCHECK {options} "
        'CMD ["python", "-m", "scripts.docker_healthcheck"]\n'
        'CMD ["uv", "run", "--no-dev", "python", "-m", "mkdocs", "serve"]\n',
        encoding="utf-8",
    )

    assert find_browser_readiness_contract_issues(tmp_path) == [
        "Dockerfile: sole health check must be HEALTHCHECK --interval=30s "
        "--timeout=3s --start-period=10s --retries=3 CMD "
        '["python", "-m", "scripts.docker_healthcheck"]'
    ]


def test_browser_readiness_contract_rejects_an_effective_entrypoint(
    tmp_path: Path,
) -> None:
    """An entrypoint must not replace or reinterpret the exact preview command."""

    write_runtime_sources(tmp_path, _VALID_CONSUMERS)
    dockerfile = tmp_path / "Dockerfile"
    dockerfile.write_text(
        dockerfile.read_text(encoding="utf-8") + 'ENTRYPOINT ["false"]\n',
        encoding="utf-8",
    )

    assert find_browser_readiness_contract_issues(tmp_path) == [
        "Dockerfile: must not define an ENTRYPOINT; found 1"
    ]


def test_browser_readiness_contract_rejects_duplicate_health_checks(
    tmp_path: Path,
) -> None:
    """A later HEALTHCHECK must not silently replace the canonical one."""

    write_runtime_sources(tmp_path, _VALID_CONSUMERS)
    dockerfile = tmp_path / "Dockerfile"
    dockerfile.write_text(
        dockerfile.read_text(encoding="utf-8") + "HEALTHCHECK NONE\n",
        encoding="utf-8",
    )

    assert find_browser_readiness_contract_issues(tmp_path) == [
        "Dockerfile: must define exactly one effective HEALTHCHECK; found 2"
    ]
