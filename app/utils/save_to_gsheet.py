import gspread
from oauth2client.service_account import ServiceAccountCredentials
from app.config import GOOGLE_SHEET_NAME, GOOGLE_CREDENTIALS_FILE
import logging

logger = logging.getLogger(__name__)


def save_to_google_sheet(row_data: dict):
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            GOOGLE_CREDENTIALS_FILE, scope
        )
        client = gspread.authorize(creds)
        sheet = client.open(GOOGLE_SHEET_NAME).sheet1

        # Ensure headers exist
        headers = sheet.row_values(1)
        if not headers:
            headers = list(row_data.keys())
            sheet.append_row(headers)

        # Match row data to header order
        row = [row_data.get(header, "") for header in headers]
        sheet.append_row(row, value_input_option="USER_ENTERED")

    except Exception as e:
        logger.exception("Failed to save to Google Sheet")


# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# from app.config import GOOGLE_SHEET_NAME, GOOGLE_CREDENTIALS_FILE
# import logging

# logger = logging.getLogger(__name__)


# def save_to_google_sheet(row_data: dict):
#     try:
#         scope = [
#             "https://spreadsheets.google.com/feeds",
#             "https://www.googleapis.com/auth/drive",
#         ]
#         creds = ServiceAccountCredentials.from_json_keyfile_name(
#             GOOGLE_CREDENTIALS_FILE, scope
#         )
#         client = gspread.authorize(creds)

#         # Debug: List all accessible spreadsheets
#         print("🔍 Spreadsheets visible to service account:")
#         for sheet_meta in client.list_spreadsheet_files():
#             print(f" - {sheet_meta['name']}")

#         # Try to open the spreadsheet
#         sheet = client.open(GOOGLE_SHEET_NAME).sheet1

#         # Get or create headers
#         headers = sheet.row_values(1)
#         if not headers:
#             headers = list(row_data.keys())
#             sheet.append_row(headers)

#         # Match row data to header order
#         row = [row_data.get(header, "") for header in headers]
#         sheet.append_row(row, value_input_option="USER_ENTERED")

#     except Exception:
#         logger.exception("Failed to save to Google Sheet")
