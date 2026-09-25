import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class OrderFeedPage(BasePage):
    # 1. Локаторы счетчиков (Объявлены строго внутри класса, с отступом 4 пробела)
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
        # 1. Очищаем номер от знака #
        clean_number = order_number.replace("#", "").strip()

        # 2. Формируем вариант номера с ведущими нулями (до 6 знаков), например "040395"
        padded_number = clean_number.zfill(6)

        # 3. Ищем элемент, который содержит ЛИБО чистый номер, ЛИБО номер с нулями
        # строго под заголовком колонки "В работе:"
        xpath = (
            f"//p[contains(text(), 'В работе:')]/following-sibling::ul"
            f"//*[contains(text(), '{clean_number}') or contains(text(), '{padded_number}')]"
        )
        return (By.XPATH, xpath)

    # feed_page.py

    @allure.step("Проверить, что заказ {order_number} появился в разделе «В работе»")
    def is_order_in_progress(self, order_number: str, timeout: int = 30) -> bool:
        """Проверяет появление номера заказа в разделе 'В работе' с обновлением страницы."""
        clean_number = order_number.replace("#", "").strip()
        padded_number = clean_number.zfill(6)

        # Более гибкий локатор - ищем номер в любом месте страницы
        xpath = (
            f"//ul//*[contains(text(), '{clean_number}') or contains(text(), '{padded_number}')]"
        )
        locator = (By.XPATH, xpath)

        # Пробуем найти с несколькими обновлениями страницы
        for attempt in range(5):
            if self.is_element_visible(locator, timeout=timeout // 5):
                return True
            if attempt < 4:  # Не обновляем после последней попытки
                self.driver.refresh()
                # Ждем загрузки страницы
                self.wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Лента заказов')]")))

        return False

