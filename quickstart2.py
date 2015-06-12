# quickstart2.py makes a json file, cs111EmailsAll, which is used in filtering_emails.py
#This code was taken from https://developers.google.com/gmail/api/quickstart/python and modified for our needs
from datetime import datetime
import os

from apiclient.discovery import build
from httplib2 import Http
import oauth2client
from oauth2client import client
from oauth2client import tools

import base64
import email

from apiclient import errors


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print 'Storing credentials to ' + credential_path
    return credentials

messageList = [] # list of all messages
def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    
    credentials = get_credentials()
    service = build('gmail', 'v1', http=credentials.authorize(Http()))
    
    #following code taken from https://developers.google.com/gmail/api/v1/reference/users/messages/list and modified 
    try:
        #gets a list of all the emails from your account that were 'to:cs111-spring15
        response = service.users().messages().list(userId='me', q='to:cs111-spring15').execute()
      
        if 'messages' in response:
            messageList.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId='me', q='to:cs111-spring15',pageToken=page_token).execute()
            messageList.extend(response['messages'])

    except errors.HttpError, error:
        print 'An error occurred: %s' % error
    
    for message in messageList:
        GetMessage(service, 'me', message['id'])


allEmails = [] # list of all the emails 
def GetMessage(service, user_id, msg_id):
  """Get a Message with given ID.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A Message.
  """
  try:
    message = service.users().messages().get(userId=user_id, id= msg_id, format= 'full').execute()
    allEmails.append(message)
   
    # Payload formats: full gives lots of random stuff in addition to keys/values
    # minimal gives keys/values (snippets)
    # raw gives random stuff (cleaner than full)
    

  except errors.HttpError, error:
    print 'An error occurred: %s' % error



if __name__ == '__main__':
    main()
    import json
    json.dump(allEmails,open('cs111EmailsALL.json','w'))#dump takes object and open file for writing