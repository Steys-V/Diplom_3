import time
import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class OrderFeedPage(BasePage):
    TOTAL_ORDERS_COUNTER = (
        By.XPATH,
        "//p[contains(text(), 'Выполнено за все время')]"
        "/following-sibling::p[contains(@class, 'text_type_digits-large')]",
    )
    TODAY_ORDERS_COUNTER = (
        By.XPATH,
        "//p[contains(text(), 'Выполнено за сегодня')]"
        "/following-sibling::p[contains(@class, 'text_type_digits-large')]",
    )
    IN_PROGRESS_SECTION = (
        By.XPATH,
        "//p[contains(text(), 'В работе:')]/following-sibling::ul"
    )

    @allure.step("Получить значение счётчика «Выполнено за всё время»")
    def get_total_orders_count(self) -> int:
        return int(self.get_text(self.TOTAL_ORDERS_COUNTER))

    @allure.step("Получить значение счётчика «Выполнено за сегодня»")
    def get_today_orders_count(self) -> int:
        return int(self.get_text(self.TODAY_ORDERS_COUNTER))

    @allure.step("Дождаться увеличения счётчика заказов ({counter_name})")
    def wait_for_counter_to_increase(self, initial_value: int, counter_name: str = "total", attempts: int = 5) -> bool:
        locator = self.TOTAL_ORDERS_COUNTER if counter_name == "total" else self.TODAY_ORDERS_COUNTER
        current_value = initial_value
        for _ in range(attempts):
            current_value = int(self.get_text(locator))
            if current_value > initial_value:
                return True
            self.refresh_and_wait(locator)
        return current_value > initial_value

    def _in_progress_number_locator(self, order_number: str):
        clean_number = order_number.replace("#", "").strip()
        padded_number = clean_number.zfill(6)
        # ✅ МАГИЯ: contains(., '...') проверяет весь видимый текст, а не только прямой текстовый узел.
        # Это решает проблему, когда число есть на экране, но Selenium его "не видит".
        xpath = (
            f"//p[contains(text(), 'В работе:')]/following-sibling::ul"
            f"//*[contains(., '{clean_number}') or contains(., '{padded_number}')]"
        )
        return (By.XPATH, xpath)

    @allure.step("Проверить, что заказ {order_number} появился в разделе «В работе»")
    def is_order_in_progress(self, order_number: str, timeout: int = 30) -> bool:
        """Проверяет появление номера заказа в разделе 'В работе'."""
        # ✅ ИСПОЛЬЗУЕМ ТОЛЬКО правильный локатор, как требовал ревьюер
        locator = self._in_progress_number_locator(order_number)

        # Даём бэкенду 2 секунды на обработку заказа перед первой проверкой
        time.sleep(2)

        for attempt in range(5):
            try:
                if self.is_element_visible(locator, timeout=5):
                    return True
            except Exception:
                pass  # Игнорируем временные ошибки, переходим к обновлению

            if attempt < 4:
                self.driver.refresh()
                # Ждем появления заголовка, подтверждая, что страница действительно перезагрузилась
                self.is_element_visible((By.XPATH, "//h1[contains(text(), 'Лента заказов')]"), timeout=5)
                time.sleep(1)  # Небольшая пауза после загрузки

        return False

    @allure.step("Проверить, что лента заказов открыта")
    def is_feed_opened(self) -> bool:
        return self.is_element_visible(self.IN_PROGRESS_SECTION)