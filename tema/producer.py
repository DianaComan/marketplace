"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Thread, Lock
import time

class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.products = products
        self.marketplace = marketplace
        self.wait_time = republish_wait_time
        self.id_producer = 0

    def run(self):
        locks = Lock()
        with locks:
            self.id_producer = self.marketplace.register_producer()
        #Producerea produselor.
        while True:
            for produs in self.products:
                for _ in range(produs[1]):
                    check = False
                    while not check:
                        check = self.marketplace.publish(self.id_producer, produs[0])
                        if not check:
                            time.sleep(produs[2])
                        else:
                            time.sleep(self.wait_time)
