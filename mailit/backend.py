# For backend gmail calls

from __future__ import print_function

import base64
import os.path
from email.mime.text import MIMEText

import dateutil.parser as parser
from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send']


def buildemail(emailreturned: dict, service) -> list:
    '''x'''
    temp_dict = {}
    m_id = emailreturned['id']  # get id of individual message
    message = service.users().messages().get(userId="me", id=m_id).execute()
    if 'UNREAD' in message['labelIds']:
        temp_dict['Status'] = 'UNREAD'
    else:
        temp_dict['Status'] = 'READ'
    payld = message['payload']  # get payload of the message
    headr = payld['headers']  # get header of the payload

    for one in headr: 
        print(one['name']) # getting the Subject
        if one['name'] == 'Subject' or one['name'] == 'subject':
            msg_subject = one['value']
            temp_dict['Subject'] = msg_subject

            if msg_subject[0:5].lower() == 'pr1: ': temp_dict['Priority'] = 1
            elif msg_subject[0:5].lower() == 'pr2: ': temp_dict['Priority'] = 2
            elif msg_subject[0:5].lower() == 'pr3: ': temp_dict['Priority'] = 3
            elif msg_subject[0:5].lower() == 'pr4: ': temp_dict['Priority'] = 4
            elif msg_subject[0:5].lower() == 'pr5: ': temp_dict['Priority'] = 5
            else: temp_dict['Priority'] = 6
        else:
            pass

    for two in headr:  # getting the date
        if two['name'] == 'Date':
            msg_date = two['value']
            date_parse = (parser.parse(msg_date))
            m_date = (date_parse.date())
            temp_dict['Date'] = str(m_date)
        else:
            pass

    for three in headr:  # getting the Sender
        if three['name'] == 'From' or three['name'] == 'from':
            msg_from = three['value']
            temp_dict['Sender'] = msg_from
        else:
            pass

    temp_dict['Snippet'] = message['snippet']

    try:

        # Fetching message body
        mssg_parts = payld['parts']  # fetching the message parts
        part_one = mssg_parts[0]  # fetching first element of the part
        part_body = part_one['body']  # fetching body of the message
        part_data = part_body['data']  # fetching data from the body
        # decoding from Base64 to UTF-8
        clean_one = part_data.replace("-", "+")
        # decoding from Base64 to UTF-8
        clean_one = clean_one.replace("_", "/")
        # decoding from Base64 to UTF-8
        clean_two = base64.b64decode(bytes(clean_one, 'UTF-8'))
        temp_dict['Message_body'] = clean_two

    except:
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
    unread_msgs = service.users().messages().list(
        userId='me', labelIds=['INBOX', 'UNREAD']).execute()

    for i in unread_msgs['messages']:
        count += 1

        finallist.append(buildemail(i, service))
        if count == numberofemails:
            return finallist


def getread(numberofemails: int) -> list:
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
    unread_msgs = service.users().messages().list(
        userId='me', q="label:read").execute()

    for i in unread_msgs['messages']:
        dicti = buildemail(i, service)
        if 'Subject' in dicti.keys():
            finallist.append(dicti)
            count += 1
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
    unread_msgs = service.users().messages().list(
        userId='me', labelIds=['INBOX']).execute()

    for i in unread_msgs['messages']:
        count += 1

        finallist.append(buildemail(i, service))
        if count == numberofemails:
            return finallist


def pushmsg(service, message):
    '''x'''
    try:
        message = (service.users().messages().send(
            userId="me", body=message).execute())
        print('Message Id: %s' % message['id'])
        return True , None
    except Exception as e:
        print("Failed", e)
        return False , e


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
    return pushmsg(service, {'raw': base64.urlsafe_b64encode(message.as_string().encode('utf-8')).decode()})


def getrecenthtml(numberofemails: int) -> list:
    recentdict = getrecent(numberofemails)
    totalstringlst = []
    totalstring = ''

    for i in recentdict:
        print(i.keys(), 'hello')
        string ="""<button class="emailRow pr"""
        string += str(i['Priority']) + " " 
        string += i['Status']+"""">
        <div class="emailRow__options">
        <input type="checkbox" name="" id="" />
        <span class="material-icons"> star_border </span>
        <span class="material-icons"> label_important </span>
        </div><h3 class="emailRow__title">"""
        string += i['Sender']
        string += """</h3><div class="emailRow__message">
        <h4>"""
        string += i['Subject']
        string += """<span class="emailRow__description">  """
        string += i['Snippet']
        string += """</span></h4></div>
                    <p class="emailRow__time">"""
        string += i['Date']
        string += """</p></button></a>"""

        totalstringlst.append({"html":string,"priority":i['Priority']})

    #Sorted
    # def sortonprio(value):
    #     return value['priority']
    sortonprio = lambda value: value['priority']
    totalstringlst.sort(key = sortonprio)
    for i in totalstringlst:
        totalstring += i['html']
    return totalstring

def getuseremailid():
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

    profile = service.users().getProfile(userId='me').execute()
    return profile['emailAddress']

if __name__ == '__main__':
    # sendemail("anishr890@gmail.com","sankalpmukim@gmail.com","Does this work","please tell me it works")
    print(getrecenthtml(5))
