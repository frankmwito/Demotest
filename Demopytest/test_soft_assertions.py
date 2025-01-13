import softest
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestSoftLambdatest(softest.TestCase):  # Class name starts with 'Test'
    def test_soft_assertions(self):  # Method name starts with 'test_'
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        
        try:
            driver.get("https://ecommerce-playground.lambdatest.io/")
            driver.maximize_window()
            
            # Search for "Iphone" and verify
            search = driver.find_element(By.CSS_SELECTOR, "div[id='entry_217822'] input[placeholder='Search For Products']")
            search.send_keys("iphone")
            
            wait = WebDriverWait(driver, timeout=5, poll_frequency=0.5)
            input = wait.until(EC.presence_of_element_located((By.XPATH, "(//img[@title='iPhone'])[1]")))
            input.click()
            
            WebDriverWait(driver, timeout=5, poll_frequency=1)
            product = driver.find_element(By.XPATH, "//h1[normalize-space()='iPhone']").text
            self.soft_assert(self.assertEqual, "iphone".lower(), product.lower(), "Assertion Error: That is not what we searched for")
            
            self.assert_all()
            
            
        
        finally:
            driver.quit()
