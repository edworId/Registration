from tkinter import *
from tkinter import ttk
import sqlite3
import os
import pandas as pd
import webbrowser

#PRECISA BAIXAR AS BIBLIOTECAS 
#PIP3 INSTALL OPENPYXL NECESSÁRIO PARA GERAR ARQUIVO EXCEL
#pyinstaller --onefile --noconsole --windowed cadastro.py


#PARA SALVAR ARQUIVOS DIRETO NO DIRETÓRIO DE INTERESSE
#os.chdir('/home/edmundo/Documentos/projetos/cadastro') 
#os.chdir('/home/edmundo/Documentos/projetos/sistema')

root = Tk()
        

class funcs():
    def limpa_tela(self):
        self.Instituto_entry.delete(0, END)
        self.cpf_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.mail_entry.delete(0, END)
        self.cidade_entry.delete(0, END)
        self.estado_entry.delete(0, END)
        self.mat_entry.delete(0, END)
        self.tel_entry.delete(0, END)
    def conecta_bd(self):
        self.conn = sqlite3.connect("alunos.bd")
        self.cursor = self.conn.cursor(); #print("Conectando ao Banco de Dados.. .")
    def desconecta_bd(self):
        self.conn.close(); #print("Desconectado do Banco de Dados")
    def tabs(self):
        self.conecta_bd() 
        ## Criando Tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS alunos(
                nome CHAR(30) NOT NULL,
                cpf CHAR(15) PRIMARY KEY,
                telefone CHAR(12),
                cidade CHAR(30),
                estado CHAR(30),
                mail CHAR(30) NOT NULL,
                mat CHAR(15) NOT NULL,
                Instituto CHAR (10) NOT NULL
            );
        """)

        self.conn.commit(); #print("Banco de Dados Criado!!")
        self.desconecta_bd()
    def variaveis(self):
        self.nome = self.nome_entry.get()
        self.cpf = self.cpf_entry.get()
        self.telefone = self.tel_entry.get()
        self.cidade = self.cidade_entry.get()
        self.estado = self.estado_entry.get()
        self.mail = self.mail_entry.get()
        self.mat = self.mat_entry.get()
        self.Instituto = self.Instituto_entry.get()
    def add_aluno(self):
        self.variaveis()
        self.conecta_bd()

        self.cursor.execute("""INSERT INTO alunos (nome, cpf, telefone, cidade, estado, mail, mat, Instituto) VALUES (?, ?, ?, ?, ?, ?, ?, ?) """, (self.nome, self.cpf, self.telefone, self.cidade, self.estado, self.mail, self.mat, self.Instituto))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()      
    def select_lista(self):
        self.lista.delete(*self.lista.get_children())
        self.conecta_bd()
        lex = self.cursor.execute(""" SELECT nome, cpf, telefone, cidade, estado, mail, mat, Instituto FROM alunos ORDER BY nome; """)
        for i in lex:
            self.lista.insert("", END, values = i)
        self.desconecta_bd()
    def twoclick(self, event):
        self.limpa_tela()
        self.lista.selection()

        for n in self.lista.selection():
            col1, col2, col3, col4, col5, col6, col7, col8 = self.lista.item(n, 'values')
            self.nome_entry.insert(END, col1)
            self.cpf_entry.insert(END, col2)
            self.tel_entry.insert(END, col3)
            self.cidade_entry.insert(END, col4)
            self.estado_entry.insert(END, col5)
            self.mail_entry.insert(END, col6)
            self.mat_entry.insert(END, col7)
            self.Instituto_entry.insert(END, col8)
    def deleta_aluno(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM alunos WHERE cpf = '{}' """.format(self.cpf))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()
    def altera_aluno(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE alunos SET nome = ?, telefone = ?, cidade = ?, estado = ?, mail = ?, mat = ?, Instituto = ? WHERE cpf = '{}' """.format(self.cpf), (self.nome, self.telefone, self.cidade, self.estado, self.mail, self.mat, self.Instituto))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()
    def quit(self): 
        self.root.destroy()
    def ex_dados(self):
        conectar_bd = sqlite3.connect("alunos.bd")
        c = conectar_bd.cursor()
        c.execute("SELECT *, oid FROM alunos")
        alunos_dados = c.fetchall()
        alunos_dados = pd.DataFrame(alunos_dados, columns = ['','nome', 'cpf', 'telefone', 'cidade', 'estado', 'mail', 'mat', 'Instituto'])
        #alunos_dados.to_csv("DADOS_ALUNOS.csv")
        alunos_dados.to_excel("DADOS_ALUNOS.xlsx")

        conectar_bd.commit()
        
        conectar_bd.close()
    def buscar(self):
        self.variaveis()
        self.conecta_bd()
        self.lista.delete(*self.lista.get_children())

        #self.cpf_entry.insert(END, )
        #cpf = self.cpf_entry.get()
        self.cpf = self.cpf_entry.get()
        self.cursor.execute(
            """ SELECT nome, cpf, telefone, cidade, estado, mail, mat, Instituto FROM alunos
            WHERE cpf LIKE '{}' ORDER BY nome ASC """.format(self.cpf))
        buscanome = self.cursor.fetchall()
        for i in buscanome:
            self.lista.insert("", END, values = i)
        self.limpa_tela()
        
        self.desconecta_bd()

    def link1(self):
        webbrowser.open('https://github.com/edworId') # TO OPEN A LINK IN YOUR BROWSER
    
    def link2(self):
            webbrowser.open('https://github.com/edworId/Registration/blob/main/README.md') # TO OPEN A LINK IN YOUR BROWSER



class Application(funcs):
    def __init__(self):
        self.root = root #PRECISA DO ROOT POIS NÃO ESTÁ DENTRO DA CLASSE
        self.tela() #PRECISA CHAMAR ANTES DO LOOP A FUNÇÃO TEAL
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.tabs()
        self.select_lista()
        self.menus()
        root.mainloop() #LOOP TELA
    def tela(self):
        self.root.title("CADASTRO DE ALUNOS") #TITULO
        self.root.configure(background = '#E0FFFF')
        self.root.geometry("720x500") #SETAR TAMANHO INICIAL
        self.root.resizable(True, True) #RESPONSIVIDADE DO TAMANHO DE TELA
        self.root.maxsize(width= 1280, height= 920) #MAXIMO DE TAMANHO
        self.root.minsize(width= 500, height= 300) #MINIMO DE TAMANHO
    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd = 4, bg = '#fffff0', highlightbackground = '#000000', highlightthickness = 0.5)
        self.frame_1.place(relx=0.01, rely=0.01, relwidth=0.98,relheight=0.46)

        self.frame_2 = Frame(self.root, bd = 4, bg = '#fffff0', 
                                highlightbackground = '#000000', highlightthickness = 0.5)
        self.frame_2.place(relx=0.01, rely=0.525, relwidth=0.98,relheight=0.46)
    def widgets_frame1(self):
        ### CRIAÇÃO DO BOTÃO LIMPAR
        self.bt_limpar = Button(self.frame_1, text = "Limpar", bd = 4, bg = "#E6E6FA", fg = "#FF4500", font = ('arial', 10, 'bold'), command = self.limpa_tela)
        self.bt_limpar.place(relx = 0.2, rely = 0.1, relwidth = 0.1, relheight = 0.15)
        
        ### CRIAÇÃO DO BOTÃO BUSCAR
        self.bt_buscar = Button(self.frame_1, text = "Buscar-CPF", bd = 4, bg = "#E6E6FA", fg = "#FF4500", font = ('arial', 10, 'bold'), command = self.buscar)
        self.bt_buscar.place(relx = 0.3, rely = 0.1, relwidth = 0.1, relheight = 0.15)
        
        ### CRIAÇÃO DO BOTÃO NOVO
        self.bt_novo = Button(self.frame_1, text = "Novo", bd = 4, bg = "#E6E6FA", fg = "#FF4500", font = ('arial', 10, 'bold'), command = self.add_aluno)
        self.bt_novo.place(relx = 0.5, rely = 0.1, relwidth = 0.1, relheight = 0.15)
        
        ### CRIAÇÃO DO BOTÃO ALTERAR
        self.bt_alterar = Button(self.frame_1, text = "Alterar", bd = 4, bg = "#E6E6FA", fg = "#FF4500", font = ('arial', 10, 'bold'), command = self.altera_aluno)
        self.bt_alterar.place(relx = 0.6, rely = 0.1, relwidth = 0.1, relheight = 0.15)
        
        ### CRIAÇÃO DO BOTÃO APAGAR
        self.bt_apagar = Button(self.frame_1, text = "Apagar", bd = 4, bg = "#E6E6FA", fg = "#FF4500", font = ('arial', 10, 'bold'), command = self.deleta_aluno)
        self.bt_apagar.place(relx = 0.7, rely = 0.1, relwidth = 0.1, relheight = 0.15)

        ### CRIAÇÃO DO BOTÃO SAIR
        self.bt_sair = Button(self.frame_1, text = "Sair", bd = 4, bg = "#E6E6FA", fg = "#FF4500", font = ('arial', 10, 'bold'), command = self.quit)
        self.bt_sair.place(relx = 0.8, rely = 0.1, relwidth = 0.1, relheight = 0.15)

        ## CRIAÇÃO DA LABEL E ENTRADA DO CPF
        self.lb_cpf = Label(self.frame_1, text = "CPF:", bg = '#fffff0')
        self.lb_cpf.place(relx = 0.07, rely = 0.04, relheight = 0.1)

        self.cpf_entry = Entry(self.frame_1)
        self.cpf_entry.place(relx = 0.02, rely = 0.15, relwidth = 0.15)
        
        ## CRIAÇÃO DA LABEL E ENTRADA DO NOME
        self.lb_nome = Label(self.frame_1, text = "Nome:", bg = '#fffff0')
        self.lb_nome.place(relx = 0.13, rely = 0.35)

        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx = 0.02, rely = 0.45, relwidth = 0.3)

        ## CRIAÇÃO DA LABEL E ENTRADA DO EMAIL
        self.lb_mail = Label(self.frame_1, text = "E-mail:", bg = '#fffff0')
        self.lb_mail.place(relx = 0.51, rely = 0.35)

        self.mail_entry = Entry(self.frame_1)
        self.mail_entry.place(relx = 0.4, rely = 0.45, relwidth = 0.3)
        
        ## CRIAÇÃO DA LABEL E ENTRADA DO TELEFONE
        self.lb_tel = Label(self.frame_1, text = "Telefone:", bg = '#fffff0')
        self.lb_tel.place(relx = 0.8, rely = 0.35)

        self.tel_entry = Entry(self.frame_1)
        self.tel_entry.place(relx = 0.77, rely = 0.45, relwidth = 0.15)
        
        ## CRIAÇÃO DA LABEL E ENTRADA DA CIDADE - ESTADO
        self.lb_cidade = Label(self.frame_1, text = "CIDADE - ESTADO:", bg = '#fffff0')
        self.lb_cidade.place(relx = 0.118, rely = 0.65)

        self.cidade_entry = Entry(self.frame_1)
        self.cidade_entry.place(relx = 0.02, rely = 0.75, relwidth = 0.25)
        
        self.estado_entry = Entry(self.frame_1)
        self.estado_entry.place(relx = 0.27, rely = 0.75, relwidth = 0.14)

        ## CRIAÇÃO DA LABEL E ENTRADA DO INSTITUTO
        self.lb_Instituto = Label(self.frame_1, text = "Instituto (SIGLA):", bg = '#fffff0')
        self.lb_Instituto.place(relx = 0.5, rely = 0.65)

        self.Instituto_entry = Entry(self.frame_1)
        self.Instituto_entry.place(relx = 0.5105, rely = 0.75, relwidth = 0.15)

        ## CRIAÇÃO DA LABEL E ENTRADA DA MATRICULA
        self.lb_mat = Label(self.frame_1, text = "Matrícula:", bg = '#fffff0')
        self.lb_mat.place(relx = 0.797, rely = 0.65)

        self.mat_entry = Entry(self.frame_1)
        self.mat_entry.place(relx = 0.77, rely = 0.75, relwidth = 0.15)

        
    def lista_frame2(self):
        self.lista = ttk.Treeview(self.frame_2, height = 3, column = ("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8"))
        self.lista.heading("#0", text = "")
        self.lista.heading("#1", text = "NOME")
        self.lista.heading("#2", text = "CPF")
        self.lista.heading("#3", text = "TELEFONE")
        self.lista.heading("#4", text = "CIDADE")
        self.lista.heading("#5", text = "ESTADO")
        self.lista.heading("#6", text = "E-MAIL")
        self.lista.heading("#7", text = "MATRICULA")
        self.lista.heading("#8", text = "INSTITUTO")

        self.lista.column("#0", width = 1)
        self.lista.column("#1", width = 63)
        self.lista.column("#2", width = 63)
        self.lista.column("#3", width = 63)
        self.lista.column("#4", width = 63)
        self.lista.column("#5", width = 63)
        self.lista.column("#6", width = 63)
        self.lista.column("#7", width = 63)
        self.lista.column("#8", width = 63)

        self.lista.place(relx = 0.01, rely = 0.01, relwidth = 0.95, relheight = 0.95)

        self.scroolLista = Scrollbar(self.frame_2, orient = 'vertical')
        self.lista.configure(yscroll = self.scroolLista.set)
        self.scroolLista.place(relx = 0.96, rely = 0.1, relwidth = 0.04, relheight = 0.85)
        self.lista.bind("<Double-1>", self.twoclick)
    def menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        file1 = Menu(menubar)
        file2 = Menu(menubar)
        file3 = Menu(menubar) 

        menubar.add_cascade(label = "Opções", menu = file1)
        menubar.add_cascade(label = "Sobre", menu = file2)

        file1.add_command(label = "Limpar Entradas", command = self.limpa_tela)
        file1.add_command(label = "Exportar Dados", command = self.ex_dados)
        file1.add_command(label = "GitHub EdworId", command = self.link1)
        file2.add_command(label = "Readme Project", command = self.link2)


Application()
