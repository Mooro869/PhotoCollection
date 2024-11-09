import sys
from time import sleep
import sqlite3
import config as cfg

from PyQt6 import QtCore, QtWidgets, QtGui, uic
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLabel, QComboBox, QTableWidgetItem


class PhotoCollection(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(cfg.main_window, self)
        self.create_alb.clicked.connect(self.new_alb)

        self.create_tag.triggered.connect(self.cr_tag)
        self.edit_tag.triggered.connect(self.ed_tag)
        self.del_tag.triggered.connect(self.dl_tag)
        self.all_tags.triggered.connect(self.all_tag)

    def cr_tag(self):
        self.tag = New_Tag()
        self.tag.show()

    def ed_tag(self):
        ...

    def dl_tag(self):
        self.tag = Del_Tag()
        self.tag.show()

    def new_alb(self):
        self.alb = New_Album()
        self.alb.show()

    def all_tag(self):
        self.all_tags = All_Tags()
        self.all_tags.show()


class New_Tag(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(cfg.new_tag, self)
        self.new_tag_btn.clicked.connect(self.check_new_tag)

    def check_new_tag(self):
        con = sqlite3.connect(cfg.bd_file)
        cur = con.cursor()
        cur.execute(f"INSERT INTO tags(title_tag) VALUES({self.new_tag_text.text()})")
        con.commit()
        con.close()
        self.close()

        '''
        проверка на существование тэга
        '''


class Del_Tag(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(cfg.del_tag, self)
        self.del_tag_btn.clicked.connect(self.check_del_tag)

    def check_del_tag(self):
        con = sqlite3.connect(cfg.bd_file)
        cur = con.cursor()
        cur.execute(f"DELETE FROM tags WHERE title_tag = '{self.del_tag_text.text()}'")

        # self.statusBar().showMessage(f'{cfg.del_tag_text}')

        con.commit()
        con.close()
        self.close()

    # решить проблему со статусБаром

    '''
    проверка на существования тэга
    '''


class New_Album(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(cfg.new_album, self)
        self.new_alb_btn.clicked.connect(self.check_new_album)

    def check_new_album(self):
        con = sqlite3.connect(cfg.bd_file)
        cur = con.cursor()
        cur.execute(f"INSERT INTO album(title_alb) VALUES('{self.new_alb_text.text()}')")
        con.commit()
        con.close()
        self.close()


class All_Tags(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(cfg.all_tag, self)
    #    self.InitUI()
    #
    # def InitUI(self):
    #     self.tableWidget.itemChanged.connect(self.test)
    #
    #     #self.close()
    #
    # def test(self):
    #     con = sqlite3.connect(cfg.bd_file)
    #     cur = con.cursor()
    #
    #     row = self.tableWidget.rowCount()
    #     self.tableWidget.setItem(row, 0, QTableWidgetItem(cur.execute("SELECT id_tag FROM tags")))
    #     self.tableWidget.setItem(row, 1, QTableWidgetItem(cur.execute("SELECT title_tag FROM tags")))
    #
    #     con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Установка иконки
    icon = QtGui.QIcon(cfg.icon)
    app.setWindowIcon(icon)

    ex = PhotoCollection()
    ex.show()
    sys.exit(app.exec())
