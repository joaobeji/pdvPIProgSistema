import conexao_DB as conn
import mysql.connector

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QMenu
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence, QMovie
from PyQt5 import QtCore

import types
import sys

# Manipulação de diretório
import os

# Geração do PDF
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

import PersonalizarComponentes as personaComponentes

Acao = ""
# ----------- FUNÇÕES COMUNS -------------------
# Ajuste larguras fixas nas colunas
def ajustarLargurasColunas():
    # Ajusta as larguras das colunas
    vFormCadastroProduto.tabelaDados.setColumnWidth(0, 100)
    vFormCadastroProduto.tabelaDados.setColumnWidth(1, 397)
    vFormCadastroProduto.tabelaDados.setColumnWidth(2, 100)
    vFormCadastroProduto.tabelaDados.setColumnWidth(3, 125)
    vFormCadastroProduto.tabelaDados.setColumnWidth(4, 200)

    vFormCadUsuario.tabelaDados.setColumnWidth(0, 100)
    vFormCadUsuario.tabelaDados.setColumnWidth(1, 200)
    vFormCadUsuario.tabelaDados.setColumnWidth(2, 437)
    vFormCadUsuario.tabelaDados.setColumnWidth(3, 200)

    vFormPedido.tabelaDados.setColumnWidth(0, 50)
    vFormPedido.tabelaDados.setColumnWidth(1, 241)
    vFormPedido.tabelaDados.setColumnWidth(2, 70)
    vFormPedido.tabelaDados.setColumnWidth(3, 80)
    vFormPedido.tabelaDados.setColumnWidth(4, 80)

def PersonalizarLabels(pSucesso, pSelf):
    if pSucesso == "S":
        pSelf.lblMensagem.setStyleSheet(personaComponentes.LabelSucesso)
    else:
        pSelf.lblMensagem.setStyleSheet(personaComponentes.LabelErro)

def limparEdits():   
    vFormLogin.edtNome.setText("")
    vFormLogin.edtSenha.setText("")

    vFormCadastroProduto.edtCodigo.setText("")
    vFormCadastroProduto.edtNome.setText("")  
    vFormCadastroProduto.edtPreco.setText("")  
    vFormCadastroProduto.edtQuantidade.setText("")   
    vFormCadastroProduto.cbCategoria.setCurrentText("Categorias")  # Reseta o combobox para o valor padrão

    vFormCadUsuario.edtCodigo.setText("")
    vFormCadUsuario.edtUsuario.setText("")
    vFormCadUsuario.edtNome.setText("")
    vFormCadUsuario.edtSenha.setText("")

def limparAposTempo():
    global vTimer 
    vTimer = QTimer()
    vTimer.setSingleShot(True)  
    vTimer.timeout.connect(limparLabel)
    vTimer.start(3000)

def limparLabel():
    vFormCadastroProduto.lblMensagem.setText("")
    vFormCadUsuario.lblMensagem.setText("")
   
def voltarParaTelaAnterior():
    vFormCadastroProduto.close()
    vFormCadUsuario.close()

def preencherTodosCampos(pSelf, pCad):
    global Acao
   
    # PRODUTOS
    if pCad == "P":

        vCodigoProd = pSelf.edtCodigo.text()
        vDescricaoProd = pSelf.edtNome.text()
        vPrecoProd = pSelf.edtPreco.text().replace(',', '.')
        vQuantidadeProd = pSelf.edtQuantidade.text().replace(',', '.')
        vCategoriaProd = pSelf.cbCategoria.currentText()

        if vCodigoProd == "" or vDescricaoProd == "" or vPrecoProd == "" or vQuantidadeProd == "" or vCategoriaProd == "Categorias":
            PersonalizarLabels("E", pSelf)
            pSelf.lblMensagem.setText("Preencha todos os campos obrigatórios!")
            limparAposTempo()
            pSelf.edtCodigo.setFocus()  
            Acao = "Editar"
            return False   
        else: 
            Acao = "Adicionar"
            return True
    elif pCad == "U":   

        # USUÁRIOS
        vCodigoU = vFormCadUsuario.edtCodigo.text()
        vUsuarioU = vFormCadUsuario.edtUsuario.text()
        vNomeU = vFormCadUsuario.edtNome.text()
        vSenhaU = vFormCadUsuario.edtSenha.text()

        if vCodigoU == "" or vUsuarioU == "" or vNomeU == "" or vSenhaU == "":
            PersonalizarLabels("E", pSelf)
            pSelf.lblMensagem.setText("Preencha todos os campos obrigatórios!")
            limparAposTempo()
            pSelf.edtCodigo.setFocus() 
            Acao = "Editar"
            return False   
        else: 
            Acao = "Adicionar"
            return True
    
def conectar_banco():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',
        database='db_pastelaria'
    )

def fecharSistema():
    conn.vBanco.close()
    sys.exit()

def inicia_processo(self):
    self.movie = QMovie("img/spinner.gif")
    self.movie.setScaledSize(QSize(50, 50)) # Define o tamanho do GIF
    self.label_spinner.setMovie(self.movie)

    self.movie.start() # Inicia a animação
    self.label_spinner.show()
    self.movie.start()

    # Inicia o timer com um tempo mínimo de 2 segundos (2000 milissegundos)
    self.timer_espera = QTimer()
    self.timer_espera.singleShot(2000, lambda: finalizar_tarefa(vFormPedido))

