# Project Setup Guide

## Prerequisites
Before running the project, ensure you have the following installed:
- Python 3.x
- SQLite3
- Internet connection (for API requests)
- Required Python libraries:
  - `requests`
  - `sqlite3`
  - `datetime`

## Installation

1. **Clone the repository**
   ```sh
   git clone <repository_url>
   cd <project_directory>
   ```

2. pip install -r requirements .txt
3. 
   ```sh
   pip install requests
   ```

## Configuration

- Ensure the API credentials in the script (`fetch_and_store_sales_data`) are correct.
- Modify `from_date` and `to_date` as needed before running the script.

## Running the Project

To execute the script and fetch sales data:
```sh
python main.py
```

## Expected Output
- The script fetches sales data from the API and stores it in `sales_database.db`.
- If successful, it prints:
  ```
  Data successfully fetched and stored
  ```
- In case of an error, an appropriate error message is displayed.

## Verifying Data

To check if data is stored correctly in SQLite:
```sh
sqlite3 sales_database.db
SELECT * FROM sales_data;
```

## Troubleshooting

1. **Database Errors**
   - Ensure SQLite3 is installed.
   - Check if `sales_database.db` is being created in the project directory.

2. **API Errors**
   - Verify API credentials.
   - Check for internet connectivity.
