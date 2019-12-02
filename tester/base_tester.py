import os
import re

class BaseTester():

    def __str__(self):
        txt=""



        if len(self.results):
            for r in self.results:
                sanitized_url = r['url']
                sanitized_url = re.sub(r"(https?://)(.*?):(.*?)@", r'\1REDACTED:REDACTED@', sanitized_url, count=0, flags=0)

                char = "\u221A" if r['success'] else "X"
                txt += "(%s) URL: %s\n" %  (char, sanitized_url)

                txt+= "- assertions: %d\n" % len(r['assertions'])
                for a in r['assertions']:
                    char = "\u221A" if a['success'] else "X"
                    txt+= "-- (%s): %s\n" % (char, a['text'])
                    if not a['success']:
                        txt+= "---: %s\n" % a['error']

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