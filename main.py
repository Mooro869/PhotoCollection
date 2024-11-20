import sys
from time import sleep
import sqlite3

from PyQt6.QtGui import QPixmap
from PyQt6 import QtGui, uic
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QFormLayout, QFileDialog

import config



class PhotoCollection(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(config.main_window, self)

        # Нужно для того чтобы была возможность иметь доступ к statusbar в каждом классе
        global status_bar
        status_bar = self.statusbar

        # Обработка кнопок главного окна
        self.create_alb.clicked.connect(self.new_alb)
        self.update_btn.clicked.connect(self.update_ui)
        self.choose_album.clicked.connect(self.choose_alb)
        self.add_image.clicked.connect(self.add_img)


        # Обработка тегов из menuBar
        self.create_tag_2.triggered.connect(self.cr_tag)
        self.edit_tag_2.triggered.connect(self.ed_tag)
        self.del_tag_2.triggered.connect(self.dl_tag)

        # Обработка альбомов из menuBar
        self.del_album.triggered.connect(self.dl_alb)
        self.edit_album.triggered.connect(self.ed_album)

        # # Обработчик экспортов из menuBar
        # self.export_csv.triggered.connect(...)

    def cr_tag(self):  # Обработчик создания нового тега
        self.tag = New_Tag()
        self.tag.show()

    def ed_tag(self):  # Обработчик изменения тега
        self.edit_tag = Edit_Tag()
        self.edit_tag.show()

    def dl_tag(self):  # Обработчик удаления тега
        self.tag = Del_Tag()
        self.tag.show()

    def new_alb(self):  # Обработчик создания нового альбома
        self.new_al = New_Album()
        self.new_al.show()

    def dl_alb(self):  # Обработчик удаления альбомов
        self.dl_al = Del_Album()
        self.dl_al.show()

    def ed_album(self):  # Обработчки изменения альбомов
        self.ed_alb = Edit_Album()
        self.ed_alb.show()

    def dl_image(self):  # Обработчик изменения альбомов
        ...

    # Функция для выбора альбома и обновления comboBox с изображениями
    def choose_alb(self):
        ...

    # Функция для добавления изображений в выбранный альбом
    def add_img(self):
        self.add = Add_Image()
        self.add.show()

    # Функция для обновления интерфейса
    def update_ui(self):
        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        result = cur.execute('SELECT title FROM album').fetchall()
        self.comboBox_album.addItems([item[0] for item in result])
        con.close()


'''
ТЕГИ
'''

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
        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        result = cur.execute('SELECT title FROM tags')
        self.comboBox.addItems([item[0] for item in result])
        con.close()

    def check_del_tag(self):
        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        cur.execute(f"DELETE FROM tags WHERE title = '{self.comboBox.currentText()}'")
        con.commit()
        con.close()
        self.close()
        status_bar.showMessage(f'{config.del_tag_text}', 3_000)


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
        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        cur.execute(
                    f"UPDATE tags "
                    f"SET title = '{self.lineEdit.text()}' WHERE title = '{self.comboBox.currentText()}'"
                    )
        con.commit()
        con.close()
        self.close()
        status_bar.showMessage(f'{config.edit_tag_text}', 3_000)


'''
АЛЬБОМЫ
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


class Del_Album(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(config.del_album, self)
        self.del_alb_btn.clicked.connect(self.check_del_alb)
        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        result = cur.execute('SELECT title FROM album')
        self.comboBox.addItems([item[0] for item in result])
        con.close()

    def check_del_alb(self):
        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        cur.execute(f"DELETE FROM album WHERE title = '{self.comboBox.currentText()}'")
        con.commit()
        con.close()
        self.close()
        status_bar.showMessage(f'{config.del_album_text}', 3_000)


class Edit_Album(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(config.edit_album, self)
        self.pushButton.clicked.connect(self.ok)

        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        result = cur.execute('SELECT title FROM album').fetchall()
        self.comboBox.addItems([item[0] for item in result])
        con.close()


    def ok(self):
        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        cur.execute(
                    f"UPDATE album "
                    f"SET title = '{self.lineEdit.text()}' WHERE title = '{self.comboBox.currentText()}'"
                    )
        con.commit()
        con.close()
        self.close()
        status_bar.showMessage(f'{config.edit_album_text}', 3_000)


'''
ИЗОБРАЖЕНИЯ
'''

class Add_Image(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(config.add_image, self)
        self.pushButton.clicked.connect(self.add)
        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        result = cur.execute('SELECT title FROM album')
        self.comboBox.addItems([item[0] for item in result])
        con.close()

    def convertToBinaryData(self, filename):
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData

    def add(self):
        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        photo = QFileDialog.getOpenFileName(self, 'Выберите изображение', '')[0]

        cur.execute(f"""INSERT INTO image(file) 
        VALUES ({(self.convertToBinaryData(photo),)})""")

        con.commit()
        con.close()
        self.close()
        status_bar.showMessage(f'{config.add_image_text}', 3_000)

class Del_Image(QWidget):
    ...

class Edit_Image(QWidget):
    ...

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Установка иконки
    icon = QtGui.QIcon(config.icon)
    app.setWindowIcon(icon)

    ex = PhotoCollection()
    ex.show()
    sys.exit(app.exec())
