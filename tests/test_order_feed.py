import pytest
import allure
import time


@allure.feature("Лента заказов")
class TestOrderFeed:

    def helper_prepare_user_and_login(self, main_page):
        # 4 пробела от края класса
        timestamp = int(time.time())
        email = f"stey_ui_{timestamp}@yandex.ru"
        password = "password123"
        name = "Anastasia"
        main_page.register_user_via_ui(name, email, password)
        main_page.login(email, password)

    @allure.title("При создании нового заказа счётчик «Выполнено за всё время» увеличивается")
    def test_total_orders_counter_increases(self, main_page):
        # 4 пробела от края класса
        main_page.click_order_feed()
        initial_total = main_page.get_total_orders_count()

        main_page.click_constructor()
        self.helper_prepare_user_and_login(main_page)
        main_page.drag_and_drop_ingredient_to_basket()
        main_page.click_create_order()
        main_page.close_modal()

        main_page.click_order_feed()
        assert main_page.wait_for_counter_to_increase(initial_total, "total")

    @allure.title("При создании нового заказа счётчик «Выполнено за сегодня» увеличивается")
    def test_today_orders_counter_increases(self, main_page):
        # 4 пробела от края класса
        main_page.click_order_feed()
        initial_today = main_page.get_today_orders_count()

        main_page.click_constructor()
        self.helper_prepare_user_and_login(main_page)
        main_page.drag_and_drop_ingredient_to_basket()
        main_page.click_create_order()
        main_page.close_modal()

        main_page.click_order_feed()
        assert main_page.wait_for_counter_to_increase(initial_today, "today")

    @allure.title("После оформления заказа его номер появляется в разделе «В работе»")
    def test_order_number_appears_in_progress_section(self, main_page):
        # 4 пробела от края класса
        self.helper_prepare_user_and_login(main_page)
        main_page.drag_and_drop_ingredient_to_basket()
        main_page.click_create_order()
        order_number = main_page.get_order_number_from_modal()
        main_page.close_modal()

        main_page.click_order_feed()
        assert main_page.is_order_in_progress(order_number)
