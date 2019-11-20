from pathlib import Path
import os
import time
import yaml
import selenium

from tester.tester import Tester
from tester.test_partition import TestPartition

from multiprocessing import Process, Pool

POOL_SIZE = 2

def load_yaml(filePath):
    with open(filePath, 'r') as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
    return cfg

def run_instance(test_setup):

    test_instance = test_setup[1]

    t = Tester(test_setup[0])
    print(t)

    if bool(test_instance):
        t.run_test(test_instance)
        # t.print_results()
        print(t)
    t.closeDriver()

    return


if __name__ == '__main__':
    config = load_yaml('./configuration.yml')
    test_suite = load_yaml('./suite.yml')
    # print(test_suite)
    # exit()

    if config["pool_size"]:
        POOL_SIZE = config["pool_size"]

    print("starting test with %d parallel instances" % POOL_SIZE)

    # start run
    start_time = time.time()

    x = TestPartition.partition_suite(test_suite, POOL_SIZE)

    testers = []
    for i in range(POOL_SIZE):
        testers.append( ( Tester.DRIVER_CHROME, x[i]) )

    with Pool(processes=POOL_SIZE) as pool:
        pool.map(run_instance, testers)

    print ("\n--- Execution took {} seconds ---".format((time.time() - start_time)))
    exit()