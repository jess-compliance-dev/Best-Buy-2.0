from products import Product

class Store:
    """Setup Store class"""

    def __init__(self, products):
        """Initialize the store with a list of products."""
        self.products = products  # store all products

    def add_product(self, product):
        """Add a new product to the store."""
        self.products.append(product)

    def remove_product(self, product):
        """Remove a product from the store."""
        if product in self.products:
            self.products.remove(product)

    def get_total_quantity(self) -> int:
        """Return the total quantity of all active products in the store."""
        total = 0
        for p in self.products:
            if p.is_active():
                total += p.get_quantity()
        return total

    def get_all_products(self) -> list:
        """Return a list of all active products."""
        active_products = []
        for p in self.products:
            if p.is_active():
                active_products.append(p)
        return active_products

    def order(self, shopping_list) -> float:
        """
        Take a list of tuples (Product, quantity).
        Buy the products and return the total price of the order.
        """
        total_price = 0
        for item in shopping_list:
            product = item[0]
            quantity = item[1]
            total_price += product.buy(quantity)
        return total_price