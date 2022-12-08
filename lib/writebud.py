import re
from tkinter import *
from tkinter import ttk
from tkinter import filedialog, simpledialog
from tkinter.scrolledtext import ScrolledText
from PIL import Image
from datetime import datetime
from tkinter  import messagebox
import sys
import googletrans
from googletrans import Translator
from tkinter import font as tkfont
import os
import cv2
from matplotlib import pyplot as plt
import pytesseract
import fitz
import io
import pyperclip as pc
from fpdf import FPDF


#declaraçao do tesseract
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#variáveis gerais
app_width = 960
app_height = 540
cor_fundo = "#24262b"

#declaração das linguagens
language = googletrans.LANGUAGES
languageV = list(language.values())
lang1 = language.keys()

#configurando o básico da janela principal
root = Tk()
root.title("Writebud")
root.iconbitmap("icoico.ico")
root.resizable(0,0)
root.geometry('960x540+0+0')

global msgForUpload
global msgForGenerate
msgForUpload=StringVar()
msgForGenerate=StringVar()

#declaração do frame esquerdo e configuração
left_frame = Frame(root)
left_frame.pack(side='left', fill='y')
left_frame.config(width=400, bg="#303030")
Label(left_frame, text="Boas vindas ao Writebud!", bg="#303030", fg="#ffffff").grid(row=0, column=0, sticky=NW, pady=5, padx=5)

#declaração do frame direito e configuração, com a integração do bloco de notas
right_frame = Frame(root)
right_frame.pack(side="right", fill='both', expand=1)
right_frame.config(width=1000, bg="#4e4e4e")
txt = ScrolledText(right_frame, width=90, height=40)
txt.pack(side='left', fill="both")
txt.config(width=1000, bg="#4e4e4e", fg="#d0d0d0", font=("Consolas", 12))

#declaração de funções especiais 
def ent_fullscreen():   #toggle fullscreen
	root.attributes("-fullscreen", True)

def exit_fullscreen():  #toggle off fullscreen
	root.attributes("-fullscreen", False)

def launchTrans():      #abrindo nova janela (para o tradutor)
	global second
	second = Toplevel()
	second.title("tradutor")
	second.geometry("600x400")
	second.iconbitmap("icoico.ico")
	second.resizable(0,0)

	def label_update(): #update dos comboboxes
		c = combo1.get()
		c1 = combo2.get()
		label1.configure(text=c)
		label2.configure(text=c1)
		second.after(1000, label_update)
	
	def translate_now(): #ferramenta de tradução
		text_=text1.get(1.0, END)
		t1 = Translator()
		trans_text = t1.translate(text_, src=combo1.get(), dest=combo2.get())
		trans_text = trans_text.text

		text2.delete(1.0, END)
		text2.insert(END, trans_text)


	#declaração do primeiro combobox
	combo1 = ttk.Combobox(second, width=10, values=languageV, font=("Roboto 14"), state='r')
	combo1.place(x=50, y=20)
	combo1.set("portuguese")

	label1 = Label(second, text="Portuguese", font=("segoe 10 bold"), bg="white", width=20, bd=5,
		relief=GROOVE)
	label1.place(x=30, y=50)

	f = Frame(second, bg="Black", bd=5)
	f.place(x=10, y=90, width=210+20, height=250)

	text1 = Text(f, font="Arial 15", bg="white", relief=GROOVE, wrap=WORD)
	text1.place(x=0, y=0, width=210, height=240)

	scrollbar1 = Scrollbar(f)
	scrollbar1.pack(side='right', fill='y')

	scrollbar1.configure(command=text1.yview)
	text1.configure(yscrollcommand=scrollbar1.set)

#segundo combobox
	combo2 = ttk.Combobox(second, width=10, values=languageV, font=("Roboto 14"), state='r')
	combo2.place(x=400, y=20)
	combo2.set("Select Language")

	label2 = Label(second, text="English", font=("segoe 10 bold"), bg="white", width=20, bd=5,
		relief=GROOVE)
	label2.place(x=380, y=50)

	g = Frame(second, bg="Black", bd=5)
	g.place(x=358, y=90, width=210+20, height=250)

	text2 = Text(g, font="Arial 15", bg="white", relief=GROOVE, wrap=WORD)
	text2.place(x=0, y=0, width=210, height=240)

	scrollbar2 = Scrollbar(g)
	scrollbar2.pack(side='right', fill='y')

	scrollbar2.configure(command=text2.yview)
	text2.configure(yscrollcommand=scrollbar2.set)

	label_update()

#botão de tradução
	translate_bttn = Button(second, text = "Traduzir", font=('Roboto', 15), 
		activebackground= 'white', cursor='hand2',
		bd=1, width=9, height=2, bg='black', fg='white',command=translate_now)
	translate_bttn.place(x=245, y=60+150)

