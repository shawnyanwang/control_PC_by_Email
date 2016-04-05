#-*-coding:utf8-*-

import os
import win32api
from utils.mccLog import mccLog

class executor(object):
    def __init__(self, commandDict, openDict):
        self.mccLog = mccLog()
        self.commandDict = commandDict
        self.openDict = openDict

    def execute(self, exe, mailHelper1):
        self.mailHelper1 = mailHelper1
        subject = exe['subject']
        self.mccLog.mccWriteLog('Start to process the command')
        if subject != 'pass':
            self.mailHelper1.sendMail('pass','Slave')
            if subject in self.commandDict:
                self.mccLog.mccWriteLog('Run the command')
                try:
                    command = self.commandDict[subject]
                    os.system(command)
                    self.mailHelper1.sendMail('Success','Boss')
                    self.mccLog.mccWriteLog('Successful to run the command')
                except Exception, e:
                    self.mccLog.mccError('Fail to run the command' + str(e))
                    self.mailHelper1.sendMail('error', 'Boss', e)
            elif subject in self.openDict:
                self.mccLog.mccWriteLog('Open the file')
                try:
                    openFile = self.openDict[subject]
                    win32api.ShellExecute(0, 'open', openFile, '', '', 1)
                    self.mailHelper1.sendMail('Success', 'Boss')
                    self.mccLog.mccWriteLog('Successful to open file')
                except Exception, e:
                    self.mccLog.mccError('Fail to open file' + str(e))
                    self.mailHelper1.sendMail('error', 'Boss', e)
            elif subject[:7].lower() == 'sandbox':
                self.sandBox(exe['message'])
            else:
                self.mailHelper1.sendMail('error', 'boss', 'no such command')

    def sandBox(self, code):
        """sandbox:test.py$n$import win32api$c$if 1 + 1 == 2:$c$$$$$win32api.MessageBox(0, 'sandbox', 'this is sandbox')"""

        name = code.split('\r\n')[0]

        # code = code.split('/r/n')[1:]
        codestr = '#'+'\n'.join(code.split('\r\n'))
        # codestr = '\n'.join(code.split('$c$'))
        # codestr = codestr.replace('\r\n', '\n ')
        print codestr
        with open(name.replace('\r\n',''), 'w+') as f:
            f.write(codestr)
        os.system('python ' + name)
