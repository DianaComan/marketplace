"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2020
"""
from itertools import repeat

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.size = queue_size_per_producer
        self.count_prod = 0
        self.count_cart = 0
        self.c_product = 0
        self.queuep = [[] for _ in repeat(None, 300)]
        self.cart = [[] for _ in repeat(None, 800)]
        self.rqueuep = [[] for _ in repeat(None, 300)]


    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.count_prod = self.count_prod + 1
        return self.count_prod - 1

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        lung = len(self.queuep[producer_id])
        if lung >= self.size:
            return False
        self.queuep[producer_id].append(product)
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.count_cart = self.count_cart + 1
        return self.count_cart - 1

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        #foloseste o lista auxiliara pt a tine minte producatori in caz ca se sterge un produs
        for i in range(self.count_prod):
            if product in self.queuep[i]:
                self.cart[cart_id].append(product)
                self.queuep[i].remove(product)
                self.rqueuep[i].append(product)
                return True
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        if product in self.cart[cart_id]:
            self.cart[cart_id].remove(product)
            for i in range(self.count_prod):
                if product in self.rqueuep[i]:
                    self.rqueuep[i].remove(product)
                    self.queuep[i].append(product)
                    break

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        return self.cart[cart_id]
