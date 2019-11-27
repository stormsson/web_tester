import time

from tester.base_tester import BaseTester
from tester.driver_factory import DriverFactory

from selenium import webdriver
import selenium.common.exceptions as selenium_exceptions
from selenium.webdriver.firefox.options import Options

import requests

# https://selenium-python.readthedocs.io/api.html
# https://selenium.dev/selenium/docs/api/javascript/module/selenium-webdriver/index_exports_WebElement.html

from tester.selenium_validators import test_contains

class SeleniumTester(BaseTester):

    DRIVER_CHROME = "Chrome"
    DRIVER_FIREFOX = "Firefox"
    DRIVER_SAFARI = "Safari"


    def __init__(self, driver_type=None, verbose=False, init_options=None):
        self.options = None
        self.init_options = init_options
        self.driver = None
        self.driver_type = driver_type
        self.results = []
        self.verbose = verbose


    def init_driver(self):
        if self.verbose:
            print("init webdriver %s " % self.driver_type)
        if self.driver_type == self.DRIVER_CHROME:
            self.initChrome()
        elif self.driver_type == self.DRIVER_FIREFOX:
            self.initFirefox()

        self.set_driver_resolution()


    def set_driver_resolution(self):
        res = False

        try:
            res = self.init_options['browser_resolution']
        except Exception as e:
            pass

        if res:
            res = res.split("x")
            self.driver.set_window_size(res[0], res[1])

    def initFirefox(self):
        if self.driver is not None:
            raise RuntimeError("Webdriver already init: %s instance present." % self.driver_type)

        start_time = time.time()

        self.driver = DriverFactory.getFirefoxDriver()
        self.driver_type = self.DRIVER_FIREFOX

        if self.verbose:
            print ("\n--- End setup: {} seconds ---".format((time.time() - start_time)))
        return

    def initChrome(self):
        if self.driver is not None:
            raise RuntimeError("Webdriver already init: %s instance present." % self.driver_type)

        start_time = time.time()

        self.driver = DriverFactory.getChromeDriver()
        self.driver_type = self.DRIVER_CHROME

        if self.verbose:
            print ("\n--- End setup: {} seconds ---".format((time.time() - start_time)))
        return

    def get_results(self):
        return self.results

    def apply_validators(self, validators):
        success = True
        reports = []
        for validator in validators:

            if validator['type'] == 'contains':
                selector = validator['selector']
                try:
                    value = validator['contains']
                except Exception as e:
                    value = None

                validator_result = test_contains(self.driver, selector, value)
                reports.append(validator_result)
                success = success and validator_result['success']

            else:
                success = False

        return success, reports



    """
    fetch the url using a selenium webdriver
    """
    def fetch_url(self, url, method="get"):
        r = True

        try:
            self.driver.get(url)
        except (selenium_exceptions.InvalidArgumentException, Exception) as e:
            r = {
                'text': "Driver can access url: %s" % url,
                'success': False,
                'error': str(e)
            }

        return r


    def _run_webdriver_test(self, t):
        test_result = {
            'url': t['url'],
            'assertions':[],
            'success': True
        }

        r = self.fetch_url(t['url'])
        # self.driver.save_screenshot("test.png")

        if r is not True:
            test_result['assertions'].append(r)
        else:
            validators_success, reports = self.apply_validators(t['validators'])
            test_result['assertions'] += reports
            test_result['success'] = test_result['success'] and validators_success

        return test_result



    def run_test(self, page):

        for t in page:

            if self.verbose:
                print("checking url: %s" % t['url'])

            try:
                selenium_validators = t['validators']
            except Exception as e:
                selenium_validators = None

            if selenium_validators:
                test_result = self._run_webdriver_test(t)
                self.results.append(test_result)

        return

    def close_driver(self):
        if self.driver is not None:
            self.driver.close()
            self.driver = None
            self.driver_type = None