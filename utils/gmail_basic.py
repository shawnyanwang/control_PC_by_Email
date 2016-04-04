
# import email
import os
import re
class gmail():
    # initialize
    def __init__(self, username='ciyuliu@gmail.com', password='wwwcctvcom514'):
        self.username = username
        self.password = password
        self.recieve_box = None
        self.send_box = None
        self.last_email = None
        self.sender = None
        self.subject = None
        self.message = None
    # LOGGING IN TO THE INBOX
    def login(self, reciever_sever = 'imap.gmail.com', reciever_port = 993,
    sender_sever = 'smtp.gmail.com', sender_port =587):
        import imaplib
        import smtplib
        # log in reciever server
        self.recieve_box = imaplib.IMAP4_SSL(reciever_sever,reciever_port)
        self.recieve_box.login(self.username, self.password)
        self.recieve_box.select("inbox") # connect to inbox.
        self.send_box = smtplib.SMTP(sender_sever,sender_port)
        self.send_box.starttls()
        self.send_box.login(self.username, self.password)

    # GUSING UIDS INSTEAD OF VOLATILE SEQUENTIAL IDS
    def obtain_last_email(self):
        result, data = self.recieve_box.uid('search', None, "ALL") # search and return uids instead
        latest_email_uid = data[0].split()[-1]
        result, data = self.recieve_box.uid('fetch', latest_email_uid, '(RFC822)')
        self.last_email = data[0][1]

    # PARSING RAW EMAILS
    def parse_email(self):
        import email
        email_message = email.message_from_string(self.last_email)
        self.sender = email_message['From']
        self.subject = email_message['Subject']
        # print email_message.items() # print all headers
        accepted_types = ['text/plain']
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() in accepted_types:
                    self.message = part.get_payload()
        else:
            if email_message.get_content_type() in accepted_types:
                self.message = email_message.get_payload()

    def get_last_email_from_adress(self):
        # return self.sender
        return re.search('<(.*?)>',str(self.sender),re.S).group(1)

    def get__last_email_subject(self):
        return self.subject

    def get__last_email_message(self):
        return self.message

    def send(self, toaddr, subject='', msg=''):
        fromaddr = self.username

        headers = ["From: " + fromaddr,
               "Subject: " + subject,
                   "To: " + toaddr,
                   "MIME-Version: 1.0",
                   "Content-Type: text/html"]
        headers = "\r\n".join(headers)
        self.send_box.sendmail(fromaddr, toaddr, headers + "\r\n\r\n" + msg)


if __name__== '__main__':
    g = gmail()
    g.login()
    g.obtain_last_email()
    g.parse_email()
    print g.get_last_email_from_adress()
    print g.get__last_email_subject()
    print g.get__last_email_message()
    g.send('shawnyanwang@gmail.com','fox','what does the fox say')
