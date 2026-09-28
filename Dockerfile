# syntax=docker/dockerfile:1

# Estágio de build: valida a sintaxe e compila bytecode sem instalar dependências.
FROM python:3.12-slim AS builder
WORKDIR /build
COPY app.py .
RUN python -m py_compile app.py

# Estágio final: imagem menor, sem ferramentas de compilação.
FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app

# Usuário sem privilégios para reduzir o impacto de vulnerabilidades.
RUN addgroup --system app && adduser --system --ingroup app app
COPY --from=builder /build/app.py .
USER app

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/?damage=100&attacks=2', timeout=2)"
CMD ["python", "app.py"]
