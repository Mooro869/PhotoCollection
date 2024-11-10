import sys
from time import sleep
import sqlite3
import config as cfg

from PyQt6 import QtCore, QtWidgets, QtGui, uic
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLabel, QComboBox, QTableWidgetItem, QToolBar



class PhotoCollection(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(cfg.main_window, self)
        self.create_alb.clicked.connect(self.new_alb)

        # Нужно для того чтобы была возможность иметь доступ к statusbar в каждом классе
        global status_bar
        status_bar = None
        status_bar = self.statusbar

        # Обработка тегов из menuBar
        self.create_tag.triggered.connect(self.cr_tag)
        self.edit_tag.triggered.connect(self.ed_tag)
        self.del_tag.triggered.connect(self.dl_tag)
        self.all_tags.triggered.connect(self.all_tag)

        self.edits_tags.triggered.connect(self.alls_tags)

        # # Обработчик экспортов из menuBar
        # self.export_txt.triggered.connect(...)
        # self.export_csv.triggered.connect(...)
        #
        # # !!! ВОЗМОЖНО !!!        # self.export_xml.triggered.connect(...)
        # self.export_json.triggered.connect(...)
        # self.export_xlsx.triggered.connect(...)

    def alls_tags(self):
        self.tags_menu = Tags_Menu()
        self.tags_menu.show()


    def cr_tag(self):  # Обработчик создания нового тега
        self.tag = New_Tag()
        self.tag.show()

    def ed_tag(self):  # Обработчик изменения тега
        ...

    def dl_tag(self):  # Обработчик удаления тега
        self.tag = Del_Tag()
        self.tag.show()


    def new_alb(self):  # Обработчик создания нового альбома
        self.alb = New_Album()
        self.alb.show()

    def all_tag(self):  # Обработчик появления всех тегов
        self.all_tg = All_Tags()
        self.all_tg.show()




class New_Tag(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(cfg.new_tag, self)
        self.new_tag_btn.clicked.connect(self.check_new_tag)

    def check_new_tag(self):
        con = sqlite3.connect(cfg.bd_file)
        cur = con.cursor()
        cur.execute(f"INSERT INTO tags(title) VALUES({self.new_tag_text.text()})")
        con.commit()
        con.close()
        self.close()
        status_bar.showMessage(f'{cfg.new_tag_text}', 3_000)

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
        cur.execute(f"DELETE FROM tags WHERE title = '{self.del_tag_text.text()}'")
        con.commit()
        con.close()
        self.close()
        status_bar.showMessage(f'{cfg.del_tag_text}', 3_000)


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
        cur.execute(f"INSERT INTO album(title) VALUES('{self.new_alb_text.text()}')")
        con.commit()
        con.close()
        self.close()
        status_bar.showMessage(f'{cfg.new_album_text}', 3_000)


class All_Tags(QWidget):
    def __init__(self):
        super().__init__()
        self.win = uic.loadUi(cfg.all_tag, self)
        self.InitUI()

    def InitUI(self):
        self.win.snow()
        # con = sqlite3.connect(cfg.bd_file)
        # cur = con.cursor()
        # result = cur.execute(f'SELECT tags.id, tags.title FROM tags').fetchall()
        # self.tableWiget.setRowCount(len(result))
        # self.tableWiget.setColumnCount(len(result[0]))
        # for i, element in enumerate(result):
        #     for j, value in enumerate(element):
        #         self.tableWiget.setItem(i, j, QTableWidgetItem(str(value)))
        # con.close()

class Tags_Menu(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(cfg.tags_window, self)
        #self.InitUI(self)

        # self.con = sqlite3.connect(cfg.bd_file)
        # cur = self.con.cursor()
        # self.con.close()






if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Установка иконки
    icon = QtGui.QIcon(cfg.icon)
    app.setWindowIcon(icon)

    ex = PhotoCollection()
    ex.show()
    sys.exit(app.exec())
