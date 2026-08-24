# GymTracker

Sistema pessoal para registrar treinos de musculação e exercícios aeróbicos, e acompanhar evolução ao longo do tempo (progressão de carga, volume de repetições, frequência de treinos).

Projeto de uso único (usuário único), sem cadastro aberto.

## Funcionalidades

- Registro de treino de musculação: exercício, séries, repetições, carga (kg).
- Registro de treino aeróbico: exercício (esteira, bicicleta, escada), tempo, distância.
- Catálogo de exercícios (seed inicial + CRUD).
- Histórico de treinos.
- Acompanhamento de evolução: progressão de carga, volume, frequência.

## Stack

Python + [uv](https://docs.astral.sh/uv/) · FastAPI · Jinja2 · SQLAlchemy + Alembic · PostgreSQL · pytest · ruff · Docker · JWT.

Arquitetura hexagonal (domain / application / infrastructure). Detalhes em [CLAUDE.md](./CLAUDE.md) e PRD completo em [.prd/prd_gymtracker.md](./.prd/prd_gymtracker.md).

## Rodando local

```bash
uv sync
docker compose up --build   # sobe app + postgres
uv run alembic upgrade head
```

Acesse `http://localhost:8000`.

## Testes

```bash
uv run pytest
```

## Git flow

`main` (produção) · `develop` (integração) · `feature/*` · `release/*` · `hotfix/*`.
