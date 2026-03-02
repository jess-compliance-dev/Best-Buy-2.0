from products import Product
from store import Store

# color codes
RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[34m"
RESET = "\033[0m"


def start(store):
    """Show menu to user"""
    while True:
        print("\n*** Welcome to the Best-Buy Store ***")
        print("1. List all products in store")
        print("2. Show total amount in store")
        print("3. Make an order")
        print("4. Quit")

        choice = input(f"{BLUE}Enter your choice (1-4): {RESET}")

        if choice == "1":
            # List all products
            print("\nProducts in store:")
            for p in store.get_all_products():
                p.show()

        elif choice == "2":
            # Show total quantity
            total = store.get_total_quantity()
            print(f"{GREEN}\nTotal quantity of all active products: {total}{RESET}")

        elif choice == "3":
            # Make an order
            print("\nMaking an order:")
            order_list = []
            active_products = store.get_all_products()

            # Show products with numbers
            for index, p in enumerate(active_products):
                print(
                    f"{index + 1}. {p.name} - Price: {p.price}, Quantity: {p.get_quantity()}"
                )

            while True:
                prod_choice = input(
                    f"{BLUE}Which product # do you want? (empty to finish): {RESET}"
                )

                if prod_choice.strip() == "":
                    break

                if (
                    not prod_choice.isdigit()
                    or int(prod_choice) < 1
                    or int(prod_choice) > len(active_products)
                ):
                    print(f"{RED}Invalid choice. Try again.{RESET}")
                    continue

                quantity = input(f"{BLUE}What amount do you want? {RESET}")

                if not quantity.isdigit() or int(quantity) < 1:
                    print(f"{RED}Invalid quantity. Try again.{RESET}")
                    continue

                prod_index = int(prod_choice) - 1
                order_list.append(
                    (active_products[prod_index], int(quantity))
                )
                print(f"{GREEN}Product added to list!{RESET}")

            # Place the order
            if order_list:
                try:
                    total_price = store.order(order_list)
                    print(f"{GREEN}Order made! Total payment: {total_price} €{RESET}")
                except Exception as e:
                    if "out of stock" in str(e).lower():
                        print(f"{RED}Error while placing order: A product is out of stock!{RESET}")
                    else:
                        print(f"{RED}Error while placing order: {e}{RESET}")

        elif choice == "4":
            # Quit
            print(f"{GREEN}Thank you for visiting the store!{RESET}")
            break

        else:
            print(f"{RED}Invalid choice. Please enter 1-4.{RESET}")


def main():
    product_list = [
        Product("MacBook Air M2", 1450, 100),
        Product("Bose QuietComfort Earbuds", 250, 500),
        Product("Google Pixel 7", 500, 250),
        Product("Xiaomi Ultra 15 Pro", 946, 50),
        Product("Samsung ww80t604alxas2 washing machine", 548, 30),
        Product("WMF Lono Milk Frother Milk & Choc", 99, 150),
    ]

    best_buy = Store(product_list)

    # Start the menu
    start(best_buy)


if __name__ == "__main__":
    main()