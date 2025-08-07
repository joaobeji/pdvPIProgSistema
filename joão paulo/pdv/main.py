import conexao_DB as conn

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox


# -------------------------------------------


# --------------- AS FUNÇÕES --------------------

# JOÃO PAULO (FUNÇÕES)
def cadastrarProduto():

    if vFormCadastroProduto.btnAdicionar.text() == "Salvar":
        SalvarProdutoEditado()
        ListarProdutos()
        vFormCadastroProduto.btnAdicionar.setText("Adicionar")
        vFormCadastroProduto.lblTitulo.setText("CADASTRO & LISTA DE PRODUTOS")
    else:
        vCodigo = vFormCadastroProduto.edtCodigo.text()
        vDescricao = vFormCadastroProduto.edtNome.text()
        vPreco = vFormCadastroProduto.edtPreco.text().replace(',', '.')
        vQuantidade = vFormCadastroProduto.edtQuantidade.text().replace(',', '.')
        vCategoria = vFormCadastroProduto.cbCategoria.currentText()
        # vCategoria = vFormCadastroProduto.edtCategoria.text()

        try:

            vCursor = conn.vBanco.cursor()
            vComandoSQL = "INSERT INTO PRODUTOS (codigo, descricao, preco, quantidade, categoria) VALUES (%s, %s, %s, %s, %s)"
            vDados = (str(vCodigo), str(vDescricao), str(vPreco), str(vQuantidade), str(vCategoria)) 
            vCursor.execute(vComandoSQL, vDados)
            conn.vBanco.commit()

            QtWidgets.QMessageBox.information(vFormCadastroProduto, "Sucesso", "Produto cadastrado com sucesso!")
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
    vFormCadastroProduto.tabelaDados.resizeColumnsToContents() # Ajusta as colunas ao conteúdo
    vFormCadastroProduto.tabelaDados.horizontalHeader().setStretchLastSection(True) # Ajusta a última coluna para ocupar o espaço restante
    vFormCadastroProduto.tabelaDados.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch) # Ajusta todas as colunas para ocupar o espaço disponível

def excluirProduto():
    vLinhaSelecionada = vFormCadastroProduto.tabelaDados.currentRow()  # Obtém a linha selecionada

    if vLinhaSelecionada < 0:
        QtWidgets.QMessageBox.warning(vFormCadastroProduto, "Aviso", "Selecione um produto para excluir.")
        return

    vCodigo = vFormCadastroProduto.tabelaDados.item(vLinhaSelecionada, 0).text()  # Obtém o ID do produto selecionado

    try:
        vCursor = conn.vBanco.cursor()
        vComandoSQL = "DELETE FROM PRODUTOS WHERE codigo = %s"
        vCursor.execute(vComandoSQL, (vCodigo,))
        conn.vBanco.commit()

        QtWidgets.QMessageBox.information(vFormCadastroProduto, "Sucesso", "Produto excluído com sucesso!")
        ListarProdutos()  # Atualiza a lista de produtos após a exclusão

    except conn.Error as erro:
        QtWidgets.QMessageBox.critical(vFormCadastroProduto, "Erro", f"Ocorreu um erro ao excluir o produto: {erro}")

