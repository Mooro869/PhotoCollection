import sys
from time import sleep
import sqlite3
from PyQt6 import QtGui, uic
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
import config


class PhotoCollection(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(config.main_window, self)

        # Нужно для того чтобы была возможность иметь доступ к statusbar в каждом классе
        global status_bar
        status_bar = None
        status_bar = self.statusbar

        # Обработка кнопок главного окна
        self.create_alb.clicked.connect(self.new_alb)

        # Обработка тегов из menuBar
        self.create_tag_2.triggered.connect(self.cr_tag)
        self.edit_tag_2.triggered.connect(self.ed_tag)
        self.del_tag_2.triggered.connect(self.dl_tag)

        # Обработка альбомов из menuBar

        # # Обработчик экспортов из menuBar
        # self.export_csv.triggered.connect(...)

    '''
    ТЕГИ
    '''

    def cr_tag(self):  # Обработчик создания нового тега
        self.tag = New_Tag()
        self.tag.show()

    def ed_tag(self):  # Обработчик изменения тега
        self.edit_tag = Edit_Tag()
        self.edit_tag.show()

    def dl_tag(self):  # Обработчик удаления тега
        self.tag = Del_Tag()
        self.tag.show()

    '''
    АЛЬБОМЫ
    '''

    def new_alb(self):  # Обработчик создания нового альбома
        self.alb = New_Album()
        self.alb.show()


class New_Tag(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(config.new_tag, self)
        self.new_tag_btn.clicked.connect(self.check_new_tag)

    def check_new_tag(self):
        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        cur.execute(f"INSERT INTO tags(title) VALUES('{self.new_tag_text.text()}')")
        con.commit()
        con.close()
        self.close()
        status_bar.showMessage(f'{config.new_tag_text}', 3_000)

        '''
        проверка на существование тега
        '''


class Del_Tag(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(config.del_tag, self)
        self.del_tag_btn.clicked.connect(self.check_del_tag)

    def check_del_tag(self):
        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        cur.execute(f"DELETE FROM tags WHERE title = '{self.del_tag_text.text()}'")
        con.commit()
        con.close()
        self.close()
        status_bar.showMessage(f'{config.del_tag_text}', 3_000)

    '''
    проверка на существования тега
    '''


class New_Album(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(config.new_album, self)
        self.new_alb_btn.clicked.connect(self.check_new_album)

    def check_new_album(self):
        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        cur.execute(f"INSERT INTO album(title) VALUES('{self.new_alb_text.text()}')")
        con.commit()
        con.close()
        self.close()
        status_bar.showMessage(f'{config.new_album_text}', 3_000)


class Edit_Tag(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(config.edit_tag, self)
        self.pushButton.clicked.connect(self.ok)

        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        result = cur.execute('SELECT title FROM tags').fetchall()
        self.comboBox.addItems([item[0] for item in result])
        con.close()

    def ok(self):
        status_bar.showMessage(f'{config.edit_tag_text}', 3_000)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Установка иконки
    icon = QtGui.QIcon(config.icon)
    app.setWindowIcon(icon)

    ex = PhotoCollection()
    ex.show()
    sys.exit(app.exec())
