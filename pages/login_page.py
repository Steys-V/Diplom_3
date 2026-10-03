import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    EMAIL_INPUT = (By.XPATH, "//label[text()='Email']/following-sibling::input")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    SUBMIT_LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти']")
    REGISTER_LINK = (By.XPATH, "//a[text()='Зарегистрироваться']")

    @allure.step("Перейти на форму регистрации")
    def click_register_link(self):
        self.click_element(self.REGISTER_LINK)

    @allure.step("Дождаться отображения формы входа")
    def wait_for_login_form(self):
        self.find_element(self.SUBMIT_LOGIN_BUTTON)

    @allure.step("Войти под пользователем {email}")
    def login(self, email: str, password: str):
        self.find_element(self.EMAIL_INPUT).send_keys(email)
        self.find_element(self.PASSWORD_INPUT).send_keys(password)
        self.click_element(self.SUBMIT_LOGIN_BUTTON)
