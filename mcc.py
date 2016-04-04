#-*-coding:utf-8 -*-

import time
import sys
from utils.mailHelper1 import mailHelper1
from utils.excutor import executor
from utils.configReader import configReader

__Author__ = 'kingname'
__Verson__ = 0.5

reload(sys)
sys.setdefaultencoding('utf-8')

class MCC(object):
    CONFIGPATH = '_config.ini'
    KEY_COMMAND = 'Command'
    KEY_OPEN = 'Open'
    KEY_BOSS = 'Boss'
    KEY_TIMELIMIT = 'timelimit'

    def __init__(self):
        self.mailHelper1 = mailHelper1()
        self.configReader = configReader(self.CONFIGPATH)
        commandDict = self.configReader.getDict(self.KEY_COMMAND)
        openDict = self.configReader.getDict(self.KEY_OPEN)
        self.timeLimit = int(self.configReader.readConfig(self.KEY_BOSS, self.KEY_TIMELIMIT))
        self.excutor = executor(commandDict, openDict)
        self.toRun()

    def toRun(self):
        while True:
            self.mailHelper1 = mailHelper1()
            self.run()
            time.sleep(self.timeLimit)

    def run(self):
        mailBody = self.mailHelper1.acceptMail()
        print self.mailHelper1.analysisMail(mailBody)
        if mailBody:
            exe = self.mailHelper1.analysisMail(mailBody)
            if exe:
                self.excutor.execute(exe, self.mailHelper1)

if __name__=='__main__':
        mcc = MCC()