def finalizar_tarefa(self):
    self.movie.stop()
    self.label_spinner.hide()
    vFormPedido.label_spinner.setVisible(False)
    resetar_venda(self)   

# --------------- AS FUNÇÕES --------------------

# JOÃO PAULO (FUNÇÃO DE CADASTRO & LISTAGEM DE PRODUTOS)
def cadastrarProduto():

    if vFormCadastroProduto.btnAdicionar.text() == "Salvar":
        SalvarProdutoEditado()
        ListarProdutos()
        if Acao != "Editar":
            vFormCadastroProduto.btnAdicionar.setText("Adicionar")
            vFormCadastroProduto.lblTitulo.setText("CADASTRO & LISTA DE PRODUTOS")
    else:
        vCodigo = vFormCadastroProduto.edtCodigo.text()
        vDescricao = vFormCadastroProduto.edtNome.text()
        vPreco = vFormCadastroProduto.edtPreco.text().replace(',', '.')
        vQuantidade = vFormCadastroProduto.edtQuantidade.text().replace(',', '.')
        vCategoria = vFormCadastroProduto.cbCategoria.currentText()

        # Verifica se todos os campos obrigatórios estão preenchidos
        if not preencherTodosCampos(vFormCadastroProduto, "P"):
            return
        
        try:

            vCursor = conn.vBanco.cursor()
            vComandoSQL = "INSERT INTO PRODUTOS (codigo, descricao, preco, quantidade, categoria) VALUES (%s, %s, %s, %s, %s)"
            vDados = (str(vCodigo), str(vDescricao), str(vPreco), str(vQuantidade), str(vCategoria)) 
            vCursor.execute(vComandoSQL, vDados)
            conn.vBanco.commit()

            PersonalizarLabels("S", vFormCadastroProduto)
            vFormCadastroProduto.lblMensagem.setText("Produto cadastrado com sucesso!")
            limparAposTempo()
            vFormCadastroProduto.edtCodigo.setFocus()  

            ListarProdutos()  # Atualiza a lista de produtos
            limparEdits()

        except conn.Error as erro:
            if "Duplicate entry" in str(erro):
                QtWidgets.QMessageBox.warning(
                    vFormCadastroProduto,
                    "Erro",
                    f"Código {vCodigo} já cadastrado. Por favor, escolha outro código."
                )
            else:
                QtWidgets.QMessageBox.critical(
                    vFormCadastroProduto,
                    "Erro",
                    f"Ocorreu um erro ao cadastrar o produto: {erro}"
                )

def ListarProdutos():

    ajustarLargurasColunas()
    vCursor = conn.vBanco.cursor()
    vComandoSQL = "SELECT codigo, descricao, preco, quantidade, categoria  FROM PRODUTOS"  
    vCursor.execute(vComandoSQL)
    vDadosRetornados = vCursor.fetchall()

    if not vDadosRetornados:
        QtWidgets.QMessageBox.warning(vFormCadastroProduto, "Aviso", "Nenhum produto cadastrado para gerar o PDF.")
        return

    # Preenche a tabela com os dados retornados
    vFormCadastroProduto.tabelaDados.setRowCount(len(vDadosRetornados))  # Define o número de linhas
    vFormCadastroProduto.tabelaDados.setColumnCount(5)  # Define o número de colunas

    for i in range(len(vDadosRetornados)):
        for j in range(0, 5):
            vFormCadastroProduto.tabelaDados.setItem(i, j, QtWidgets.QTableWidgetItem(str(vDadosRetornados[i][j])))
    
    # Assim, a tabela ficará sempre ajustada ao conteúdo e ao tamanho da tela!
    # vFormCadastroProduto.tabelaDados.resizeColumnsToContents() # Ajusta as colunas ao conteúdo
    # vFormCadastroProduto.tabelaDados.horizontalHeader().setStretchLastSection(True) # Ajusta a última coluna para ocupar o espaço restante
    # vFormCadastroProduto.tabelaDados.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch) # Ajusta todas as colunas para ocupar o espaço disponível

def excluirProduto():
    vLinhaSelecionada = vFormCadastroProduto.tabelaDados.currentRow()  # Obtém a linha selecionada

    if vLinhaSelecionada < 0:
        PersonalizarLabels("E", vFormCadastroProduto)
        vFormCadastroProduto.lblMensagem.setText("Selecione um produto para excluir.")
        return

    vCodigo = vFormCadastroProduto.tabelaDados.item(vLinhaSelecionada, 0).text()  # Obtém o ID do produto selecionado

    try:
        vCursor = conn.vBanco.cursor()
        vComandoSQL = "DELETE FROM PRODUTOS WHERE codigo = %s"
        vCursor.execute(vComandoSQL, (vCodigo,))
        conn.vBanco.commit()

        PersonalizarLabels("S", vFormCadastroProduto)
        vFormCadastroProduto.lblMensagem.setText("Produto excluído com sucesso!")
        limparAposTempo()
        vFormCadastroProduto.edtCodigo.setFocus()  # Foca no campo de código
        ListarProdutos()  # Atualiza a lista de produtos após a exclusão

    except conn.Error as erro:
        QtWidgets.QMessageBox.critical(vFormCadastroProduto, "Erro", f"Ocorreu um erro ao excluir o produto: {erro}")

