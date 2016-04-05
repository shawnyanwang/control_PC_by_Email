import re
import gmail_basic
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
        self.account = None
        self.loginMail()
        self.configSlaveMail()

    def loginMail(self):
        self.mccLog.mccWriteLog('Start to log in gmail')
        try:
            self.account = gmail_basic.gmail(self.username, self.password)
            self.account.login()
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
            self.account.obtain_last_email()
            self.mccLog.mccWriteLog('Success to grap Email')
            return True
        except Exception, e:
            self.mccLog.mccError('Fail to grap Email' + str(e))
            return False

    def analysisMail(self):
        self.mccLog.mccWriteLog('Start to grap the sender and subject')
        try:
            self.account.parse_email()
            subject = self.account.get__last_email_subject()
            print subject
            message = self.account.get__last_email_message()
            print message
            sender = self.account.get_last_email_from_adress()
            print sender



            command = {'subject': subject, 'sender': sender, 'message':message}
            self.mccLog.mccWriteLog('Success to grap the sender and subject')
            return command
        except Exception, e:
            self.mccLog.mccError('Fail to grap the sender and subject' + str(e))
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
                self.account.send(self.username, subject, body)
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
    mail.acceptMail()
    print mail.analysisMail()
    mail.sendMail('OK','Boss')
