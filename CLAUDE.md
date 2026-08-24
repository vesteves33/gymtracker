# CLAUDE.md

Guia para trabalhar neste repositório. Ver PRD completo em `.prd/prd_gymtracker.md`.

## Projeto

GymTracker — sistema pessoal (usuário único) para registro de treinos de musculação e exercícios aeróbicos, com acompanhamento de evolução (carga, volume, frequência).

## Stack

- **Linguagem/gerenciador**: Python + [uv](https://docs.astral.sh/uv/)
- **Framework web**: FastAPI
- **Front**: Jinja2 (server-side, acoplado ao FastAPI — sem SPA nesta fase)
- **ORM/migrations**: SQLAlchemy + Alembic
- **Banco**: PostgreSQL
- **Testes**: pytest
- **Lint**: ruff
- **Auth**: JWT (usuário/senha)
- **Empacotamento**: Docker / docker-compose (serviços `app` + `db`)
- **CI**: GitHub Actions (lint + testes + build da imagem Docker, obrigatório antes de merge)

## Arquitetura

Hexagonal / Clean Architecture:

```
app/
  domain/          # entidades, value objects, regras de negocio puras (sem dependencia externa)
    entities/
    ports/          # interfaces (ex: TreinoRepository)
  application/      # casos de uso, dependem so de domain (via ports)
    use_cases/
  infrastructure/   # adapters concretos
    db/              # SQLAlchemy models, repositorios, migrations Alembic
    web/             # rotas FastAPI, templates Jinja2, schemas Pydantic
    auth/            # JWT
  main.py           # composition root
tests/
  unit/             # domain + application, sem DB
  integration/      # infra, com DB real
```

Regra de dependência: `domain` não importa nada de `infrastructure`. `application` depende só de `domain`. `infrastructure` é o único lugar que conhece FastAPI/SQLAlchemy/Jinja2.

## Comandos uv

```bash
uv sync                          # instala dependencias (le pyproject.toml/uv.lock)
uv add <pacote>                  # adiciona dependencia
uv add --dev <pacote>            # adiciona dependencia de dev
uv run fastapi dev app/main.py   # sobe servidor em modo dev
uv run pytest                    # roda todos os testes
uv run pytest tests/unit         # roda so testes unitarios (sem DB)
uv run ruff check .              # lint
uv run ruff format .             # formata codigo
uv run alembic upgrade head      # aplica migrations
uv run alembic revision --autogenerate -m "mensagem"  # gera nova migration
```

## Docker

```bash
docker compose up --build   # sobe app + postgres local
docker compose down         # derruba
```

## Git flow

Branches: `main` (estável/produção), `develop` (integração), `feature/*`, `release/*`, `hotfix/*`.

- Features partem de `develop` e voltam pra `develop` via PR.
- `main` só recebe merge de `release/*` ou `hotfix/*`.
- CI (lint + testes + build Docker) precisa passar antes de qualquer merge.

## Convenções

- Testes unitários (`tests/unit`) não tocam banco de dados — mockar/fake nos ports do domínio.
- Testes de integração (`tests/integration`) rodam contra Postgres real.
- Toda mudança de schema passa por migration Alembic — nunca alterar tabela direto no banco.
- Não adicionar dependências fora do `pyproject.toml` gerenciado por `uv`.
