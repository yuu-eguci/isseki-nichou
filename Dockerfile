# syntax=docker/dockerfile:1
FROM python:3.14-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ISSEKI_DB=/data/isseki.sqlite3
RUN useradd --create-home --uid 10001 isseki
WORKDIR /game
COPY KillBirds.py ./
COPY app/ app/
# 空の named volume を /data にマウントすると、初回だけこの DB がコピーされます。
RUN mkdir /data && cp app/isseki.sqlite3 /data/ && chown -R isseki:isseki /data
USER isseki
CMD ["python", "KillBirds.py"]

FROM runtime AS dev
USER root
COPY requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY pyproject.toml ./
COPY tests/ tests/
ENV RUFF_NO_CACHE=true
USER isseki
CMD ["pytest"]
