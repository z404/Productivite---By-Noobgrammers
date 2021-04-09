# For backend gmail calls

from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import dateutil.parser as parser
from bs4 import BeautifulSoup
import base64
from email.mime.text import MIMEText

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']

def buildemail(emailreturned: dict, service) -> list:
    '''x'''
    temp_dict = {}
    m_id = emailreturned['id'] # get id of individual message
    message = service.users().messages().get(userId="me", id=m_id).execute()

    payld = message['payload'] # get payload of the message 
    headr = payld['headers'] # get header of the payload


    for one in headr: # getting the Subject
        if one['name'] == 'Subject':
            msg_subject = one['value']
            temp_dict['Subject'] = msg_subject
        else:
            pass


    for two in headr: # getting the date
        if two['name'] == 'Date':
            msg_date = two['value']
            date_parse = (parser.parse(msg_date))
            m_date = (date_parse.date())
            temp_dict['Date'] = str(m_date)
        else:
            pass

    for three in headr: # getting the Sender
        if three['name'] == 'From':
            msg_from = three['value']
            temp_dict['Sender'] = msg_from
        else:
            pass

    temp_dict['Snippet'] = message['snippet']

    try:
    
        # Fetching message body
        mssg_parts = payld['parts'] # fetching the message parts
        part_one  = mssg_parts[0] # fetching first element of the part 
        part_body = part_one['body'] # fetching body of the message
        part_data = part_body['data'] # fetching data from the body
        clean_one = part_data.replace("-","+") # decoding from Base64 to UTF-8
        clean_one = clean_one.replace("_","/") # decoding from Base64 to UTF-8
        clean_two = base64.b64decode (bytes(clean_one, 'UTF-8')) # decoding from Base64 to UTF-8
        temp_dict['Message_body'] = clean_two

    except :
        pass

    return temp_dict

def getunread(numberofemails: int) -> list:
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    count = 0
    finallist = []
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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

    service = build('gmail', 'v1', credentials=creds)
    unread_msgs = service.users().messages().list(userId='me',labelIds=['INBOX','UNREAD']).execute()
    
    for i in unread_msgs['messages']:
        count+=1

        finallist.append(buildemail(i, service))
        if count == numberofemails:
            return finallist
    
def getrecent(numberofemails: int) -> list:
    count = 0
    finallist = []
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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

    service = build('gmail', 'v1', credentials=creds)
    unread_msgs = service.users().messages().list(userId='me',labelIds=['INBOX']).execute()

    for i in unread_msgs['messages']:
        count+=1

        finallist.append(buildemail(i, service))
        if count == numberofemails:
            return finallist

def pushmsg(service, message):
    '''x'''
    try:
        message = (service.users().messages().send(userId="me", body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except Exception as e:
        print("Failed",e)

def sendemail(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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

    service = build('gmail', 'v1', credentials=creds)

    pushmsg(service, {'raw': base64.urlsafe_b64encode(message.as_string().encode('utf-8')).decode()})

if __name__ == '__main__':
    sendemail("anishr890@gmail.com","sankalpmukim@gmail.com","Does this work","please tell me it works")