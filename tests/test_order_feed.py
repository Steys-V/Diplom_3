import allure
from pages.login_page import LoginPage

TEST_INGREDIENT_NAME = "Флюоресцентная булка R2-D3"


def login_via_ui(pages, email: str, password: str):
    """Вход через UI с использованием данных из фикстуры api_user."""
    pages.main.header.click_login()
    pages.login.login(email, password)
    pages.main.wait_for_authorized_state()


@allure.feature("Лента заказов")
class TestOrderFeed:

    @allure.title("При создании нового заказа счётчик «Выполнено за всё время» увеличивается")
    def test_total_orders_counter_increases(self, pages, api_user):
        pages.main.header.click_order_feed()
        initial_total = pages.feed.get_total_orders_count()
        pages.main.header.click_constructor()

        login_via_ui(pages, api_user["email"], api_user["password"])

        pages.main.drag_and_drop_ingredient_to_basket(TEST_INGREDIENT_NAME)
        pages.main.click_create_order()
        pages.main.close_modal()
        pages.main.header.click_order_feed()
        assert pages.feed.wait_for_counter_to_increase(initial_total, "total")

    @allure.title("При создании нового заказа счётчик «Выполнено за сегодня» увеличивается")
    def test_today_orders_counter_increases(self, pages, api_user):
        pages.main.header.click_order_feed()
        initial_today = pages.feed.get_today_orders_count()
        pages.main.header.click_constructor()

        login_via_ui(pages, api_user["email"], api_user["password"])

        pages.main.drag_and_drop_ingredient_to_basket(TEST_INGREDIENT_NAME)
        pages.main.click_create_order()
        pages.main.close_modal()
        pages.main.header.click_order_feed()
        assert pages.feed.wait_for_counter_to_increase(initial_today, "today")

    @allure.title("После оформления заказа его номер появляется в разделе «В работе»")
    def test_order_number_appears_in_progress_section(self, pages, api_user):
        login_via_ui(pages, api_user["email"], api_user["password"])
        pages.main.drag_and_drop_ingredient_to_basket(TEST_INGREDIENT_NAME)
        pages.main.click_create_order()
        order_number = pages.main.get_order_number_from_modal()
        pages.main.close_modal()
        pages.main.header.click_order_feed()

        assert pages.feed.is_order_in_progress(order_number, timeout=60)