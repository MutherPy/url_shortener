# Міграції бази даних

Alembic використовує `asyncpg` та SQLAlchemy як рушій підключення.
ORM-моделі не потрібні: `target_metadata = None`, SQL пишеться вручну.

Команди нижче виконуються з каталогу `url_shortener`.

## Встановлення

```bash
virt/bin/python -m pip install -r requirements-migrations.txt
```

Параметри підключення беруться з `DbConfigs` у `configs.py`:
`POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_USER`, `POSTGRES_PASSWORD`,
`POSTGRES_DB`. Завантажується `.env` у корені `url_shortener`;
змінні середовища мають пріоритет. Пароль не записується в `alembic.ini`.

## Створення міграції

```bash
virt/bin/python -m alembic revision -m "create urls table"
```

У `migrations/versions/` з'явиться Python-файл із порожніми
`upgrade()` та `downgrade()`. Запиши свій SQL через `op.execute()`:

```python
def upgrade() -> None:
    op.execute("""
        CREATE TABLE urls (
            id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            original_url TEXT NOT NULL
        )
    """)


def downgrade() -> None:
    op.execute("DROP TABLE urls")
```

Це лише приклад: схему таблиць ти визначаєш сам.
Для кожної окремої SQL-команди використовуй окремий `op.execute()`.
Створюй ревізії без `--autogenerate`: міграції не генеруються з ORM-моделей.

## Застосування та відкат

```bash
# Застосувати всі міграції
virt/bin/python -m alembic upgrade head

# Відкотити останню міграцію
virt/bin/python -m alembic downgrade -1

# Поточна версія БД та історія міграцій
virt/bin/python -m alembic current
virt/bin/python -m alembic history

# Згенерувати SQL без підключення до БД
virt/bin/python -m alembic upgrade head --sql
```

Якщо запускаєш Alembic з іншого каталогу, вкажи абсолютний шлях
до `url_shortener/alembic.ini` через `-c`.
