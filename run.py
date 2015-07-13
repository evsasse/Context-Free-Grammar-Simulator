import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from ui_main import Ui_form_main

from grammar import Grammar
from recursive_descent_parser import RecursiveDescentParser

class GUI(QDialog):
	def __init__(self):
		super(GUI, self).__init__()

		# Set up the user interface from Designer.
		self.ui = Ui_form_main()
		self.ui.setupUi(self)

		# Connect up the buttons.
		self.ui.btn_read.clicked.connect(self.btn_read_clicked)
		self.ui.btn_save.clicked.connect(self.btn_save_clicked)

		self.ui.btn_verify.clicked.connect(self.default_button_behavior)
		self.ui.btn_parser.clicked.connect(self.default_button_behavior)

		self.ui.btn_recognize.clicked.connect(self.default_button_behavior)

	def default_button_behavior(self):
		print("Not implemented!!!")

	def btn_read_clicked(self):
		file = QFileDialog.getOpenFileName(self, 'Ler a gramática de um arquivo')
		with open(file[0]) as f: s = f.read()
		self.ui.text_grammar.setText(s)

	def btn_save_clicked(self):
		file = QFileDialog.getSaveFileName(self, 'Salvar a gramática em um arquivo')
		with open(file[0]) as f: s = f.write(self.ui.text_grammar.toPlainText())

app = QApplication(sys.argv)
window = GUI()
window.show()
sys.exit(app.exec_())
