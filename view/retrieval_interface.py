from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout,QHBoxLayout
from PyQt5.QtCore import QStringListModel
from qfluentwidgets import ComboBox, setFont, PushButton, BodyLabel, FlowLayout, ListView, FluentIcon as FIF, LineEdit, TextBrowser
from database.sql_util import get_session, get_data
# from database.sql_config import local_config, remote_config 

class RetrievalInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('retrievalInterface')
        self.init_window()
        self.init_data()
        setFont(self, 12)

    def init_window(self):

        self.retrievalLayout = QGridLayout(self)  # 只有主布局设置父控件为self
        self.retrievalLayout.setContentsMargins(30, 50, 30, 20)
        self.retrievalLayout.setSpacing(15)  # 垂直和水平间距都设为15像素

        # Search layout
        self.searchLayout = QVBoxLayout()
        
        # Filter layout
        self.filterLayout = QHBoxLayout()
        
        self.bookCategory = BodyLabel('书名')
        self.bookFilter = ComboBox()
        self.volumeCategory = BodyLabel('卷名')
        self.volumeFilter = ComboBox()
        self.searchButton = PushButton('搜索')
        
        self.filterLayout.addWidget(self.bookCategory)
        self.filterLayout.addWidget(self.bookFilter)
        self.filterLayout.addWidget(self.volumeCategory)
        self.filterLayout.addWidget(self.volumeFilter)
        self.filterLayout.addWidget(self.searchButton)
        
        self.retrievaledLabel = BodyLabel('检索结果')
        self.articleList = ListView()
        
        self.searchLayout.addLayout(self.filterLayout)
        self.searchLayout.addWidget(self.retrievaledLabel)
        self.searchLayout.addWidget(self.articleList)
        
        # 创建显示布局
        self.displayLayout = QVBoxLayout()

        self.queryLayout = QHBoxLayout()
        self.queryInput = LineEdit()
        self.queryInput.setPlaceholderText('请输入问题')
        self.queryButton = PushButton('提问')

        self.queryLayout.addWidget(self.queryInput)
        self.queryLayout.addWidget(self.queryButton)

        self.articleTitle = BodyLabel('文章标题')
        self.articleContent = TextBrowser()

        self.displayLayout.addLayout(self.queryLayout)
        self.displayLayout.addWidget(self.articleTitle)
        self.displayLayout.addWidget(self.articleContent)

        
        # 将子布局添加到主布局
        self.retrievalLayout.addLayout(self.searchLayout, 0, 0)
        self.retrievalLayout.addLayout(self.displayLayout, 0, 1)
    
    def init_data(self):
        self.session = get_session()

        metadata = get_data(self.session, '析出资源', ["基础文献记录标识号", "所属卷", "正题名"])
        volumeInfo = get_data(self.session, "卷名", ["文献编号", "卷属", "卷名"])
        bookInfo = get_data(self.session, "基础资源", ["正题名", "加工编号"])
        self.book2id = {book[0]: book[1] for book in bookInfo}
        self.book2volumes={}
        self.volume2title = {}
        self.articles ={}
        for volume in volumeInfo:
            self.book2volumes[volume[0]] = self.book2volumes.get(volume[0], [])+[volume[1]]
            self.volume2title[(volume[0],volume[1])] = volume[2]
        for article in metadata:
            if article[1] is not None:
                self.articles[(article[0], article[1])] = self.articles.get((article[0], article[1]), []) + [article[2]]

        self.bookFilter.addItems(self.book2id.keys())
        self.bookFilter.currentIndexChanged.connect(self.update_volume_filter)
        self.update_volume_filter()
        self.searchButton.clicked.connect(self.update_article_list)
    
    def update_volume_filter(self):
        self.volumeFilter.clear()
        self.volumeFilter.addItems(self.book2volumes[self.book2id[self.bookFilter.currentText()]])
    
    def update_article_list(self):
        self.currentBook = self.book2id[self.bookFilter.currentText()]
        self.currentVolume = self.volumeFilter.currentText()
        slm = QStringListModel()
        slm.setStringList(self.articles[(self.book2id[self.bookFilter.currentText()], self.volumeFilter.currentText())])
        self.articleList.setModel(slm)
        self.articleList.clicked.connect(self.update_article_content)
    
    def update_article_content(self):
        title = self.articleList.currentIndex().data()
        text = get_data(self.session, "析出资源", ["内容"], 
                        [("基础文献记录标识号", self.currentBook),
                         ("所属卷", self.currentVolume),
                         ("正题名", title)])[0]
        self.articleTitle.setText(title)
        self.articleContent.setText(text[0])
        