def EditarProduto():
    
    vFormCadastroProduto.btnAdicionar.setText("Salvar")   
    vLinhaSelecionada = vFormCadastroProduto.tabelaDados.currentRow()  # Obtém a linha selecionada

    if vLinhaSelecionada < 0:
        PersonalizarLabels("E", vFormCadastroProduto)
        vFormCadastroProduto.lblMensagem.setText("Selecione um produto para editar.")
        return
    
    vFormCadastroProduto.lblTitulo.setText(f"Editando produto com código: {vFormCadastroProduto.tabelaDados.item(vLinhaSelecionada, 0).text()}")


    vCodigo = vFormCadastroProduto.tabelaDados.item(vLinhaSelecionada, 0).text()
    vDescricao = vFormCadastroProduto.tabelaDados.item(vLinhaSelecionada, 1).text()
    vPreco = vFormCadastroProduto.tabelaDados.item(vLinhaSelecionada, 2).text().replace('R$ ', '').replace(',', '.')
    vQuantidade = vFormCadastroProduto.tabelaDados.item(vLinhaSelecionada, 3).text().replace(',', '.')
    vCategoria = vFormCadastroProduto.tabelaDados.item(vLinhaSelecionada, 4).text()

    # Preenche os campos do formulário de cadastro com os dados do produto selecionado
    vFormCadastroProduto.edtCodigo.setText(vCodigo)
    vFormCadastroProduto.edtNome.setText(vDescricao)
    vFormCadastroProduto.edtPreco.setText(vPreco)
    vFormCadastroProduto.edtQuantidade.setText(vQuantidade)
    vFormCadastroProduto.cbCategoria.setCurrentText(vCategoria)

def SalvarProdutoEditado():
    vCodigo = vFormCadastroProduto.edtCodigo.text()
    vDescricao = vFormCadastroProduto.edtNome.text()
    vPreco = vFormCadastroProduto.edtPreco.text().replace(',', '.')
    vQuantidade = vFormCadastroProduto.edtQuantidade.text().replace(',', '.')
    vCategoria = vFormCadastroProduto.cbCategoria.currentText()

    # Verifica se todos os campos obrigatórios estão preenchidos
    if not preencherTodosCampos(vFormCadastroProduto, "P"):
        return
      
    try:

        vLinhaSelecionada = vFormCadastroProduto.tabelaDados.currentRow()  # Obtém a linha selecionada

        # Obtém o ID do produto a ser editado
        vCodigoSelecionado = vFormCadastroProduto.tabelaDados.item(vLinhaSelecionada, 0).text()

        vCursor = conn.vBanco.cursor()
        vComandoSQL = "UPDATE PRODUTOS SET codigo = %s, descricao = %s, preco = %s, quantidade = %s, categoria = %s WHERE codigo = %s"
        vDados = (str(vCodigo), str(vDescricao), str(vPreco), str(vQuantidade), str(vCategoria), str(vCodigoSelecionado))
        vCursor.execute(vComandoSQL, vDados)
        conn.vBanco.commit()

        PersonalizarLabels("S", vFormCadastroProduto)
        vFormCadastroProduto.lblMensagem.setText("Produto editado com sucesso!")
        
        limparAposTempo()
        limparEdits()

        ListarProdutos()  # Atualiza a lista de produtos após a edição

    except conn.Error as erro:
        QtWidgets.QMessageBox.critical(vFormCadastroProduto, "Erro", f"Ocorreu um erro ao editar o produto: {erro}")

def pesquisarProduto(): 
    vCodigo = vFormCadastroProduto.edtCodigoPesquisar.text()
    vDescricao = vFormCadastroProduto.edtNomePesquisar.text()

    vCursor = conn.vBanco.cursor()

    if vCodigo != "":
        vFormCadastroProduto.edtNome.setText("")
        vComandoSQL = "SELECT codigo, descricao, preco, quantidade, categoria FROM PRODUTOS WHERE CODIGO LIKE %s"
        vCursor.execute(vComandoSQL, ('%' + vCodigo + '%',))
    elif vDescricao != "":
        vFormCadastroProduto.edtCodigoPesquisar.setText("")
        vComandoSQL = "SELECT codigo, descricao, preco, quantidade, categoria FROM PRODUTOS WHERE DESCRICAO LIKE %s"
        vCursor.execute(vComandoSQL, ('%' + vDescricao + '%',))
    else:
        ListarProdutos()
        return  
    
    vDadosRetornados = vCursor.fetchall()

    vFormCadastroProduto.tabelaDados.setRowCount(len(vDadosRetornados))
    vFormCadastroProduto.tabelaDados.setColumnCount(5)
    
    for linha in range(len(vDadosRetornados)):
        for coluna in range(0, 5):
            vFormCadastroProduto.tabelaDados.setItem(linha, coluna, QtWidgets.QTableWidgetItem(str(vDadosRetornados[linha][coluna])))

    # vFormCadastroProduto.tabelaDados.resizeColumnsToContents()
    # vFormCadastroProduto.tabelaDados.horizontalHeader().setStretchLastSection(True)
    # vFormCadastroProduto.tabelaDados.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)



