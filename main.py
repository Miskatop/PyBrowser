import sys
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication as App

app = App(sys.argv)

class Browser:
	"""docstring for Browser"""
	config = {
		'URL_START':'https://google.com',
		'DEFAULT_STYLES': '''
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
						''',
		'search_engine':0,
		'search_sqrts': ['https://google.com/search?q=',
						 'https://go.mail.ru/search?q=',
						 'https://yandex.com/search/?text=',
						 'https://duckduckgo.com/?q=',]
	}
	tab_cnt = []
	# window and layouts
	window =        QWidget()
	_vertival =     QVBoxLayout()
	_horizonal =    QHBoxLayout()
	# window elements
	add_tab_btn =   QPushButton("➕")
	close_tab_btn = QPushButton("❌")
	search_btn =    QPushButton("🔍")
	back_btn =      QPushButton("◀")
	tabs =          QTabWidget()
	url_line =      QLineEdit()
	search_engine = QComboBox()
	load_progress = QProgressBar()	

	# methods
	# lambda - methods
	loading = lambda self, p : self.load_progress.setValue(p)
	tab = lambda self:self.tabs.currentIndex()

	# def - methods
	def engine_change(self, x):self.config['search_engine'] = x
	def add_tab(self):
		# append tab contents and urls
		self.tab_cnt.append([QWebEngineView(), [self.config['URL_START']]])
		# load handlers
		tab = self.tab_cnt[-1]
		tab[0].loadStarted.connect(self.start_load)
		tab[0].loadProgress.connect(self.loading)
		tab[0].loadFinished.connect(lambda x: self.end_load())

		# loading a page
		tab[0].load(QUrl(tab[1][-1]))
		
		# adding tabs
		self.tabs.addTab(self.tab_cnt[-1][0], self.tab_cnt[-1][1][-1])
		self.tabs.setCurrentIndex(int(self.tab()) + 1)

	def close_tab(self):
		i = self.tab()
		if len(self.tab_cnt) > 1:
			# deleting tab data
			del self.tab_cnt[i]
			# removing tabs and loading names
			self.tabs.removeTab(i)

	def start_load(self):
		i = self.tab()
		url = self.tab_cnt[i][0].url().toString()
		show_url = url[:30] if len(url) > 30 else url
		self.window.setWindowTitle('WebLab - ' + show_url)	
		self.url_line.setText(url)
		self.tabs.setTabText(i , show_url)

	def load_content(self, path):
		with open(path, 'r') as f:
			cnt = f.read()
		return cnt

	def style(self, arg = ''):
		self.window.setStyleSheet(self.config['DEFAULT_STYLES'] if len(arg) < 30 else arg)

	def end_load(self):
		i = self.tab()
		url = self.tab_cnt[i][0].url()
		self.tab_cnt[i][1].append(url.toString())
		self.start_load()
		self.loading(0)

	def add_handlers(self):
		self.add_tab_btn.clicked.connect(self.add_tab)
		self.close_tab_btn.clicked.connect(self.close_tab)
		self.search_btn.clicked.connect(self.search)
		self.back_btn.clicked.connect(self.back_last_url)
		self.search_engine.currentIndexChanged.connect(self.engine_change)

	def back_last_url(self):
		pass

	def search(self):
		url = self.url_line.text()
		i = self.tab()
		url = url.split(' ')
		if 'http://' in url or 'https://' in url or 'file:///' in url:
			self.tab_cnt[i][0].load(QUrl(url))
		else:
			self.tab_cnt[i][0].load(QUrl(self.search_query(url)))

	def search_query(self, list_):
		base = self.config['search_sqrts'][self.config['search_engine']]
		for i in list_:base+=i+'+'
		return base

	def run(self):
		# init
		self.load_progress.setTextVisible(False)
		self.load_progress.setMaximum(100)
		self.load_progress.setValue(0)
		self.search_engine.addItem("Google")
		self.search_engine.addItem("Mail")
		self.search_engine.addItem("Yandex")
		self.search_engine.addItem("DuckDuckGo")
		# setup
		self.add_tab()
		self.add_handlers()
		# sreating
		self.window.setWindowState(Qt.WindowMaximized)
		self._horizonal.addWidget(self.load_progress)
		self._horizonal.addWidget(self.url_line)
		self._horizonal.addWidget(self.search_btn)
		self._horizonal.addWidget(self.back_btn)
		self._horizonal.addWidget(self.add_tab_btn)
		self._horizonal.addWidget(self.close_tab_btn)
		self._horizonal.addWidget(self.search_engine)
		self._vertival.addLayout(self._horizonal)
		self._vertival.addWidget(self.tabs)
		self.window.setLayout(self._vertival)
		# runing
		self.window.show()

x = Browser()
x.run()
x.style(x.load_content('out.cwd'))
sys.exit(app.exec_())