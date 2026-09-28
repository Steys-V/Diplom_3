import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    DEFAULT_TIMEOUT = 10

    def __init__(self, driver, timeout: int = DEFAULT_TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ---------- поиск и чтение ----------
    @allure.step("Найти элемент {locator}")
    def find_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    @allure.step("Найти все элементы {locator}")
    def find_elements(self, locator):
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    @allure.step("Получить текст элемента {locator}")
    def get_text(self, locator) -> str:
        return self.find_element(locator).text

    @allure.step("Проверить видимость элемента {locator}")
    def is_element_visible(self, locator, timeout: int | None = None) -> bool:
        wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
        try:
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    @allure.step("Проверить невидимость элемента {locator}")
    def is_element_invisible(self, locator, timeout: int | None = None) -> bool:
        wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
        try:
            wait.until(EC.invisibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    # ---------- клики ----------
    @allure.step("Кликнуть по элементу {locator}")
    def click_element(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    @allure.step("Кликнуть через JavaScript по элементу {locator}")
    def click_via_js(self, locator):
        """Клик через JS — нужен, когда обычный клик перехватывает оверлей/модалка."""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].click();", element)
        return element

    # ---------- прочая работа с драйвером ----------
    @allure.step("Обновить страницу и дождаться элемента {locator}")
    def refresh_and_wait(self, locator):
        """Обновляет страницу и явно ждёт, пока элемент снова появится."""
        self.driver.refresh()
        return self.find_element(locator)

    @allure.step("Открыть страницу по адресу {url}")
    def open_page(self, url: str):
        """Открывает страницу по-указанному URL."""
        self.driver.get(url)

    @allure.step("Ожидать условие {condition}")
    def wait_until(self, condition, timeout: int | None = None):
        """Явное ожидание произвольного условия."""
        wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
        return wait.until(condition)

    @allure.step("Перетащить элемент {source_locator} на {target_locator}")
    def drag_and_drop(self, source_locator, target_locator):
        """Перетаскивание элемента через эмуляцию HTML5 Drag-and-Drop событий."""
        source = self.find_element(source_locator)
        target = self.find_element(target_locator)
        js_script = """
        const source = arguments[0];
        const target = arguments[1];
        const dataTransfer = new DataTransfer();
        source.dispatchEvent(new DragEvent('dragstart', { bubbles: true, cancelable: true, dataTransfer }));
        target.dispatchEvent(new DragEvent('dragover', { bubbles: true, cancelable: true, dataTransfer }));
        target.dispatchEvent(new DragEvent('drop', { bubbles: true, cancelable: true, dataTransfer }));
        source.dispatchEvent(new DragEvent('dragend', { bubbles: true, cancelable: true, dataTransfer }));
        """
        self.driver.execute_script(js_script, source, target)