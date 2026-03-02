class Product:
    """Setup class Product"""

    def __init__(self, name, price, quantity):
        """
        Initialize class Product und include error handling and add name,
        price and quantity as variable instances
        """

        if not name:
            raise ValueError("No empty name allowed")
        if price < 0:
            raise ValueError("Price must be greater than 0")
        if quantity < 0:
            raise ValueError("Quantity must be greater than 0")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True

        if self.quantity == 0:
            self.active = False


    def get_quantity(self) -> int:
        """Return the quantity of the product"""
        return self.quantity

    def set_quantity(self, quantity):
        """Set the quantity incl. error handling and deactivate if value is 0"""
        if quantity < 0:
            raise ValueError("Quantity must be greater than 0")

        self.quantity = quantity
        if quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        """Return True if the product is active, otherwise False."""
        return self.active

    def activate(self):
        """Activates product"""
        self.active = True

    def deactivate(self):
        """Deactivates product"""
        self.active = False

    def show(self):
        """Prints the purchase"""
        print(f"Product: {self.name}, Price: {self.price}, Quantity: {self.quantity}")

    def buy(self, quantity) -> float:
        """
        Buy a certain quantity of the product.
        Returns the total price.
        Raises an exception if quantity is not active or out of stock.
        """
        #purchase request must be larger than 0
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        #product must be active
        if not self.active:
            raise Exception("Product ist currently not available")

        # check if item is in stock
        if quantity > self.quantity:
            raise Exception("Product is out of stock")

        #price calculation & update stock
        total_price = quantity * self.price
        self.quantity -= quantity

        #deactivates product if quantity equal to 0
        if self.quantity == 0:
            self.deactivate()

        return total_price

