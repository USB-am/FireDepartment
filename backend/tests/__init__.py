import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from main import app
from data_base import Base, get_session
from data_base import models


TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


@pytest.fixture(scope="session")
def event_loop():
    ''' Создаем event loop для всей сессии тестов '''
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def async_engine():
    ''' Создаем асинхронный engine для тестов '''
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=True,
        poolclass=NullPool,
    )

    # Создаем все таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Очищаем после всех тестов
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(async_engine):
    ''' Создаем асинхронную сессию для каждого теста '''
    async_session = sessionmaker(
        async_engine, 
        class_=AsyncSession, 
        expire_on_commit=False
    )

    async with async_session() as session:
        yield session
        await session.rollback()
        await session.close()


@pytest_asyncio.fixture
async def client(db_session):
    ''' Создаем асинхронный клиент с переопределенной зависимостью get_session '''

    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


class TestUserRoutes:
    ''' Тесты для маршрутов пользователя '''

    @pytest.mark.asyncio
    async def test_create_user(self, client, db_session):
        ''' Тест создания пользователя '''
        # Тестовые данные
        test_user = {
            "username": "asynctestuser",
            "email": "async@example.com",
            "full_name": "Async Test User"
        }

        # Отправляем POST запрос
        response = await client.post("/users/", json=test_user)

        # Проверяем ответ
        assert response.status_code == 200
        response_data = response.json()

        # Проверяем данные ответа
        assert "id" in response_data
        assert response_data["username"] == test_user["username"]
        assert response_data["email"] == test_user["email"]
        assert response_data["full_name"] == test_user["full_name"]

        # Проверяем, что запись действительно существует в БД
        from sqlalchemy import select
        from your_app.models import User

        result = await db_session.execute(
            select(User).where(User.id == response_data["id"])
        )
        db_user = result.scalar_one_or_none()

        assert db_user is not None
        assert db_user.username == test_user["username"]

        # Удаляем запись
        await db_session.delete(db_user)
        await db_session.commit()

        # Проверяем, что запись удалена
        result = await db_session.execute(
            select(User).where(User.id == response_data["id"])
        )
        deleted_user = result.scalar_one_or_none()
        assert deleted_user is None

    @pytest.mark.asyncio
    async def test_get_user(self, client, db_session):
        ''' Тест получения пользователя '''
        # Создаем тестового пользователя
        from your_app.models import User
        from sqlalchemy import select

        test_user = User(
            username="asyncget",
            email="asyncget@example.com",
            full_name="Async Get User"
        )
        db_session.add(test_user)
        await db_session.commit()
        await db_session.refresh(test_user)

        # Получаем пользователя через API
        response = await client.get(f"/users/{test_user.id}")

        # Проверяем ответ
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["username"] == test_user.username
        assert response_data["email"] == test_user.email

        # Удаляем пользователя
        await db_session.delete(test_user)
        await db_session.commit()

        # Проверяем, что пользователь не найден
        response = await client.get(f"/users/{test_user.id}")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_create_user_with_existing_username(self, client, db_session):
        ''' Тест создания пользователя с существующим username '''
        # Создаем пользователя
        from your_app.models import User

        existing_user = User(
            username="duplicate",
            email="duplicate@example.com",
            full_name="Duplicate User"
        )
        db_session.add(existing_user)
        await db_session.commit()

        # Пытаемся создать пользователя с тем же username
        test_user = {
            "username": "duplicate",
            "email": "different@example.com",
            "full_name": "Different User"
        }

        response = await client.post("/users/", json=test_user)

        # Проверяем, что получили ошибку
        assert response.status_code == 400  # или другой код ошибки

        # Очищаем
        await db_session.delete(existing_user)
        await db_session.commit()

    @pytest.mark.asyncio
    async def test_update_user(self, client, db_session):
        ''' Тест обновления пользователя '''
        # Создаем пользователя
        from your_app.models import User

        user = User(
            username="updateuser",
            email="update@example.com",
            full_name="Update User"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        # Обновляем данные
        update_data = {
            "full_name": "Updated Full Name",
            "email": "updated@example.com"
        }

        response = await client.put(f"/users/{user.id}", json=update_data)

        # Проверяем ответ
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["full_name"] == update_data["full_name"]
        assert response_data["email"] == update_data["email"]

        # Проверяем в БД
        from sqlalchemy import select
        result = await db_session.execute(
            select(User).where(User.id == user.id)
        )
        updated_user = result.scalar_one()
        assert updated_user.full_name == update_data["full_name"]

        # Очищаем
        await db_session.delete(updated_user)
        await db_session.commit()

    @pytest.mark.asyncio
    async def test_delete_user(self, client, db_session):
        ''' Тест удаления пользователя '''
        # Создаем пользователя
        from your_app.models import User
        from sqlalchemy import select

        user = User(
            username="deleteuser",
            email="delete@example.com",
            full_name="Delete User"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        # Удаляем через API
        response = await client.delete(f"/users/{user.id}")

        # Проверяем ответ
        assert response.status_code == 200
        assert response.json()["message"] == "User deleted successfully"

        # Проверяем, что пользователь действительно удален из БД
        result = await db_session.execute(
            select(User).where(User.id == user.id)
        )
        deleted_user = result.scalar_one_or_none()
        assert deleted_user is None

    @pytest.mark.asyncio
    async def test_list_users(self, client, db_session):
        ''' Тест получения списка пользователей '''
        # Создаем нескольких пользователей
        from your_app.models import User

        users_data = [
            User(username="user1", email="user1@example.com", full_name="User One"),
            User(username="user2", email="user2@example.com", full_name="User Two"),
            User(username="user3", email="user3@example.com", full_name="User Three"),
        ]

        for user in users_data:
            db_session.add(user)
        await db_session.commit()

        # Получаем список
        response = await client.get("/users/")

        # Проверяем ответ
        assert response.status_code == 200
        response_data = response.json()
        assert len(response_data) >= 3

        # Очищаем
        for user in users_data:
            await db_session.delete(user)
        await db_session.commit()

    @pytest.mark.asyncio
    async def test_concurrent_user_creation(self, client, db_session):
        ''' Тест конкурентного создания пользователей '''
        import asyncio

        async def create_user(username):
            user_data = {
                "username": username,
                "email": f"{username}@example.com",
                "full_name": f"User {username}"
            }
            return await client.post("/users/", json=user_data)

        # Запускаем несколько запросов одновременно
        tasks = [
            create_user(f"concurrent{i}") 
            for i in range(5)
        ]

        responses = await asyncio.gather(*tasks)

        # Проверяем результаты
        success_count = sum(1 for r in responses if r.status_code == 200)
        assert success_count == 5

        # Очищаем
        from your_app.models import User
        from sqlalchemy import delete

        await db_session.execute(delete(User))
        await db_session.commit()