def showTrans():             #mostrando a janela
	second.deiconify()

def hideTrans():             #escondendo a janela
	second.withdraw()


def launchOCR():
	global thirds
	thirds = Toplevel()
	thirds.title("")
	thirds.iconbitmap("icoico.ico")
	thirds.geometry('500x500')
	width_thirds = 500
	height_thirds = 500
	Label(thirds, wraplength=width_thirds,text="Boas vindas! por favor, aperte o botão abaixo caso já tenha uma imagem com texto.Caso seja de uma área reduzida de texto, recomendamos que, se possível, use 'win(tecla windows)+shift+s' para tirar uma screenshot do texto, e salve-o em algum lugar. O texto irá automaticamente para a área de transferência.").pack()

	def copia_copia():
		cestinha = filedialog.askopenfilename()
		img = Image.open(cestinha)
		ocr_result = pytesseract.image_to_string(img)
		pc.copy(ocr_result)

	opcao1 = Button(thirds, text="Opção 1 - imagem pronta", command=copia_copia).pack()

def showOCR(): #mostra o OCR
	thirds.deiconify()

def hideOCR(): #esconde o OCR
	thirds.withdraw()

#o básico do notepad
def cmdNew():     #file menu New option
    global fileName
    if len(txt.get('1.0', END+'-1c'))>0:
        if messagebox.askyesno("Notepad", "Do you want to save changes?"):
            cmdSave()
        else:
            txt.delete(0.0, END)
    #root.title("Notepad")

def cmdOpen():     #file menu Open option
    fd = filedialog.askopenfile(parent = root, mode = 'r')
    t = fd.read()     #t is the text read through filedialog
    txt.delete(0.0, END)
    txt.insert(0.0, t)
    
def cmdSave():     #file menu Save option
    fd = filedialog.asksaveasfile(mode = 'w', defaultextension = '.txt')
    if fd!= None:
        data = txt.get('1.0', END)
    try:
        fd.write(data)
    except:
        messagebox.showerror(title="Error", message = "Not able to save file!")
     
def cmdSaveAs():     #file menu Save As option
    fd = filedialog.asksaveasfile(mode='w', defaultextension = '.txt')
    t = txt.get(0.0, END)     
    try:
        fd.write(t.rstrip())
    except:
        messagebox.showerror(title="Error", message = "Not able to save file!")

def cmdExit():     #file menu Exit option
    if messagebox.askyesno("Notepad", "Are you sure you want to exit?"):
        root.destroy()

def cmdCut():     #edit menu Cut option
    txt.event_generate("<<Cut>>")

def cmdCopy():     #edit menu Copy option
    txt.event_generate("<<Copy>>")

def cmdPaste():     #edit menu Paste option
    txt.event_generate("<<Paste>>")

def cmdClear():     #edit menu Clear option
    txt.event_generate("<<Clear>>")
       
def cmdFind():     #edit menu Find option
    txt.tag_remove("Found",'1.0', END)
    find = simpledialog.askstring("Find", "Find what:")
    if find:
        idx = '1.0'     #idx stands for index
    while 1:
        idx = txt.search(find, idx, nocase = 1, stopindex = END)
        if not idx:
            break
        lastidx = '%s+%dc' %(idx, len(find))
        txt.tag_add('Found', idx, lastidx)
        idx = lastidx
    txt.tag_config('Found', foreground = 'white', background = 'blue')
    txt.bind("<1>", click)

def click(event):     #handling click event
    txt.tag_config('Found',background='white',foreground='black')

def cmdSelectAll():     #edit menu Select All option
    txt.event_generate("<<SelectAll>>")
    
def cmdTimeDate():     #edit menu Time/Date option
    now = datetime.now()
    # dd/mm/YY H:M:S
    dtString = now.strftime("%d/%m/%Y %H:%M:%S")
    label = messagebox.showinfo("Time/Date", dtString)

def cmdSobre():     #help menu About option
    label = messagebox.showinfo("Sobre o Writebud", "Feito como parte essencial (junto com o Jukebox) para o trabalho de conclusão de curso da UNIPESU - \nAntônio Cláudio Mendonça Moura Rodrigues")

def convertL():
	pdf = FPDF()
	pdf.add_page()
	pdf.set_font("Arial", size=12)
	f = open(fname, "r")
	for x in f:
		pdf.cell(200, 10, txt=x, ln=1, align='L')
	pdf.output("PDFresult/Timbas entertainment.pdf")
	msgForGenerate.set("Text converted to PDF successfully!!!")

def convertC():
	pdf = FPDF()
	pdf.add_page()
	pdf.set_font("Arial", size=12)
	f = open(fname, "r")
	for x in f:
		pdf.cell(200, 10, txt=x, ln=1, align='C')
	pdf.output("PDFresult/Timbas entertainment.pdf")
	msgForGenerate.set("Text converted to PDF successfully!!!")

