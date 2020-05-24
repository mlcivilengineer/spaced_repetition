import datetime
import pickle
from selenium import webdriver
# from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from selenium.webdriver.chrome.options import Options

def create_spaced_repetition_event(service, name, today_date, spaced_time=3, timeZone='America/Sao_Paulo'):
  delta = datetime.timedelta(spaced_time)
  event_date = str(today_date + delta)
  event = {
    'summary': name,
    'start': {
      'date': event_date,
      'timeZone': timeZone,
    },
    'end': {
      'date': event_date,
      'timeZone': timeZone,
    },
    'reminders': {
      'useDefault': False,
      'overrides': [
        {'method': 'email', 'minutes': 24 * 60},
        {'method': 'popup', 'minutes': 10},2
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


with open('credentials/token.pickle', 'rb') as token:
    creds = pickle.load(token)
service = build('calendar', 'v3', credentials=creds)

today_date = datetime.date.today()
NOTION_URL = 'https://www.notion.so/Study-Notes-be00b11bb10844a7aee3ce59f3454bd2'

DRIVER_PATH = './drivers/chromedriver'
chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(DRIVER_PATH, options=chrome_options)
driver.get(NOTION_URL)

response = driver.find_element_by_css_selector(
    '#notion-app > div > div.notion-cursor-listener > div > div.notion-scroller.vertical.horizontal > div.notion-page-content')

if '@Today' in response.text:
  title = f'Study Recap of {str(today_date)}'
  create_spaced_repetition_event(service, title, today_date, spaced_time=1)
  create_spaced_repetition_event(service, title, today_date, spaced_time=4)
  create_spaced_repetition_event(service, title, today_date, spaced_time=10)
  create_spaced_repetition_event(service, title, today_date, spaced_time=30)