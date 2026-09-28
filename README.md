# Calculadora DPS em Docker

Atividade de criação de uma imagem Docker eficiente usando uma calculadora de dano por segundo (DPS).

## Executar no GitHub Codespaces

```bash
docker build -t calcdps:1.0 .
docker run -d --name calcdps -p 8000:8000 calcdps:1.0
curl "http://localhost:8000/?damage=250&attacks=2&crit=20"
docker ps
docker logs calcdps
```

Resultado esperado:

```json
{"damage": 250.0, "attacks_per_second": 2.0, "critical_bonus_percent": 20.0, "dps": 600.0}
```

## Escolhas de otimização

- Multi-stage build: o estágio `builder` valida o código e não é levado para a imagem final.
- `python:3.12-slim`: reduz o tamanho em relação à imagem completa do Python.
- Sem dependências externas: não há download de pacotes nem camadas desnecessárias.
- Usuário não-root: o processo não roda como administrador.
- `.dockerignore`: evita enviar arquivos irrelevantes ao contexto de build.
- Healthcheck: permite verificar automaticamente se a API está respondendo.

A evidência de execução deve ser capturada no terminal do Codespace após rodar os comandos acima.
