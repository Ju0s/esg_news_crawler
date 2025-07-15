import os
import json
import base64
from oauth2client.service_account import ServiceAccountCredentials
import gspread

def get_gspread_client():
    encoded = os.environ.get("GOOGLE_CREDENTIALS_B64")  # 환경변수에서 받기
    if not encoded:
        raise ValueError("GOOGLE_CREDENTIALS_B64 환경변수가 없습니다.")

    decoded_json = base64.b64decode(encoded).decode('utf-8')
    creds_dict = json.loads(decoded_json)

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)
