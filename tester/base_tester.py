class BaseTester():

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

    def close_driver(self):
        pass