import re
import gmaillib
from email.mime.text import MIMEText
from configReader import configReader
from mccLog import mccLog

class mailHelper1(object):
    CONFIGPATH = '_config.ini'

    def __init__(self):
        self.mccLog = mccLog()
        cfReader = configReader(self.CONFIGPATH)
        self.username = cfReader.readConfig('Slave', 'username')
        self.password = cfReader.readConfig('Slave', 'password')
        self.bossMail = cfReader.readConfig('Boss', 'mail')
        self.loginMail()
        self.configSlaveMail()

    def loginMail(self):
        self.mccLog.mccWriteLog('Start to log in gmail')
        try:
            self.account = gmaillib.account(self.username, self.password)
            print 'Success log in Email'
            self.mccLog.mccWriteLog('Log in gmail')
        except Exception,e:
            print 'Log in failed'
            self.mccLog.mccError('Fail to log in gmail' + str(e))
            exit()

    def acceptMail(self):
        self.mccLog.mccWriteLog('Start to grap Email')
        try:
            # get the
            self.mailBody = self.account.inbox(start=0, amount=1)[0]
            self.mccLog.mccWriteLog('Success to grap Email')
            return self.mailBody

        except Exception, e:
            self.mccLog.mccError('Fail to grap Email' + str(e))
            return None

    def analysisMail(self, mailBody):
        self.mccLog.mccWriteLog('Start to grap the sender and subject')
        try:
            subject = re.search('Subject: (.*?)\n',str(self.mailBody),re.S).group(1)
            # print subject
            sender = re.search("From: (.*?)\n",str(self.mailBody),re.S).group(1)

            # print sender
            command = {'subject': subject, 'sender': sender}
            self.mccLog.mccWriteLog('Fail to grap the sender and subject')
            return command
        except Exception, e:
            self.mccLog.mccError('Success to grap the sender and subject' + str(e))
            return None

    def configSlaveMail(self):
        self.mccLog.mccWriteLog('Start to set up sending')
        try:
            self.mccLog.mccWriteLog('Success to set up sending')
        except Exception, e:
            self.mccLog.mccError('Fail to set up sending' + str(e))
            exit()

    def sendMail(self, subject, receiver, body='Success'):
        self.mccLog.mccWriteLog('Start to send mail'+ ' to ' + receiver)
        if receiver == 'Slave':
            try:
                # print self.username, self.username, msg.as_string()
                self.account.send(self.username+'@gmail.com', subject, body)
                self.mccLog.mccWriteLog('Success to send mail')
                return True
            except Exception,e:
                self.mccLog.mccError('Fail to send mail' + str(e))
                return False

        elif receiver == 'Boss':
            try:
                self.account.send(self.bossMail, subject, body)
                self.mccLog.mccWriteLog('Success to send mail')
            except Exception,e:
                self.mccLog.mccError('Fail to send mail' + str(e))
                return False

if __name__ == '__main__':

    mail = mailHelper1()
    body = mail.acceptMail()
    print mail.analysisMail(body)
    mail.sendMail('OK','Boss')
