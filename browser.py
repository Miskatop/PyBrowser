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
search_btn = QPushButton("Search")
back_btn = QPushButton("Back")

# variables
current_url = 'https://www.google.com'

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
		tabWidget.addTab(web_eng[web_eng.index(i)], current_url)
		tabWidget.setCurrentIndex(web_eng.index(i))


# Functions
def title(_title):
	win.setWindowTitle('WebLab - ' + str(_title.split('//')[-1]))	
	url_line.setText(_title)

add_tab_button.clicked.connect(add_tab)
search_btn.clicked.connect(search)

def window():
	web_eng[0].load(QUrl(current_url))
	win.setWindowState(Qt.WindowMaximized)
	hbox.addWidget(url_line)
	hbox.addWidget(search_btn)
	hbox.addWidget(back_btn)
	hbox.addWidget(add_tab_button)
	vbox.addLayout(hbox)
	construct_tabs()
	vbox.addWidget(tabWidget)
	win.setLayout(vbox)
	win.show()
	sys.exit(app.exec_())

window()