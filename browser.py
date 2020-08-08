import sys
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication, QMainWindow

# app and engine
app = QApplication(sys.argv)
web_eng = [QWebEngineView()]
urls = ['https://google.com']
win = QWidget()

# layouts
vbox = QVBoxLayout()
hbox = QHBoxLayout()
tabWidget = QTabWidget()

# elements
url_line = QLineEdit()
add_tab_button =  QPushButton("+")
CloseTab = QPushButton("X")
search_btn = QPushButton("Search")
back_btn = QPushButton("Back")
progressBar = QProgressBar()


# settings
progressBar.setMaximum(100)
progressBar.setTextVisible(False)
progressBar.setValue(0)

# functions
def to_google(args):
	url = 'https://google.com/search?q='
	for arg in args :
		url += arg
	return url

def search():
	tab = tabWidget.currentIndex()
	urls[tab] = url_line.text()
	url = urls[tab]
	if not 'http://' in url or 'https://' in url:
		url = to_google(url.split(' '))
	web_eng[tab].load(QUrl(url))

def add_tab():
	web_eng.append(QWebEngineView())
	urls.append('https://google.com')
	construct_tabs()

def construct_tabs():
	for i in web_eng:
		web_eng[web_eng.index(i)].load(QUrl(urls[web_eng.index(i)]))
		web_eng[web_eng.index(i)].loadStarted.connect(title)
		web_eng[web_eng.index(i)].loadProgress.connect(loading)
		web_eng[web_eng.index(i)].loadFinished.connect(lambda x: progressBar.setValue(0))
		tabWidget.addTab(web_eng[web_eng.index(i)], title())
		tabWidget.setCurrentIndex(web_eng.index(i))

def close_tab():
	x = tabWidget.currentIndex()
	del web_eng[x]
	del urls[x]
	tabWidget.removeTab(x)

def loading(proc):
	progressBar.setValue(proc)

def title():
	urls[tabWidget.currentIndex()] = web_eng[tabWidget.currentIndex()].url().toString()
	
	show_url = urls[tabWidget.currentIndex()]
	if len(show_url) > 30:
		show_url = str(urls[tabWidget.currentIndex()])[:30]

	win.setWindowTitle('WebLab - ' + show_url)	
	url_line.setText(urls[tabWidget.currentIndex()])
	tabWidget.setTabText(tabWidget.currentIndex() ,show_url)

# handlers
add_tab_button.clicked.connect(add_tab)
CloseTab.clicked.connect(close_tab)
search_btn.clicked.connect(search)

def window():
	web_eng[0].load(QUrl(urls[tabWidget.currentIndex()]))
	win.setWindowState(Qt.WindowMaximized)
	hbox.addWidget(url_line)
	hbox.addWidget(search_btn)
	hbox.addWidget(back_btn)
	hbox.addWidget(add_tab_button)
	hbox.addWidget(CloseTab)
	hbox.addWidget(progressBar)
	vbox.addLayout(hbox)
	construct_tabs()
	vbox.addWidget(tabWidget)
	win.setLayout(vbox)
	win.show()
	sys.exit(app.exec_())

window()