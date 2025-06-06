from models.land_buyer import LandBuyer
from models.agent import Agent
from models.connection import Connection
from models.listing import Listing
from models.base import Session

class PropertyTrackerCLI:
    def __init__(self):
        self.session = Session()

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
                    print(f"Please enter a number between 0 and {max_choice}")
            except ValueError:
                print("Please enter a valid number")
    
    def display_entity_menu(self, entity_name):
        print(f"\n--- {entity_name.upper()} MANAGEMENT ---")
        print(f"1. Create {entity_name}")
        print(f"2. View All {entity_name}s")
        print(f"3. Find {entity_name} by ID")
        print(f"4. Update {entity_name}")
        print(f"5. Delete {entity_name}")
        if entity_name in ["LandBuyer", "Agent"]:
            print(f"6. View Related Objects")
            print("7. Find by Attribute")
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

    def get_optional_input(self, prompt, current_value):
        """Get input with option to keep current value"""
        full_prompt = f"{prompt} (current: {current_value}, press Enter to keep): "
        new_value = input(full_prompt).strip()
        return new_value if new_value else current_value

    def get_optional_float_input(self, prompt, current_value):
        """Get float input with option to keep current value"""
        while True:
            try:
                full_prompt = f"{prompt} (current: {current_value}, press Enter to keep): "
                new_value = input(full_prompt).strip()
                if not new_value:
                    return current_value
                return float(new_value)
            except ValueError:
                print("Please enter a valid number")

    def get_optional_bool_input(self, prompt, current_value):
        """Get boolean input with option to keep current value"""
        current_str = "yes" if current_value else "no"
        full_prompt = f"{prompt} (current: {current_str}, press Enter to keep): "
        new_value = input(full_prompt).strip().lower()
        if not new_value:
            return current_value
        return new_value in ['y', 'yes']

    # LAND BUYER MANAGEMENT
    def land_buyer_management(self):
        while True:
            self.display_entity_menu("LandBuyer")
            choice = self.get_user_choice(7)

            if choice == 1:
                self.create_land_buyer()
            elif choice == 2:
                self.view_all_land_buyers()
            elif choice == 3:
                self.find_land_buyer_by_id()
            elif choice == 4:
                self.update_land_buyer()
            elif choice == 5:
                self.delete_land_buyer()
            elif choice == 6:
                self.view_land_buyer_related_objects()
            elif choice == 7:
                self.find_land_buyer_by_attribute()
            elif choice == 0:
                break
        
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
            print(f"Error: {e}")

    def update_land_buyer(self):
        print("\n--- UPDATE LAND BUYER ---")
        land_buyer_id = self.safe_int_input("Enter land buyer ID to update: ")
        buyer = LandBuyer.find_by_id(self.session, land_buyer_id)
        
        if not buyer:
            print(f"Land buyer with ID {land_buyer_id} not found.")
            return
        
        print(f"Current land buyer info: {buyer.buyer_info}")
        print("\nEnter new values (press Enter to keep current value):")
        
        try:
            # Get updated values
            new_name = self.get_optional_input("Enter new name", buyer.name)
            new_email = self.get_optional_input("Enter new email", buyer.email)
            new_phone = self.get_optional_input("Enter new phone", buyer.phone or "None")
            new_phone = new_phone if new_phone != "None" else None
            
            # Update the buyer
            LandBuyer.update_by_id(self.session, land_buyer_id, name=new_name, email=new_email, phone=new_phone)
            print(f"Land buyer updated successfully!")
            print(f"   {buyer.buyer_info}")
        except ValueError as e:
            print(f"Error: {e}")

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
            print(f"Land buyer with ID {land_buyer_id} not found.")

    def delete_land_buyer(self):
        print("\n--- DELETE LAND BUYER ---")
        land_buyer_id = self.safe_int_input("Enter buyer ID to delete: ")
        buyer = LandBuyer.find_by_id(self.session, land_buyer_id)
        if buyer:
            print(f"Land buyer to delete: {buyer.buyer_info}")
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
            print(f"\nConnections ({len(buyer.connections)}):")
            for connection in buyer.connections:
                if connection.agent:
                    print(f"   - {connection.agent.name}")
                else:
                    print(f"   - Agent ID: {connection.agent_id}")
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
            choice = self.get_user_choice(7)
            
            if choice == 1:
                self.create_agent()
            elif choice == 2:
                self.view_all_agents()
            elif choice == 3:
                self.find_agent_by_id()
            elif choice == 4:
                self.update_agent()
            elif choice == 5:
                self.delete_agent()
            elif choice == 6:
                self.view_agent_related_objects()
            elif choice == 7:
                self.find_agent_by_attribute()
            elif choice == 0:
                break
    
    def create_agent(self):
        print("\n--- CREATE AGENT ---")
        try:
            name = self.safe_input("Enter agent name: ")
            license_number = self.safe_input("Enter license number: ")
            email = self.safe_input("Enter email: ")
            phone = self.safe_input("Enter phone (optional): ", required=False)
            
            agent = Agent.create(self.session, name, license_number, email, phone)
            print(f"Agent created successfully!")
            print(f"   {agent.full_info}")
        except ValueError as e:
            print(f"Error: {e}")

    def update_agent(self):
        print("\n--- UPDATE AGENT ---")
        agent_id = self.safe_int_input("Enter agent ID to update: ")
        agent = Agent.find_by_id(self.session, agent_id)
        
        if not agent:
            print(f"Agent with ID {agent_id} not found.")
            return
        
        print(f"Current agent info: {agent.full_info}")
        print("\nEnter new values (press Enter to keep current value):")
        
        try:
            # Get updated values
            new_name = self.get_optional_input("Enter new name", agent.name)
            new_license = self.get_optional_input("Enter new license number", agent.license_number)
            new_email = self.get_optional_input("Enter new email", agent.email)
            new_phone = self.get_optional_input("Enter new phone", agent.phone or "None")
            new_phone = new_phone if new_phone != "None" else None
            
            # Update the agent
            Agent.update_by_id(self.session, agent_id, name=new_name, license_number=new_license, 
                        email=new_email, phone=new_phone)
            print(f"Agent updated successfully!")
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
            print(f"Agent found:")
            print(f"   {agent.full_info}")
        else:
            print(f"Agent with ID {agent_id} not found.")
    
    def delete_agent(self):
        print("\n--- DELETE AGENT ---")
        agent_id = self.safe_int_input("Enter agent ID to delete: ")
        agent = Agent.find_by_id(self.session, agent_id)
        if agent:
            print(f"Agent to delete: {agent.full_info}")
            confirm = input("Are you sure? (yes/no): ").lower()
            if confirm == 'yes':
                agent.delete(self.session)
                print("Agent deleted successfully!")
            else:
                print("Deletion cancelled.")
        else:
            print(f"Agent with ID {agent_id} not found.")
    
    def view_agent_related_objects(self):
        print("\n--- AGENT RELATED OBJECTS ---")
        agent_id = self.safe_int_input("Enter agent ID: ")
        agent = Agent.find_by_id(self.session, agent_id)
        if agent:
            print(f"Agent: {agent.full_info}")
            print(f"\nListings ({len(agent.listings)}):")
            for listing in agent.listings:
                price_str = f"${listing.price}" if listing.price else "Price TBD"
                status = "Available" if listing.is_available else "Unavailable"
                print(f"   - {listing.address} ({price_str}) - {status}")
            print(f"\nConnected to ({len(agent.connections)} land buyer(s)):")
            for connection in agent.connections:
                if connection.land_buyer:
                    print(f"   - {connection.land_buyer.name} ({connection.land_buyer.email})")
                else:
                    print(f"   - Land Buyer ID: {connection.land_buyer_id}")
        else:
            print(f"Agent with ID {agent_id} not found.")
    
    def find_agent_by_attribute(self):
        print("\n--- FIND AGENT BY NAME ---")
        agent_name = self.safe_input("Enter agent name to search: ")
        agents = Agent.find_by_name(self.session, agent_name)
        if agents:
            print(f"Found {len(agents)} agent(s):")
            for agent in agents:
                print(f"   {agent.full_info}")
        else:
            print(f"No agents found with name containing '{agent_name}'.")

    # CONNECTION MANAGEMENT
    def connections_management(self):
        while True:
            self.display_entity_menu("Connection")
            choice = self.get_user_choice(5)
            
            if choice == 1:
                self.create_connection()
            elif choice == 2:
                self.view_all_connections()
            elif choice == 3:
                self.find_connection_by_id()
            elif choice == 4:
                self.update_connection()
            elif choice == 5:
                self.delete_connection()
            elif choice == 0:
                break

    def create_connection(self):
        print("\n--- CREATE CONNECTION ---")
        try:
            agent_id = self.safe_int_input("Enter agent ID: ")
            land_buyer_id = self.safe_int_input("Enter land buyer ID: ")
           
            connection = Connection.create(self.session, agent_id, land_buyer_id)
            print(f"Connection created successfully!")
            print(f"   {connection.full_info}")
        except ValueError as e:
            print(f"Error: {e}")

    def update_connection(self):
        print("\n--- UPDATE CONNECTION ---")
        connection_id = self.safe_int_input("Enter connection ID to update: ")
        connection = Connection.find_by_id(self.session, connection_id)
        
        if not connection:
            print(f"Connection with ID {connection_id} not found.")
            return
        
        print(f"Current connection info: {connection.full_info}")
        print("\nEnter new values (press Enter to keep current value):")
        
        try:
            # Get updated values
            print(f"Current Agent ID: {connection.agent_id}")
            new_agent_input = input("Enter new agent ID (press Enter to keep): ").strip()
            new_agent_id = int(new_agent_input) if new_agent_input else connection.agent_id
            
            print(f"Current Land Buyer ID: {connection.land_buyer_id}")
            new_buyer_input = input("Enter new land buyer ID (press Enter to keep): ").strip()
            new_buyer_id = int(new_buyer_input) if new_buyer_input else connection.land_buyer_id
            
            # Update the connection
            Connection.update_by_id(self.session, connection_id, agent_id=new_agent_id, land_buyer_id=new_buyer_id)
            print(f"Connection updated successfully!")
            print(f"   {connection.full_info}")
        except ValueError as e:
            print(f"Error: {e}")
    
    def view_all_connections(self):
        print("\n--- ALL CONNECTIONS ---")
        connections = Connection.get_all(self.session)
        if not connections:
            print("No connections found.")
        else:
            for connection in connections:
                print(f"   {connection.full_info}")
    
    def find_connection_by_id(self):
        print("\n--- FIND CONNECTION BY ID ---")
        connection_id = self.safe_int_input("Enter connection ID: ")
        connection = Connection.find_by_id(self.session, connection_id)
        if connection:
            print(f"Connection found:")
            print(f"   {connection.full_info}")
        else:
            print(f"Connection with ID {connection_id} not found.")
    
    def delete_connection(self):
        print("\n--- DELETE CONNECTION ---")
        connection_id = self.safe_int_input("Enter connection ID to delete: ")
        connection = Connection.find_by_id(self.session, connection_id)
        if connection:
            print(f"Connection to delete: {connection.full_info}")
            confirm = input("Are you sure? (yes/no): ").lower()
            if confirm == 'yes':
                connection.delete(self.session)
                print("Connection deleted successfully!")
            else:
                print("Deletion cancelled.")
        else:
            print(f"Connection with ID {connection_id} not found.")

    # LISTINGS MANAGEMENT
    def listings_management(self):
        while True:
            self.display_entity_menu("Listing")
            choice = self.get_user_choice(5)
            
            if choice == 1:
                self.create_listing()
            elif choice == 2:
                self.view_all_listings()
            elif choice == 3:
                self.find_listing_by_id()
            elif choice == 4:
                self.update_listing()
            elif choice == 5:
                self.delete_listing()
            elif choice == 0:
                break
    
    def create_listing(self):
        print("\n--- CREATE LISTING ---")
        try:
            agent_id = self.safe_int_input("Enter agent ID: ")
            address = self.safe_input("Enter property address: ")
            price = self.safe_float_input("Enter price : ", required=True)
            size = self.safe_input("Enter property size: ", required=False)
            description = self.safe_input("Enter description (optional): ", required=False)
            is_available = input("Is listing available? (y/n, default y): ").lower() != 'n'
            
            listing = Listing.create(self.session, agent_id, address, size, price, description, is_available)
            print(f"Listing created successfully!")
            print(f"   {listing.full_info}")
        except ValueError as e:
            print(f"Error: {e}")

    def update_listing(self):
        print("\n--- UPDATE LISTING ---")
        listing_id = self.safe_int_input("Enter listing ID to update: ")
        listing = Listing.find_by_id(self.session, listing_id)
        
        if not listing:
            print(f"Listing with ID {listing_id} not found.")
            return
        
        print(f"Current listing info: {listing.full_info}")
        print("\nEnter new values (press Enter to keep current value):")
        
        try:
            # Get updated values
            print(f"Current Agent ID: {listing.agent_id}")
            new_agent_input = input("Enter new agent ID (press Enter to keep): ").strip()
            new_agent_id = int(new_agent_input) if new_agent_input else listing.agent_id
            
            new_address = self.get_optional_input("Enter new address", listing.address)
            new_size = self.get_optional_input("Enter new size", listing.size or "None")
            new_size = new_size if new_size != "None" else None
            
            new_price = self.get_optional_float_input("Enter new price", listing.price)
            
            new_description = self.get_optional_input("Enter new description", listing.description or "None")
            new_description = new_description if new_description != "None" else None
            
            new_is_available = self.get_optional_bool_input("Is listing available? (y/n)", listing.is_available)
            
            # Update the listing
            Listing.update_by_id(self.session, listing_id, agent_id=new_agent_id, address=new_address, 
                          size=new_size, price=new_price, description=new_description, 
                          is_available=new_is_available)
            print(f"Listing updated successfully!")
            print(f"   {listing.full_info}")
        except ValueError as e:
            print(f"Error: {e}")
    
    def view_all_listings(self):
        print("\n--- ALL LISTINGS ---")
        listings = Listing.get_all(self.session)
        if not listings:
            print("No listings found.")
        else:
            for listing in listings:
                print(f"   {listing.full_info}")
    
    def find_listing_by_id(self):
        print("\n--- FIND LISTING BY ID ---")
        listing_id = self.safe_int_input("Enter listing ID: ")
        listing = Listing.find_by_id(self.session, listing_id)
        if listing:
            print(f"Listing found:")
            print(f"   {listing.full_info}")
        else:
            print(f"Listing with ID {listing_id} not found.")
    
    def delete_listing(self):
        print("\n--- DELETE LISTING ---")
        listing_id = self.safe_int_input("Enter listing ID to delete: ")
        listing = Listing.find_by_id(self.session, listing_id)
        if listing:
            print(f"Listing to delete: {listing.full_info}")
            confirm = input("Are you sure? (yes/no): ").lower()
            if confirm == 'yes':
                listing.delete(self.session)
                print("Listing deleted successfully!")
            else:
                print("Deletion cancelled.")
        else:
            print(f"Listing with ID {listing_id} not found.")

    def run(self):
        print("Welcome to Property Tracker CLI!")
        try:
            while True:
                self.display_main_menu()
                choice = self.get_user_choice(5)
                
                if choice == 1:
                    self.land_buyer_management()
                elif choice == 2:
                    self.agent_management()
                elif choice == 3:
                    self.connections_management()
                elif choice == 4:
                    self.listings_management()
                elif choice == 5:
                    print("\nThank you for using Property Tracker CLI!")
                    break
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
        finally:
            self.session.close()


# To run the application
if __name__ == "__main__":
    app = PropertyTrackerCLI()
    app.run()