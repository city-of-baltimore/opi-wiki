# Local development image for the OPI Foundations wiki.
#
# Runs the same uv-managed MkDocs toolchain the maintainers use, so a
# contributor can preview the site with `docker compose up` and no local
# Python or uv install. Production still deploys to GitHub Pages, not this
# image (see .github/workflows/deploy.yml and AGENTS.md).
# Match the uv version pinned in GitHub Actions and pin the multi-platform
# manifest so local preview builds do not drift underneath maintainers.
FROM ghcr.io/astral-sh/uv:0.11.28-python3.14-trixie-slim@sha256:b6e3a8825dfb232a6b962228f0b5cf98ee1d2b4263f62c2639f68887f4e634a2

RUN groupadd --gid 10001 opi \
    && useradd --uid 10001 --gid opi --home-dir /app --no-create-home \
        --shell /usr/sbin/nologin opi

WORKDIR /app
RUN chown opi:opi /app

# Let mkdocs serve be reachable from outside the container. mkdocs.yml reads this
# via !ENV and defaults to 127.0.0.1:5208 (the registry slot) when it is unset, so
# a host-side `mkdocs serve` stays on loopback while the container binds all
# interfaces and docker-compose publishes it back to 127.0.0.1:5208.
ENV MKDOCS_DEV_ADDR=0.0.0.0:8000

# Install dependencies first, from the lockfile, for cacheable layers.
COPY --chown=opi:opi pyproject.toml uv.lock ./
USER opi
RUN uv sync --frozen --no-dev --no-cache

# Copy the rest of the project (macros in main.py and scripts/ are needed at
# build time by the mkdocs-macros plugin).
COPY --chown=opi:opi . .
RUN mkdir -p /app/site

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/', timeout=2)"]

# Live-reload preview server. docker-compose mounts the source over /app so
# edits on the host refresh the browser.
CMD ["uv", "run", "--no-dev", "mkdocs", "serve", "-a", "0.0.0.0:8000"]
