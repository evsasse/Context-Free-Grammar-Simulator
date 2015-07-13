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

		self.ui.btn_verify.clicked.connect(self.btn_verify_clicked)
		self.ui.btn_parser.clicked.connect(self.btn_parser_clicked)

		self.ui.btn_recognize.clicked.connect(self.btn_recognize_clicked)

		self._current_parser = None

	def default_button_behavior(self):
		print("Not implemented!!!")

	def btn_read_clicked(self):
		file = QFileDialog.getOpenFileName(self, 'Ler a gramática de um arquivo')
		with open(file[0]) as f: s = f.read()
		self.ui.text_grammar.setText(s)

	def btn_save_clicked(self):
		file = QFileDialog.getSaveFileName(self, 'Salvar a gramática em um arquivo')
		with open(file[0],'w') as f: s = f.write(self.ui.text_grammar.toPlainText())

	def btn_verify_clicked(self):
		if(self.verify_grammar_ll1()):
			QMessageBox.information(self,'Verificar se a gramática é LL(1)','A gramática é LL(1)!')

	def btn_parser_clicked(self):
		if(self.verify_grammar_ll1()):
			g = Grammar.text_to_grammar(self.ui.text_grammar.toPlainText())
			r = RecursiveDescentParser(g)
			self._current_parser = r
			self.ui.text_parser.setText(r.parser_code().strip().replace('\t','    '))
			QMessageBox.information(self,'Geração do parser descendente recursivo','O parser foi gerado!')

	def btn_recognize_clicked(self):
		if self._current_parser == None:
			QMessageBox.critical(self,'Reconhecimento de sentença','O parser ainda não foi gerado!')
			raise Exception('Reconhecimento de sentença','O parser ainda não foi gerado!')

		try:
			sentence = self.ui.line_sentence.text()
			self._current_parser.parse(sentence)
			QMessageBox.information(self,'Reconhecimento de sentença','A sentença "%s" foi reconhecida!'%(sentence))
		except Exception as err:
			if err.args[0] == 'PARSING' and err.args[1] == '$':
				QMessageBox.critical(self,'Reconhecimento de sentença','A sentença "%s" NÃO foi reconhecida!\n\n'%(sentence)+'O fim do reconhecimento foi alcançado, mas a sentença\nainda não havia acabado. Estava no símbolo "%s"'%(err.args[2]))
				raise Exception('Reconhecimento de sentença','Esperava "$" mas %s foi recebido'%(err.args[2]))
			elif err.args[0] == 'PARSING' and isinstance(err.args[2],list):
				symbols = ('", "'.join(err.args[2]))
				QMessageBox.critical(self,'Reconhecimento de sentença','A sentença "%s" NÃO foi reconhecida!\n\n'%(sentence)+'Durante o não terminal "%s" esperava-se:\n"%s" mas "%s" foi recebido'%(err.args[1],symbols,err.args[3]))
				raise Exception('Reconhecimento de sentença','Durante "%s" esperava-se %s mas "%s" foi recebido'%(err.args[1],symbols,err.args[3]))
			elif err.args[0] == 'PARSING':
				QMessageBox.critical(self,'Reconhecimento de sentença','A sentença "%s" NÃO foi reconhecida!\n\n'%(sentence)+'Durante o não terminal "%s" esperava-se:\n"%s" mas "%s" foi recebido'%(err.args[1],err.args[2],err.args[3]))
				raise Exception('Reconhecimento de sentença','Durante "%s" esperava-se %s mas "%s" foi recebido'%(err.args[1],err.args[2],err.args[3]))

	def verify_grammar_ll1(self):
		try:
			g = Grammar.text_to_grammar(self.ui.text_grammar.toPlainText())
		except Exception:
			QMessageBox.critical(self,'Erro durante criação da gramática','O texto que foi tentado a conversão para gramática não é válido')
			raise Exception('Erro durante criação da gramática','O texto que foi tentado a conversão para gramática não é válido')

		try:
			g.is_ll1()
			return True
		except Exception as err:
			if err.args[0] == 'LEFT_RECURSION':
				nts = ', '.join(err.args[1])
				QMessageBox.critical(self,'Recursão à esquerda','Os seguintes não terminais levam a uma recursão à esquerda:\n\t%s'%(nts))
				raise Exception('Recursão à esquerda','Os seguintes não terminais levam a uma recursão à esquerda: %s'%(nts))
			elif err.args[0] == 'LEFT_FACTORING':
				nts = ', '.join(err.args[1])
				QMessageBox.critical(self,'Fatoração à esquerda','Os seguintes não terminais não estão fatorados à esquerda:\n\t%s'%(nts))
				raise Exception('Fatoração à esquerda','Os seguintes não terminais não estão fatorados à esquerda: %s'%(nts))
			elif err.args[0] == 'FIRST_FOLLOW_CONFLICT':
				nts = ', '.join(err.args[1])
				QMessageBox.critical(self,'Conflito first/follow','Houve conflito entre o first e o follow dos seguintes não terminais:\n\t%s'%(nts))
				raise Exception('Conflito first/follow','Houve conflito entre o first e o follow dos seguintes não terminais: %s'%(nts))
			else:
				QMessageBox.critical(self,'Erro inesperado',err.__repr__())
				raise Exception('Erro inesperado',err.__repr__())

		return True

app = QApplication(sys.argv)
window = GUI()
window.show()
sys.exit(app.exec_())
