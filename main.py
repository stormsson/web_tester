from pathlib import Path
import os
import time
import yaml
import selenium
import argparse

from tester.selenium_tester import SeleniumTester
from tester.request_tester import RequestTester
from tester.test_partition import TestPartition

from multiprocessing import Process, Pool

POOL_SIZE = 2
DEFAULT_SUITE_FILE = './suite.yml'
args = []

def load_yaml(filePath):
    with open(filePath, 'r') as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
    return cfg

def run_instance(test_setup):

    #( driver type, test suite, init_options)
    # test_suite = test_setup[1]

    (driver_type, test_suite, init_options) = test_setup

    if driver_type == 'RequestTester':
        try:
            v = test_suite[0]['request_validators']
            if v:
                t = RequestTester()
        except (KeyError, IndexError) as e:
            test_suite = False

    else:
        try:
            v = test_suite[0]['validators']
            if v :
                t = SeleniumTester(driver_type=driver_type, init_options=init_options)
                t.init_driver()
        except (KeyError, IndexError) as e:
            test_suite = False


    if bool(test_suite):
        t.run_test(test_suite)
        print(t)
        t.close_driver()

    return

def parse_arguments():
    global args
    parser = argparse.ArgumentParser(description='Test things on the interwebs.')
    parser.add_argument('--selenium', dest='use_selenium',action='store_true',
                    help='Enable selenium testing')

    parser.add_argument('--test_file')
    args = vars(parser.parse_args())

    return args

if __name__ == '__main__':
    parse_arguments()

    config = load_yaml('./configuration.yml')
    suite_path = DEFAULT_SUITE_FILE if not args['test_file'] else args['test_file']
    test_suite = load_yaml(suite_path)

    if config["pool_size"]:
        POOL_SIZE = config["pool_size"]


    tester_init_options=None
    if config["tester_init_options"]:
        tester_init_options = config["tester_init_options"]

    print("starting test with %d parallel instances" % POOL_SIZE)

    # start run
    start_time = time.time()

    x = TestPartition.partition_suite(test_suite, POOL_SIZE)

    testers = []
    for i in range(POOL_SIZE):
        testers.append( ( "RequestTester", x[i], tester_init_options) )

        if args['use_selenium']:
            # testers.append( ( SeleniumTester.DRIVER_FIREFOX, x[i], tester_init_options) )
            testers.append( ( SeleniumTester.DRIVER_CHROME, x[i], tester_init_options) )


    with Pool(processes=POOL_SIZE) as pool:
        pool.map(run_instance, testers)

    print ("\n--- Execution took {} seconds ---".format((time.time() - start_time)))
    exit()