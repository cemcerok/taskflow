# TaskFlow

TaskFlow — минимальный REST API для управления задачами. Данные хранятся в
PostgreSQL и сохраняются между перезапусками контейнеров.

## Технологии

- Python 3.12
- FastAPI и Pydantic v2
- SQLAlchemy 2.x в асинхронном режиме
- PostgreSQL 17 и asyncpg
- Docker и Docker Compose

## Запуск

1. Создайте локальный файл настроек:

   ```bash
   cp .env.example .env
   ```

2. Замените `POSTGRES_PASSWORD` в `.env` на собственный пароль.

3. Соберите и запустите сервисы:

   ```bash
   docker compose up --build
   ```

API будет доступен по адресу <http://localhost:8000>, интерактивная документация —
по адресу <http://localhost:8000/docs>. При первом запуске приложение автоматически
создаёт таблицу `tasks`. Существующие таблицы и данные не удаляются.

Остановить сервисы без удаления данных:

```bash
docker compose down
```

## Переменные окружения

Приложение собирает безопасный асинхронный `postgresql+asyncpg://` URL из
значений окружения, переданных Docker Compose:

- `POSTGRES_USER` — пользователь PostgreSQL;
- `POSTGRES_PASSWORD` — пароль PostgreSQL;
- `POSTGRES_DB` — имя базы данных.

Файл `.env` исключён из Git. В репозитории хранится только безопасный шаблон
`.env.example`.

## API

| Метод | Маршрут | Назначение |
|---|---|---|
| `GET` | `/` | Информация о сервисе |
| `GET` | `/health` | Проверка доступности API |
| `GET` | `/tasks` | Список задач |
| `GET` | `/tasks/{task_id}` | Получить задачу |
| `POST` | `/tasks` | Создать задачу (`201 Created`) |
| `PUT` | `/tasks/{task_id}` | Полностью обновить задачу |
| `PATCH` | `/tasks/{task_id}` | Обновить переданные поля |
| `DELETE` | `/tasks/{task_id}` | Удалить задачу (`204 No Content`) |

Поля задачи: `id`, `title`, `description`, `completed`, `created_at`.

## Проверка состояния

```bash
curl http://localhost:8000/health
```

Ожидаемый ответ: `{"status":"ok"}`.

Автоматические тесты используют отдельную in-memory БД и не затрагивают PostgreSQL:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
```

> `create_all()` создаёт отсутствующие таблицы, но не обновляет существующую
> структуру. Если старая таблица `tasks` несовместима с текущей моделью, запуск
> завершится с понятным сообщением. В таком случае нужна отдельная миграция данных.
