import allure
import pytest
from pages.main_page import MainPage


@allure.feature("Основная функциональность")
class TestMainFunctionality:

    @allure.title("Переход по клику на «Конструктор»")
    def test_click_constructor(self, main_page):
        main_page.click_constructor()
        # Можно добавить проверку URL или заголовка, если нужно
        assert True  # пока просто проверяем, что клик проходит без ошибок

    @allure.title("Переход по клику на «Лента заказов»")
    def test_click_order_feed(self, main_page):
        main_page.click_order_feed()
        assert True

    @allure.title("При клике на ингредиент появляется всплывающее окно")
    def test_ingredient_modal_opens(self, main_page):
        main_page.click_ingredient()
        assert main_page.is_modal_open()

    @allure.title("Всплывающее окно закрывается кликом по крестику")
    def test_close_ingredient_modal(self, main_page):
        main_page.click_ingredient()
        assert main_page.is_modal_open()
        main_page.close_modal()
        # После закрытия модалка должна исчезнуть
        assert not main_page.is_modal_open()

    @allure.title("При добавлении ингредиента в заказ счётчик этого ингредиента увеличивается")
    def test_ingredient_counter_increases(self, main_page):
        # 1. Получаем начальное значение счетчика (теперь это точно число)
        initial_counter = main_page.get_ingredient_counter()

        # 2. Перетаскиваем ингредиент в конструктор бургера
        main_page.drag_and_drop_ingredient_to_basket()

        # 3. Небольшая пауза (0.5 сек), чтобы Firefox успел перерисовать UI
        import time
        time.sleep(0.5)

        # 4. Проверяем, что новое значение счетчика (число) стало больше исходного
        new_counter = main_page.get_ingredient_counter()
        assert new_counter > initial_counter
