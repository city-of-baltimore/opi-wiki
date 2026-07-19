# Local development image for the OPI Foundations wiki.
#
# Runs the same uv-managed MkDocs toolchain the maintainers use, so a
# contributor can preview the site with `docker compose up` and no local
# Python or uv install. Production still deploys to GitHub Pages, not this
# image (see .github/workflows/deploy.yml and AGENTS.md).
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Let mkdocs serve be reachable from outside the container.
ENV MKDOCS_DEV_ADDR=0.0.0.0:8000

# Install dependencies first, from the lockfile, for cacheable layers.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy the rest of the project (macros in main.py and scripts/ are needed at
# build time by the mkdocs-macros plugin).
COPY . .

EXPOSE 8000

# Live-reload preview server. docker-compose mounts the source over /app so
# edits on the host refresh the browser.
CMD ["uv", "run", "--no-dev", "mkdocs", "serve", "-a", "0.0.0.0:8000"]
