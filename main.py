# from dotenv import load_dotenv
from src.gsheet import setup_google_sheets, populate_data
from src.apollo import fetch_people_by_company  # or mock_fetch_people_by_company for testing

def main():
    # Load environment variables if needed
    # load_dotenv()

    SHEET_NAME = " "
    API_ENDPOINT = ()
    TAB_NAME = " "

    # Initialize Google Sheets
    try:
        print("Initializing Google Sheets...")
        sheet = setup_google_sheets(SHEET_NAME)
        print("Google Sheets successfully initialized!")
    except Exception as e:
        print(f"Failed to initialize Google Sheets: {e}")
        return

    # Prompt whether to run the automation
    run_automation = input("Do you want to run the Apollo automation? (yes/no): ").strip().lower()
    if run_automation not in ('yes', 'y'):
        print("Automation canceled.")
        return

    # Ask initially if the user wants to unlock emails using enrichment
    unlock_emails_input = input("Do you want to unlock emails using enrichment? (yes/no): ").strip().lower()
    unlock_emails = True if unlock_emails_input in ('yes', 'y') else False

    # Get the 'Companies' tab
    try:
        companies_tab = sheet.worksheet("Companies")
        print("Accessed 'Companies' tab successfully.")
    except Exception as e:
        print(f"Error accessing 'Companies' tab: {e}")
        return

    # Read company names from the 'Companies' column (skip header)
    company_names = companies_tab.col_values(1)[1:]
    if not company_names:
        print("No company names found in the 'Companies' tab.")
        return

    # Process companies in batches of 100
    batch_size = 100
    total_companies = len(company_names)
    for idx, company_name in enumerate(company_names, start=1):
        if not company_name.strip():
            continue

        print(f"Processing company ({idx}/{total_companies}): {company_name}")

        # Fetch data from Apollo using the provided endpoint and the unlock_emails flag
        data = fetch_people_by_company(API_ENDPOINT, company_name, per_page=5, unlock_emails=unlock_emails)
        print(f"Fetched data for {company_name}: {data}")

        if data:
            try:
                formatted_data = []
                for person in data:
                    if isinstance(person, dict):
                        name_parts = person.get("name", "").split(" ", 1)
                        first_name = name_parts[0] if name_parts else "Unknown"
                        last_name = name_parts[1] if len(name_parts) > 1 else "Unknown"

                        formatted_data.append([
                            first_name,
                            last_name,
                            person.get("title", "Unknown Title"),
                            person.get("organization", "Unknown Company"),
                            person.get("email", "No Email")
                        ])

                if formatted_data:
                    populate_data(sheet, TAB_NAME, formatted_data)
                    print(f"Data for '{company_name}' appended successfully.")
                else:
                    print(f"No valid data for '{company_name}'.")
            except Exception as e:
                print(f"Error populating data for '{company_name}': {e}")
        else:
            print(f"No data fetched for '{company_name}'.")

        # After processing every 100 companies, prompt the user again about unlocking emails.
        if idx % batch_size == 0 and idx < total_companies:
            continue_unlock = input("Processed 100 companies. Do you want to continue unlocking emails using enrichment? (yes/no): ").strip().lower()
            if continue_unlock not in ('yes', 'y'):
                print("Emails will no longer be unlocked for subsequent companies.")
                unlock_emails = False

if __name__ == "__main__":
    main()
