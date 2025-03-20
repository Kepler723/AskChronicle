# coding:utf-8
import sys

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme,Theme,
                            NavigationAvatarWidget, SplitFluentWindow, FluentTranslator)
from qfluentwidgets import FluentIcon as FIF
from view.retrieval_interface import RetrievalInterface 
from view.setting_interface import SettingInterface 
from view.generator_interface import GeneratorInterface

class Window(SplitFluentWindow):
    def __init__(self):
        super().__init__()

        # create sub interface
        self.retrievalInterface = RetrievalInterface()
        self.generatorInterface = GeneratorInterface()
        self.settingInterface = SettingInterface()

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.retrievalInterface, FIF.SEARCH, '地方志检索')
        self.addSubInterface(self.generatorInterface, FIF.STOP_WATCH, '自定义问答生成')
        
        self.navigationInterface.addItem(
            routeKey='helpDocs',
            icon=FIF.HELP,
            text='帮助文档',
            onClick=self.goToHelpDocs,
            position=NavigationItemPosition.BOTTOM,
        )
            
        self.navigationInterface.addItem(
            routeKey='settingInterface',
            icon=FIF.SETTING,
            text='设置',
            onClick=self.goToSetting,
            position=NavigationItemPosition.BOTTOM,
        )
        self.navigationInterface.setExpandWidth(280)

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('AskChronicle')
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
    
    def goToSetting(self):
        pass

    def goToHelpDocs(self):
        pass

if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)

    # install translator
    translator = FluentTranslator()
    app.installTranslator(translator)

    w = Window()
    w.show()
    app.exec_()