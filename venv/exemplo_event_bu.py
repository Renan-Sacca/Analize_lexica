from tkinter import *
from functools import *

def bt_click(botao):
    lb["text"] = botao["text"]

janela = Tk()
janela.title("Janela principal")

bt1 = Button(janela,width=20, text="botao 1")
bt1["command"] = partial(bt_click,bt1)
bt1.place(x=100,y=100)

bt2 = Button(janela,width=20, text="botao 2")
bt2["command"] = partial(bt_click,bt2)
bt2.place(x=150,y=150)

lb = Label(janela,text="Teste")
lb.place(x=100,y=150)
janela.geometry("300x300+100+100")

janela.mainloop()