def convertR():
	pdf = FPDF()
	pdf.add_page()
	pdf.set_font("Arial", size=12)
	f = open(fname, "r")
	for x in f:
		pdf.cell(200, 10, txt=x, ln=1, align='R')
	pdf.output("PDFresult/Timbas entertainment.pdf")
	msgForGenerate.set("Text converted to PDF successfully!!!")

def exportPDF():
	filename = filedialog.askopenfilename(filetypes =[('Text Files', '*.txt')])
	msgForUpload.set("Uploaded:"+filename)
	global fname
	fname=filename

def calling_export():
	global forNOW
	forNOW = Toplevel()
	forNOW.title("exportando!")
	forNOW.geometry('500x500')
	forNOW.iconbitmap("icoico.ico")
	topframe = Frame(forNOW)
	topframe.pack(fill='both', expand=1)
	topframe.configure(width=400, bg="#303030")
	Label(topframe, text="AOBA",textvariable=msgForUpload,font="Consolas 15",bg = "#303030", fg="#ffffff").pack()
	Button(topframe, text='Margem para esquerda', command=convertL, bg="#4d4949", fg="#ffffff", activebackground="#242222", activeforeground="#ffffff", font="consolas 10").pack()
	Button(topframe, text='Margem no centro', command=convertC, bg="#4d4949", fg="#ffffff", activebackground="#242222", activeforeground="#ffffff", font="consolas 10").pack()
	Button(topframe, text='Margem para direita', command=convertR, bg="#4d4949", fg="#ffffff", activebackground="#242222", activeforeground="#ffffff", font="consolas 10").pack()
	Button(topframe,text="Selecione o .txt",command=exportPDF, bg="#4d4949", fg="#ffffff", activebackground="#242222", activeforeground="#ffffff", font="consolas 10").pack()
	Label(topframe,text="Hello",textvariable=msgForGenerate,font="Consolas 15",bg = "#303030", fg="#ffffff").pack()

#botões para controle de tela
fullsc_btn = Button(left_frame, text="fullscreen", command=ent_fullscreen)
fullsc_btn.grid(row=2, column=0, pady=5, sticky=SW)
fullsc_btn.config(bg="#4d4949", fg="#ffffff", activebackground="#242222", activeforeground="#ffffff", font="consolas 10", relief=RAISED)

nosc_btn = Button(left_frame, text="normal", command=exit_fullscreen)
nosc_btn.grid(row=2, column=1, pady=5, sticky=W)
nosc_btn.config(bg="#4d4949", fg="#ffffff", activebackground="#242222", activeforeground="#ffffff", font="consolas 10", relief=RAISED)

#botões para a manipulação do tradutor
btn1 = Button(left_frame, text="Carregar tradutor", command=launchTrans, relief=RAISED)
btn1.grid(row=3, column=0, sticky=W, pady=5)
btn1.config(width=20, bg="#4d4949", fg="#ffffff", activebackground="#242222", activeforeground="#ffffff", font="consolas 10")

btn2 = Button(left_frame, text="Mostrar", command=showTrans, relief=RAISED)
btn2.grid(row=3, column=1, sticky=NW, padx= 5, pady=5)
btn2.config(bg="#4d4949", fg="#ffffff", activebackground="#242222", activeforeground="#ffffff", font="consolas 10")

btn3 = Button(left_frame, text="Esconder", command=hideTrans, relief=RAISED)
btn3.grid(row=3, column=2, sticky=NS, pady=5)
btn3.config(bg="#4d4949", fg="#ffffff", activebackground="#242222", activeforeground="#ffffff", font="consolas 10")

#botões para manipulação do OCR
btn4 = Button(left_frame, text="Carregar OCR", command=launchOCR, relief=RAISED)
btn4.grid(row=4, column=0, sticky=W, pady=5)
btn4.config(width=20, bg="#4d4949", fg="#ffffff", activebackground="#242222", activeforeground="#ffffff", font="consolas 10")

btn5 = Button(left_frame, text="Mostrar", command=showOCR, relief=RAISED)
btn5.grid(row=4, column=1, sticky=NW, padx= 5, pady=5)
btn5.config(bg="#4d4949", fg="#ffffff", activebackground="#242222", activeforeground="#ffffff", font="consolas 10")

btn6 = Button(left_frame, text="Esconder", command=hideOCR, relief=RAISED)
btn6.grid(row=4, column=2, sticky=NS, pady=5)
btn6.config(bg="#4d4949", fg="#ffffff", activebackground="#242222", activeforeground="#ffffff", font="consolas 10")

