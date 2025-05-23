from playwright.sync_api import sync_playwright
import pytest

FULL_NAME = 'Connor McGregor'
EMAIL = 'theonetheonly@yahoo.com'
CURRENT_ADDRESS = 'Ireland'
PERMANENT_ADDRESS = 'Around the globe'
URL = "https://demoqa.com/"
DIV_OUTPUT_FRAME_selector = "div[contains(@class,'col-md-12 col-sm-1')]"
EXPAND_COLLAPSE_TITLES_LOCATOR_SELECTOR = "//span[@class='rct-title']"
TITLE_SELECTOR = "//span[@class='rct-text' and .//span[@class='rct-title' and text()='{}']]"

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
            browser = p.chromium.launch(headless=False, slow_mo=800)
            self.page = browser.new_page()
            self.page.goto(URL)

            yield

            browser.close()

    def select_card_body(self, card_name):
        self.page.locator(f"//div[contains(@class, 'top-card') and .//h5[text()='{card_name}']]").click()

    def select_element_button_left_panel(self, button_name):
        self.page.locator(f"//li[contains(@class, 'btn-light') and .//span[text()='{button_name}']]").click()

    def get_ui_titles_after_clicking_button(self, action_name):
        try:
            button_selector = f"//div[@class='rct-options']/button[contains(@class, 'rct-option-{action_name}-all')]"
            self.page.locator(button_selector).click()
            list_of_titles_locator = self.page.locator(EXPAND_COLLAPSE_TITLES_LOCATOR_SELECTOR).all()
            return [title.inner_text() for title in list_of_titles_locator]

        except Exception as exception:
            print(f"Failed to get ui titles after clicking button : {action_name} -> {exception}")
            return None

    def format_input_for_output(self, input_text):
        documents = input_text.split(">")
        yield documents  # to iterate in documents until chosen one
        if documents[-1].endswith(".doc"):
            documents[-1] = documents[-1][:-4].split()
            documents[-1][0] = documents[-1][0].lower()
            documents[-1][0] = documents[-1][0] + documents[-1][1]
            aux = documents[-1][0]
            documents[-1].pop()
            documents[-1].pop()
            documents.remove([])
            documents = [doc.lower() for doc in documents]
            documents.append(aux)
        yield documents  # locate checkbox for last document

    def search_document_in_path(self, list_of_documents_to_iterate, list_of_documents, last_doc):
        print(f" ---->    {list_of_documents_to_iterate}")
        for each_doc in list_of_documents_to_iterate:
            if each_doc == last_doc:
                continue
            else:
                self.page.locator(f"//span[@class='rct-text' and .//span[@class='rct-title' and"
                                  f" text()='{each_doc}']]/"
                                  "button[@title='Toggle']").click()
        if last_doc[0].isupper():
            check_box = self.page.locator(f"//label[@for='tree-node-{last_doc.lower()}']/"
                                          f"span[@class='rct-checkbox']")
        else:
            check_box = self.page.locator(f"//label[@for='tree-node-{last_doc}']/"
                                          f"span[@class='rct-checkbox']")
        check_box.click()
        if check_box.is_checked():
            output = self.page.locator("//div[@id='result']/span[@class='text-success']").all()
            return [each_output.inner_text() for each_output in output]
        return None

    def search_document_and_enable_last_title(self, list_titles):
        if len(list_titles) > 1:
            for title in list_titles[:-1]:
                self.page.locator(TITLE_SELECTOR.format(title) + "/button[@title='Toggle']").click()

        check_box = self.page.locator(TITLE_SELECTOR.format(list_titles[-1]) + "//span[@class='rct-checkbox']")
        check_box.check()
        if check_box.is_checked():
            return True
        return False

    def get_output_ui(self):
        output = self.page.locator("//div[@id='result']/span[@class='text-success']").all()
        return [each_output.inner_text() for each_output in output]

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

        titles_expand = self.get_ui_titles_after_clicking_button("expand")

        assert titles_expand == list_expected_expand, "There are not the same elements for EXPAND BUTTON"
        print("\nThere are all the items !")

        collapse_items_list_titles = self.get_ui_titles_after_clicking_button("collapse")
        assert collapse_items_list_titles == list_expected_collapse, ("There are not"
                                                                      " the same elements for COLLAPSE BUTTON")
        print("The collapse button working fine !")

    def test_verify_document_in_output_checked(self):
        TITLES_MENU_TO_OUTPUT_MAPPED_DICT = {
            'Word File.doc': 'wordFile',
            'Excel File.doc': 'excelFile',
        }
        self.select_card_body("Elements")
        self.select_element_button_left_panel("Check Box")
        search_input_doc = input("Choose a path (Example : Document1>Document2>Document3... ) : ")
        list_search_input_doc = search_input_doc.split(">")
        is_checked = self.search_document_and_enable_last_title(list_search_input_doc)
        assert is_checked, "I can not checked the box for last title"
        last_title_formated = list_search_input_doc[-1].lower() if ".doc" not in list_search_input_doc[-1] else\
            TITLES_MENU_TO_OUTPUT_MAPPED_DICT[list_search_input_doc[-1]]
        assert last_title_formated in self.get_output_ui(), "The title was not found in the output"
        # generator = self.format_input_for_output(search_input_doc)
        # first_list_with_docs_formated = next(generator)
        # second_list_with_docs_formated = next(generator)
        # last_doc = second_list_with_docs_formated[-1]
        # if last_doc[0].isupper():
        #     assert last_doc.lower() in self.search_document_in_path(first_list_with_docs_formated, second_list_with_docs_formated, last_doc), \
        #         "The title was not found in the output"
        # else:
        #     assert last_doc in self.search_document_in_path(first_list_with_docs_formated, second_list_with_docs_formated, last_doc), \
        #         "The title was not found in the output"
        # print("The title was found in the output")

    def test_verify_radio_buttons(self):
        self.select_card_body("Elements")
        self.select_element_button_left_panel("Radio Button")
        RADIO_BUTTON_SELECTOR = "//div[contains(@class,'custom-control-inline')]/input[@id='{}']"
        RADIO_BUTTON_OUTPUT_SELECTOR = "//p[@class='mt-3']/span[text() = '{}']"
        yes_radio_button = self.page.locator(RADIO_BUTTON_SELECTOR.format('yesRadio'))

        if yes_radio_button.is_visible():
            yes_radio_button.check(force=True)
        assert self.page.locator(RADIO_BUTTON_OUTPUT_SELECTOR.format("Yes")).is_visible(), "I can't click Yes button"

        impressive_radio_button = self.page.locator(RADIO_BUTTON_SELECTOR.format('impressiveRadio'))
        if impressive_radio_button.is_visible():
            impressive_radio_button.check(force=True)
        assert self.page.locator(RADIO_BUTTON_OUTPUT_SELECTOR.format("Impressive")).is_visible(), \
            "I can't click Impressive button"

        no_radio_button = self.page.locator(RADIO_BUTTON_SELECTOR.format('noRadio'))
        assert no_radio_button.is_disabled(), " NO Button is enabled "

    def test_verify_click_buttons(self):
        self.select_card_body("Elements")
        self.select_element_button_left_panel("Buttons")

        self.page.locator("#doubleClickBtn").click(click_count=2)
        output = self.page.locator("#doubleClickMessage").inner_text()
        assert output == "You have done a double click", "Something went wrong with double click button"

        self.page.locator("#rightClickBtn").click(button="right")
        output = self.page.locator("#rightClickMessage").inner_text()
        assert output == "You have done a right click", "Something went wrong with right click button"

        self.page.locator("button[class='btn btn-primary']:text-is('Click Me')").click(button="left")
        output = self.page.locator("#dynamicClickMessage").inner_text()
        assert output == "You have done a dynamic click", "Something went wrong with left click button"


