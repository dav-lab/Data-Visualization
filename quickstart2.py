# quickstart2.py makes a json file, cs111EmailsAll, which is used in filtering_emails.py

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

messageList = []
def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    
    credentials = get_credentials()
    service = build('gmail', 'v1', http=credentials.authorize(Http()))

    #results = service.users().messages().list(userId='me', q='to:cs111-spring15').execute()
    #for messages in results['messages']:
    #    GetMessage(service, 'me', messages['id'])
    
    try:
        response = service.users().messages().list(userId='me', q='to:cs111-spring15').execute()
        
        if 'messages' in response:
            messageList.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId='me', q='to:cs111-spring15',pageToken=page_token).execute()
            messageList.extend(response['messages'])

        #mList= messageList
    except errors.HttpError, error:
        print 'An error occurred: %s' % error
    for message in messageList:
        GetMessage(service, 'me', message['id'])


allEmails = []
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
    
    #return raw
    #print 'Message snippet: %s' % message['raw']
    #message = service.users().messages().get(userId=user_id, id= msg_id).payload.parts[0].body.data
    #print message
    #print 'Message snippet: %s' % message['payload']
#
   #msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
#
    #mime_msg = email.message_from_string(msg_str)
    #mime_msg = email.Parser().parsestr(msg_str,'<p>')

    #print mime_msg

    #msg_str = base64.urlsafe_b64decode(message['payload']['parts'][0]['body']['data'].encode('ASCII')) #Worked to get the message
    #print msg_str
     
  except errors.HttpError, error:
    print 'An error occurred: %s' % error



if __name__ == '__main__':
    main()
    import json
    json.dump(allEmails,open('cs111EmailsALL.json','w'))#dump takes object and open file for writing