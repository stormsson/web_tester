import tempfile

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class DriverFactory():
    WEBDRIVER_GECKODRIVER_PATH="/usr/local/bin/geckodriver"
    WEBDRIVER_CHROMEDRIVER_PATH="/usr/local/bin/chromedriver"

    @staticmethod
    def getChromeDriver():
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(executable_path=DriverFactory.WEBDRIVER_CHROMEDRIVER_PATH, chrome_options=options)
        return driver

    def getFirefoxDriver():
        profile = tempfile.mkdtemp(".selenium")

        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("-profile")
        options.add_argument(profile)
        options.accept_insecure_certs = True
        options.log.level = "trace"

        driver = webdriver.Firefox(options=options)
        return driver
