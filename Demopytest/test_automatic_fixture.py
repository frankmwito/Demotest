# set an automatic fixture

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import key_actions
import pytest


#  setup browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) 

@pytest.fixture
def shared_credentials():
    first_name = "Frank"
    last_name = "Lambert"
    mail = "flambert22@gmail.com"
    telephone = 1312345678
    password = 1234567890
    return first_name, last_name, mail, telephone, password

@pytest.fixture(autouse=True)
def setup_automatic_fixture():
    print("Automatic Pytest Fixture")

@pytest.fixture(scope="module")
def setup_teardown1():
   driver.get("https://ecommerce-playground.lambdatest.io/")
   yield 
   print("this is the setup")
   driver.quit()
   print("This is the Teardown")


@pytest.mark.usefixtures(setup_teardown1)
def test_signup(shared_credentials):
    first_name, last_name, Email, telephone, password = shared_credentials
    my_account = driver.find_element(By.XPATH,'//*[@id="widget-navbar-217834"]/ul/li[6]/a')
    actions = ActionChains(driver)
    actions.move_to_element(my_account).perform()
    register = driver.find_element(By.XPATH,"//span[normalize-space()='Register']")
    register.click
    
        # Fill the registration form with shared credentials
    driver.find_element(By.ID, "input-firstname").send_keys(first_name)
    driver.find_element(By.ID, "input-lastname").send_keys(last_name)
    driver.find_element(By.ID, "input-email").send_keys(Email)
    driver.find_element(By.ID, "input-telephone").send_keys(telephone)
    driver.find_element(By.ID, "input-password").send_keys(password)
    driver.find_element(By.ID, "input-confirm").send_keys(password)
    
    driver.find_element(By.XPATH, "//label[normalize-space()='Yes']").click()
    driver.find_element(By.XPATH, "//label[normalize-space()='No']").click()

    # Agree to terms and submit the form
    driver.find_element(By.XPATH, "//label[@for='input-agree']").click()
    driver.find_element(By.XPATH, "//input[@value='Continue']").click()
    
    assert "success" in driver.current_url or "account/success" in driver.current_url, "Registration was not successful."
    text = driver.find_element(By.XPATH, "//h1[normalize-space()='Your Account Has Been Created!']").text
    print(text)
    assert "success" in text, "Failed Registration"
 
@pytest.mark.usefixtures(setup_teardown1)
def test_login(shared_credentials):
    first_name, last_name, Email, telephone, password = shared_credentials
    # Navigate to login page
    myaccount = driver.find_element(By.XPATH, '//*[@id="widget-navbar-217834"]/ul/li[6]/a')
    actions = ActionChains(driver)
    actions.move_to_element(myaccount).perform()
    login = driver.find_element(By.XPATH, "//a[@href='https://ecommerce-playground.lambdatest.io/index.php?route=account/login']")
    login.click()

    # Use the loaded credentials for login
    driver.find_element(By.ID, "input-email").send_keys(Email)
    driver.find_element(By.ID, "input-password").send_keys(password)
    driver.find_element(By.XPATH, "//input[@value='Login']").click()
    welcome = driver.find_element(By.XPATH, "(//h2[normalize-space()='My Account'])[1]").text
    assert "my account" == welcome.lower(), "You have failed to login"