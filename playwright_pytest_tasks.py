from playwright.sync_api import sync_playwright, expect
import pytest

FULL_NAME = 'Connor McGregor'
EMAIL = 'theonetheonly@yahoo.com'
CURRENT_ADDRESS = 'Ireland'
PERMANENT_ADDRESS = 'Around the globe'
URL = "https://demoqa.com/"
DIV_OUTPUT_FRAME_selector = "div[contains(@class,'col-md-12 col-sm-1')]"
EXPAND_BUTTON_LOCATOR = "//div[@class='rct-options']/button[contains(@class, 'rct-option-expand-all')]"
EXPAND_TITLES_LOCATOR = "//span[@class='rct-title']"
COLLAPSE_BUTTON_LOCATOR = "//div[@class='rct-options']/button[contains(@class, 'rct-option-collapse-all')]"
COLLAPSE_TITLSE_LOCATOR = "//span[@class='rct-title']"

# def run(playwright: Playwright):
#     browser = playwright.chromium.launch(headless=False, slow_mo=10)
#     page = browser.new_page()
#
#     page.goto("https://demoqa.com/")
#     page.locator("//div[contains(@class, 'top-card') and .//h5[text()='Elements']]").click()
#     page.locator("//li[contains(@class, 'btn-light') and .//span[text()='Text Box']]").click()
#     full_name = page.locator("//input[@id='userName']").fill(FULL_NAME)
#     email = page.locator("//input[@id='userEmail']").fill(EMAIL)
#     current_adress = page.locator("//textarea[@id='currentAddress']").fill(CURRENT_ADDRESS)
#     permanent_adress = page.locator("//textarea[@id='permanentAddress']").fill(PERMANENT_ADDRESS)
#
#     page.locator("//button[@id='submit']").click()
#
#     output_full_name = page.locator("//div[contains(@class,'col-md-12 col-sm-1')]/"
#                                     "p[@id='name']").inner_text().replace("Name:", "")
#     output_email = page.locator("//div[contains(@class,'col-md-12 col-sm-1')]/"
#                                 "p[@id='email']").inner_text().replace("Email:", "")
#     output_current_address = page.locator("//div[contains(@class,'col-md-12 col-sm-1')]/"
#                                           "p[@id='currentAddress']").inner_text().replace("Current Address :", "")
#     output_permanent_address = (page.locator("//div[contains(@class,'col-md-12 col-sm-1')]"
#                                             "/p[@id='permanentAddress']").inner_text().replace("Permananet "
#                                                                                                "Address :", ""))
#
#     initial_list = [FULL_NAME, EMAIL, CURRENT_ADDRESS, PERMANENT_ADDRESS]
#     output_list = [output_full_name, output_email, output_current_address, output_permanent_address]
#     same_data = lambda: initial_list == output_list
#     assert same_data(), "They are not the same"
#     print("They are the same !")
#     browser.close()


# with sync_playwright() as p:
#     run(p)


# @pytest.fixture
# def select(page, button):
#     return page.locator(button).clicked()
#
#
# @pytest.fixture
# def fill_context(page, button, context):
#     return page.page.locator(button).fill(context)


class TestClass:
    page = None

    @pytest.fixture(autouse=True, scope="function")
    def open_close_browser(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            self.page = browser.new_page()
            self.page.goto(URL)

            yield

            browser.close()

    def select_card_body(self, card_name):
        self.page.locator(f"//div[contains(@class, 'top-card') and .//h5[text()='{card_name}']]").click()

    def select_element_button_left_panel(self, button_name):
        self.page.locator(f"//li[contains(@class, 'btn-light') and .//span[text()='{button_name}']]").click()

    def get_ui_titles_after_clicking_button(self, button_locator,titles_locator):
        self.page.locator(button_locator).click()
        list_of_titles_locator = self.page.locator(titles_locator).all()
        return [title.inner_text() for title in list_of_titles_locator]


    def test_verify_text_box_view(self):
        self.select_card_body("Elements")
        self.select_element_button_left_panel("Text Box")
        self.page.locator("//input[@id='userName']").fill(FULL_NAME)
        self.page.locator("//input[@id='userEmail']").fill(EMAIL)
        self.page.locator("//textarea[@id='currentAddress']").fill(CURRENT_ADDRESS)
        self.page.locator("//textarea[@id='permanentAddress']").fill(PERMANENT_ADDRESS)

        self.page.locator("//button[@id='submit']").click()

        output_full_name_ui = self.page.locator(f"//{DIV_OUTPUT_FRAME_selector}/"
                                                "p[@id='name']").inner_text().replace("Name:", "")
        output_email_ui = self.page.locator(f"//{DIV_OUTPUT_FRAME_selector}/"
                                            "p[@id='email']").inner_text().replace("Email:", "")
        output_current_address_ui = self.page.locator(f"//{DIV_OUTPUT_FRAME_selector}/"
                                                      "p[@id='currentAddress']").inner_text().replace(
            "Current Address :", "")
        output_permanent_address_ui = (self.page.locator(f"//{DIV_OUTPUT_FRAME_selector}"
                                                         "/p[@id='permanentAddress']").inner_text().replace(
            "Permananet "
            "Address :", ""))

        initial_list = [FULL_NAME, EMAIL, CURRENT_ADDRESS, PERMANENT_ADDRESS]
        output_list = [output_full_name_ui, output_email_ui, output_current_address_ui, output_permanent_address_ui]
        same_data = lambda: initial_list == output_list
        assert same_data(), "They are not the same"
        print("They are the same !")

    def test_verify_expand_collapse_buttons(self):
        list_expected_expand = ["Home",
                                "Desktop",
                                "Notes",
                                "Commands",
                                "Documents",
                                "WorkSpace",
                                "React",
                                "Angular",
                                "Veu",
                                "Office",
                                "Public",
                                "Private",
                                "Classified",
                                "General",
                                "Downloads",
                                "Word File.doc",
                                "Excel File.doc"]
        list_expected_collapse = ["Home"]
        self.select_card_body("Elements")
        self.select_element_button_left_panel("Check Box")

        titles = self.get_ui_titles_after_clicking_button(EXPAND_BUTTON_LOCATOR, EXPAND_TITLES_LOCATOR )

        assert titles == list_expected_expand, "There are not the same elements for EXPAND BUTTON"
        print("\nThere are all the items !")

        collapse_items_list_titles = self.get_ui_titles_after_clicking_button(COLLAPSE_BUTTON_LOCATOR,
                                                                              COLLAPSE_TITLSE_LOCATOR)
        assert collapse_items_list_titles == list_expected_collapse, ("There are not"
                                                                      " the same elements for COLLAPSE BUTTON")
        print("The collapse button working fine !")
