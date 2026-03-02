import pytest
from products import Product

# my products in the shop
product_list = [
    Product("MacBook Air M2", 1450, 100),
    Product("Bose QuietComfort Earbuds", 250, 500),
    Product("Google Pixel 7", 500, 250),
    Product("Xiaomi Ultra 15 Pro", 946, 50),
    Product("Samsung ww80t604alxas2 washing machine", 548, 30),
    Product("WMF Lono Milk Frother Milk & Choc", 99, 150),
]

# normal case
def test_create_normal_product():
    product = product_list[0]
    assert product.name == "MacBook Air M2"
    assert product.price == 1450
    assert product.quantity == 100
    assert product.is_active() == True

# invalid values
def test_create_product_invalid_name_or_price():
    # empty name
    with pytest.raises(ValueError):
        Product("", 1450, 100)
    # negative price
    with pytest.raises(ValueError):
        Product("MacBook Air M2", -10, 100)
    # negative amount
    with pytest.raises(ValueError):
        Product("MacBook Air M2", 1450, -5)

# product is out of stock
def test_product_becomes_inactive_when_quantity_zero():
    product = Product("Bose QuietComfort Earbuds", 250, 1)
    product.buy(1)
    assert product.get_quantity() == 0
    assert product.is_active() == False


# Amount > Availability of the product
def test_buy_more_than_available_raises_exception():
    product = Product("Headphones", 150, 3)
    with pytest.raises(Exception):
        product.buy(5)

# Buying scenario
def test_buy_product_updates_quantity_and_returns_total():
    product = Product("WMF Lono Milk Frother Milk & Choc", 99, 150)
    total_price = product.buy(130)
    assert total_price == 12870 # 130 * 99
    assert product.get_quantity() == 20  # 150 - 130
    assert product.is_active() == True