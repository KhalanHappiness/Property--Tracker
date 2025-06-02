# Property Tracker 

Property tracker is a command-line interface application for managing real estate properties, agents, land buyers, and their connections. Built with Python and SQLAlchemy ORM.

## Features

- **Land Buyer Management**: Create, view, search, update, and manage land buyers
- **Agent Management**: Manage real estate agents and their information
- **Connection Management**: Track relationships between agents and land buyers
- **Listing Management**: Manage property listings and their details
- **Interactive CLI**: User-friendly command-line interface with menu navigation

## Project Structure

```
property-tracker/
├── models/
│   ├── base.py          # Database base configuration
│   ├── land_buyer.py    # Land buyer model
│   ├── agent.py         # Agent model
│   ├── connection.py    # Connection model (agent-buyer relationships)
│   └── listing.py       # Property listing model
├── cli.py              # CLI application entry point
└── README.md           # This file
```

## Requirements

- Python 3.7+
- SQLAlchemy
- A database system (SQLite, PostgreSQL, MySQL, etc.)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd property-tracker
```

2. Install dependencies:
```bash
pip install sqlalchemy
```

3. Set up your database configuration in `models/base.py`

4. Run the application:
```bash
python cli.py
```

## Usage

### Main Menu Options

1. **Land Buyer Management**
2. **Agent Management**
3. **Connection Management**
4. **Listing Management**
5. **Exit**

### Land Buyer Management

- **Create Land Buyer**: Add new land buyers with name, email, and optional phone
- **View All Land Buyers**: Display all registered land buyers
- **Find by ID**: Search for a specific land buyer by their ID
- **Update Land Buyer**: Modify existing land buyer information (name, email, phone)
- **Delete Land Buyer**: Remove a land buyer from the system
- **View Related Objects**: See connections associated with a land buyer
- **Find by Email**: Search for land buyers by email address

### Agent Management

- **Create Agent**: Register new agents with name, license number, email, and phone
- **View All Agents**: List all registered agents
- **Find by ID**: Search for agents by their ID
- **Update Agent**: Modify existing agent information (name, license number, email, phone)
- **Delete Agent**: Remove an agent from the system
- **View Related Objects**: See listings and connections for an agent
- **Find by Name**: Search for agents by name

### Connection Management

- **Create Connection**: Link an agent with a land buyer
- **View All Connections**: Display all agent-buyer relationships
- **Find by ID**: Search for specific connections
- **Update Connection**: Modify existing connections (change agent or buyer assignments)
- **Delete Connection**: Remove agent-buyer relationships

### Listing Management

- **Create Listing**: Add new property listings with details
- **View All Listings**: Display all property listings
- **Find by ID**: Search for specific listings
- **Update Listing**: Modify existing listings (address, price, size, description, availability)
- **Delete Listing**: Remove property listings

## Data Models

### Land Buyer
- ID, Name, Email, Phone (optional)
- Relationships: Connected to agents via connections

### Agent
- ID, Name, License Number, Email, Phone (optional)
- Relationships: Has multiple listings and connections to land buyers

### Connection
- ID, Agent ID, Land Buyer ID, Created At
- Represents the relationship between an agent and a land buyer

### Listing
- ID, Agent ID, Address, Price, Size, Description, Availability Status
- Belongs to a specific agent

## Features

### CRUD Operations
- **Create**: Add new records for all entities
- **Read**: View individual records or list all records
- **Update**: Modify existing records with selective field updates
- **Delete**: Remove records with confirmation prompts

### Update Functionality
The update feature allows you to modify existing records while preserving data you don't want to change:
- **Selective Updates**: Only change the fields you want to modify
- **Current Value Display**: See existing values before making changes
- **Keep Current Option**: Press Enter to retain existing values
- **Input Validation**: All existing validation rules apply to updates

### Input Validation
- Required field validation
- Type checking for numeric inputs
- Email format validation (if implemented in models)
- Duplicate prevention for connections

### Error Handling
- Database transaction rollback on errors
- User-friendly error messages
- Graceful handling of invalid inputs

### User Experience
- Clear menu navigation
- Confirmation prompts for deletions
- Formatted output displays
- Keyboard interrupt handling (Ctrl+C)
- Intuitive update interface with current value hints

## Example Usage

1. **Start the application**:
```bash
python cli.py
```

2. **Create an agent**:
   - Select "2. Agent Management"
   - Select "1. Create Agent"
   - Enter agent details when prompted

3. **Create a land buyer**:
   - Select "1. Land Buyer Management"
   - Select "1. Create Land Buyer"
   - Enter buyer details

4. **Update a land buyer**:
   - Select "1. Land Buyer Management"
   - Select "4. Update Land Buyer"
   - Enter the buyer's ID
   - Modify only the fields you want to change (press Enter to keep current values)

5. **Connect agent and buyer**:
   - Select "3. Connection Management"
   - Select "1. Create Connection"
   - Enter agent ID and land buyer ID

6. **Add property listing**:
   - Select "4. Listing Management"
   - Select "1. Create Listing"
   - Enter property details

7. **Update a listing**:
   - Select "4. Listing Management"
   - Select "4. Update Listing"
   - Enter listing ID and modify desired fields

## Database Schema

The application uses SQLAlchemy ORM with the following relationships:
- One Agent can have many Listings
- One Agent can have many Connections to Land Buyers
- One Land Buyer can have many Connections to Agents
- Connections represent many-to-many relationships between Agents and Land Buyers
- Click this link https://dbdiagram.io/d/Property-Tracker-683462c66980ade2eb6b32e9 to view the database schema on dbdiagram.io 

## Error Handling

The application includes comprehensive error handling for:
- Invalid user inputs
- Database connection issues
- Duplicate entries
- Missing records
- Transaction failures
- Update validation errors

## Future Enhancements

- Web interface
- API endpoints
- Advanced search and filtering
- Reporting features
- Export functionality
- User authentication
- Email notifications
- Bulk update operations
- Update history tracking

## By HAppiness Khalan