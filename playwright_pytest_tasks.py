from playwright.sync_api import sync_playwright
import pytest

FULL_NAME = 'Connor McGregor'
EMAIL = 'theonetheonly@yahoo.com'
CURRENT_ADDRESS = 'Ireland'
PERMANENT_ADDRESS = 'Around the globe'
URL = "https://demoqa.com/"
DIV_OUTPUT_FRAME_selector = "div[contains(@class,'col-md-12 col-sm-1')]"
EXPAND_COLLAPSE_TITLES_LOCATOR_SELECTOR = "//span[@class='rct-title']"
DICT_DOCUMENTS = {
    'root': ['home'],
    'Home': ['desktop', 'documents', 'downloads'],
    'Desktop': ['notes', 'commands'],
    'Documents': ['workspace', 'office'],
    'Downloads': ['wordFile', 'excelFile'],
    'WorkSpace': ['react', 'angular', 'veu'],
    'Office': ['public', 'private', 'classified', 'general']
}


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
            browser = p.chromium.launch(headless=False, slow_mo=1000)
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

    def test_task3(self):
        self.select_card_body("Elements")
        self.select_element_button_left_panel("Check Box")
        search_input_doc = input("Choose a path (Example : Document1>Document2>Document3... ) : ")
        generator = self.format_input_for_output(search_input_doc)
        first_list_with_docs_formated = next(generator)
        second_list_with_docs_formated = next(generator)
        last_doc = second_list_with_docs_formated[-1]
        if last_doc[0].isupper():
            assert last_doc.lower() in self.search_document_in_path(first_list_with_docs_formated, second_list_with_docs_formated, last_doc), \
                "The title was not found in the output"
        else:
            assert last_doc in self.search_document_in_path(first_list_with_docs_formated, second_list_with_docs_formated, last_doc), \
                "The title was not found in the output"
        print("The title was found in the output")

