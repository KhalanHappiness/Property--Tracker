from models.land_buyer import LandBuyer
from models.agent import Agent
from models.connection import Connection
from models.listing import Listing
from models.base import Base

class PropertyTrackerCLI:

    def display_main_menu(self):
        print("\n" + "="*50)
        print("PROPERTY TRACKER CLI APPLICATION")
        print("="*50)
        print("1. Land Buyer Management")
        print("2. Agent Management") 
        print("3. Connection Management")
        print("4. Listing Management")
        print("5. Exit")
        print("="*50)
    def get_land_buyer_choice(self, max_choice):
        while True:
            try:
                choice = int(input(f"Enter your choice (1-{max_choice}): "))
                if 0 <= choice <= max_choice:
                    return choice
                else:
                    print(f"Please enter a number between 1 and {max_choice}")
            except ValueError:
                print("Please enter a valid number")
    
    def display_entity_menu(self, entity_name):
        print(f"\n--- {entity_name.upper()} MANAGEMENT ---")
        print(f"1. Create {entity_name}")
        print(f"2. View All {entity_name}s")
        print(f"3. Find {entity_name} by ID")
        print(f"4. Delete {entity_name}")
        if entity_name in ["LandBuyer", "Agent"]:
            print(f"5. View Related Objects")
            print("6. Find by Attribute")
        print("0. Back to Main Menu")

    def safe_input(self, prompt, required=True):
        while True:
            value = input(prompt).strip()
            if value or not required:
                return value if value else None
            print("This field is required. Please enter a value.")

    def safe_int_input(self, prompt):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Please enter a valid number")

    def safe_float_input(self, prompt, required=True):
        while True:
            try:
                value = input(prompt).strip()
                if not value and not required:
                    return None
                return float(value)
            except ValueError:
                print("Please enter a valid number")
