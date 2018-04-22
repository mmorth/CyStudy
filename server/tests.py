# Basic webrowser test
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

# browser = webdriver.Firefox(executable_path="C:\\Users\\mmort\\Downloads\\geckodriver-v0.19.1-win64\\geckodriver.exe")

# browser.get('http://www.yahoo.com')
# assert 'Not-Google' in browser.title

# elem = browser.find_element_by_name('p')  # Find the search box
# elem.send_keys('seleniumhq' + Keys.RETURN)

# browser.quit()

# Selinium Test Class
import unittest

from selenium import webdriver

from selenium.webdriver.common.keys import Keys

class SeliniumTests(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox(executable_path="C:\\Users\\mmort\\Downloads\\geckodriver-v0.19.1-win64\\geckodriver.exe")

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("http://www.python.org")
        self.assertIn("Python", driver.title)
        elem = driver.find_element_by_name("q")
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found" not in driver.page_source

    def tear_down(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()