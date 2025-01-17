from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from faker import Faker
import json
import pytest

# Apply global markers
pytestmark = [pytest.mark.sanity, pytest.mark.regression]

@pytest.fixture
def setup_teardown():
    # Setup: Create WebDriver instance
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get("https://ecommerce-playground.lambdatest.io/")
    yield driver  # Pass the WebDriver instance to the test function
    # Teardown: Quit WebDriver
    driver.quit()


def save_credentials_to_file(credentials):
    with open("test_credentials.json", "w") as file:
        json.dump(credentials, file)

def load_credentials_from_file():
    with open("test_credentials.json", "r") as file:
        return json.load(file)

@pytest.mark.registration
def test_registration(setup_teardown):
    driver = setup_teardown
    faker = Faker()

    # Generate credentials
    credentials = {
        "email": faker.email(),
        "password": faker.password(),
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "telephone": faker.phone_number(),
    }

    # Navigate to registration page
    myaccount = driver.find_element(By.XPATH, '//*[@id="widget-navbar-217834"]/ul/li[6]/a')
    actions = ActionChains(driver)
    actions.move_to_element(myaccount).perform()
    register = driver.find_element(By.XPATH, "//span[normalize-space()='Register']")
    register.click()

    assert "route=account/register" in driver.current_url, "Failed to navigate to the registration page"

    # Fill the registration form with shared credentials
    driver.find_element(By.ID, "input-firstname").send_keys(credentials["first_name"])
    driver.find_element(By.ID, "input-lastname").send_keys(credentials["last_name"])
    driver.find_element(By.ID, "input-email").send_keys(credentials["email"])
    driver.find_element(By.ID, "input-telephone").send_keys(credentials["telephone"])
    driver.find_element(By.ID, "input-password").send_keys(credentials["password"])
    driver.find_element(By.ID, "input-confirm").send_keys(credentials["password"])
    
    # Save credentials to file
    save_credentials_to_file(credentials) 
    
    driver.find_element(By.XPATH, "//label[normalize-space()='Yes']").click()
    driver.find_element(By.XPATH, "//label[normalize-space()='No']").click()

    # Agree to terms and submit the form
    driver.find_element(By.XPATH, "//label[@for='input-agree']").click()
    driver.find_element(By.XPATH, "//input[@value='Continue']").click()

    # Assert URL contains "success" or "account/success"
    assert "success" in driver.current_url or "account/success" in driver.current_url, "Registration was not successful."

@pytest.mark.login
def test_login(setup_teardown):
    driver = setup_teardown

    # Load credentials from file
    credentials = load_credentials_from_file()

    # Navigate to login page
    myaccount = driver.find_element(By.XPATH, '//*[@id="widget-navbar-217834"]/ul/li[6]/a')
    actions = ActionChains(driver)
    actions.move_to_element(myaccount).perform()
    login = driver.find_element(By.XPATH, "//a[@href='https://ecommerce-playground.lambdatest.io/index.php?route=account/login']")
    login.click()

    # Use the loaded credentials for login
    driver.find_element(By.ID, "input-email").send_keys(credentials["email"])
    driver.find_element(By.ID, "input-password").send_keys(credentials["password"])
    driver.find_element(By.XPATH, "//input[@value='Login']").click()
    welcome = driver.find_element(By.XPATH, "(//h2[normalize-space()='My Account'])[1]").text
    assert "my account" == welcome.lower(), "You have failed to login"
    
