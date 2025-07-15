from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from summarize import summarize_text
import time
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/crawl-news')
def crawl_news():
    yesterday = datetime.today() - timedelta(days=1)
    sheet_name = yesterday.strftime("%Y-%m-%d")
    

    # 구글 시트 인증
    client = get_gspread_client()
    sheet = client.open("ESG 뉴스").worksheet(sheet_name)  # 날짜에 따라 동적으로 바꿀 수도 있음

    data = sheet.get_all_records()
    service = Service("chromedriver")  # chromedriver 경로
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)

    for i, row in enumerate(data):
        link = row['링크']
        driver.get(link)
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        text = ' '.join([p.text for p in soup.find_all('p')])

        if any(k in text for k in ['모집', '신청', '접수']):
            summary = summarize_text(text)
            sheet.update_cell(i + 2, 4, summary)

    driver.quit()
    return jsonify({'status': 'done'})