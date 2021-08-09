# http://www.bosontreinamentos.com.br/programacao-em-python/leitura-e-gravacao-em-arquivos-com-python/
# https://johnidm.gitbooks.io/compiladores-para-humanos/content/part1/lexical-analysis.html
from tkinter import *
import json
import regex
import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter import ttk

jsonFile = open('palavras.json', 'r')
palavras = json.loads(jsonFile.read())

regex_string = r"""(?smx)
\A
(?P<string>^\".*")
(?P<diretiva>.*$)
"""
regex_inicial = r"""(?smx)
\A
(?>
(?P<printf>^[a-zA-Z0-9_]*\(.*\);$)|
(?P<diretiva>^\#.*$)|
(?P<normal>^.*$)
)*+
"""

regex_analize = r"""(?smx)
\A
(?:
(?>
(?P<numeros>^,?\(?[0-9.]+[,;\)]?$)|
(?P<variavel>^,?\(?[a-zA-Z]+[,;\)]?$)|
(?P<varoufun>^[a-zA-Z][a-zA-Z0-9_]*(\(?.*\))?$)|
(?P<simbolos_especiais>^[.;,():+<>+\-*%={}]?$)|
(?P<simbolos_composto>^..$)
)*+
)
"""
class lexica:
    def __init__(self):
        self.count = 0
        self.linha = 1
        self.lista = []

        janela = Tk()
        janela.title("Janela principal")

        self.ed = Entry(janela)
        self.ed.grid(row=1, column=1, padx=10, pady=10)

        bt1 = Button(janela, width=20, text="Ler Arquivo", bg='#081947', fg='#fff', font=('Times BOLD', 12),command=self.bt_click)
        bt1.grid(row=1, column=2, padx=15, pady=10)
        janela.geometry("1600x1000+100+100")

        self.tv = ttk.Treeview(janela, columns=(1, 2, 3), show='headings', height=35)
        self.tv.column(1, minwidth=0, width=250)
        self.tv.column(2, minwidth=0, width=250)
        self.tv.column(3, minwidth=0, width=250)


        self.tv.heading(1, text="Linha")
        self.tv.heading(2, text="Token")
        self.tv.heading(3, text="Símbolo")

        self.tv.grid(row=7, rowspan=11, columnspan=20, padx=30, pady=10, )

        scrollbar = ttk.Scrollbar(janela, orient=tk.VERTICAL, command=self.tv.yview)
        self.tv.configure(yscroll=scrollbar.set)
        style = ttk.Style()
        # Pick a theme

        # Configure our treeview colors

        style.configure("Treeview",
                        background="#D3D3D3",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#D3D3D3"
                        )
        # Change selected color
        style.map('Treeview',
                  background=[('selected', 'blue')])

        self.tv.tag_configure('oddrow', background="white")
        self.tv.tag_configure('evenrow', background="lightblue")

        scrollbar.grid(row=7, rowspan=11, columnspan=20, sticky='nse')



        janela.mainloop()

    def valor_fl(self,valor):
        try:
            a = float(valor)
            return True
        except:
            return False


    def printff(self):
        self.lista.append([self.linha, ")", "Simbolo especial"])

        self.lista.append([self.linha, ";", "Simbolo especial"])

        
    def printf(self,texto):
        print(texto)
        self.lista.append([self.linha, texto[:6], "palavra reservada"])
        texto = texto[6:]
        self.lista.append([self.linha, texto[:1], "Simbolo especial"])
        texto = texto[1:]

        texto = texto[:-2]

        printfa = regex.match(regex_string, texto)

        texto = printfa.group("string")

        self.lista.append([self.linha, texto[:1], "Simbolo especial"])
        texto = texto[1:]
        texto = texto[:-1]

        self.lista.append([self.linha, texto, "Constante string"])

        self.lista.append([self.linha, '"', "Simbolo especial"])



        self.pp = True
        self.ppl = printfa.group("diretiva")





    def att(self):
        for s in self.lista:
            if self.count % 2 == 0:
                self.tv.insert("", tk.END, values=(s[0],s[1],s[2]), tags=('evenrow',))
            else:
                self.tv.insert("", tk.END, values=(s[0],s[1],s[2]), tags=('',))
            self.count+=1

    def controle_arquivo(self,texto):
        variavel = []
        constante_float = []
        constante_inteira = []
        valor_nao_esperado = False

        for i in texto:
            self.pp = False
            if i != texto[len(texto)-1]:
                i = i[:-1]
            if i == "":
                self.linha +=1
                continue
            dif = True
            while dif:
                if i[0] == " " or i[0] == None:
                    if len(i) > 1:
                        i = i[1:]
                    else:
                        i = ""
                        dif = False

                else:
                    dif = False
            linh_atual = regex.match(regex_inicial, i)



            if type(linh_atual.group("diretiva")) == str:
                self.lista.append([self.linha,linh_atual.group("diretiva"),"Diretiva ignore a linha"])

            elif type(linh_atual.group("printf")) == str:
                self.printf(linh_atual.group("printf"))

            if type(linh_atual.group("normal")) == str or self.pp == True:

                if self.pp == True:
                    linha_quebrada = self.ppl.split(" ")
                else:
                    v = linh_atual.group("normal")
                    linha_quebrada = v.split(" ")

                for j in linha_quebrada:
                    if j != "":


                        lexema = regex.search(regex_analize, j)
                        aux= 0
                        aux1 = 0
                        if type(lexema.group("numeros")) == str:
                            le = lexema.group("numeros")
                            if le[0] == "," or le[0] == "(":
                                self.lista.append([self.linha,le[0],"Simbolo especial"])
                                le = le[1:]
                            if le[len(le)-1] == "," or le[len(le)-1] == ";" or  le[len(le)-1] ==")" :
                                aux = le[len(le)-1]
                                le = le[:-1]
                            if le.isnumeric():
                                self.lista.append([self.linha,le ,"Constante inteira"])
                            elif self.valor_fl(le):
                                self.lista.append([self.linha, le, "Constante float"])
                            if aux != 0:
                                self.lista.append([self.linha, aux, "Simbolo especial"])


                        elif type(lexema.group("variavel")) == str:
                            le = lexema.group("variavel")
                            if le[0] == "," or le[0] == "(":
                                self.lista.append([self.linha, le[0], "Simbolo especial"])
                                le = le[1:]
                            if le[len(le) - 1] == "," or le[len(le) - 1] == ";" or le[len(le) - 1] == ")":
                                aux = le[len(le) - 1]
                                le = le[:-1]
                            if palavras["palavras_reservadas"].__contains__(le):
                                self.lista.append([self.linha,le ,"Palavra_reservada"])
                            else:
                                self.lista.append([self.linha, le, "Identificador"])
                            if aux != 0:
                                self.lista.append([self.linha, aux, "Simbolo especial"])



                        elif type(lexema.group("varoufun")) == str:
                            le = lexema.group("varoufun")
                            if le[0] == ",":
                                self.lista.append([self.linha, le, "Simbolo especial"])
                                le = le[1:]
                            if le[len(le) - 1] == "," or le[len(le) - 1] == ";":
                                aux = le[len(le) - 1]
                                le = le[:-1]
                            if le[len(le) - 2:len(le)] == "()":
                                aux1 = le[len(le) - 2:len(le) - 1]
                                le = le[:-2]

                            if palavras["palavras_reservadas"].__contains__(le):
                                self.lista.append([self.linha, le, "Palavra_reservada"])
                            else:
                                self.lista.append([self.linha, le, "Identificador"])
                            if aux != 0:
                                self.lista.append([self.linha, aux, "Simbolo especial"])

                            if aux1 != 0:
                                self.lista.append([self.linha, "(", "Simbolo especial"])
                                self.lista.append([self.linha, ")", "Simbolo especial"])

                        elif type(lexema.group("simbolos_especiais")) == str:
                            le = lexema.group("simbolos_especiais")
                            if palavras["simbolos_especiais"].__contains__(le):
                                self.lista.append([self.linha, le, "Simbolo especial"])

                        elif type(lexema.group("simbolos_composto")) == str:
                            le = lexema.group("simbolos_composto")
                            if palavras["simbolos_compostos"].__contains__(le):
                                self.lista.append([self.linha, le, "Simbolo especial"])


                if self.pp == True:
                    self.printff()


            self.linha += 1
            if self.linha == 8:
                print()

        self.att()

    def bt_click(self):
        a  = self.ed.get()
        a += ".txt"
        manipulador = open(a, 'r',encoding="utf8")
        arquivo = manipulador.readlines()
        self.controle_arquivo(arquivo)

        manipulador.close()

a = lexica()




