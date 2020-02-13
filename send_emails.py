from __future__ import print_function
from googleapiclient.discovery import build
from apiclient import errors
from email.mime.text import MIMEText
import base64
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path

EMAIL_FROM = 'corporate@cssbristol.co.uk'
EMAIL_TO = ['in18536']
EMAIL_SUBJECT = 'Happy Valentines from CSS'
SERVICE_ACCOUNT_FILE = 'credentials.json'
EMAIL_CONTENT = """Hi,\n


You have been sent a valentines card, congrats! Come to MVB foyer to see what your true love has written about you!\n

CSS\n"""

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def service_account_login():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service


def main():
    service = service_account_login()
    # Call the Gmail API
    for i in range(len(EMAIL_TO)):
        message = create_message(EMAIL_FROM, EMAIL_TO[i]+"@bristol.ac.uk", EMAIL_SUBJECT, EMAIL_CONTENT)
        send_message(service, 'me', message)


if __name__ == '__main__':
    main()
