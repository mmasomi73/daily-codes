import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import base64
from bs4 import BeautifulSoup
from datetime import datetime
import jdatetime
import pandas as pd


class EmailHandler:
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    save_directory = 'files/'

    def __init__(self, ex_number='01', start_date=None):
        self.ex_number = ex_number
        self.start_date = start_date
        self.save_directory = self.save_directory + "Ex_" + ex_number

        SCOPES = self.SCOPES

        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('gmail', 'v1', credentials=creds)

    def __getEmailLists__(self, hasAttachment = False):
        query = ""
        if self.start_date is not None:
            start_date = str(self.start_date).split(" ")[0]
            query += "after:{}".format(start_date)
        if hasAttachment:
            query += " has:attachment"
        inbox = self.service.users().messages().list(userId='me', q=query).execute()
        return inbox

    def __getEXEmails__(self, inbox):

        emails_list = []

        service = self.service
        messages = inbox.get('messages', [])
        for msg in messages:
            email_row = {}
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = txt['payload']
            headers = payload['headers']
            subject = ""
            for d in headers:
                if d['name'] == 'Subject':
                    subject = d['value']
                if d['name'] == 'From':
                    sender = d['value']
            email_row['Subject'] =subject
            email_row['From'] = sender

            parts = payload.get('parts')
            email_row['Body'] = ""
            email_row['Attachment'] = ""
            email_row['Date'] = ""
            if isinstance(parts, list):
                for part in parts:
                    body = part['body']
                    if 'data' in body:
                        data = body['data']
                        data = data.replace("-", "+").replace("_", "/")
                        decoded_data = base64.b64decode(data)
                        soup = BeautifulSoup(decoded_data.decode('utf-8'), "lxml")
                        email_row['Body'] = email_row['Body'] + " | " + soup.text
                        email_row['Body'] = email_row['Body']


                    if 'attachmentId' in part['body']:
                        attachment = service.users().messages().attachments() \
                            .get(userId='me',
                                 messageId=txt['id'],
                                 id=part['body']['attachmentId']).execute()


                        email_row['Attachment'] = email_row['Attachment'] + " | " + part['filename']
                        email_row['Attachment'] = email_row['Attachment']
                        email_date = jdatetime.datetime.utcfromtimestamp(int(txt['internalDate']) / 1000)
                        email_date = email_date.strftime("%Y/%m/%d %H:%M")
                        email_row['Date'] = email_row['Date'] + " | " + email_date

                        file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))

                        if not os.path.isdir(self.save_directory + "/files"):
                            os.makedirs(self.save_directory + "/files")
                        path = ''.join([self.save_directory + "/files/", part['filename']])
                        f = open(path, 'wb')
                        f.write(file_data)
                        f.close()

            emails_list.append(email_row)
        dataframe = pd.DataFrame(emails_list)
        if not os.path.isdir(self.save_directory + "/files"):
            os.makedirs(self.save_directory + "/files")
        dataframe.to_csv(self.save_directory + "/ lists.csv", encoding="utf-8-sig")

    def getExercises(self):
        inbox = self.__getEmailLists__(True)
        self.__getEXEmails__(inbox)