# EDUARDA & VICTOR (FUNÇÃO DE CADASTRO & LISTAGEM DE USUÁRIOS)
def cadastrarUsuario():

    if vFormCadUsuario.btnAdicionar.text() == "Salvar":
        SalvarUsuarioEditado()
        ListarUsuarios()
        if Acao != "Editar":
            vFormCadUsuario.btnAdicionar.setText("Adicionar")
            vFormCadUsuario.lblTitulo.setText("CADASTRO & LISTA DE USUÁRIOS")
    else:
        vCodigo = vFormCadUsuario.edtCodigo.text()
        vUsuario = vFormCadUsuario.edtUsuario.text()
        vSenha = vFormCadUsuario.edtSenha.text()
        vNome = vFormCadUsuario.edtNome.text()

        # Verifica se todos os campos obrigatórios estão preenchidos
        if not preencherTodosCampos(vFormCadUsuario, "U"):  
            return  

        try:

            vCursor = conn.vBanco.cursor()
            vComandoSQL = "INSERT INTO USUARIO (codigo, usuario, nome, senha) VALUES (%s, %s, %s, %s)"
            vDados = (str(vCodigo), str(vUsuario), str(vNome), str(vSenha)) 
            vCursor.execute(vComandoSQL, vDados)
            conn.vBanco.commit()

            PersonalizarLabels("S", vFormCadUsuario)
            vFormCadUsuario.lblMensagem.setText("Usuário cadastrado com sucesso!")
            limparAposTempo()
            vFormCadUsuario.edtCodigo.setFocus()  # Foca no campo de código

            ListarUsuarios()  # Atualiza a lista de produtos
            limparEdits()

        except conn.Error as erro:
            if "Duplicate entry" in str(erro):
                QtWidgets.QMessageBox.warning(
                    vFormCadastroProduto,
                    "Erro",
                    f"Código {vCodigo} já cadastrado. Por favor, escolha outro código."
                )
            else:
                QtWidgets.QMessageBox.critical(
                    vFormCadastroProduto,
                    "Erro",
                    f"Ocorreu um erro ao cadastrar o usuário: {erro}"
                )

def ListarUsuarios():

    ajustarLargurasColunas()
    vCursor = conn.vBanco.cursor()
    vComandoSQL = "SELECT codigo, usuario, nome, senha  from usuario"  
    vCursor.execute(vComandoSQL)
    vDadosRetornados = vCursor.fetchall()

    # Preenche a tabela com os dados retornados
    vFormCadUsuario.tabelaDados.setRowCount(len(vDadosRetornados))  # Define o número de linhas
    vFormCadUsuario.tabelaDados.setColumnCount(4)  # Define o número de colunas

    for i in range(len(vDadosRetornados)):
        for j in range(0, 4):
            vFormCadUsuario.tabelaDados.setItem(i, j, QtWidgets.QTableWidgetItem(str(vDadosRetornados[i][j])))
    
def excluirUsuario():
    vLinhaSelecionada = vFormCadUsuario.tabelaDados.currentRow()  # Obtém a linha selecionada


    if vLinhaSelecionada < 0:
        PersonalizarLabels("E", vFormCadUsuario)
        vFormCadUsuario.lblMensagem.setText("Selecione um usuário para excluir.")
        return

    vCodigo = vFormCadUsuario.tabelaDados.item(vLinhaSelecionada, 0).text()  # Obtém o ID do produto selecionado

    try:
        vCursor = conn.vBanco.cursor()
        vComandoSQL = "DELETE FROM USUARIO WHERE codigo = %s"
        vCursor.execute(vComandoSQL, (vCodigo,))
        conn.vBanco.commit()

        PersonalizarLabels("S", vFormCadUsuario)
        vFormCadUsuario.lblMensagem.setText("Usuário excluído com sucesso!")
        limparAposTempo()   
        vFormCadUsuario.edtCodigo.setFocus()  # Foca no campo de código
        ListarUsuarios()  # Atualiza a lista de produtos após a exclusão

    except conn.Error as erro:
        QtWidgets.QMessageBox.critical(vFormCadUsuario, "Erro", f"Ocorreu um erro ao excluir o usuário: {erro}")

