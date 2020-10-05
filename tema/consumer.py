"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Thread, Lock
import time


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        super(Consumer, self).__init__(**kwargs)
        self.carts = carts
        self.marketplace = marketplace
        self.wait_time = retry_wait_time
        self.id_cart = 0

    def run(self):
        for command in self.carts:
            locks = Lock()
            with locks:
                self.id_cart = self.marketplace.new_cart()
            #Parsarea comenzilor din fiecare cart
            for comm in command:
                if comm['type'] == "add":
                    for _ in range(comm['quantity']):
                        check = False
                        while not check:
                            check = self.marketplace.add_to_cart(self.id_cart, comm['product'])
                            if not check:
                                time.sleep(self.wait_time)
                else:
                    for _ in range(comm['quantity']):
                        self.marketplace.remove_from_cart(self.id_cart, comm['product'])
            #Plasarea comenzii
            cartt = self.marketplace.place_order(self.id_cart)
            for produs in cartt:
                print("%s bought %s" % (self.name, produs))
