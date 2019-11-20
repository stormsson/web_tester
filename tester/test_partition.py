

class TestPartition:
    @staticmethod
    def partition_suite( suite, partitions):
        results= []
        for i in range(partitions):
            results.append([])

        for idx, s in enumerate(suite):
            bucket_index = idx % partitions
            results[bucket_index].append(s)

        return results




