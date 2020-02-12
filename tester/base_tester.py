import os
import re


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class BaseTester():

    def __str__(self):
        txt=""

        test_success = 0
        test_failures = 0

        assertions_success = 0
        assertions_failures = 0

        if len(self.results):
            for r in self.results:
                sanitized_url = r['url']
                sanitized_url = re.sub(r"(https?://)(.*?):(.*?)@", r'\1REDACTED:REDACTED@', sanitized_url, count=0, flags=0)

                char = bcolors.OKGREEN+"\u221A"+bcolors.ENDC if r['success'] else bcolors.FAIL+"X"+bcolors.ENDC
                txt += "(%s) URL: %s\n" %  (char, sanitized_url)

                txt+= "- assertions: %d\n" % len(r['assertions'])
                test_has_failed_assertion = False
                for a in r['assertions']:
                    char = bcolors.OKGREEN+"\u221A"+bcolors.ENDC if a['success'] else bcolors.FAIL+"X"+bcolors.ENDC
                    txt+= "-- (%s): %s\n" % (char, a['text'])
                    if not a['success']:
                        txt+= "---: %s\n" % a['error']
                        test_has_failed_assertion = True
                        assertions_failures += 1
                    else:
                        assertions_success += 1

                if test_has_failed_assertion:
                    test_failures += 1
                else:
                    test_success += 1

            print(bcolors.OKGREEN + "Successful assertions: %d / %d" %( assertions_success, assertions_success + assertions_failures) + bcolors.ENDC)
            print(bcolors.OKGREEN +"Successful tests: %d / %d" % (test_success, test_success + test_failures)+ bcolors.ENDC)
            if assertions_failures:
                print(bcolors.FAIL + "Failed assertions: %d " %( assertions_failures) + bcolors.ENDC)

            if test_failures:
                print(bcolors.FAIL +"Failed tests: %d " % (test_failures)+ bcolors.ENDC)




        else:
            txt="0 test run"

        return txt

    def getEnvAuth(self):
        user = None
        pwd = None

        try:
            user = os.environ['BASIC_AUTH_USER']
        except Exception as e:
            pass

        try:
            pwd = os.environ['BASIC_AUTH_PWD']
        except Exception as e:
            pass

        result = False

        if user and pwd:
            result = (user, pwd)

        return result

    def close_driver(self):
        pass