# FR_Mgmt - Flask Device Management

A simple Flask web application for managing devices via MAC addresses. Designed to interact with a MariaDB database for storing and retrieving device information.

## Project Overview

- **Purpose**: Manage devices identified by MAC addresses
- **Tech Stack**: Python, Flask, MariaDB
- **Structure**: Standard Flask application with templates and static files

## Project Structure

```
FR_Mgmt/
├── app.py              # Main Flask application
├── config.py           # Database configuration (gitignored)
├── config.sample.py    # Sample configuration template
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Landing page with device list
└── static/
    └── placeholder.png # Static assets
```

## Quick Start

### Prerequisites
- Python 3.8+
- MariaDB server
- pip

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bsnellen/FR_Mgmt.git
   cd FR_Mgmt
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure database:**
   ```bash
   cp config.sample.py config.py
   # Edit config.py with your MariaDB credentials
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the app:**
   Open http://localhost:5000 in your browser

## Configuration

The application uses the following environment variables (with defaults from config.py):

- `DB_HOST`: MariaDB host (default: localhost)
- `DB_PORT`: MariaDB port (default: 3306)
- `DB_USER`: Database username (default: root)
- `DB_PASSWORD`: Database password (default: empty)
- `DB_NAME`: Database name (default: fr_mgmt)

## Database Schema

The application is designed to work with a MariaDB database. The current implementation includes a connection function that can be extended to interact with device data.

## Current Features

- Landing page displaying a list of MAC address usernames
- MariaDB connection function ready for database operations
- Standard Flask project structure

## Future Development

- Add CRUD operations for device management
- Implement user authentication
- Add database initialization scripts
- Create API endpoints for device data

## AI Development Notes

For AI agents working on this project:

- The main application logic is in `app.py`
- Database connection is handled by `get_db_connection()` function
- Configuration should be loaded from `config.py` (not committed to git)
- Templates are in the `templates/` directory
- Static files are in the `static/` directory
- The landing page currently shows placeholder MAC addresses that will be replaced with database content

## License

This project is open source and available for use.
