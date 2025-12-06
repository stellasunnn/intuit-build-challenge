import unittest
import queue
import threading

from assignment1.producer_consumer import producer, consumer, SENTINEL


class ProducerConsumerTests(unittest.TestCase):
    def run_pipeline(self, source):
        """Helper to run producer + consumer with local containers."""
        destination = []
        q = queue.Queue(maxsize=2)

        producer_thread = threading.Thread(target=producer, args=(source, q))
        consumer_thread = threading.Thread(target=consumer, args=(destination, q))

        producer_thread.start()
        consumer_thread.start()

        producer_thread.join()
        consumer_thread.join()

        return destination

    def test_basic_transfer(self):
        source = [10, 20, 30, 40, 50]
        destination = self.run_pipeline(source)
        # All items should be transferred in order
        self.assertEqual(destination, source)

    def test_empty_source(self):
        source = []
        destination = self.run_pipeline(source)
        # Source is empty, destination should remain empty
        self.assertEqual(destination, [])


if __name__ == "__main__":
    unittest.main()
