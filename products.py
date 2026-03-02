from abc import ABC, abstractmethod

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
        self.promotion = None  # Promotion variable

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

    def get_promotion(self):
        """Return current promotion, if exists"""
        return self.promotion

    def set_promotion(self, promotion):
        """Set a promotion for this product"""
        self.promotion = promotion

    def show(self):
        """Prints the purchase"""
        promo_text = f", Promotion: {self.promotion.name}" if self.promotion else ""
        print(f"Product: {self.name}, Price: {self.price}, Quantity: {self.quantity}{promo_text}")

    def buy(self, quantity) -> float:
        """
        Buy a certain quantity of the product.
        Returns the total price.
        Raises an exception if quantity is not active or out of stock.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        if not self.active:
            raise Exception("Product ist currently not available")
        if quantity > self.quantity:
            raise Exception("Product is out of stock")

        # calculate price with promotion if exists
        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = quantity * self.price

        self.quantity -= quantity
        if self.quantity == 0:
            self.deactivate()

        return total_price


class NonStockedProduct(Product):
    """Non-stock products, eg. licence, non-physical products"""

    def __init__(self, name, price):
        super().__init__(name, price, quantity=0)
        self.active = True # stays active

    def get_quantity(self):
        """Return quantity (always 0 for non-stocked products)"""
        return 0

    def buy(self, quantity) -> float:
        """Buy method for non-stocked products"""
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)
        return self.price * quantity

    def show(self):
        """Prints the purchase"""
        promo_text = f", Promotion: {self.promotion.name}" if self.promotion else ""
        print(f"Product: {self.name}, Price: {self.price} (Non-stocked, digital){promo_text}")


class LimitedProduct(Product):
    """Product with maximum amount per order"""

    def __init__(self, name, price, quantity, max_per_order=0):
        super().__init__(name, price, quantity)
        self.max_per_order = max_per_order

    def buy(self, quantity) -> float:
        """
        Buy method for limited product.
        Raises exception if quantity exceeds max_per_order.
        """
        if self.max_per_order > 0 and quantity > self.max_per_order:
            raise Exception(f"Maximum amount: {self.max_per_order}")
        return super().buy(quantity)

    def show(self):
        """Prints the purchase"""
        promo_text = f", Promotion: {self.promotion.name}" if self.promotion else ""
        print(f"Product: {self.name}, Price: {self.price}, Max per order: {self.max_per_order}, Quantity: {self.quantity}{promo_text}")


class Promotion(ABC):
    """Abstract base class for promotions"""

    def __init__(self, name):
        """Initialize promotion with a name"""
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity) -> float:
        """Apply promotion to a product for given quantity"""
        pass


class PercentDiscount(Promotion):
    """Percentage discount promotion"""

    def __init__(self, percent):
        super().__init__(f"{percent}% off")
        self.percent = percent

    def apply_promotion(self, product, quantity) -> float:
        """Calculate total price after percentage discount"""
        return quantity * product.price * (1 - self.percent / 100)


class SecondHalfPrice(Promotion):
    """Second item at half price"""

    def __init__(self):
        super().__init__("Second item at half price")

    def apply_promotion(self, product, quantity) -> float:
        """Calculate total price with second item at half price"""
        full_price_count = (quantity + 1) // 2
        half_price_count = quantity // 2
        return full_price_count * product.price + half_price_count * product.price * 0.5


class Buy2Get1Free(Promotion):
    """Buy 2, get 1 free"""

    def __init__(self):
        super().__init__("Buy 2, get 1 free")

    def apply_promotion(self, product, quantity) -> float:
        """Calculate total price for buy 2 get 1 free"""
        groups_of_three = quantity // 3
        remaining = quantity % 3
        total_price = groups_of_three * 2 * product.price + remaining * product.price
        return total_price