def EditarUsuario():
    
    vFormCadUsuario.btnAdicionar.setText("Salvar")    
    vLinhaSelecionada = vFormCadUsuario.tabelaDados.currentRow()  # Obtém a linha selecionada

    if vLinhaSelecionada < 0:
        PersonalizarLabels("E", vFormCadUsuario)
        vFormCadUsuario.lblMensagem.setText("Selecione um produto para editar.")
        return
    
    vFormCadUsuario.lblTitulo.setText(f"Editando usuário com código: {vFormCadUsuario.tabelaDados.item(vLinhaSelecionada, 0).text()}")

    vCodigo = vFormCadUsuario.tabelaDados.item(vLinhaSelecionada, 0).text()
    vUsuario = vFormCadUsuario.tabelaDados.item(vLinhaSelecionada, 1).text()
    vNome = vFormCadUsuario.tabelaDados.item(vLinhaSelecionada, 2).text()
    vSenha = vFormCadUsuario.tabelaDados.item(vLinhaSelecionada, 3).text()

    # Preenche os campos do formulário de cadastro com os dados do produto selecionado
    vFormCadUsuario.edtCodigo.setText(vCodigo)
    vFormCadUsuario.edtUsuario.setText(vUsuario)
    vFormCadUsuario.edtNome.setText(vNome)
    vFormCadUsuario.edtSenha.setText(vSenha)


def SalvarUsuarioEditado():
    vCodigo = vFormCadUsuario.edtCodigo.text()
    vUsuario = vFormCadUsuario.edtUsuario.text()
    vNome = vFormCadUsuario.edtNome.text().replace(',', '.')
    vSenha = vFormCadUsuario.edtSenha.text().replace(',', '.')

    # Verifica se todos os campos obrigatórios estão preenchidos
    if not preencherTodosCampos(vFormCadUsuario, "U"):  
        return  

    try:

        vLinhaSelecionada = vFormCadUsuario.tabelaDados.currentRow()  # Obtém a linha selecionada

        # Obtém o ID do produto a ser editado
        vCodigoSelecionado = vFormCadUsuario.tabelaDados.item(vLinhaSelecionada, 0).text()

        vCursor = conn.vBanco.cursor()
        vComandoSQL = "UPDATE USUARIO SET codigo = %s, usuario = %s, nome = %s, senha = %s WHERE codigo = %s"
        vDados = (str(vCodigo), str(vUsuario), str(vNome), str(vSenha), str(vCodigoSelecionado))
        vCursor.execute(vComandoSQL, vDados)
        conn.vBanco.commit()

        PersonalizarLabels("S", vFormCadUsuario)
        vFormCadUsuario.lblMensagem.setText("Usuário editado com sucesso!")
        
        limparAposTempo()
        limparEdits()

        ListarProdutos()  # Atualiza a lista de produtos após a edição

    except conn.Error as erro:
        QtWidgets.QMessageBox.critical(vFormCadUsuario, "Erro", f"Ocorreu um erro ao editar o produto: {erro}")

def pesquisarUsuario(): 
    vCodigo = vFormCadastroProduto.edtCodigoPesquisar.text()
    vDescricao = vFormCadastroProduto.edtNomePesquisar.text()

    vCursor = conn.vBanco.cursor()

    if vCodigo != "":
        vFormCadastroProduto.edtNome.setText("")
        vComandoSQL = "SELECT codigo, descricao, preco, quantidade, categoria FROM PRODUTOS WHERE CODIGO LIKE %s"
        vCursor.execute(vComandoSQL, ('%' + vCodigo + '%',))
    elif vDescricao != "":
        vFormCadastroProduto.edtCodigoPesquisar.setText("")
        vComandoSQL = "SELECT codigo, descricao, preco, quantidade, categoria FROM PRODUTOS WHERE DESCRICAO LIKE %s"
        vCursor.execute(vComandoSQL, ('%' + vDescricao + '%',))
    else:
        ListarProdutos()
        return  
    
    vDadosRetornados = vCursor.fetchall()

    vFormCadastroProduto.tabelaDados.setRowCount(len(vDadosRetornados))
    vFormCadastroProduto.tabelaDados.setColumnCount(5)
    
    for linha in range(len(vDadosRetornados)):
        for coluna in range(0, 5):
            vFormCadastroProduto.tabelaDados.setItem(linha, coluna, QtWidgets.QTableWidgetItem(str(vDadosRetornados[linha][coluna])))

    # vFormCadastroProduto.tabelaDados.resizeColumnsToContents()
    # vFormCadastroProduto.tabelaDados.horizontalHeader().setStretchLastSection(True)
    # vFormCadastroProduto.tabelaDados.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)


def criar_menu(botao):
    menu = QMenu(botao)

    # Opções fixas
    opcoes_fixas = [
        ("Cadastrar e Listar de Produtos", lambda: (vFormCadastroProduto.show(), ListarProdutos())),
        ("Cadastrar e Listar de Usuários", lambda: (vFormCadUsuario.show(), ListarUsuarios())),
        ("Finalizar expediente", lambda: (vFormPedido.close()))
    ]

    for nome, acao in opcoes_fixas:
        menu.addAction(nome, acao)
        menu.addSeparator()

    def mostrar_menu():
        pos = botao.mapToGlobal(botao.rect().bottomLeft())
        menu.exec_(pos)

    botao.clicked.connect(mostrar_menu)

