import allure

# Название ингредиента, используемого в тестах. Должно точно совпадать
# с названием на сайте — проверь и подставь актуальное через DevTools
# (F12 -> клик по ингредиенту -> посмотреть текст внутри карточки).
TEST_INGREDIENT_NAME = "Флюоресцентная булка R2-D3"


@allure.feature("Основная функциональность")
class TestMainFunctionality:

    @allure.title("Переход по клику на «Конструктор»")
    def test_click_constructor(self, pages):
        pages.main.header.click_constructor()
        assert pages.main.is_element_visible(pages.main.CONSTRUCTOR_BASKET)

    @allure.title("Переход по клику на «Лента заказов»")
    def test_click_order_feed(self, pages):
        pages.main.header.click_order_feed()
        assert pages.feed.is_element_visible(pages.feed.IN_PROGRESS_SECTION)

    @allure.title("При клике на ингредиент появляется всплывающее окно")
    def test_ingredient_modal_opens(self, pages):
        pages.main.click_ingredient(TEST_INGREDIENT_NAME)
        assert pages.main.is_modal_open()

    @allure.title("Всплывающее окно закрывается кликом по крестику")
    def test_close_ingredient_modal(self, pages):
        pages.main.click_ingredient(TEST_INGREDIENT_NAME)
        assert pages.main.is_modal_open()

        pages.main.close_modal()
        assert not pages.main.is_modal_open()

    @allure.title("При добавлении ингредиента в заказ счётчик этого ингредиента увеличивается")
    def test_ingredient_counter_increases(self, pages):
        initial_counter = pages.main.get_ingredient_counter(TEST_INGREDIENT_NAME)

        pages.main.drag_and_drop_ingredient_to_basket(TEST_INGREDIENT_NAME)

        assert pages.main.wait_for_ingredient_counter_increase(TEST_INGREDIENT_NAME, initial_counter)
