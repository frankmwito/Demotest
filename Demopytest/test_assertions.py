from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def test_lambdatest_button():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        driver.get("https://ecommerce-playground.lambdatest.io/")
        
        driver.maximize_window()
        # Locate elements
        myaccount = driver.find_element(By.XPATH, "//a[@role='button']//span[@class='title'][normalize-space()='My account']")
        login_button = driver.find_element(By.XPATH, "//span[normalize-space()='Login']")
        
        # Hover over the 'My Account' menu
        actions = ActionChains(driver)
        actions.move_to_element(myaccount).perform()
        
        # Verify the login button is displayed and clickable
        assert login_button.is_displayed(), "AssertionError: Login button is not displayed on the page."
        assert login_button.is_enabled(), "AssertionError: Login button is not clickable."
        
        # Click the login button
        login_button.click()
    finally:
        driver.quit()
