from playwright.sync_api import sync_playwright, Playwright
import time


def run(playwright : Playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://demoqa.com/")
    page.locator("div.card-body >> text=Elements").click()
    page.locator("span.text >> text=Text Box").click()

    full_name = page.locator("//input[@id='userName']").fill("Connor Mcgregor")
    email = page.locator("//input[@id='userEmail']").fill("connor_mcgregor@yahoo.com")
    current_adress = page.locator("//textarea[@id='currentAddress']").fill("Ireland")
    permanent_adress = page.locator("//textarea[@id='permanentAddress']").fill("Around the globe")

    page.locator("//button[@id='submit']").click()
    browser.close()


with sync_playwright() as p:
    run(p)





