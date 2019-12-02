
import time
import requests

from tester.base_tester import BaseTester
from tester.request_validators import test_header, test_http_status


class RequestTester(BaseTester):
    def __init__(self, verbose=False):
        self.results = []
        self.verbose = verbose
        self.request = None

    """
    fetch the url using requests
    """
    def fetch_url(self, t):
        r = True

        url = t['url']
        sanitized_url = url
        using_basic_auth_str =""

        method="get"
        try:
            method = t['method']
        except Exception as e:
            pass

        basic_auth = self.getEnvAuth()
        if basic_auth:
            using_basic_auth_str = "(Using Basic AUTH)"
            if "http://" in t['url']:
                t['url'] = t['url'].replace("http://", "http://"+basic_auth[0]+":"+basic_auth[1]+"@")
            elif "https://" in t['url']:
                t['url'] = t['url'].replace("https://", "https://"+basic_auth[0]+":"+basic_auth[1]+"@")


        try:
            self.request = requests.get(url)
        except Exception as e:
            r = {
                'text': "Request Driver can access url: (%s) %s %s " % ( method.upper(), sanitized_url, using_basic_auth_str ),
                'success': False,
                'error': str(e)
            }

        return r

    def apply_request_validators(self, validators):
        success = True
        reports = []

        for validator in validators:
            if validator['type'] == 'header':
                header = validator['name']
                try:
                    value = validator['contains']
                except Exception as e:
                    value = None

                validator_result = test_header(self.request, header, value)
                reports.append(validator_result)
                success = success and validator_result['success']
            elif validator['type'] == 'http_status':
                value = validator['is']
                validator_result = test_http_status(self.request, value)
                reports.append(validator_result)
                success = success and validator_result['success']
            else:
                success = False

        return success, reports

    def run_test(self, page):

        for t in page:

            if self.verbose:
                print("checking url: %s" % t['url'])

            try:
                request_validators = t['request_validators']
            except Exception as e:
                request_validators = None

            if request_validators:
                test_result = self._run_requests_test(t)
                self.results.append(test_result)
        return

    def _run_requests_test(self, t):

        try:
            method = t['method']
        except Exception as e:
            method = "get"

        test_result = {
            'url': t['url'],
            'method': method,
            'assertions':[],
            'success': True
        }

        r = self.fetch_url(t)

        if r is not True:
            test_result['assertions'].append(r)
        else:
            validators_success, reports = self.apply_request_validators(t['request_validators'])
            test_result['assertions'] += reports
            test_result['success'] = test_result['success'] and validators_success

        return test_result