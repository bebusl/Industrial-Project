import sys
from PyQt5.uic import loadUi
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QFileDialog, QProgressBar, QTableWidget, \
    QAbstractItemView, QPushButton, QDesktopWidget, QTableWidgetItem
from transformers import AutoTokenizer
import re
import emoji
from soynlp.normalizer import repeat_normalize

Height = 400
Width = 600

emojis = ''.join(emoji.UNICODE_EMOJI.keys())
pattern = re.compile(f'[^ .,?!/@$%~％·∼()\x00-\x7Fㄱ-ㅣ가-힣{emojis}]+')
url_pattern = re.compile(
    r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')


def clean(x):
    x = pattern.sub(' ', x)
    x = url_pattern.sub('', x)
    x = x.strip()
    x = repeat_normalize(x, num_repeats=2)

    return x


class SelectForm(QDialog):
    def __init__(self):
        super(SelectForm, self).__init__()
        loadUi('select-form.ui', self)
        self.selectFile.clicked.connect(self.select_file_clicked)

    def select_file_clicked(self):
        file_list = QFileDialog.getOpenFileName(self)
        self.open_process_form(file_list[0])

    def open_process_form(self, path):
        process_form = ProcessForm(path)
        widget.addWidget(process_form)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ProcessForm(QDialog):
    POS = 'T-POS'
    NEG = 'T-NEG'
    NEU = 'T-NEU'
    NATURAL = 'O'

    def __init__(self, path):
        super(ProcessForm, self).__init__()
        loadUi('process-form.ui', self)
        self.review_size = 0
        self.reviews = []
        self.original = []
        self.output = []
        self.cur_index = 0
        self.load_file(path)
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(650, 200, 300, 40)
        self.pbar.setMaximum(self.review_size - 1)
        self.pbar.setValue(self.cur_index)
        self.pbar.setFormat("%i/%d" % (self.pbar.value() + 1, self.pbar.maximum() + 1))
        self.tableWidget = QTableWidget(self)
        self.tableWidget.move(50, 50)
        self.tableWidget.resize(1500, 130)
        self.tableWidget.setRowCount(2)
        self.tableWidget.setColumnCount(len(self.reviews[0]))
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.cellClicked.connect(self.__mycell_clicked)
        self.setTableWidgetData()
        prevBtn = QPushButton('Prev', self)
        prevBtn.move(500, 205)
        prevBtn.clicked.connect(self.getPrevReview)
        passBtn = QPushButton('Pass', self)
        passBtn.move(1450, 180)
        passBtn.clicked.connect(self.passReview)
        nextBtn = QPushButton('Next', self)
        nextBtn.move(1000, 205)
        nextBtn.clicked.connect(self.getNextReview)
        saveBtn = QPushButton('Save', self)
        saveBtn.move(1450, 300)
        saveBtn.clicked.connect(self.saveResult)
        self.setWindowTitle('Cap11 LabelingTool')
        self.resize(1600, 350)
        self.center()
        widget.setFixedHeight(350)
        widget.setFixedWidth(1600)


    def __mycell_clicked(self, row, col):
        before = self.output[self.cur_index][col]

        if before == self.NATURAL:
            self.output[self.cur_index][col] = self.POS
        elif before == self.POS:
            self.output[self.cur_index][col] = self.NEG
        else:
            self.output[self.cur_index][col] = self.NATURAL

        self.setTableWidgetData()

    def getNextReview(self):
        self.tableWidget.scrollTo(self.tableWidget.model().index(0, 0))

        self.cur_index += 1

        self.cur_index = self.cur_index % self.review_size
        self.pbar.setFormat("%i/%d" % (self.cur_index + 1, self.pbar.maximum() + 1))
        self.setTableWidgetData()

    def getPrevReview(self):
        self.tableWidget.scrollTo(self.tableWidget.model().index(0, 0))

        self.cur_index -= 1
        self.cur_index = self.cur_index % self.review_size
        self.pbar.setFormat("%i/%d" % (self.cur_index + 1, self.pbar.maximum() + 1))

        self.setTableWidgetData()

    def passReview(self):
        del self.original[self.cur_index]
        del self.reviews[self.cur_index]
        del self.output[self.cur_index]

        self.review_size = len(self.reviews)
        self.pbar.setMaximum(self.review_size - 1)
        self.cur_index = self.cur_index % self.review_size
        self.pbar.setFormat("%i/%d" % (self.cur_index + 1, self.pbar.maximum() + 1))
        self.tableWidget.scrollTo(self.tableWidget.model().index(0, 0))

        self.setTableWidgetData()

    def saveResult(self):
        with open("./output.txt", 'w') as outputFile:
            for i in range(self.cur_index + 1):
                outputFile.write(self.original[i])
                outputFile.write('####')
                for label in range(len(self.output[i])):
                    outputFile.write("%s=%s" % (self.reviews[i][label], self.output[i][label]))
                outputFile.write('\n')

    def setTableWidgetData(self):
        self.tableWidget.setColumnCount(len(self.reviews[self.cur_index]))
        self.pbar.setValue(self.cur_index)

        for idx, word in enumerate(self.reviews[self.cur_index]):
            status = self.output[self.cur_index][idx]
            newItem = QTableWidgetItem(word)
            color = QtCore.Qt.white
            if status == self.NEU:
                color = QtCore.Qt.gray
            elif status == self.POS:
                color = QtCore.Qt.green
            elif status == self.NEG:
                color = QtCore.Qt.red

            newItem.setBackground(color)

            self.tableWidget.setItem(0, idx, newItem)
            self.tableWidget.setItem(1, idx, QTableWidgetItem(status))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

    def load_file(self, path):
        with open(path, 'r', encoding="utf-8-sig") as f:
            for line in f.readlines():
                line = clean(line.replace("\n", ""))
                words = tokenizer.tokenize(line)
                words = [word.replace("#", "") for word in words]
                self.original.append(line)
                self.reviews.append(words)
                self.output.append([self.NATURAL] * len(words))

        self.review_size = len(self.reviews)


tokenizer = AutoTokenizer.from_pretrained("./bert/")
app = QApplication(sys.argv)
select_form = SelectForm()

widget = QStackedWidget()
widget.addWidget(select_form)
widget.setFixedHeight(Height)
widget.setFixedWidth(Width)
widget.show()

sys.exit(app.exec_())

