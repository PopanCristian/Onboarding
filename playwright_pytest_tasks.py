from playwright.sync_api import sync_playwright,expect
import pytest
FULL_NAME = 'Connor McGregor'
EMAIL = 'theonetheonly@yahoo.com'
CURRENT_ADDRESS = 'Ireland'
PERMANENT_ADDRESS = 'Around the globe'



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

URL = "https://demoqa.com/"
DIV_OUTPUT_FRAME = "div[contains(@class,'col-md-12 col-sm-1')]"
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

    def test_task1_output(self):
        self.page.locator("//div[contains(@class, 'top-card') and .//h5[text()='Elements']]").click()
        self.page.locator("//li[contains(@class, 'btn-light') and .//span[text()='Text Box']]").click()
        full_name_selector = self.page.locator("//input[@id='userName']").fill(FULL_NAME)
        email_selector = self.page.locator("//input[@id='userEmail']").fill(EMAIL)
        current_adress_selector = self.page.locator("//textarea[@id='currentAddress']").fill(CURRENT_ADDRESS)
        permanent_adress_selector = self.page.locator("//textarea[@id='permanentAddress']").fill(PERMANENT_ADDRESS)

        self.page.locator("//button[@id='submit']").click()

        output_full_name_selector = self.page.locator(f"//{DIV_OUTPUT_FRAME}/"
                                        "p[@id='name']").inner_text().replace("Name:", "")
        output_email_selector = self.page.locator(f"//{DIV_OUTPUT_FRAME}/"
                                    "p[@id='email']").inner_text().replace("Email:", "")
        output_current_address_selector = self.page.locator(f"//{DIV_OUTPUT_FRAME}/"
                                              "p[@id='currentAddress']").inner_text().replace("Current Address :", "")
        output_permanent_address_selector = (self.page.locator(f"//{DIV_OUTPUT_FRAME}"
                                                "/p[@id='permanentAddress']").inner_text().replace("Permananet "
                                                                                                   "Address :", ""))

        initial_list = [FULL_NAME, EMAIL, CURRENT_ADDRESS, PERMANENT_ADDRESS]
        output_list = [output_full_name_selector, output_email_selector, output_current_address_selector, output_permanent_address_selector]
        same_data = lambda: initial_list == output_list
        assert same_data(), "They are not the same"
        print("They are the same !")

    def test_task2(self):
        self.page.locator("//div[contains(@class, 'top-card') and .//h5[text()='Elements']]").click()
        self.page.locator("//li[contains(@class, 'btn-light') and .//span[text()='Check Box']]").click()
        self.page.locator("//div[@class='rct-options']/"
                                           "button[contains(@class, 'rct-option-expand-all')]").click()
        list_expected = ["Home",
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
        expand_locator = self.page.locator("//span[@class='rct-title']")
        expect(expand_locator).to_have_text(list_expected)
        print("There are all the items !")