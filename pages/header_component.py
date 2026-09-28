
import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class HeaderComponent(BasePage):
    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[text()='Конструктор']")
    ORDER_FEED_BUTTON = (By.XPATH, "//p[text()='Лента Заказов']")
    LOGIN_LINK = (By.XPATH, "//button[text()='Войти в аккаунт']")

    @allure.step("Перейти в раздел «Конструктор»")
    def click_constructor(self):
        self.click_via_js(self.CONSTRUCTOR_BUTTON)

    @allure.step("Перейти в раздел «Лента заказов»")
    def click_order_feed(self):
        self.click_via_js(self.ORDER_FEED_BUTTON)

    @allure.step("Открыть форму входа")
    def click_login(self):
        self.click_element(self.LOGIN_LINK)
