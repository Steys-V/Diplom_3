import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class RegisterPage(BasePage):
    NAME_INPUT = (By.XPATH, "//label[text()='Имя']/following-sibling::input")
    EMAIL_INPUT = (By.XPATH, "//label[text()='Email']/following-sibling::input")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    SUBMIT_BUTTON = (By.XPATH, "//button[text()='Зарегистрироваться']")

    @allure.step("Зарегистрировать пользователя {email}")
    def register(self, name: str, email: str, password: str):
        self.find_element(self.NAME_INPUT).send_keys(name)
        self.find_element(self.EMAIL_INPUT).send_keys(email)
        self.find_element(self.PASSWORD_INPUT).send_keys(password)
        self.click_element(self.SUBMIT_BUTTON)
