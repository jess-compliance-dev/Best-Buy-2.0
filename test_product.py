import pytest
from products import Product, NonStockedProduct, LimitedProduct, PercentDiscount, Buy2Get1Free, SecondHalfPrice

# my products in the shop
product_list = [
    Product("MacBook Air M2", 1450, 100),
    Product("Bose QuietComfort Earbuds", 250, 500),
    Product("Google Pixel 7", 500, 250),
    Product("Xiaomi Ultra 15 Pro", 946, 50),
    Product("Samsung ww80t604alxas2 washing machine", 548, 30),
    Product("WMF Lono Milk Frother Milk & Choc", 99, 150),
    NonStockedProduct("Windows License", 125),
    LimitedProduct("Shipping", 10, 250, 1)
]


# creating promotions
second_half_price = SecondHalfPrice()
buy2_get1_free = Buy2Get1Free()
thirty_percent = PercentDiscount(30)

# apply promotions on specific articles
product_list[0].set_promotion(second_half_price)
product_list[4].set_promotion(buy2_get1_free)
product_list[7].set_promotion(thirty_percent)

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

# digital product
def test_buy_non_stocked_product():
    license_product = product_list[6]  # Windows License
    total_price = license_product.buy(3)
    assert total_price == 125 * 3
    assert license_product.get_quantity() == 0
    assert license_product.is_active() == True  # stays active

# buy limited amounts
def test_buy_limited_product():
    shipping = product_list[7]  # Shipping
    total_price = shipping.buy(1)
    assert total_price == 7
    assert shipping.get_quantity() == 249  # 250 - 1
    assert shipping.is_active() == True
    # Buying more than maximum per order should fail
    with pytest.raises(Exception):
        shipping.buy(2)

# test 19% discount
def test_percent_discount_single_item():
    """19% discount"""
    product = Product("Discounted MacBook", 1450, 10)
    discount = PercentDiscount(19)
    product.set_promotion(discount)
    total = product.buy(1)
    assert total == 1450 * 0.81
    assert product.get_quantity() == 9

# test Buy2Get 1 free
def test_buy2_get1_free_existing_product():
    """Buy 2, get 1 free"""
    product = product_list[5]
    promo = Buy2Get1Free()
    product.set_promotion(promo)

    total = product.buy(6)
    assert total == 396
    assert product.get_quantity() == 144