def EditarProduto():
    
    vFormCadastroProduto.btnAdicionar.setText("Salvar")
    print(vFormCadastroProduto.btnAdicionar.text())
    
    vLinhaSelecionada = vFormCadastroProduto.tabelaDados.currentRow()  # Obtém a linha selecionada

    vFormCadastroProduto.lblTitulo.setText(f"Editando produto com código: {vFormCadastroProduto.tabelaDados.item(vLinhaSelecionada, 0).text()}")

    if vLinhaSelecionada < 0:
        QtWidgets.QMessageBox.warning(vFormCadastroProduto, "Aviso", "Selecione um produto para editar.")
        return

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


    try:

        vLinhaSelecionada = vFormCadastroProduto.tabelaDados.currentRow()  # Obtém a linha selecionada

        # Obtém o ID do produto a ser editado
        vCodigoSelecionado = vFormCadastroProduto.tabelaDados.item(vLinhaSelecionada, 0).text()

        vCursor = conn.vBanco.cursor()
        vComandoSQL = "UPDATE PRODUTOS SET codigo = %s, descricao = %s, preco = %s, quantidade = %s, categoria = %s WHERE codigo = %s"
        vDados = (str(vCodigo), str(vDescricao), str(vPreco), str(vQuantidade), str(vCategoria), str(vCodigoSelecionado))
        vCursor.execute(vComandoSQL, vDados)
        conn.vBanco.commit()

        QtWidgets.QMessageBox.information(vFormCadastroProduto, "Sucesso", "Produto editado com sucesso!")
        limparEdits()
        vFormCadastroProduto.close()
        vFormCadastroProduto.show()  # Reabre o formulário de listagem
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

    vFormCadastroProduto.tabelaDados.resizeColumnsToContents()
    vFormCadastroProduto.tabelaDados.horizontalHeader().setStretchLastSection(True)
    vFormCadastroProduto.tabelaDados.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)





# EDUARDA & VICTOR (FUNÇÕES)
def ListagemUsuarios():
    vFormCadUsuario.show()
    vFormPedido.close()
    vCursor = conn.vBanco.cursor()
    vComandoSQL = "SELECT * FROM usuario"
    vCursor.execute(vComandoSQL)
    vDadosRetornados = vCursor.fetchall()

    vFormCadUsuario.tabelaDados.setRowCount(len(vDadosRetornados))
    vFormCadUsuario.tabelaDados.setColumnCount(3)

    for linha in range(len(vDadosRetornados)):
        for coluna in range(0,5):
            vFormCadUsuario.tabelaDados.setItem(linha, coluna, QtWidgets.QTableWidgetItem(str(vDadosRetornados[linha][coluna])))

    vFormCadUsuario.tabelaDados.resizeColumnsToContents()
    vFormCadUsuario.tabelaDados.horizontalHeader().setStretchLastSection(True)
    vFormCadUsuario.tabelaDados.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

def cadastroUsuario():

    vCodigoUsuario = vFormCadUsuario.edtCodigo.text()
    vSenha = vFormCadUsuario.edtSenha.text()
    vNome = vFormCadUsuario.edtNome.text()
    vUsuario = vFormCadUsuario.edtUsuario.text()
    
    try:
        vCursor = conn.vBanco.cursor()
        if vCodigoUsuario != "" and vNome != "" and vSenha != "":
            vCursor.execute("INSERT INTO usuario values ('"+vCodigoUsuario+"', '"+vNome+"', '"+vSenha+"','"+vUsuario+"')")
            conn.vBanco.commit()
            QtWidgets.QMessageBox.information(vFormCadUsuario, "Sucesso!", "Usuário cadastrado com sucesso!")
        else:
            QtWidgets.QMessageBox.warning(vFormCadUsuario, "Aviso!", "Todos os campos são obrigatórios.")
            return
    except conn.Error as vERRO:
        QtWidgets.QMessageBox.critical(vFormCadUsuario,"Erro!", f"Erro ao inserir registro no banco de dados: {vERRO}")
        return

def excluirUsuario():
    vLinhaSelecionada = vFormCadUsuario.tabelaDados.currentRow()  # Obtém a linha selecionada

    if vLinhaSelecionada < 0:
        QtWidgets.QMessageBox.warning(vFormCadUsuario, "Aviso", "Selecione um usuario para excluir.")
        return

    vCodigo = vFormCadUsuario.tabelaDados.item(vLinhaSelecionada, 0).text()  # Obtém o ID do produto selecionado

    try:
        vCursor = conn.vBanco.cursor()
        vComandoSQL = "DELETE FROM Usuario WHERE codigo = %s"
        vCursor.execute(vComandoSQL, (vCodigo,))
        conn.vBanco.commit()

        QtWidgets.QMessageBox.information(vFormCadUsuario, "Sucesso", "usuario excluído com sucesso!")
        ListarProdutos()  # Atualiza a lista de produtos após a exclusão

    except conn.Error as erro:
        QtWidgets.QMessageBox.critical(vFormCadUsuario, "Erro", f"Ocorreu um erro ao excluir o usuario: {erro}")

