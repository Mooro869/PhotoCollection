import sys
import sqlite3
import config

from PyQt6.QtGui import QPixmap
from PyQt6 import QtGui, uic
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QFormLayout, QFileDialog


class PhotoCollection(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(config.main_window, self)
        self.setFixedSize(1000, 600)

        # Нужно для того чтобы была возможность иметь доступ к statusbar в каждом классе
        global status_bar
        status_bar = self.statusbar

        # Установка изображения в главном окне
        self.pixmap = QPixmap(config.image)
        self.label_img.setPixmap(self.pixmap)

        # Обработка кнопок главного окна
        self.create_alb.clicked.connect(self.new_alb)
        self.update_btn.clicked.connect(self.update_alb)
        self.choose_album.clicked.connect(self.choose_alb)
        self.add_image.clicked.connect(self.add_img)
        self.choose_image.clicked.connect(self.actual)

        # Обработка тегов из menuBar
        self.create_tag_2.triggered.connect(self.cr_tag)
        self.edit_tag_2.triggered.connect(self.ed_tag)
        self.del_tag_2.triggered.connect(self.dl_tag)

        # Обработка альбомов из menuBar
        self.del_album.triggered.connect(self.dl_alb)
        self.edit_album.triggered.connect(self.ed_album)

        # Обработка изображений из menuBar
        self.del_image.triggered.connect(self.dl_image)
        self.edit_image.triggered.connect(self.ed_image)

        # Обработчик экспортов из menuBar
        self.export_txt.triggered.connect(self.exp_txt)

        # Обработчик информации о программе
        self.about.triggered.connect(self.about_text)

    def add_img(self):  # Функция для добавления изображений в выбранный альбом
        self.add = Add_Image()
        self.add.show()

    def cr_tag(self):  # Обработчик создания нового тега
        self.tag = New_Tag()
        self.tag.show()

    def ed_tag(self):  # Обработчик изменения тега
        self.edit_tag = Edit_Tag()
        self.edit_tag.show()

    def dl_tag(self):  # Обработчик удаления тега
        self.tag = Del_Tag()
        self.tag.show()

    def new_alb(self):  # Обработчик создания альбома
        self.new_al = New_Album()
        self.new_al.show()

    def dl_alb(self):  # Обработчик удаления альбомов
        self.dl_al = Del_Album()
        self.dl_al.show()

    def ed_album(self):  # Обработчики изменения альбомов
        self.ed_alb = Edit_Album()
        self.ed_alb.show()

    def dl_image(self):  # Обработчик удаления изображений
        self.dl_img = Del_Image()
        self.dl_img.show()

    def ed_image(self):  # Обработчик изменения изображений
        self.ed_img = Edit_Image()
        self.ed_img.show()

    def choose_alb(self):  # Функция для выбора альбома и обновления comboBox с изображениями
        self.comboBox_image.clear()
        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        result = cur.execute(
            f'SELECT title FROM image WHERE id_album = (SELECT id FROM album WHERE title = "{self.comboBox_album.currentText()}")').fetchall()
        self.comboBox_image.addItems([item[0] for item in result])
        con.close()

    def update_alb(self):  # Функция для обновления интерфейса
        self.comboBox_album.clear()
        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        result = cur.execute('SELECT title FROM album').fetchall()
        self.comboBox_album.addItems([item[0] for item in result])
        con.close()

    @staticmethod
    def write_to_file(data, filename='image.jpg'):  # Функция для преобразования двоичных данных в нужный формат
        with open(filename, 'wb') as file:
            file.write(data)
        return filename

    def actual(self):  # Функция для вывода изображений на главный экран
        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        res = cur.execute(
            f'SELECT file FROM image WHERE title = "{self.comboBox_image.currentText()}"').fetchall()[0][0]
        con.close()
        self.pixmap = QPixmap(self.write_to_file(res))
        scaled_pixmap = self.pixmap.scaled(691, 471)
        self.actual_img.setPixmap(scaled_pixmap)

    def exp_txt(self):
        con = sqlite3.connect(config.bd_file)
        c = con.cursor()
        lst = []
        for row in c.execute('SELECT title FROM album').fetchall():
            lst.append(row)
        print(lst)
        with open("output_info.txt", 'w', encoding='UTF-8') as file:
            for x in lst:
                for n in x:
                    file.write(str(n) + '\n')
        con.close()
        status_bar.showMessage(f'{config.export_txt_text}', 3_000)

    def about_text(self):  # Функция для вывода информации о программе
        self.about = About()
        self.about.show()


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

        check = cur.execute('SELECT title FROM tags WHERE title=?',
                            (self.new_tag_text.text(),)).fetchall()
        if len(check) == 0:
            cur.execute(f"INSERT INTO tags(title) VALUES('{self.new_tag_text.text()}')")
            con.commit()
            con.close()
            self.close()
            status_bar.showMessage(f'{config.new_tag_text}', 3_000)
        else:
            status_bar.showMessage('Ошибка', 3_000)
            con.close()
            self.close()


class Del_Tag(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(config.del_tag, self)
        self.del_tag_btn.clicked.connect(self.check_del_tag)
        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        result = cur.execute('SELECT title FROM tags').fetchall()
        self.comboBox.addItems([item[0] for item in result])
        con.close()

    def check_del_tag(self):
        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        cur.execute(f"DELETE FROM tags WHERE title = '{self.comboBox.currentText()}'").fetchall()
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
        check = cur.execute('SELECT title FROM album WHERE title=?',
                            (self.new_alb_text.text(),)).fetchall()
        if len(check) == 0:
            cur.execute(f"INSERT INTO album(title) VALUES('{self.new_alb_text.text()}')").fetchall()
            con.commit()
            con.close()
            self.close()
            status_bar.showMessage(f'{config.new_album_text}', 3_000)
        else:
            status_bar.showMessage('Ошибка', 3_000)
            con.close()
            self.close()


class Del_Album(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(config.del_album, self)
        self.del_alb_btn.clicked.connect(self.check_del_alb)
        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        result = cur.execute('SELECT title FROM album').fetchall()
        self.comboBox.addItems([item[0] for item in result])
        con.close()

    def check_del_alb(self):
        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        cur.execute(f"DELETE FROM album WHERE title = '{self.comboBox.currentText()}'").fetchall()
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
        result = cur.execute('SELECT title FROM album').fetchall()
        self.comboBox.addItems([item[0] for item in result])
        con.close()

    @staticmethod
    def convertToBinaryData(filename):
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData

    def add(self):
        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        photo = QFileDialog.getOpenFileName(self, 'Выберите изображение', '')[0]
        cur.execute(f"""INSERT INTO image(file, title, id_album) 
                        VALUES (?, '{self.lineEdit.text()}', (SELECT id FROM album WHERE title = 
                        '{self.comboBox.currentText()}'))""", (self.convertToBinaryData(photo),))
        con.commit()
        con.close()
        self.close()
        status_bar.showMessage(f'{config.add_image_text}', 3_000)


class Del_Image(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(config.del_image, self)

        self.update_album.clicked.connect(self.update_alb)
        self.delete_images.clicked.connect(self.delete_img)
        self.update_img.clicked.connect(self.update_images)

        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        result = cur.execute('SELECT title FROM album').fetchall()
        self.comboBox_alb.addItems([item[0] for item in result])
        con.close()

    def update_alb(self):
        self.comboBox_alb.clear()
        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        result = cur.execute('SELECT title FROM album').fetchall()
        self.comboBox_alb.addItems([item[0] for item in result])
        con.close()

    def update_images(self):
        self.comboBox_img.clear()
        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        result = cur.execute(
            f'SELECT title FROM image WHERE id_album = (SELECT id FROM album '
            f'WHERE title = "{self.comboBox_alb.currentText()}")').fetchall()
        self.comboBox_img.addItems([item[0] for item in result])
        con.close()

    def delete_img(self):
        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        cur.execute(f'''
                            DELETE FROM image
                            WHERE id_album = (SELECT id FROM album WHERE title = "{self.comboBox_alb.currentText()}")
                            AND title = "{self.comboBox_img.currentText()}"
                            ''').fetchall()
        con.commit()
        con.close()
        self.close()
        status_bar.showMessage(f'{config.del_image_text}', 3_000)


class Edit_Image(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(config.edit_image, self)

        self.update_album.clicked.connect(self.update_alb)
        self.edit_image.clicked.connect(self.ed_img)
        self.update_img.clicked.connect(self.update_images)

        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        result = cur.execute('SELECT title FROM album').fetchall()
        self.comboBox_alb.addItems([item[0] for item in result])
        con.close()

    def update_alb(self):
        self.comboBox_alb.clear()
        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        result = cur.execute('SELECT title FROM album').fetchall()
        self.comboBox_alb.addItems([item[0] for item in result])
        con.close()

    def update_images(self):
        self.comboBox_img.clear()
        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        result = cur.execute(
            f'SELECT title FROM image WHERE id_album = (SELECT id FROM album '
            f'WHERE title = "{self.comboBox_alb.currentText()}")').fetchall()
        self.comboBox_img.addItems([item[0] for item in result])
        con.close()

    def ed_img(self):
        con = sqlite3.connect(config.bd_file)
        cur = con.cursor()
        cur.execute(f'''
                    UPDATE image
                    SET title = "{self.lineEdit.text()}"
                    WHERE id_album = (SELECT id FROM album WHERE title = "{self.comboBox_alb.currentText()}")
                    AND title = "{self.comboBox_img.currentText()}"
                    ''').fetchall()
        con.commit()
        con.close()
        self.close()
        status_bar.showMessage(f'{config.edit_image_text}', 3_000)


class About(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(config.about_file, self)

        

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Установка иконки
    icon = QtGui.QIcon(config.icon)
    app.setWindowIcon(icon)

    ex = PhotoCollection()
    ex.show()
    sys.exit(app.exec())