# KAUÊ & LUCAS (FUNÇÕES)
def realizar_login():

    usuario = vFormLogin.edtNome.text()
    senha = vFormLogin.edtSenha.text()

    vCursor = conn.vBanco.cursor()

    while True:
        try:

            vCursor.execute("SELECT SENHA, NOME FROM usuario WHERE usuario ='{}'".format(usuario))
            vRetorno = vCursor.fetchall()

            if not vRetorno:
                QMessageBox.warning(vFormLogin, "Erro", f"Usuário {usuario} não cadastrado.")
                # limparAposTempo()
                return

            senha_usuario = vRetorno[0][0]
            nome_usuario = vRetorno[0][1]

            if senha == senha_usuario:
                limparEdits()
                vFormLogin.close()
                vFormPedido.show()
                ajustarLargurasColunas()

                vFormPedido.edtCodigoProduto.setEnabled(False)
                vFormPedido.edtQTD.setEnabled(False)
                break
            else:
                QMessageBox.warning(vFormLogin, "Erro", "senha incorretos.")
                # limparAposTempo()
                return

        except conn.Error as e:
            print(conn.Error) 
            QMessageBox.warning(vFormLogin, "Erro", f"Ocorreu erro ao fazer login: {e}")
            # limparAposTempo()
            return


def adicionar_produto(self, pPreco_unitario):

    vFormPedido.label_spinner.setVisible(False)
    nome = self.lblDescricao.text()
    codigo = vFormPedido.edtCodigoProduto.text()
    quantidade = float(vFormPedido.edtQTD.text())

    total = quantidade * pPreco_unitario
    linha = self.tabelaDados.rowCount()
    self.tabelaDados.insertRow(linha)

    # Coluna 0 – Código (centralizado)
    item_codigo = QTableWidgetItem(str(codigo))
    item_codigo.setTextAlignment(Qt.AlignCenter)
    self.tabelaDados.setItem(linha, 0, item_codigo)

    # Coluna 1 – Nome do produto (esquerda)
    item_nome = QTableWidgetItem(nome)
    item_nome.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    self.tabelaDados.setItem(linha, 1, item_nome)

    # Coluna 2 – Quantidade (centralizado)
    item_qtd = QTableWidgetItem(str(quantidade))
    item_qtd.setTextAlignment(Qt.AlignCenter)
    self.tabelaDados.setItem(linha, 2, item_qtd)

    # Coluna 3 – Preço Unitário (direita)
    item_preco = QTableWidgetItem(f"R$ {pPreco_unitario:.2f}")
    item_preco.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
    self.tabelaDados.setItem(linha, 3, item_preco)

    # Coluna 4 – Total (direita)
    item_total = QTableWidgetItem(f"R$ {total:.2f}")
    item_total.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
    self.tabelaDados.setItem(linha, 4, item_total)

    calcular_total_geral(self)
    atualizar_qtd_itens(self)
    setar_campos(self)

def calcular_total_geral(self):
    total_geral = 0.0
    linhas = self.tabelaDados.rowCount()

    for linha in range(linhas):
        item = self.tabelaDados.item(linha, 4)  # Coluna 4 = Total da linha
        if item is not None:
            texto = item.text().replace('R$', '').replace(',', '.').strip()
            try:
                valor = float(texto)
                total_geral += valor
            except ValueError:
                pass  # Ignora valores inválidos, se houver

    # Exibe o total geral em algum campo do layout (por exemplo, um QLabel)
    self.lblValorProdutos.setText(f"R$ {total_geral:.2f}")

def atualizar_qtd_itens(self):
    total_itens = self.tabelaDados.rowCount()
    self.lblQTDItens.setText(str(total_itens))

def setar_campos(self):
    self.edtCodigoProduto.clear()
    self.edtCodigoProduto.setFocus()
    self.edtQTD.setText("1")  # Define quantidade padrão como 1

def buscar_produto_por_codigo(self):
    codigo = self.edtCodigoProduto.text()

    if codigo.strip() == "": # 
        return

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("SELECT descricao, preco FROM produtos WHERE codigo = %s", (codigo,))
        resultado = cursor.fetchone()
        
        conexao.close()

        if resultado:
            nome, preco = resultado
            self.lblDescricao.setText(nome)
            adicionar_produto(self, preco)  # Adiciona o produto à tabela automaticamente
        else:
            self.lblDescricao.setText("Produto não encontrado")

    except Exception as e:
        print("Erro ao buscar produto:", e)

def iniciar_venda(self):

    vFormPedido.edtCodigoProduto.setEnabled(True)
    vFormPedido.edtQTD.setEnabled(True)

    if self.tabelaDados.rowCount() == 0:

        self.edtCodigoProduto.clear()
        self.edtQTD.setText("1")  # Define quantidade padrão como 1
        self.lblDescricao.setText("")

        self.edtCodigoProduto.setFocus()

        self.tabelaDados.setRowCount(0)  
        self.lblQTDItens.setText("0")
        self.lblDescricao.setText("Venda iniciada...")
    else:
        QtWidgets.QMessageBox.warning(self, "Venda em Andamento", "Finalize a venda atual antes de iniciar uma nova.")