def EditarUsuario():
    
    vFormCadUsuario.btnAdicionar.setText("Salvar")
    print(vFormCadUsuario.btnAdicionar.text())
    
    vLinhaSelecionada = vFormCadUsuario.tabelaDados.currentRow()  # Obtém a linha selecionada

    vFormCadUsuario.lblTitulo.setText(f"Editando Usuario com código: {vFormCadUsuario.tabelaDados.item(vLinhaSelecionada, 0).text()}")

    if vLinhaSelecionada < 0:
        QtWidgets.QMessageBox.warning(vFormCadUsuario, "Aviso", "Selecione um Usuario para editar.")
        return

    vCodigo = vFormCadUsuario.tabelaDados.item(vLinhaSelecionada, 0).text()
    vDescricao = vFormCadUsuario.tabelaDados.item(vLinhaSelecionada, 1).text()
    vPreco = vFormCadUsuario.tabelaDados.item(vLinhaSelecionada, 2).text().replace('R$ ', '').replace(',', '.')
    vQuantidade = vFormCadUsuario.tabelaDados.item(vLinhaSelecionada, 3).text().replace(',', '.')
    vCategoria = vFormCadUsuario.tabelaDados.item(vLinhaSelecionada, 4).text()

    # Preenche os campos do formulário de cadastro com os dados do produto selecionado
    vFormCadUsuario.edtCodigo.setText(vCodigo)
    vFormCadUsuario.edtNome.setText(vDescricao)
    vFormCadUsuario.edtPreco.setText(vPreco)
    vFormCadUsuario.edtQuantidade.setText(vQuantidade)
    vFormCadUsuario.cbCategoria.setCurrentText(vCategoria)

def SalvarUsuarioEditado():
    vCodigo = vFormCadUsuario.edtCodigo.text()
    vDescricao = vFormCadUsuario.edtNome.text()
    vPreco = vFormCadUsuario.edtPreco.text().replace(',', '.')
    vQuantidade = vFormCadUsuario.edtQuantidade.text().replace(',', '.')
    vCategoria = vFormCadUsuario.cbCategoria.currentText()


    try:

        vLinhaSelecionada = vFormCadUsuario.tabelaDados.currentRow()  # Obtém a linha selecionada

        # Obtém o ID do produto a ser editado
        vCodigoSelecionado = vFormCadUsuario.tabelaDados.item(vLinhaSelecionada, 0).text()

        vCursor = conn.vBanco.cursor()
        vComandoSQL = "UPDATE Usuario SET codigo = %s, descricao = %s, preco = %s, quantidade = %s, categoria = %s WHERE codigo = %s"
        vDados = (str(vCodigo), str(vDescricao), str(vPreco), str(vQuantidade), str(vCategoria), str(vCodigoSelecionado))
        vCursor.execute(vComandoSQL, vDados)
        conn.vBanco.commit()

        QtWidgets.QMessageBox.information(vFormCadUsuario, "Sucesso", "Produto editado com sucesso!")
        limparEdits()
        vFormCadUsuario.close()
        vFormCadUsuario.show()  # Reabre o formulário de listagem
        ListarProdutos()  # Atualiza a lista de produtos após a edição

    except conn.Error as erro:
        QtWidgets.QMessageBox.critical(vFormCadUsuario, "Erro", f"Ocorreu um erro ao editar o Usuario: {erro}")

