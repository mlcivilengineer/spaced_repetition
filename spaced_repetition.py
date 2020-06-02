import datetime
import pickle

# from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def wait_and_get_element(css_selector=None, time_to_wait=30, driver=None):
    return WebDriverWait(driver, time_to_wait).until(ec.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))


def create_spaced_repetition_event(service, name, today_date, spaced_time=3, timeZone='America/Sao_Paulo'):
    delta = datetime.timedelta(spaced_time)
    new_date = today_date + delta
    start_date = str(datetime.datetime.combine(date=new_date, time=datetime.time(hour=19)).isoformat("T"))
    end_date = str(datetime.datetime.combine(date=new_date, time=datetime.time(hour=23,minute=50)).isoformat("T"))
    event = {
        'summary': name,
        'start': {
            'dateTime': start_date,
            'timeZone': timeZone,
        },
        'end': {
            'dateTime': end_date,
            'timeZone': timeZone,
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 60},
                {'method': 'popup', 'minutes': 60},
            ],
        },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))


#
# SCOPES = ['https://www.googleapis.com/auth/calendar']
# flow = InstalledAppFlow.from_client_secrets_file(
#     'credentials.json', SCOPES)
# creds = flow.run_local_server(port=0)
# with open('token.pickle', 'wb') as token:
#     pickle.dump(creds, token)

def main(*args):
    with open('credentials/token.pickle', 'rb') as token:
        creds = pickle.load(token)
    service = build('calendar', 'v3', credentials=creds)

    today_date = datetime.date.today()
    NOTION_URL = 'https://www.notion.so/Study-Notes-be00b11bb10844a7aee3ce59f3454bd2'

    DRIVER_PATH = './drivers/chromedriver'
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(DRIVER_PATH, options=chrome_options)
    driver.get(NOTION_URL)

    response = wait_and_get_element(
        '#notion-app > div > div.notion-cursor-listener > div.notion-frame > div.notion-scroller.vertical.horizontal > div.notion-page-content',
        driver=driver)

    print(response.text)

    if '@Today' in response.text:
        title = f'Study Recap of {str(today_date)}'
        print(f'creating events for {title}')
        create_spaced_repetition_event(service, title, today_date, spaced_time=1)
        create_spaced_repetition_event(service, title, today_date, spaced_time=4)
        create_spaced_repetition_event(service, title, today_date, spaced_time=11)
        create_spaced_repetition_event(service, title, today_date, spaced_time=32)

if __name__ == '__main__':
    main()