def finalizar_venda(self):

    # Verifica se há produtos na venda
    if self.tabelaDados.rowCount() == 0:
        QtWidgets.QMessageBox.warning(self, "Venda vazia", "Adicione pelo menos um item antes de finalizar a venda.")
        return
    
    vFormPedido.label_spinner.setVisible(True)
    vFormPedido.lblDescricao.setText("Finalizando Venda...")

    vFormPedido.edtCodigoProduto.setEnabled(False)
    vFormPedido.edtQTD.setEnabled(False)

    # Confirmação de finalização
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()

        # 1. Calcular total geral
        total_geral = 0.0
        linhas = self.tabelaDados.rowCount()
        for linha in range(linhas):
            item = self.tabelaDados.item(linha, 4)  # Coluna Total
            if item:
                texto = item.text().replace('R$', '').replace(',', '.').strip()
                try:
                    total_geral += float(texto)
                except ValueError:
                    pass

        # 2. Inserir venda
        data_hora = datetime.now()
        cursor.execute("INSERT INTO vendas (data, total) VALUES (%s, %s)", (data_hora, total_geral))
        venda_id = cursor.lastrowid

        # 3. Inserir itens da venda e atualizar estoque
        for linha in range(linhas):
            codigo = self.tabelaDados.item(linha, 0).text()
            nome = self.tabelaDados.item(linha, 1).text()
            quantidade = float(self.tabelaDados.item(linha, 2).text())
            preco_unitario = float(self.tabelaDados.item(linha, 3).text().replace('R$', '').replace(',', '.').strip())
            total = float(self.tabelaDados.item(linha, 4).text().replace('R$', '').replace(',', '.').strip())

            # Inserir item
            cursor.execute("""
                INSERT INTO itens_venda 
                (venda_id, codigo_produto, nome_produto, quantidade, preco_unitario, total)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (venda_id, codigo, nome, quantidade, preco_unitario, total))


            # Verifica o estoque atual
            cursor.execute("SELECT quantidade FROM produtos WHERE codigo = %s", (codigo,))
            estoque_atual = cursor.fetchone()[0]

            if quantidade > estoque_atual:
                vFormPedido.label_spinner.setVisible(False)
                QtWidgets.QMessageBox.warning(self, "Estoque insuficiente", f"Produto '{nome}' possui apenas {estoque_atual} unidades em estoque.")
                conexao.rollback()
                conexao.close()
                return

            # Atualizar estoque
            cursor.execute("""
                UPDATE produtos
                SET quantidade = quantidade - %s
                WHERE codigo = %s
            """, (quantidade, codigo))

        conexao.commit()
        conexao.close()

        self.label_spinner.hide() 
        inicia_processo(vFormPedido)       

        limparAposTempo()
        gerar_pdf_venda(self, venda_id, total_geral)
        
    except Exception as e:
        vFormPedido.label_spinner.setVisible(False)
        print("Erro ao finalizar venda:", e)
        QtWidgets.QMessageBox.critical(self, "Erro", "Erro ao finalizar a venda.")

def resetar_venda(self):
    # Limpa campos de entrada
    self.edtCodigoProduto.clear()
    self.edtQTD.clear()
  
    # Exibe status do sistema
    self.lblDescricao.setText("CAIXA LIVRE")

    # Limpa a tabela
    self.tabelaDados.setRowCount(0)

    # Reseta totais
    self.lblValorProdutos.setText("R$ 0.00")
    self.lblQTDItens.setText("0")

def gerar_pdf_venda(self, venda_id, total_geral):
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT codigo_produto, nome_produto, quantidade, preco_unitario, total 
            FROM itens_venda 
            WHERE venda_id = %s
        """, (venda_id,))
        itens = cursor.fetchall()
        conexao.close()

        # Cria pasta relatorios/ se ainda não existir
        pasta_relatorios = "relatorios"
        if not os.path.exists(pasta_relatorios):
            os.makedirs(pasta_relatorios)

        # Define caminho do PDF
        nome_arquivo = os.path.join(pasta_relatorios, f"venda_{venda_id}.pdf")

        c = canvas.Canvas(nome_arquivo, pagesize=A4)
        largura, altura = A4
        y = altura - 50

        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Comprovante de Venda - PDV Pastelaria Central")
        y -= 30

        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        c.drawString(400, y, f"Nº Venda: {venda_id}")
        y -= 40

        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Cód")
        c.drawString(100, y, "Descrição")
        c.drawString(300, y, "Qtd")
        c.drawString(350, y, "P. Unit.")
        c.drawString(430, y, "Total")
        y -= 20

        c.setFont("Helvetica", 10)
        for item in itens:
            if y < 100:
                c.showPage()
                y = altura - 50
            codigo, nome, qtd, preco_unitario, total = item
            c.drawString(50, y, str(codigo))
            c.drawString(100, y, nome[:25])
            c.drawString(300, y, str(qtd))
            c.drawString(350, y, f"R$ {preco_unitario:.2f}")
            c.drawString(430, y, f"R$ {total:.2f}")
            y -= 20

        y -= 20
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"Total da Venda: R$ {total_geral:.2f}")

        c.save()

        # QtWidgets.QMessageBox.information(self, "PDF Gerado", f"PDF salvo em: {nome_arquivo}")

    except Exception as e:
        print("Erro ao gerar PDF:", e)
        QtWidgets.QMessageBox.critical(self, "Erro", "Erro ao gerar o PDF.")

