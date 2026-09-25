
import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.header_component import HeaderComponent


class MainPage(BasePage):
    CONSTRUCTOR_BASKET = (By.XPATH, "//ul[contains(@class, 'BurgerConstructor_basket')]")
    MODAL = (By.XPATH, "//section[contains(@class, 'Modal_modal_opened')]")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")
    CREATE_ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")
    ORDER_NUMBER_IN_MODAL = (By.XPATH, "//h2[contains(@class, 'Modal_modal__title')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.header = HeaderComponent(driver)

    @staticmethod
    def ingredient_link_locator(ingredient_name: str):
        """Локатор ссылки конкретного ингредиента — привязан к его
        названию, а не к позиции в списке."""
        return (
            By.XPATH,
            "//a[contains(@class, 'BurgerIngredient_ingredient') and "
            f".//p[contains(text(), '{ingredient_name}')]]",
        )

    @staticmethod
    def ingredient_counter_locator(ingredient_name: str):
        return (
            By.XPATH,
            "//a[contains(@class, 'BurgerIngredient_ingredient') and "
            f".//p[contains(text(), '{ingredient_name}')]]"
            "//p[contains(@class, 'counter_counter__num')]",
        )

    @allure.step("Открыть страницу конструктора")
    def open(self, url: str):
        self.driver.get(url)

    @allure.step("Кликнуть по ингредиенту «{ingredient_name}»")
    def click_ingredient(self, ingredient_name: str):
        self.click_element(self.ingredient_link_locator(ingredient_name))

    @allure.step("Проверить, что модальное окно ингредиента открыто")
    def is_modal_open(self) -> bool:
        return self.is_element_visible(self.MODAL)

    @allure.step("Закрыть модальное окно ингредиента")
    def close_modal(self):
        self.click_via_js(self.MODAL_CLOSE_BUTTON)
        self.is_element_invisible(self.MODAL)

    @allure.step("Получить значение счётчика ингредиента «{ingredient_name}»")
    def get_ingredient_counter(self, ingredient_name: str) -> int:
        locator = self.ingredient_counter_locator(ingredient_name)
        if not self.is_element_visible(locator, timeout=2):
            return 0
        return int(self.get_text(locator))

    @allure.step("Дождаться увеличения счётчика ингредиента «{ingredient_name}»")
    def wait_for_ingredient_counter_increase(self, ingredient_name: str, initial_value: int, timeout: int = 5) -> bool:
        locator = self.ingredient_counter_locator(ingredient_name)

        def _counter_increased(driver):
            elements = driver.find_elements(*locator)
            if not elements:
                return False
            text = elements[0].text
            return text.isdigit() and int(text) > initial_value

        return self.wait_until(_counter_increased, timeout=timeout)

    @allure.step("Перетащить ингредиент «{ingredient_name}» в конструктор")
    def drag_and_drop_ingredient_to_basket(self, ingredient_name: str):
        self.drag_and_drop(self.ingredient_link_locator(ingredient_name), self.CONSTRUCTOR_BASKET)

    @allure.step("Оформить заказ")
    def click_create_order(self):
        self.click_element(self.CREATE_ORDER_BUTTON)

    @allure.step("Получить номер заказа из модального окна")
    def get_order_number_from_modal(self, timeout: int = 10) -> str:
        def _has_real_number(driver):
            text = driver.find_element(*self.ORDER_NUMBER_IN_MODAL).text.strip()
            return text not in ("", "9999", "0000")

        self.wait_until(_has_real_number, timeout=timeout)
        return self.get_text(self.ORDER_NUMBER_IN_MODAL).strip()

    @allure.step("Дождаться завершения авторизации")
    def wait_for_authorized_state(self):
        # Явное ожидание вместо предположения "раз залогинились — значит всё ок":
        # кнопка "Оформить заказ" видна только авторизованному пользователю.
        self.find_element(self.CREATE_ORDER_BUTTON)
