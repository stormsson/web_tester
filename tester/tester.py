import time
from selenium import webdriver
import selenium.common.exceptions as selenium_exceptions


# https://selenium-python.readthedocs.io/api.html
# https://selenium.dev/selenium/docs/api/javascript/module/selenium-webdriver/index_exports_WebElement.html

from tester.validators import test_contains

class Tester():

    DRIVER_CHROME = "Chrome"
    DRIVER_FIREFOX = "Firefox"
    DRIVER_SAFARI = "Safari"

    def __init__(self, type=None, verbose=False):
        self.options = None
        self.driver = None
        self.driverType = None
        self.results = []
        self.verbose = verbose

        if type == self.DRIVER_CHROME:
            self.initChrome()

    def initChrome(self):
        if self.driver is not None:
            raise RuntimeError("Webdriver already init: %s instance present." % self.driverType)

        start_time = time.time()

        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--headless")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(chrome_options=self.options)
        self.driverType = self.DRIVER_CHROME
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

    def fetch_url(self, url):
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

    def __str__(self):
        txt=""
        if len(self.results):
            for r in self.results:
                char = "\u221A" if r['success'] else "X"
                txt += "(%s) URL: %s\n" %  (char, r['url'])

                txt+= "- assertions: %d\n" % len(r['assertions'])
                for a in r['assertions']:
                    char = "\u221A" if a['success'] else "X"
                    txt+= "-- (%s): %s\n" % (char, a['text'])
                    if not a['success']:
                        txt+= "---: %s\n" % a['error']

        else:
            txt="0 test run"

        return txt

    # def print_results(self):
    #     for r in self.results:
    #         char = "\u221A" if r['success'] else "X"
    #         print("(%s) URL: %s" %  (char, r['url']))
    #         print("- assertions: %d" % len(r['assertions']))
    #         for a in r['assertions']:
    #             char = "\u221A" if a['success'] else "X"
    #             print("-- (%s): %s" % (char, a['text']))
    #             if not a['success']:
    #                 print("---: %s" % a['error'])
    #         print("\n")



    def run_test(self, page):

        for t in page:
            test_result = {
                'url': t['url'],
                'assertions':[],
                'success': True
            }

            if self.verbose:
                print("checking url: %s" % t['url'])
            fetch_ok = True
            test_passed = True


            r = self.fetch_url(t['url'])
            if r is not True:
                test_result['assertions'].append(r)
                fetch_ok = False
                test_passed = False

            if fetch_ok:
                validators_success, reports = self.apply_validators(t['validators'])
                test_result['assertions'] += reports
                test_result['success'] = test_result['success'] and validators_success

            self.results.append(test_result)

        return

    def closeDriver(self):
        if self.driver is not None:
            self.driver.close()
            self.driver = None
            self.driverType = None



    # def do_test(self):
    #     start_time = time.time()

    #     # self..get('https://www.febalcasa.com/it/')
    #     self.driver.get('https://www.ferrari.com/en-EN/auto/f8-tributo')

    #     #pippo = self.driver.find_element_by_css_selector("div.main")
    #     try:
    #         pippo = self.driver.find_element_by_css_selector("h1")
    #         print ("EEE" + pippo.text)
    #     except Exception as e:
    #         pass


    #     print ("title: " + self.driver.title)

    #     print ("\n--- Closing: {} seconds ---".format((time.time() - start_time)))