import sys
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication

class App:

	DEFAULT_STYLE = '''
		QPushButton{
			font-size: 12px;
			border-radius: 13px;
			padding: 5px;
			border: none;
		}
		QPushButton:hover{
			background: #ccc;
		}
		QProgressBar{
			max-width: 100px;
		}
		QLineEdit{
			height: 30px;
			border-radius: 7.5px;
		}
	'''

	def __init__(self, *args):
		self.urls = []
		self.viewers = []

		# init elements
		self.window =        QWidget()
		self._vl =           QVBoxLayout()
		self._hl =           QHBoxLayout()
		self.tabs =          QTabWidget()
		self.url_line =      QLineEdit()
		self.add_tab_btn =   QPushButton("➕")
		self.close_tab_btn = QPushButton("❌")
		self.search_btn =    QPushButton("🔍")
		self.back_btn =      QPushButton("◀")
		self.load =          QProgressBar()

		# setting
		self.load.setTextVisible(False)
		self.load.setMaximum(100)
		self.load.setValue(0)

		# handlers
		self.add_tab_btn.clicked.connect(self.add_tab)
		self.close_tab_btn.clicked.connect(self.close_tab)
		self.search_btn.clicked.connect(self.search)


		# construct and show window
		self.add_tab()
		self.style(self.load_content('browser_out.mbc'))
		self.construct_window()


	loading = lambda s, p : s.load.setValue(p)

	tab_i = lambda s: s.tabs.currentIndex() 

	def to_google(self, args):
		url = 'https://google.com/search?q='
		for arg in args :
			url += arg
		return url

	def search(self):
		i = self.tab_i()
		_url = self.url_line.text()
		if 'http://' in _url or 'https://' in _url or 'file:///' in _url:
			self.viewers[i].load(QUrl(_url))
		else:
			self.viewers[i].load(QUrl(self.to_google(_url.split(' '))))
		
		self.urls[i] = _url

	def add_tab(self):
		# append tab contents and urls
		self.viewers.append(QWebEngineView())
		self.urls.append('https://google.com')
		
		# load handlers
		self.viewers[-1].loadStarted.connect(self.start_load)
		self.viewers[-1].loadProgress.connect(self.loading)
		self.viewers[-1].loadFinished.connect(lambda x: self.end_load())

		# loading a page
		self.viewers[-1].load(QUrl(self.urls[self.tab_i()]))
		
		# adding tabs
		self.tabs.addTab(self.viewers[-1], 'https://google.com')
		self.tabs.setCurrentIndex(int(self.tab_i()) + 1)

	def close_tab(self):
		i = self.tab_i()
		# deleting tab data
		del self.viewers[i]
		del self.urls[i]
		# removing tabs and loading names
		self.tabs.removeTab(i)
		self.start_load()

	def start_load(self):
		i = self.tab_i()
		self.urls[i] = self.viewers[i].url().toString()
		show_url = self.urls[i]

		if len(show_url) > 30:
			show_url = str(self.urls[i])[:30]

		self.window.setWindowTitle('WebLab - ' + show_url)	
		self.url_line.setText(self.urls[i])
		self.tabs.setTabText(i , show_url)

	def end_load(self):
		self.start_load()
		self.load.setValue(0)

	def construct_window(self):
		self.window.setWindowState(Qt.WindowMaximized)
		self._hl.addWidget(self.load)
		self._hl.addWidget(self.url_line)
		self._hl.addWidget(self.search_btn)
		self._hl.addWidget(self.back_btn)
		self._hl.addWidget(self.add_tab_btn)
		self._hl.addWidget(self.close_tab_btn)
		self._vl.addLayout(self._hl)
		self._vl.addWidget(self.tabs)
		self.window.setLayout(self._vl)
		self.window.show()

	def load_content(self, path):
		with open(path, 'r') as f:
			cnt = f.read()
		return cnt

	def style(self, arg = ''):
		if len(arg) > 30:
			self.window.setStyleSheet(arg)
		else:
			self.window.setStyleSheet(self.DEFAULT_STYLE)

app = QApplication(sys.argv)
App()
sys.exit(app.exec_())