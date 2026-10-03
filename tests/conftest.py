from dataclasses import dataclass
import pytest
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.feed_page import OrderFeedPage
from utils.urls import Urls
from helpers.api import register_user, login_user, delete_user


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    browser = request.param
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options,
        )
    else:
        options = webdriver.FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        driver = webdriver.Firefox(options=options)

    yield driver
    driver.quit()


@dataclass
class Pages:
    main: MainPage
    login: LoginPage
    register: RegisterPage
    feed: OrderFeedPage


@pytest.fixture
def pages(driver) -> Pages:
    main_page = MainPage(driver)
    main_page.open(Urls.BASE_URL)
    return Pages(
        main=main_page,
        login=LoginPage(driver),
        register=RegisterPage(driver),
        feed=OrderFeedPage(driver),
    )


@pytest.fixture(scope="function")
def api_user():
    """Создаёт пользователя через API перед тестом и удаляет после."""
    unique_id = str(uuid.uuid4())[:8]
    user_data = {
        "email": f"test_{unique_id}@mail.ru",
        "password": "password123",
        "name": f"Test User {unique_id}",
    }

    response = register_user(
        user_data["email"],
        user_data["password"],
        user_data["name"],
    )
    response.raise_for_status()

    yield user_data

    try:
        login_resp = login_user(user_data["email"], user_data["password"])
        login_resp.raise_for_status()
        access_token = login_resp.json().get("accessToken")
        delete_resp = delete_user(access_token)
        delete_resp.raise_for_status()
    except Exception as e:
        print(f"Warning: Failed to delete user {user_data['email']}: {e}")