#botões para o notepad
btn7 = Button(left_frame, text="Novo", command=cmdNew, relief=RAISED)
btn7.grid(row=5, column=0, sticky=W, padx= 5, pady=5)
btn7.config(bg="#4d4949", fg="#ffffff", activebackground="#242222", activeforeground="#ffffff", font="consolas 10")
btn8 = Button(left_frame, text="Abrir...", command=cmdOpen, relief=RAISED)
btn8.grid(row=5, column=1, sticky=NW, padx= 5, pady=5)
btn8.config(bg="#4d4949", fg="#ffffff", activebackground="#242222", activeforeground="#ffffff", font="consolas 10")
btn9 = Button(left_frame, text="Salvar", command=cmdSave, relief=RAISED)
btn9.grid(row=5, column=2, sticky=NS, padx= 5, pady=5)
btn9.config(bg="#4d4949", fg="#ffffff", activebackground="#242222", activeforeground="#ffffff", font="consolas 10")

btn10 = Button(left_frame, text="Salvar como:", command=cmdSaveAs, relief=RAISED)
btn10.grid(row=6, column=0, sticky=W, padx= 5, pady=5)
btn10.config(bg="#4d4949", fg="#ffffff", activebackground="#242222", activeforeground="#ffffff", font="consolas 10")
btn11 = Button(left_frame, text="Sair", command=cmdExit, relief=RAISED)
btn11.grid(row=6, column=1, sticky=NW, padx= 5, pady=5)
btn11.config(bg="#4d4949", fg="#ffffff", activebackground="#242222", activeforeground="#ffffff", font="consolas 10")

btn12 = Button(left_frame, text="Cortar", command=cmdCut, relief=RAISED)
btn12.grid(row=7, column=0, sticky=W, padx= 5, pady=5)
btn12.config(bg="#4d4949", fg="#ffffff", activebackground="#242222", activeforeground="#ffffff", font="consolas 10")
btn13 = Button(left_frame, text="Copiar", command=cmdCopy, relief=RAISED)
btn13.grid(row=7, column=1, sticky=NW, padx= 5, pady=5)
btn13.config(bg="#4d4949", fg="#ffffff", activebackground="#242222", activeforeground="#ffffff", font="consolas 10")
btn14 = Button(left_frame, text="Colar", command=cmdPaste, relief=RAISED)
btn14.grid(row=7, column=2, sticky=NS, padx= 5, pady=5)
btn14.config(bg="#4d4949", fg="#ffffff", activebackground="#242222", activeforeground="#ffffff", font="consolas 10")

btn15 = Button(left_frame, text="Deletar", command=cmdClear, relief=RAISED)
btn15.grid(row=8, column=0, sticky=W, padx= 5, pady=5)
btn15.config(bg="#4d4949", fg="#ffffff", activebackground="#242222", activeforeground="#ffffff", font="consolas 10")
btn16 = Button(left_frame, text="Achar...", command=cmdFind, relief=RAISED)
btn16.grid(row=8, column=1, sticky=NW, padx= 5, pady=5)
btn16.config(bg="#4d4949", fg="#ffffff", activebackground="#242222", activeforeground="#ffffff", font="consolas 10")
btn17 = Button(left_frame, text="Selecionar tudo", command=cmdSelectAll, relief=RAISED)
btn17.grid(row=8, column=2, sticky=NS, pady=5)
btn17.config(bg="#4d4949", fg="#ffffff", activebackground="#242222", activeforeground="#ffffff", font="consolas 10")

btn18 = Button(left_frame, text="Tempo/Hora", command=cmdTimeDate, relief=RAISED)
btn18.grid(row=9, column=0, sticky=W, padx= 5, pady=5)
btn18.config(bg="#4d4949", fg="#ffffff", activebackground="#242222", activeforeground="#ffffff", font="consolas 10")
btn19 = Button(left_frame, text="Sobre!", command=cmdSobre, relief=RAISED)
btn19.grid(row=9, column=1, sticky=NW, padx= 5, pady=5)
btn19.config(bg="#4d4949", fg="#ffffff", activebackground="#242222", activeforeground="#ffffff", font="consolas 10")
btn20 = Button(left_frame, text="Converter para PDF", command=calling_export, relief=RAISED)
btn20.grid(row=9, column=2, sticky=NS, pady=5)
btn20.config(bg="#4d4949", fg="#ffffff", activebackground="#242222", activeforeground="#ffffff", font="consolas 10")

#btn20 = Button(left_frame, text="Ajuda?", command=cmdHelpy, relief=SUNKEN)
#btn20.grid(row=11, column=1, sticky=NS, pady=5)
#btn20.config(bg="#4d4949", fg="#ffffff", activebackground="#242222", activeforeground="#ffffff", font="consolas 10")

root.mainloop()