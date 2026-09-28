from dataclasses import dataclass

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.feed_page import OrderFeedPage
from utils.urls import Urls


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    browser = request.param

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1920,1080")
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
    """Контейнер со всеми страницами — тест обращается к нужной
    странице через pages.main / pages.login и т.д."""
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
