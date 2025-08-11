FROM python:3.13-slim
LABEL org.opencontainers.image.source=https://github.com/Stephen-Hallett/Scopus-Check
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /frontend

COPY . /frontend

RUN uv sync --frozen

EXPOSE 8080

ENTRYPOINT [ "uv", "run", "streamlit", "run", "main.py", "--server.port", "8080"]