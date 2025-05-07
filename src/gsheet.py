import gspread
from google.oauth2.service_account import Credentials

# Define columns for the Google Sheet
COLUMNS = [
    "First Name", "Last Name", "Title", "Company", "Email"
]

# Embedded credentials (for testing purposes only)
credentials = {
    "type": "service_account",
    "project_id": "bliss-drive-automation",
    "private_key_id": "ebcc998cbb1117791242ae4ef7c169f7307f6072",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDf9mn89NncyHwy\naK1khgSjf3m7suY+WVWRAWbA/Du/rLeWOi4s3gfebVjEtcgV6/0XPkE1BnSrPCI/\njli5q7zEYIQGszbTXSaovuvCg6Z8QH3YPaaftArz5rDLlpXhodMURXNelMnFvxip\n4ME90qhwaVQXgZE75KhSUYKKzqYsQwl64kuw+0NQ1f+/1Z4v7QdJaAPYJqsfmnhH\nNh5cBHSWFqRaNuW1YLX+80Dgbye6mQD6SgVK6nCyKtR4rXgQ2yN6qfEZMZhqgukK\nH7z6uqd1uIhfI+rFS2wx6uBsD6T+uA6y+RQZ8hFPvgfXOcDo26xEtn7VvnVqKmNr\nmtn+lJJDAgMBAAECggEAVICdkfdyoka08bIkRir44hWtgUApdnnvepRcSFGDW7lX\n1aNjG8O0lVyNoz7xXTAa4OO458BlUdyREYjsejXNtgyyk/KXq51Ygk/zFYPl07jj\noqz0Swq8HTW8HDzXlXgg8+OWeafLD8UgEay/TMvIiQ180JevDDmkttaRWj1JXqZB\n4Qr+bNWgMz13S5hEo/jV6769jQJ6dPLQ70w1oEOYR0OlRXRVvby8DsjGtAiZaSFt\nnOfjRhLvmR6/Q5ScBrJnDZ16eooPGzQBKJboyl2I8NoLecuaPZd5cP1lA0yzJLKP\niPp6NkccPKwiby/D+WcqQ0J7+VbEMEa8KPtH/2C0TQKBgQDtUaCM7J4rtGREu4+V\nDl1qHEse2iouapjHBp3ynboUnq2HdScMy+MyFHrI/u1F36VCOPqYrYd3Qz7jgUC2\nQeYbCkcMKx5jCrAT/flzOIsaFCsLq8/o3JyVZoA9ReZ2FFJtcEyKTYZjFrH+qtQ6\n0PBSpFGdg2CbvFr0jzZlmIcHrQKBgQDxl6KPZj1+t2wL5Hq1YRdrJS+j8/WRDRid\nY6MmnnK0NYH8NwjeEnzhdsojB+sf6xAVYl/oyYdrdX38IkLTsem5nhAPZwBFiZ3q\nQmx0rbhQvDptkkvtO3ZL7/q1HUqc+k/4KBpv21iZoMtRr8Wp8Y+Dcph/PZ9HrsN3\nP+jkyEX/rwKBgF2isVgpHBdea5l676H+MvllBHa92ZrK0FDm2XcaqIruOMWTgb7Y\ny2G9Ft0rSG8jWM8SMD4BacuyqqOVIfVHdwUAPxwb/zdQxjx9HulJTAkUIA/Q0I2u\nTdHcyYhjhhTc29D2WBzRjc6W68/xkx9JxSi2UMV3Sqzn2nNX9jyLu+tZAoGBAJyZ\njuzm9/uYh7fZvVSu/9AbBZt/+nCwjYEP4eSZln6LpJtJTT0tvLclGffFHTrOUtmZ\nr9OkNlyIh0aVKr4wN/FyrLRfLsTkZHFB5y1moe/rYvA9gWvgPFkS0G7v8rp4YrfX\nvvM8ulyy5rgneLgk9cLd2E26MvHzLY6x5ZPO4djPAoGBANMogPSY+l9vLsBvN5ev\nREvLQmNZ7pjglUfEcb4tgdScMCDDmrUKNRC+oo8Yz6f572Y2kPHK0J0uigoUoM39\npAOLJxoCRN4PL/txljG2EYyhlAF+d3bmJK9nXF9WZB5threofAaMZNu4xip6Pqbg\nIKGFv6FRruOMRlwLmQ9NuWW1\n-----END PRIVATE KEY-----\n",
    "client_email": "blissdriveautomation@bliss-drive-automation.iam.gserviceaccount.com",
    "client_id": "110749820896612419611",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/blissdriveautomation%40bliss-drive-automation.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
  }

def setup_google_sheets(sheet_name):
    """
    Sets up the Google Sheets client using credentials and opens the specified sheet.

    Args:
        sheet_name (str): The name of the Google Sheet to open.

    Returns:
        gspread.Spreadsheet: The Google Sheets object.
    """
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = Credentials.from_service_account_info(credentials, scopes=scopes)
    client = gspread.authorize(creds)
    return client.open(sheet_name)

def populate_data(sheet, tab_name, data):
    """
    Append formatted data into a specified Google Sheets tab.

    Args:
        sheet (gspread.Spreadsheet): The Google Sheets object.
        tab_name (str): Name of the tab to populate.
        data (list): List of rows to populate in the tab.
    """
    try:
        # Access or create the worksheet
        try:
            worksheet = sheet.worksheet(tab_name)
        except gspread.exceptions.WorksheetNotFound:
            worksheet = sheet.add_worksheet(title=tab_name, rows=100, cols=len(COLUMNS))
            worksheet.append_row(COLUMNS)  # Set headers

        # Debugging: Print rows to confirm they are populated correctly
        print(f"Rows to append: {data}")

        # Append rows
        if data:
            worksheet.append_rows(data)
            print(f"Successfully appended data to tab: {tab_name}")
        else:
            print(f"No valid rows to append for tab: {tab_name}")
    except Exception as e:
        print(f"Error in populate_data: {e}")
