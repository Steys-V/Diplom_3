import uuid


def generate_unique_email():
    """Генерирует уникальный email для тестового пользователя."""
    unique_id = str(uuid.uuid4())[:8]
    return f"test_{unique_id}@mail.ru"


def generate_unique_name():
    """Генерирует уникальное имя для тестового пользователя."""
    unique_id = str(uuid.uuid4())[:8]
    return f"Test User {unique_id}"


def generate_user_data():
    """Генерирует полные данные тестового пользователя."""
    unique_id = str(uuid.uuid4())[:8]
    return {
        "email": f"test_{unique_id}@mail.ru",
        "password": "password123",
        "name": f"Test User {unique_id}",
    }