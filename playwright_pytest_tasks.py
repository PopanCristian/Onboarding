from playwright.sync_api import sync_playwright, Playwright
FULL_NAME = 'Connor McGregor'
EMAIL = 'theonetheonly@yahoo.com'
CURRENT_ADDRESS = 'Ireland'
PERMANENT_ADDRESS = 'Around the globe'



def run(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False, slow_mo=10)
    page = browser.new_page()

    page.goto("https://demoqa.com/")
    page.locator("//div[contains(@class, 'top-card') and .//h5[text()='Elements']]").click()
    page.locator("//li[contains(@class, 'btn-light') and .//span[text()='Text Box']]").click()
    full_name = page.locator("//input[@id='userName']").fill(FULL_NAME)
    email = page.locator("//input[@id='userEmail']").fill(EMAIL)
    current_adress = page.locator("//textarea[@id='currentAddress']").fill(CURRENT_ADDRESS)
    permanent_adress = page.locator("//textarea[@id='permanentAddress']").fill(PERMANENT_ADDRESS)

    page.locator("//button[@id='submit']").click()

    output_full_name = page.locator("//div[contains(@class,'col-md-12 col-sm-1')]/"
                                    "p[@id='name']").inner_text().replace("Name:", "")
    output_email = page.locator("//div[contains(@class,'col-md-12 col-sm-1')]/"
                                "p[@id='email']").inner_text().replace("Email:", "")
    output_current_address = page.locator("//div[contains(@class,'col-md-12 col-sm-1')]/"
                                          "p[@id='currentAddress']").inner_text().replace("Current Address :", "")
    output_permanent_address = page.locator("//div[contains(@class,'col-md-12 col-sm-1')]"
                                            "/p[@id='permanentAddress']").inner_text().replace("Permananet Address :", "")

    initial_list = [FULL_NAME,EMAIL,CURRENT_ADDRESS,PERMANENT_ADDRESS]
    output_list = [output_full_name,output_email,output_current_address,output_permanent_address]
    same_data = lambda: initial_list == output_list
    assert same_data(), "They are not the same"
    print("They are the same !")
    browser.close()


with sync_playwright() as p:
    run(p)





