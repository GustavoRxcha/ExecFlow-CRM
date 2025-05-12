import pyodbc
from tkinter import *
from funcao import *
from cores import *
from dotenv import load_dotenv
import os
from PIL import Image, ImageTk

##############################CONEXÃO-CONEXÃO-CONEXÃO###########################################################

load_dotenv()
central_user = os.getenv("CENTRAL_USER")
central_pass = os.getenv("CENTRAL_PASS")

conn = pyodbc.connect(
                f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                f'SERVER=procfitprod.intra.drogariasnissei.com.br;'
                f'DATABASE=PBS_NISSEI_DADOS;'
                #'Trusted_Connection=yes;'
                f'UID={central_user};'
                f'PWD={central_pass};'
                'Connection Timeout=3;'
            )

##############################CONEXÃO-CONEXÃO-CONEXÃO###########################################################

class Aplicacao(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("ExecFlow-CRM's")
        self.geometry("600x750")
        self.configure(bg=fundo)

        logo = Image.open("EFCRM_logo.png")  # Substitua pelo caminho correto da sua imagem
        logo = logo.resize((620, 130))
        self.logo_tk = ImageTk.PhotoImage(logo)

        # Container principal
        container = Frame(self, bg=fundo)
        container.pack(fill="both", expand=True)
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        self.telas = {}
                                                                                               
        for T in (CadastroCRM,):
            tela = T(container, self)
            self.telas[T] = tela
            tela.grid(row=0, column=0, sticky="nsew")
        
        # Mostra a Home
        self.mostrar_tela(CadastroCRM)
    
    def mostrar_tela(self, tela_class):
        tela = self.telas[tela_class]

        if hasattr(tela, 'atualizar'):
            tela.atualizar()

        tela.tkraise()

##############################CONEXÃO-CONEXÃO-CONEXÃO###########################################################

class CadastroCRM(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=fundo)
        self.controller = controller
    
        self.titulo_consulta = Label(self, text="Robô para cadastro de CRM", bg=fundo, fg=cor_texto, font=("Arial", 20, "bold"))
        self.titulo_consulta.pack(pady=(40,5))

        self.titulo_consulta = Label(self, text="| ExecFlow - Cadastro de CRM |", bg=fundo, fg=botao1, font=("Arial", 10, "bold"))
        self.titulo_consulta.pack(pady=(0,50))

        frame_cr = Frame(self, bg=fundo)
        frame_cr.pack(pady=(5, 0))

        Label(frame_cr, text="Registro CR:", bg=fundo, fg=cor_texto, font=("Arial", 15, "bold")).pack(side=LEFT, padx=(0, 10))

        self.inserir_cr = Entry(frame_cr, fg='grey', width=15, font=("Arial", 15))
        self.inserir_cr.insert(0, 'Informe o CR...')
        self.inserir_cr.bind('<FocusIn>', self.quando_clicar)
        self.inserir_cr.pack(side=LEFT, padx=(0,130))

        self.titulo_consulta = Label(self, text="&", bg=fundo, fg=cor_texto, font=("Arial", 15, "bold"))
        self.titulo_consulta.pack(pady=1)

        frame_uf = Frame(self, bg=fundo)
        frame_uf.pack(pady=(0, 10))

        Label(frame_uf, text="UF:", bg=fundo, fg=cor_texto, font=("Arial", 15, "bold")).pack(side=LEFT, padx=(0, 10))

        self.inserir_uf = Entry(frame_uf, fg='grey', width=15, font=("Arial", 15))
        self.inserir_uf.insert(0, 'Informe a UF...')
        self.inserir_uf.bind('<FocusIn>', self.quando_clicar)
        self.inserir_uf.pack(side=LEFT, padx=(0,42))

        botao_cadastrar_medicos = Button(self, text="Cadastrar", width=15, height=1, bg=botao1, fg="#ffffff", bd=3, relief="ridge", font=("Arial", 16), command=self.efetuar_cadastro)
        botao_cadastrar_medicos.pack(pady=(20,20))
        aplicar_hover(botao_cadastrar_medicos, hover, botao1)

        self.status_cadastro = Label(self, text="", bg=fundo, fg=cor_texto, font=("Arial", 13, "bold"), anchor="center", justify="center")
        self.status_cadastro.pack(pady=5, fill='x')

        Label(self, image=self.controller.logo_tk).pack(pady=(150, 10))

    def efetuar_cadastro(self):
        cr_digitado = self.inserir_cr.get()
        self.inserir_cr.delete(0, END)

        uf_digitado = self.inserir_uf.get()
        self.inserir_uf.delete(0, END)

        if cr_digitado and uf_digitado:
            self.status_cadastro.config(text="")
            status_cadastro_crm = cadastrar_crm(conn, uf_digitado, cr_digitado)
            self.status_cadastro.config(text=status_cadastro_crm, fg=cor_texto)
        else:
            self.status_cadastro.config(text="Preencha os campos corretamente.", fg=vermelho)

    def quando_clicar(self, event):
        if self.inserir_cr.get() == 'Informe o CR...':
            self.inserir_cr.delete(0, END)
            self.inserir_cr.config(fg='black')

        if self.inserir_uf.get() == 'Informe a UF...':
            self.inserir_uf.delete(0, END)
            self.inserir_uf.config(fg='black')

################################################################################################################

app = Aplicacao()
app.mainloop()