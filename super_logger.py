import enum
import json
import pickle
import xml.etree.ElementTree as ET
import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler for logging 
log_file = "shopping_cart.log"
file_handler = logging.FileHandler(log_file)

# Create a console handler for logging
console_handler = logging.StreamHandler()

# Create a formatter and set it for the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler) 
logger.addHandler(console_handler)  # Add console handler

class Product:
    def __init__(self, name, price, stock_quantity):
        self.name = name
        self.price = price
        self.stock_quantity = stock_quantity

class MenuItem(enum.Enum):
    BREAD = 1
    MILK = 2
    EGGS = 3
    APPLE = 4
    BANANA = 5
    CHECKOUT = 6

class ShoppingCart:
    def __init__(self):
        self.cart = []

    def add_to_cart(self, product):
        self.cart.append(product)
        logger.info(f"Added {product.name} to the cart")

    def total_price(self):
        return sum(product.price for product in self.cart)

    def num_of_products(self):
        return len(self.cart)

    def get_cart_items(self):
        return self.cart

def display_product_list():
    print("Product List:")
    for item in MenuItem:
        if item != MenuItem.CHECKOUT:
            product = products[item]
            print(f"{item.value}. {product.name} - ${product.price} ({product.stock_quantity} in stock)")

def save_to_pickle(cart):
    with open("cart.pickle", "wb") as file:
        pickle.dump(cart, file)
        logger.info("Saved cart to pickle file")

def save_to_json(cart):
    cart_data = [{"name": product.name, "price": product.price} for product in cart.cart]
    with open("cart.json", "w") as file:
        json.dump(cart_data, file, indent=4)
        logger.info("Saved cart to JSON file")

def save_to_xml(cart):
    root = ET.Element("cart")
    for product in cart.cart:
        product_elem = ET.SubElement(root, "product")
        ET.SubElement(product_elem, "name").text = product.name
        ET.SubElement(product_elem, "price").text = str(product.price)

    tree = ET.ElementTree(root)
    tree.write("cart.xml")
    logger.info("Saved cart to XML file")

if __name__ == "__main__":
    products = {
        MenuItem.BREAD: Product("Bread", 2.5, 10),
        MenuItem.MILK: Product("Milk", 1.5, 20),
        MenuItem.EGGS: Product("Eggs", 3.0, 15),
        MenuItem.APPLE: Product("Apple", 0.5, 30),
        MenuItem.BANANA: Product("Banana", 0.7, 25),
    }

    cart = ShoppingCart()

    while True:
        display_product_list()
        try:
            choice = int(input("Enter the number of the item you want to add to the cart (6 to checkout): "))

            if choice == 6:
                logger.info("User checked out")
                print("Items in cart:")
                for item in cart.get_cart_items():
                    print(f"{item.name} - ${item.price}")
                print(f"Number of products in the cart: {cart.num_of_products()}")
                print(f"Total price: ${cart.total_price()}")
                save_choice = input("Do you want to save your cart? (Y/N): ").strip().lower()
                if save_choice == 'y':
                    save_to_pickle(cart)
                    save_to_json(cart)
                    save_to_xml(cart)
                    print("Cart saved.")
                break

            if 1 <= choice <= 5:
                product = products.get(MenuItem(choice))
                if product and product.stock_quantity > 0:
                    cart.add_to_cart(product)
                    product.stock_quantity -= 1
                    print(f"{product.name} added to the cart.")
                else:
                    logger.error(f"Error: {product.name} is out of stock or invalid choice.")
                    print(f"Sorry, {product.name} is out of stock or invalid choice.")
            else:
                logger.error("Invalid choice. Please select a valid item or checkout.")
                print("Invalid choice. Please select a valid item or checkout.")
        except ValueError:
            logger.error("Invalid input. Please enter a valid number.")
            print("Invalid input. Please enter a valid number.")