def pesquisarUsuario(): 
    vCodigo = vFormCadUsuario.edtCodigoPesquisar.text()
    vDescricao = vFormCadUsuario.edtNomePesquisar.text()

    vCursor = conn.vBanco.cursor()

    if vCodigo != "":
        vFormCadUsuario.edtNome.setText("")
        vComandoSQL = "SELECT codigo, senha, nome, FROM Usuario WHERE CODIGO LIKE %s"
        vCursor.execute(vComandoSQL, ('%' + vCodigo + '%',))
    elif vDescricao != "":
        vFormCadUsuario.edtCodigoPesquisar.setText("")
        vComandoSQL = "SELECT codigo, senha, nome, FROM Usuario WHERE DESCRICAO LIKE %s"
        vCursor.execute(vComandoSQL, ('%' + vDescricao + '%',))
    else:
        ListarProdutos()
        return  
    
    vDadosRetornados = vCursor.fetchall()

    vFormCadUsuario.tabelaDados.setRowCount(len(vDadosRetornados))
    vFormCadUsuario.tabelaDados.setColumnCount(5)
    
    for linha in range(len(vDadosRetornados)):
        for coluna in range(0, 5):
            vFormCadUsuario.tabelaDados.setItem(linha, coluna, QtWidgets.QTableWidgetItem(str(vDadosRetornados[linha][coluna])))

    vFormCadUsuario.tabelaDados.resizeColumnsToContents()
    vFormCadUsuario.tabelaDados.horizontalHeader().setStretchLastSection(True)
    vFormCadUsuario.tabelaDados.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)


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
            print(senha_usuario)
            print(nome_usuario)

            if senha == senha_usuario:
                limparEdits()
                vFormLogin.close()
                vFormCadUsuario.show()
                ListarProdutos()
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

def criarMenu():
    # QtWidgets.QMenu
    pass
  



# ----------- FUNÇÕES COMUNS -------------------
def limparEdits():   
    vFormLogin.edtNome.setText("")
    vFormLogin.edtSenha.setText("")
    vFormCadUsuario.edtCodigo.setText("")
    vFormCadUsuario.edtNome.setText("")  
    vFormCadUsuario.edtSenha.setText("")  
    vFormCadUsuario.edtNomePesquisar.setText("")  
    vFormCadUsuario.edtCodigoPesquisar.setText("")  

    vFormLogin.edtNome.setText("")
    vFormLogin.edtSenha.setText("")

    vFormCadUsuario.edtCodigo.setText("")
    vFormCadUsuario.edtNome.setText("")  
    vFormCadUsuario.edtSenha.setText("")  
    vFormCadUsuario.edtNomePesquisar.setText("")  
    vFormCadUsuario.edtCodigoPesquisar.setText("")  
    vFormCadastroProduto.cbCategoria.setCurrentText("Categorias")  # Reseta o combobox para o valor padrão





# --------------- OS EVENTOS --------------------
vApp = QtWidgets.QApplication([])
vFormLogin = uic.loadUi("tela_login.ui")
vFormPedido = uic.loadUi("telaPedido.ui")
vFormCadUsuario = uic.loadUi("telaCadastroUsuario.ui")
vFormCadastroProduto = uic.loadUi("telaCadastroProduto.ui")



# JOÃO PAULO (CADASTRO & LISTAGEM DE PRODUTOS)
vFormCadastroProduto.btnAdicionar.clicked.connect(cadastrarProduto)
vFormCadastroProduto.btnExcluir.clicked.connect(excluirProduto)
vFormCadastroProduto.btnEditar.clicked.connect(EditarProduto)
vFormCadastroProduto.edtNomePesquisar.textChanged.connect(pesquisarProduto)
vFormCadastroProduto.edtCodigoPesquisar.textChanged.connect(pesquisarProduto)

vFormCadUsuario.btnAdicionar.clicked.connect(cadastrarProduto)

# EDUARDA & VICTOR (CADASTRO & LISTAGEM DE USUÁRIOS)

# KAUÊ & LUCAS (LOGIN NOS SISTEMA CONECTADO COM O BANCO)
vFormLogin.btn_entrar.clicked.connect(realizar_login)

# DEF QMENU
# vFormPedido.icone_menu.clicked.connect(criarMenu)



vFormLogin.show()
vApp.exec()
