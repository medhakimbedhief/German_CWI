import sys
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt, QThread, QObject
from Code.INF import infenrece
class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World", alignment=QtCore.Qt.AlignCenter)
        self.input_box = QtWidgets.QLineEdit("Enter a sentence here")
        self.loading_label = QtWidgets.QLabel("Processing Inference...", alignment=QtCore.Qt.AlignCenter)
        self.loading_spinner = QtWidgets.QProgressBar()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.input_box)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.loading_label)
        self.layout.addWidget(self.loading_spinner)

        # Initially, hide the loading elements
        self.loading_label.hide()
        self.loading_spinner.hide()

        self.button.clicked.connect(self.magic)
        self.input_box.returnPressed.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.loading_label.show()
        #self.loading_spinner.show()

        # Process the inference in the main thread to keep the GUI responsive
        detected_words, old_sentence, new_sentence = infenrece(self.input_box.text())

        result_text = f"Detected Words: {', '.join(detected_words)}\nOld Sentence: {old_sentence}\nNew Sentence: {new_sentence}"

        # Update the GUI
        self.text.setText(result_text)
        self.loading_label.hide()
        self.loading_spinner.hide()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())