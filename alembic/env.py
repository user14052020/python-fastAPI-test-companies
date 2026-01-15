from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# импорт базы и моделей
from app.core.database import Base
from app import models  # импорт всех моделей, чтобы Alembic видел их

# Alembic Config object
config = context.config

# Настройка логирования
fileConfig(config.config_file_name)

# !!! Определяем target_metadata ДО любых функций
target_metadata = Base.metadata

# Миграции в offline-режиме
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

# Миграции в online-режиме
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

# Выбираем режим работы
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
