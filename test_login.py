import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()
def test_valid_login(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    assert "inventory" in driver.current_url
def test_invalid_login(driver):
    driver.find_element(By.ID, "user-name").send_keys("wrong_user")
    driver.find_element(By.ID, "password").send_keys("wrong_password")
    driver.find_element(By.ID, "login-button").click()
    error_message = driver.find_element(
        By.CSS_SELECTOR, "[data-test='error']"
    ).text

    assert "Username and password do not match" in error_message
def test_locked_out_user(driver):
    driver.find_element(By.ID, "user-name").send_keys("locked_out_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    error_message = driver.find_element(
        By.CSS_SELECTOR, "[data-test='error']"
    ).text

    assert "locked out" in error_message.lower()
def test_empty_login(driver):
    driver.find_element(By.ID, "login-button").click()
    error_message = driver.find_element(
        By.CSS_SELECTOR, "[data-test='error']"
    ).text
    assert "Username is required" in error_message
def test_empty_password(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "login-button").click()

    error_message = driver.find_element(
        By.CSS_SELECTOR, "[data-test='error']"
    ).text

    assert "Password is required" in error_message
def test_products_page(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    products_title = driver.find_element(By.CLASS_NAME, "title")
    assert products_title.text == "Products"
def test_sort_products_low_to_high(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    sort_dropdown = Select(
        driver.find_element(By.CLASS_NAME, "product_sort_container")
    )
    sort_dropdown.select_by_value("lohi")

    price_elements = driver.find_elements(
        By.CLASS_NAME, "inventory_item_price"
    )
    prices = [
        float(price.text.replace("$", ""))
        for price in price_elements
    ]

    assert prices == sorted(prices)
def test_add_product_to_cart(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    driver.find_element(
        By.ID, "add-to-cart-sauce-labs-backpack"
    ).click()

    driver.find_element(
        By.CLASS_NAME, "shopping_cart_link"
    ).click()

    product_name = driver.find_element(
        By.CLASS_NAME, "inventory_item_name"
    )

    assert product_name.text == "Sauce Labs Backpack"
def test_cart_item_count(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    driver.find_element(
        By.ID, "add-to-cart-sauce-labs-backpack"
    ).click()

    cart_badge = driver.find_element(
        By.CLASS_NAME, "shopping_cart_badge"
    )

    assert cart_badge.text == "1"


def test_multiple_products_in_cart(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    driver.find_element(
        By.ID, "add-to-cart-sauce-labs-backpack"
    ).click()

    driver.find_element(
        By.ID, "add-to-cart-sauce-labs-bike-light"
    ).click()

    driver.find_element(
        By.CLASS_NAME, "shopping_cart_link"
    ).click()

    cart_items = driver.find_elements(
        By.CLASS_NAME, "cart_item"
    )

    assert len(cart_items) == 2


def test_remove_product_from_cart(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    driver.find_element(
        By.ID, "add-to-cart-sauce-labs-backpack"
    ).click()

    driver.find_element(
        By.CLASS_NAME, "shopping_cart_link"
    ).click()

    driver.find_element(
        By.ID, "remove-sauce-labs-backpack"
    ).click()

    cart_items = driver.find_elements(
        By.CLASS_NAME, "cart_item"
    )

    assert len(cart_items) == 0

def test_checkout_details(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    driver.find_element(
        By.ID, "add-to-cart-sauce-labs-backpack"
    ).click()

    driver.find_element(
        By.CLASS_NAME, "shopping_cart_link"
    ).click()

    driver.find_element(By.ID, "checkout").click()

    driver.find_element(
        By.ID, "first-name"
    ).send_keys("Greepitha")

    driver.find_element(
        By.ID, "last-name"
    ).send_keys("Reddy")

    driver.find_element(
        By.ID, "postal-code"
    ).send_keys("500001")

    driver.find_element(By.ID, "continue").click()

    checkout_title = driver.find_element(
        By.CLASS_NAME, "title"
    )

    assert checkout_title.text == "Checkout: Overview"


def test_checkout_without_first_name(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    driver.find_element(
        By.ID, "add-to-cart-sauce-labs-backpack"
    ).click()

    driver.find_element(
        By.CLASS_NAME, "shopping_cart_link"
    ).click()

    driver.find_element(By.ID, "checkout").click()

    driver.find_element(
        By.ID, "last-name"
    ).send_keys("Reddy")

    driver.find_element(
        By.ID, "postal-code"
    ).send_keys("500001")

    driver.find_element(By.ID, "continue").click()

    error_message = driver.find_element(
        By.CSS_SELECTOR, "[data-test='error']"
    ).text

    assert "First Name is required" in error_message