def filtrar_eventos(self, obj, event):
    if event.type() == QtCore.QEvent.KeyPress:
        key = event.key()
        if key == Qt.Key_F:
            finalizar_venda(self)
            return True  # Interrompe a propagação da tecla
        elif key == Qt.Key_A:
            adicionar_produto(self)
            return True
    return False

def cancelar_venda(self, motivo="Cancelado manualmente"):

    vFormPedido.label_spinner.setVisible(True)
    vFormPedido.lblDescricao.setText("Cancelando Venda...")

    vFormPedido.edtCodigoProduto.setEnabled(False)
    vFormPedido.edtQTD.setEnabled(False)

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()

        data_hora = datetime.now()
        operador = "Caixa 1"  

        cursor.execute("""
            INSERT INTO vendas_canceladas (data, motivo, operador)
            VALUES (%s, %s, %s)
        """, (data_hora, motivo, operador))

        conexao.commit()
        conexao.close()

        self.label_spinner.hide() 
        inicia_processo(vFormPedido)
         


    except Exception as e:
        print("Erro ao cancelar venda:", e)
        QtWidgets.QMessageBox.critical(self, "Erro", "Erro ao registrar cancelamento.")


def remover_item_selecionado(self):
    linha_selecionada = self.tabelaDados.currentRow()

    if linha_selecionada >= 0:
        self.tabelaDados.removeRow(linha_selecionada)
        calcular_total_geral(self) 
        atualizar_qtd_itens(self) 
        self.edtCodigoProduto.setFocus()


# --------------- OS EVENTOS --------------------
vApp = QtWidgets.QApplication([])
vFormLogin = uic.loadUi("tela_login.ui")
vFormPedido = uic.loadUi("telaPedido.ui")
vFormCadUsuario = uic.loadUi("telaCadastroUsuario.ui")
vFormCadastroProduto = uic.loadUi("telaCadastroProduto.ui")

# filtro de eventos 
vFormPedido.eventFilter = types.MethodType(filtrar_eventos, vFormPedido)
vApp.installEventFilter(vFormPedido)

# JOÃO PAULO (CADASTRO & LISTAGEM DE PRODUTOS)
vFormCadastroProduto.btnAdicionar.clicked.connect(cadastrarProduto)
vFormCadastroProduto.btnExcluir.clicked.connect(excluirProduto)
vFormCadastroProduto.btnEditar.clicked.connect(EditarProduto)
vFormCadastroProduto.edtNomePesquisar.textChanged.connect(pesquisarProduto)
vFormCadastroProduto.edtCodigoPesquisar.textChanged.connect(pesquisarProduto)

# EDUARDA & VICTOR (CADASTRO & LISTAGEM DE USUÁRIOS)
vFormCadUsuario.btnAdicionar.clicked.connect(cadastrarUsuario)
vFormCadUsuario.btnExcluir.clicked.connect(excluirUsuario)
vFormCadUsuario.btnEditar.clicked.connect(EditarUsuario)
vFormCadUsuario.edtNomePesquisar.textChanged.connect(pesquisarUsuario)
vFormCadUsuario.edtCodigoPesquisar.textChanged.connect(pesquisarUsuario)

criar_menu(vFormPedido.lblMenu)

# KAUÊ & LUCAS (LOGIN NOS SISTEMA CONECTADO COM O BANCO)
vFormLogin.btn_entrar.clicked.connect(realizar_login)
vFormPedido.btnFechar.clicked.connect(fecharSistema)

# Remove os controles padrão de minimizar, maximizar e fechar, exceto pelo menu do sistema.
vFormPedido.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)

# --------------- VOLTAR --------------------
vFormCadastroProduto.btnVoltar.clicked.connect(voltarParaTelaAnterior)
vFormCadUsuario.btnVoltar.clicked.connect(voltarParaTelaAnterior)

# --------------- INICIAR VENDA --------------------
vFormPedido.edtCodigoProduto.returnPressed.connect(lambda: buscar_produto_por_codigo(vFormPedido))
vFormPedido.edtQTD.returnPressed.connect(lambda: buscar_produto_por_codigo(vFormPedido))

# Atalho para Iniciar Venda com a tecla I
atalho_a = QShortcut(QKeySequence("A"), vFormPedido)
atalho_a.activated.connect(lambda: iniciar_venda(vFormPedido))

# Atalho para Finalizar Venda com a tecla F
atalho_finalizar = QShortcut(QKeySequence("F"), vFormPedido)
atalho_finalizar.setContext(Qt.ApplicationShortcut) 
atalho_finalizar.activated.connect(lambda: finalizar_venda(vFormPedido))

# Atalho para Cancelar Venda com a tecla Esc
atalho_cancelar = QShortcut(QKeySequence("Esc"), vFormPedido)
atalho_cancelar.setContext(Qt.ApplicationShortcut)
atalho_cancelar.activated.connect(lambda: cancelar_venda(vFormPedido))

# Atalho para Cancelar Venda com a tecla Esc
atalho_remover_item = QShortcut(QKeySequence("E"), vFormPedido)
atalho_remover_item.setContext(Qt.ApplicationShortcut)
atalho_remover_item.activated.connect(lambda: remover_item_selecionado(vFormPedido))



vFormLogin.show()
vApp.exec()
