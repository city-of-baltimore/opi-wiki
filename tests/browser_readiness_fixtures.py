"""Shared fixtures for browser-readiness contract tests."""

from pathlib import Path

from scripts.repo_tools.browser_readiness_contract import (
    BROWSER_READINESS_SEAM,
    BROWSER_RUNTIME_PATHS,
)

VALID_CONTEXT_SEAM = (
    "\ndef create_browser_context(browser, target):\n"
    "    context = browser.new_context(\n"
    "        service_workers='block',\n"
    "        offline=target.artifact_dir is not None,\n"
    "    )\n"
    "    install_canonical_artifact_route(context)\n"
    "    _install_live_preview_transport_route(context, target)\n"
    "    return context\n"
)


def write_runtime_sources(repo_root: Path, sources: tuple[str, str]) -> None:
    """Write a valid readiness fixture with two configured browser consumers."""

    seam = repo_root / BROWSER_READINESS_SEAM
    seam.parent.mkdir(parents=True, exist_ok=True)
    seam.write_text(
        "def load(page):\n"
        "    page.goto('https://example.test', wait_until='load')\n"
        f"{VALID_CONTEXT_SEAM}",
        encoding="utf-8",
    )
    for relative_path, source in zip(BROWSER_RUNTIME_PATHS, sources, strict=True):
        path = repo_root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source, encoding="utf-8")
    (repo_root / "mkdocs.yml").write_text(
        "dev_addr: !ENV [MKDOCS_DEV_ADDR, '127.0.0.1:5208']\n"
        "hooks:\n  - scripts/mkdocs_site_url.py\n",
        encoding="utf-8",
    )
    (repo_root / "docker-compose.yml").write_text(
        "services:\n"
        "  wiki:\n"
        "    build: .\n"
        "    environment:\n"
        "      OPI_SITE_URL: http://127.0.0.1:5208/opi-wiki/\n"
        "    ports:\n"
        '      - "127.0.0.1:5208:8000"\n'
        "    volumes:\n"
        "      - .:/app\n"
        "      - /app/.venv\n"
        "      - /app/site\n",
        encoding="utf-8",
    )
    (repo_root / "Dockerfile").write_text(
        "ENV MKDOCS_DEV_ADDR=0.0.0.0:8000\n"
        "HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 "
        'CMD ["python", "-m", "scripts.docker_healthcheck"]\n'
        'CMD ["uv", "run", "--no-dev", "python", "-m", "mkdocs", "serve"]\n',
        encoding="utf-8",
    )
    (repo_root / "Taskfile.yml").write_text(
        "tasks:\n"
        "  build:\n"
        "    cmds:\n"
        "      - uv run python -m mkdocs build --strict\n"
        "  serve:\n"
        "    cmds:\n"
        "      - uv run python -m mkdocs serve -a 127.0.0.1:5208\n",
        encoding="utf-8",
    )
    hook = repo_root / "scripts/mkdocs_site_url.py"
    hook.parent.mkdir(parents=True, exist_ok=True)
    hook.write_text("def on_config(config):\n    return config\n", encoding="utf-8")
