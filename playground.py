import httplib2, os, oauth2client, base64, requests, gspread, globe
from oauth2client import client, tools
from lxml import html, etree
from random import randint
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs
from oauth2client.service_account import ServiceAccountCredentials
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery  #needed for gmail service
# About script - http://stackoverflow.com/questions/37201250/sending-email-via-gmail-python

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/home/user256/PycharmProjects/passwords/sheets_client_secrets.json', scope)
client = gspread.authorize(creds)

def main():
    getwod()
    #email()

#globe.linguee, globe.verbix

def email():
    to = "johnwilliamfegan@gmail.com"
    sender = "johnwilliamfegan@gmail.com"
    subject = "German word of the day:  " + globe.wod.value
    message_text_html  = r"The word of the day is" + globe.wod.value + "<br/> It's conjugated as: " + globe.verbix + "<br/>You can get more details on " + globe.linguee
    message_text_plain = "Hi\nPlain Email"
    create_message_and_send(sender, to, subject, message_text_plain, message_text_html)

def getwod():
    randcell = randint(0, 100)
    wks = client.open("German Verbs").sheet1
    globe.wod = wks.acell("B"+str(randcell))
    verbix = urlparse("http://www.verbix.com/webverbix/German/" + globe.wod.value + ".html")
    linguee = urlparse("http://www.linguee.de/deutsch-englisch/search?query=" + globe.wod.value + "&source=auto")

    doc = html.parse(linguee.geturl())
    lines = doc.xpath("//div[2]/div[1]/div/div[1]/div[1]/div/div/div/div/div[*]/div/div[*]")
    print(lines)
    globe.linguee = linguee.geturl()
    globe.verbix = verbix.geturl()

    page = requests.get(linguee.geturl()).content



"""
    list = []
    for x in lines:
        for y in x.xpath("span"):
            list += y
    buffer = ''
    for i in range(len(list)):
        buffer += str(list[i])
    print(buffer)
"""



def get_credentials():
    # If needed create folder for credential
    home_dir = os.path.expanduser("/home/user256/PycharmProjects/passwords")
    credential_dir = os.path.join(home_dir, '.credentials') # >>C:\Users\Me\.credentials   (it's a folder)
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)  #create folder if doesnt exist
    credential_path = os.path.join(credential_dir, 'cred send mail.json')
    store = oauth2client.file.Storage(credential_path) #Store the credential
    credentials = store.get()
    if not credentials or credentials.invalid:
        CLIENT_SECRET_FILE = '/home/user256/PycharmProjects/passwords/consolesecrets.json'
        APPLICATION_NAME = 'Gmail API Python Send Email'
        #The scope URL for read/write access to a user's calendar data  
        SCOPES = 'https://www.googleapis.com/auth/gmail.send'
        # Create a flow object. (it assists with OAuth 2.0 steps to get user authorization + credentials)
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
    return credentials

## Get creds, prepare message and send it
def create_message_and_send(sender, to, subject,  message_text_plain, message_text_html):
    credentials = get_credentials()
    # Create an httplib2.Http object to handle our HTTP requests, and authorize it using credentials.authorize()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    ## without attachment
    message_without_attachment = create_message_without_attachment(sender, to, subject, message_text_html, message_text_plain)
    send_Message_without_attachement(service, "me", message_without_attachment, message_text_plain)

def create_message_without_attachment (sender, to, subject, message_text_html, message_text_plain):
    #Create message container
    message = MIMEMultipart('alternative') # needed for both plain & HTML (the MIME type is multipart/alternative)
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = to

    #Create the body of the message (a plain-text and an HTML version)
    message.attach(MIMEText(message_text_plain, 'plain'))
    message.attach(MIMEText(message_text_html, 'html'))

    raw_message_no_attachment = base64.urlsafe_b64encode(message.as_bytes())
    raw_message_no_attachment = raw_message_no_attachment.decode()
    body  = {'raw': raw_message_no_attachment}
    return body

def send_Message_without_attachement(service, user_id, body, message_text_plain):
    try:
        message_sent = (service.users().messages().send(userId=user_id, body=body).execute())
    except errors.HttpError as error:
        print ('An error occurred: {error}')

if __name__ == '__main__':
        main()