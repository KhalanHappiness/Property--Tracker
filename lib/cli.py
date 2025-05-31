from models.land_buyer import LandBuyer
from models.agent import Agent
from models.connection import Connection
from models.listing import Listing
from models.base import Session
session = Session()

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
    def get_user_choice(self, max_choice):
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

    #Land Buyer Management
    def land_buyer_management(self):
        self.display_entity_menu("LandBuyer")
        choice = self.get_user_choice(6)

        if choice == 1:
            self.create_land_buyer()
        elif choice == 2:
            self.view_all_land_buyers()
        elif choice == 3:
            self.find_land_buyer_by_id()
        elif choice == 4:
            self.delete_land_buyer()
        elif choice == 5:
            self.view_land_buyer_related_objects()
        elif choice == 6:
            self.find_land_buyer_by_attribute()
        elif choice == 0:
            return
        
    def create_land_buyer(self):
        print("\n--- CREATE LAND BUYER ---")
        try:
            name = self.safe_input("Enter land buyer's name: ")
            email = self.safe_input("Enter email: ")
            phone = self.safe_input("Enter phone (optional): ", required=False)
            
            land_buyer = LandBuyer.create(self.session, name, email, phone)
            print(f"Buyer created successfully!")
            print(f"   {land_buyer.buyer_info}")
        except ValueError as e:
            print(f" Error: {e}")

    def view_all_land_buyers(self):
        print("\n--- ALL LAND BUYERS ---")
        buyers = LandBuyer.get_all(self.session)
        if not buyers:
            print("No land buyers found.")
        else:
            for buyer in buyers:
                print(f"   {buyer.buyer_info}")

    def find_land_buyer_by_id(self):
        print("\n--- FIND LAND BUYER BY ID ---")
        land_buyer_id = self.safe_int_input("Enter land buyer ID: ")
        buyer = LandBuyer.find_by_id(self.session, land_buyer_id)
        if buyer:
            print(f"Land Buyer found:")
            print(f"   {buyer.buyer_info}")
        else:
            print(f" land buyer with ID {land_buyer_id} not found.")

    def delete_land_buyer(self):
        print("\n--- DELETE LAND BUYER ---")
        land_buyer_id = self.safe_int_input("Enter buyer ID to delete: ")
        buyer = LandBuyer.find_by_id(self.session, land_buyer_id)
        if buyer:
            print(f"land buyer to delete: {buyer.buyer_info}")
            confirm = input("Are you sure? (yes/no): ").lower()
            if confirm == 'yes':
                buyer.delete(self.session)
                print("Buyer deleted successfully!")
            else:
                print("Deletion cancelled.")
        else:
            print(f"Buyer with ID {land_buyer_id} not found.")
    
    def view_land_buyer_related_objects(self):
        print("\n--- LAND BUYER RELATED OBJECTS ---")
        land_buyer_id = self.safe_int_input("Enter land buyer ID: ")
        buyer = LandBuyer.find_by_id(self.session, land_buyer_id)
        if buyer:
            print(f"Land Buyer: {buyer.buyer_info}")
            print(f"\Connections ({len(buyer.connections)}):")
            for connection in buyer.connections:
                print(f"   - {connection.agent.name} ")
           
        else:
            print(f"Buyer with ID {land_buyer_id} not found.")
    
    def find_land_buyer_by_attribute(self):
        print("\n--- FIND LAND BUYER BY EMAIL ---")
        email = self.safe_input("Enter email to search: ")
        buyer = LandBuyer.find_by_email(self.session, email)
        if buyer:
            print(f"Buyer found:")
            print(f"   {buyer.buyer_info}")
        else:
            print(f"Buyer with email '{email}' not found.")

    # AGENT MANAGEMENT
    def agent_management(self):
        while True:
            self.display_entity_menu("Agent")
            choice = self.get_user_choice(6)
            
            if choice == 1:
                self.create_agent()
            elif choice == 2:
                self.view_all_agents()
            elif choice == 3:
                self.find_agent_by_id()
            elif choice == 4:
                self.delete_agent()
            elif choice == 5:
                self.view_agent_related_objects()
            elif choice == 6:
                self.find_agent_by_attribute()
            elif choice == 0:
                break
    
    def create_agent(self):
        print("\n--- CREATE AGENT ---")
        try:
            name = self.safe_input("Enter business name: ")
            email = self.safe_input("Enter email: ")
            license_number = self.safe_input("Enter license number: ")
            phone = self.safe_input("Enter phone (optional): ", required=False)
            
            agent = Agent.create(self.session, name, email, license_number, phone)
            print(f"agent created successfully!")
            print(f"   {agent.full_info}")
        except ValueError as e:
            print(f"Error: {e}")
    
    def view_all_agents(self):
        print("\n--- ALL AGENTS ---")
        agents = Agent.get_all(self.session)
        if not agents:
            print("No agents found.")
        else:
            for agent in agents:
                print(f"   {agent.full_info}")
    
    def find_agent_by_id(self):
        print("\n--- FIND AGENT BY ID ---")
        agent_id = self.safe_int_input("Enter agent ID: ")
        agent = Agent.find_by_id(self.session, agent_id)
        if agent:
            print(f"agent found:")
            print(f"   {agent.full_info}")
        else:
            print(f"agent with ID {agent_id} not found.")
    
    def delete_agent(self):
        print("\n--- DELETE AGENT ---")
        agent_id = self.safe_int_input("Enter agent ID to delete: ")
        agent = Agent.find_by_id(self.session, agent_id)
        if agent:
            print(f"agent to delete: {agent.full_info}")
            confirm = input("Are you sure? (yes/no): ").lower()
            if confirm == 'yes':
                agent.delete(self.session)
                print("agent deleted successfully!")
            else:
                print("Deletion cancelled.")
        else:
            print(f"agent with ID {agent_id} not found.")
    
    def view_agent_related_objects(self):
        print("\n--- AGENT RELATED OBJECTS ---")
        agent_id = self.safe_int_input("Enter agent ID: ")
        agent = Agent.find_by_id(self.session, agent_id)
        if agent:
            print(f"agent: {agent.full_info}")
            print(f"\n Listings ({len(agent.listings)}):")
            for listing in agent.listings:
                price_str = f"${listing.price}" if listing.price else "Price TBD"
                status = "Available" if listing.is_available else "Unavailable"
                print(f"   - {listing.name} ({price_str}) - {status}")
            print(f"\n Connected to ({len(agent.connections)} land buyers):")
            for connection in agent.connections:
                print(f"   - {connection.land_buyer.name} ({connection.land_buyer.email})")
        else:
            print(f"agent with ID {agent_id} not found.")
    
    def find_agent_by_attribute(self):
        print("\n--- FIND AGENT BY NAME ---")
        agent_name = self.safe_input("Enter agent name to search: ")
        agents = Agent.find_by_name(self.session, agent_name)
        if agents:
            print(f"Found {len(agents)} agent(s):")
            for agent in agents:
                print(f"   {agent.full_info}")
        else:
            print(f"No agents found withname containing '{agent_name}'.")

    #CONNECTION MANAGEMENT
    def connections_management(self):
        while True:
            self.display_entity_menu("Connections")
            choice = self.get_user_choice(4)
            
            if choice == 1:
                self.create_connection()
            elif choice == 2:
                self.view_all_connections()
            elif choice == 3:
                self.find_connection_by_id()
            elif choice == 4:
                self.delete_connection()
            elif choice == 0:
                break

    def create_connection(self):
        print("\n--- CREATE CONNECTION ---")
        try:
            land_buyer_id = self.safe_int_input("Enter land buyer ID: ")
            agent_id = self.safe_int_input("Enter agent ID: ")
           
            connection = Connection.create(self.session, land_buyer_id, agent_id)
            print(f"connection created successfully!")
            print(f"   {connection.full_info}")
        except ValueError as e:
            print(f"Error: {e}")
    
    def view_all_connections(self):
        print("\n--- ALL connectionS ---")
        connections = Connection.get_all(self.session)
        if not connections:
            print("No connections found.")
        else:
            for connection in connections:
                print(f"   {connection.full_info}")
    
    def find_connection_by_id(self):
        print("\n--- FIND connection BY ID ---")
        connection_id = self.safe_int_input("Enter connection ID: ")
        connection = Connection.find_by_id(self.session, connection_id)
        if connection:
            print(f"connection found:")
            print(f"   {connection.full_info}")
        else:
            print(f"connection with ID {connection_id} not found.")
    
    def delete_connection(self):
        print("\n--- DELETE connection ---")
        connection_id = self.safe_int_input("Enter connection ID to delete: ")
        connection = Connection.find_by_id(self.session, connection_id)
        if connection:
            print(f"connection to delete: {connection.full_info}")
            confirm = input("Are you sure? (yes/no): ").lower()
            if confirm == 'yes':
                connection.delete(self.session)
                print("connection deleted successfully!")
            else:
                print("Deletion cancelled.")
        else:
            print(f"connection with ID {connection_id} not found.")
    

    