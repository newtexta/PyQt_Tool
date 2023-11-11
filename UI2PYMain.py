# https://github.com/newtexta/PyQt_Tool.git
import os
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QStringListModel,Qt
from PyQt5.QtWidgets import QWidget,QFileDialog,QPushButton,QLineEdit,QProgressBar,QApplication,QAction,QMenu,QSystemTrayIcon,QMessageBox
from PyQt5.QtSql import QSqlTableModel,QSqlDatabase
from PyQt5.Qt import Qt
from UI2PY import Ui_Form
import sqlite3
import shutil

class UI2PY(QWidget,Ui_Form):
	def __init__(self):
		super(UI2PY,self).__init__()
		self.setupUi(self)
		a = os.path.abspath('.')
		a = a.split("\\")
		a = tuple(a)
		a = '/'.join(a)
		a += "/converter.png"
		icon = QIcon(a)
		self.setWindowIcon(icon)
		self.tray_icon = QSystemTrayIcon(self)
		self.tray_icon.setIcon(QIcon(a))
		show_action = QAction("Show", self)
		show_action.triggered.connect(self.showNormal)
		hide_action = QAction("Hide",self)
		hide_action.triggered.connect(self.hide_show)
		quit_action = QAction("Quit", self)
		quit_action.triggered.connect(self.close)
		tray_menu = QMenu()
		tray_menu.addAction(show_action)
		tray_menu.addAction(hide_action)
		tray_menu.addAction(quit_action)
		self.tray_icon.setContextMenu(tray_menu)
		self.tray_icon.show()
		self.pushButton.clicked.connect(self.convert)
		self.pushButton_2.clicked.connect(self.finish)
		self.pushButton_2.setEnabled(False)
		self.pushButton_3.clicked.connect(self.fileopen)
		self.pushButton_4.clicked.connect(self.openfolder2)
		self.pushButton_5.clicked.connect(self.openfolder)
		self.string_list = []
		self.model = QStringListModel()
		self.model.setStringList(self.string_list)
		self.listView.setModel(self.model)
		self.setup_context_menu()
		self.string_list2 = []
		self.model2 = QStringListModel()
		self.model2.setStringList(self.string_list2)
		self.listView_2.setModel(self.model2)
		self.setup_context_menu2()
		self.pv = 0
		self.progressBar.setMinimum(0)
		self.progressBar.setMaximum(100)
		self.progressBar.setValue(self.pv)
		self.progressBar.setStyleSheet("QProgressBar { border: 2px solid orange; border-radius: 5px; color: rgb(20,20,20);  background-color: #FFFFFF; text-align: center;}QProgressBar::chunk {background-color: rgb(100,200,200); border-radius: 25px; margin: 0.1px;  width: 1px;}")
		self.progressBar.setFormat('Loaded  %p%'.format(self.progressBar.value()-self.progressBar.minimum()))

	def hide_show(self):
		self.hide()

	def close(self):
		sys.exit()

	def closeEvent(self,event):
		reply = QMessageBox.question(self,u'Asking',u'Minimize to the pallet?',QMessageBox.No|QMessageBox.Yes)
		if reply == QMessageBox.Yes:
			event.ignore()
			self.hide()
		else:
			sys.exit()

	def setup_context_menu2(self):
		self.listView_2.setContextMenuPolicy(Qt.CustomContextMenu)
		self.listView_2.customContextMenuRequested.connect(self.show_context_menu2)
		self.refresh_action2 = QAction("Refresh", self.listView_2)
		self.delete_action2 = QAction("Delete Line",self.listView_2)
		self.clear_action2 = QAction("Clear All",self.listView_2)
		self.refresh_action2.triggered.connect(self.refresh_table_view2)
		self.delete_action2.triggered.connect(self.handle_click2)
		self.clear_action2.triggered.connect(self.clear2)

	def clear2(self):
		self.string_list2 = []
		self.model2.setStringList(self.string_list2)

	def show_context_menu2(self, position):
		menu2 = QMenu(self.listView_2)
		menu2.addAction(self.refresh_action2)
		menu2.addAction(self.delete_action2)
		menu2.addAction(self.clear_action2)
		menu2.exec_(self.listView_2.viewport().mapToGlobal(position))

	def refresh_table_view2(self):
		pass

	def handle_click2(self):  
		selectindex2 = self.listView_2.currentIndex()
		itemmodel2 = self.listView_2.model()
		itemmodel2.removeRow(selectindex2.row())

	def setup_context_menu(self):
		self.listView.setContextMenuPolicy(Qt.CustomContextMenu)
		self.listView.customContextMenuRequested.connect(self.show_context_menu)
		self.refresh_action = QAction("Refresh", self.listView)
		self.delete_action = QAction("Delete Line",self.listView)
		self.clear_action = QAction("Clear All",self.listView)
		self.clear_action.triggered.connect(self.clear)
		self.refresh_action.triggered.connect(self.refresh_table_view)
		self.delete_action.triggered.connect(self.handle_click)

	def clear(self):
		self.string_list = []
		self.model.setStringList(self.string_list)

	def show_context_menu(self, position):
		menu = QMenu(self.listView)
		menu.addAction(self.refresh_action)
		menu.addAction(self.delete_action)
		menu.addAction(self.clear_action)
		menu.exec_(self.listView.viewport().mapToGlobal(position))

	def refresh_table_view(self):
		pass

	def handle_click(self):  
		selectindex = self.listView.currentIndex()
		itemmodel = self.listView.model()
		itemmodel.removeRow(selectindex.row())

	def fileopen(self):
		a = os.path.abspath('.')
		a = a.split("\\")
		a = tuple(a)
		a = '/'.join(a)
		stablepath = a + "/"
		datapath = a + "/resource/initial.sqlite"
		conn = sqlite3.connect(datapath)
		cu = conn.cursor()
		cu.execute("SELECT * FROM pathway")
		result = cu.fetchall()
		cu.close()
		conn.close()
		pathone = list(result[0])
		path = pathone[1]
		file_dialog = QFileDialog()
		if os.path.exists(path):
			file_path, _ = file_dialog.getOpenFileName(self, "Open File", path, "QTUI Files (*.ui);;All Files (*)")
			if file_path:
				savepath = file_path.split("/")
				savepath.pop(-1)
				savepath = "/".join(savepath)
				savepath += "/"
				conn = sqlite3.connect(datapath)
				cu = conn.cursor()
				cu.execute("UPDATE pathway SET LastPath = ? WHERE id = ?",(savepath,1))
				conn.commit()
				cu.close()
				conn.close()
				if file_path in self.string_list:
					pass
				else:
					self.string_list.append(file_path)
					self.model.setStringList(self.string_list)
		else:
			file_path, _ = file_dialog.getOpenFileName(self, "Open File", ".", "QTUI Files (*.ui);;All Files (*)")
			conn = sqlite3.connect(datapath)
			cu = conn.cursor()
			cu.execute("UPDATE pathway SET LastPath = ? WHERE id = ?",(stablepath,1))
			conn.commit()
			cu.close()
			conn.close()
			if file_path:
				if os.path.exists(file_path):
					savepath = file_path.split("/")
					savepath.pop(-1)
					savepath = "/".join(savepath)
					savepath += "/"
					conn = sqlite3.connect(datapath)
					cu = conn.cursor()
					cu.execute("UPDATE pathway SET LastPath = ? WHERE id = ?",(savepath,1))
					conn.commit()
					cu.close()
					conn.close()
					if file_path in self.string_list:
						pass
					else:
						self.string_list.append(file_path)
						self.model.setStringList(self.string_list)

	def openfolder(self):
		a = os.path.abspath('.')
		a = a.split("\\")
		a = tuple(a)
		a = '/'.join(a)
		stablepath = a + "/"
		datapath = a + "/resource/initial.sqlite"
		conn = sqlite3.connect(datapath)
		cu = conn.cursor()
		cu.execute("SELECT * FROM pathway2")
		result = cu.fetchall()
		cu.close()
		conn.close()
		pathone = list(result[0])
		path = pathone[1]
		options = QFileDialog.Options()
		file_dialog = QFileDialog()
		if os.path.exists(path):
			file_path = file_dialog.getExistingDirectory(self, "Select Folder", path, options=options)
			if file_path:
				savepath = file_path.split("/")
				savepath.pop(-1)
				savepath = "/".join(savepath)
				savepath += "/"
				conn = sqlite3.connect(datapath)
				cu = conn.cursor()
				cu.execute("UPDATE pathway2 SET LastPath = ? WHERE id = ?",(savepath,1))
				conn.commit()
				cu.close()
				conn.close()
				for root, dirs, files in os.walk(file_path):
					for file in files:
						root = root.replace("\\","/")
						text = root + "/" + file
						if text[-1] == "i" and text[-2] == "u" and text[-3] == ".":
							if text in self.string_list:
								pass
							else:
								self.string_list.append(text)
								self.model.setStringList(self.string_list)
		else:
			file_path = file_dialog.getExistingDirectory(self, "Select Folder", path, options=options)
			conn = sqlite3.connect(datapath)
			cu = conn.cursor()
			cu.execute("UPDATE pathway2 SET LastPath = ? WHERE id = ?",(stablepath,1))
			conn.commit()
			cu.close()
			conn.close()
			if file_path:
				if os.path.exists(file_path):
					savepath = file_path.split("/")
					savepath.pop(-1)
					savepath = "/".join(savepath)
					savepath += "/"
					conn = sqlite3.connect(datapath)
					cu = conn.cursor()
					cu.execute("UPDATE pathway2 SET LastPath = ? WHERE id = ?",(savepath,1))
					conn.commit()
					cu.close()
					conn.close()
					for root, dirs, files in os.walk(file_path):
						for file in files:
							root = root.replace("\\","/")
							text = root + "/" + file
							if text[-1] == "i" and text[-2] == "u" and text[-3] == ".":
								if text in self.string_list:
									pass
								else:
									self.string_list.append(text)
									self.model.setStringList(self.string_list)

	def openfolder2(self):
		a = os.path.abspath('.')
		a = a.split("\\")
		a = tuple(a)
		a = '/'.join(a)
		stablepath = a + "/"
		datapath = a + "/resource/initial.sqlite"
		conn = sqlite3.connect(datapath)
		cu = conn.cursor()
		cu.execute("SELECT * FROM pathway3")
		result = cu.fetchall()
		cu.close()
		conn.close()
		pathone = list(result[0])
		path = pathone[1]
		options = QFileDialog.Options()
		file_dialog = QFileDialog()
		if os.path.exists(path):
			file_path = file_dialog.getExistingDirectory(self, "Select Folder", path, options=options)
			if file_path:
				savepath = file_path.split("/")
				savepath.pop(-1)
				savepath = "/".join(savepath)
				savepath += "/"
				conn = sqlite3.connect(datapath)
				cu = conn.cursor()
				cu.execute("UPDATE pathway3 SET LastPath = ? WHERE id = ?",(savepath,1))
				conn.commit()
				cu.close()
				conn.close()
				file_path += "/"
				self.lineEdit.setText(file_path)

		else:
			file_path = file_dialog.getExistingDirectory(self, "Select Folder", path, options=options)
			conn = sqlite3.connect(datapath)
			cu = conn.cursor()
			cu.execute("UPDATE pathway3 SET LastPath = ? WHERE id = ?",(stablepath,1))
			conn.commit()
			cu.close()
			conn.close()
			if file_path:
				if os.path.exists(file_path):
					savepath = file_path.split("/")
					savepath.pop(-1)
					savepath = "/".join(savepath)
					savepath += "/"
					conn = sqlite3.connect(datapath)
					cu = conn.cursor()
					cu.execute("UPDATE pathway3 SET LastPath = ? WHERE id = ?",(savepath,1))
					conn.commit()
					cu.close()
					conn.close()
					file_path += "/"
					self.lineEdit.setText(file_path)

	def convert(self):
		self.pushButton.setEnabled(False)
		self.pushButton_3.setEnabled(False)
		self.pushButton_4.setEnabled(False)
		self.pushButton_5.setEnabled(False)
		self.lineEdit.setEnabled(False)
		self.listView.setEnabled(False)
		self.listView_2.setEnabled(False)
		step = 100/len(self.string_list)
		num = 0
		for path in self.string_list:
			new_dir = path.split("/")
			file_name = new_dir.pop(-1)
			file_name2 = file_name[0:-3]
			file_name2 += ".py"
			new_dir = tuple(new_dir)
			new_dir = "/".join(new_dir)
			os.chdir(new_dir)
			order = f"pyuic5 {file_name} -o {file_name2}"
			os.system(order)
			if self.lineEdit.text():
				path2 = self.lineEdit.text()
				if os.path.exists(path2):
					source = new_dir + "/" + file_name2
					destination = path2 + file_name2
					shutil.move(source, destination)
					self.string_list2.append(destination)
					self.model2.setStringList(self.string_list2)
				else:
					self.string_list2 = self.string_list
					self.model2.setStringList(self.string_list2)
			else:
				self.string_list2 = self.string_list
				self.model2.setStringList(self.string_list2)
			num += 1
			if num == len(self.string_list):
				self.progressBar.setValue(100)
				self.pushButton_2.setEnabled(True)
			else:
				self.pv += step
				self.pv = int(self.pv)
				self.progressBar.setValue(self.pv)

	def finish(self):
		self.pushButton.setEnabled(True)
		self.pushButton_2.setEnabled(False)
		self.progressBar.setValue(0)
		self.pushButton_3.setEnabled(True)
		self.pushButton_4.setEnabled(True)
		self.pushButton_5.setEnabled(True)
		self.lineEdit.setEnabled(True)
		self.listView.setEnabled(True)
		self.listView_2.setEnabled(True)

if __name__ == "__main__":
	app = QApplication(sys.argv)
	UI2PY = UI2PY()
	UI2PY.show()
	sys.exit(app.exec())