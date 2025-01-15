from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import pytest

@pytest.mark.usefixtures("setup_method")
class TestMarkers:
    @pytest.fixture(scope="class", autouse=True)
    def setup_method(self, request):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get("https://ecommerce-playground.lambdatest.io/")
        self.driver.maximize_window()
        request.addfinalizer(lambda: self.driver.quit() if hasattr(self, "driver") else None)

    @pytest.mark.login
    def test_login(self):
        # Login functionality
        actions = ActionChains(self.driver)
        my_account = self.driver.find_element(By.XPATH, "//a[@role='button']//span[@class='title'][normalize-space()='My account']")
        actions.move_to_element(my_account).perform()
        login_button = self.driver.find_element(By.XPATH, "//span[normalize-space()='Login']")
        login_button.click()

        # Validate login page
        assert "login" in self.driver.current_url, "Failed to navigate to the login page"

    @pytest.mark.registration
    def test_registration(self):
        # Registration functionality
        actions = ActionChains(self.driver)
        my_account = self.driver.find_element(By.XPATH, "//a[@role='button']//span[@class='title'][normalize-space()='My account']")
        actions.move_to_element(my_account).perform()
        register_button = self.driver.find_element(By.XPATH, "//span[normalize-space()='Register']")
        register_button.click()

        # Validate registration page
        assert "register" in self.driver.current_url, "Failed to navigate to the registration page"
