from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
import pandas as pd
import io
from . import ticket_types
from datetime import date,datetime,timedelta

def access_gmail():
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None

    if os.path.exists('design_lab/token.pickle'):
        with open('design_lab/token.pickle','rb') as token:
            creds= pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json',SCOPES)
            creds= flow.run_local_server(port=0)
        
        with open('design_lab/token.pickle','wb') as token:
            pickle.dump(creds,token)
    return creds

def find_latest_email(serv):
   
    query = "from:reports@obsres.com"

    #gets the messages from the specific sender
    results = serv.users().messages().list(userId='me',q=query).execute()
    messages = []
    if 'messages' in results:
        messages.extend(results['messages'])

    #returns a list of dictionaries containing the message ids
    #response = service.users().messages().get(userId='me',id=messages[0]['id']).execute()
    #print(response)

    #should be the first message id sent by the bot
    return messages[0]['id']

def get_attachment(serv,messageId):

    results = serv.users().messages().get(userId='me',id=messageId).execute()

    #looping through email contends
    for part in results['payload']['parts']:

        #if this part has a filename
        if part['filename']:

            #save the attachment id
            att_id = part['body']['attachmentId']
            return att_id

    return None
   


def get_csv_contents(serv,attId,messId):
    attachment =  serv.users().messages().attachments().get(userId='me',id=attId,messageId=messId).execute()
    data = attachment['data']
    str_csv = base64.urlsafe_b64decode(data.encode('UTF-8')).decode('utf-8')
    df = pd.read_csv(io.StringIO(str_csv))
    #remove NaN rows
    df.dropna(axis=0,how='all',inplace=True)

    #get date and convert to date object
    d = df['date'].iloc[-1]
    current_date = [int(x) for x in d.split('/')]
    month,day,year = current_date
    current_date = date(year,month,day)

    #all but last ticket type
    group_range = df['ticket'].iloc[0:-1].tolist()
    grade_range = ticket_types.filter_and_order_group_range(group_range)

    #daily total
    total = df['qty'].iloc[-1]

    return current_date,grade_range,total

def get_information():
    creds = access_gmail()
    service = build('gmail','v1',credentials=creds)
    message_id = find_latest_email(service)
    attachment_id = get_attachment(service,message_id)
    if attachment_id == None:
        return (0,0,0)
    contents = get_csv_contents(service,attachment_id,message_id)
    return contents
    



