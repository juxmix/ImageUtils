#!/usr/bin/env python3
import logging
import os
import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path
from tkinter import Menu
from tkinter import filedialog as fd
from tkinter import ttk

# create logger
logger = logging.getLogger('MinWindow.py')
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)


class MainWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        master.title("Utilidades de fotos")
        # Tamaño inicial de la ventana
        master.geometry('550x350')

        self.crea_menu(master)

        # Variables
        self.dir_name_var = tk.StringVar()
        self.img_name_var = tk.StringVar()

        self.crea_widgets(master)

    def lst_callback(self, evento):
        seleccion = evento.widget.curselection()
        if seleccion:
            index = seleccion[0]
            nombre = evento.widget.get(index)
            self.img_name_var.set(nombre)
            logger.info("Img: " + nombre)
            fullname = os.path.join(self.dir_name_var.get(), nombre)
            logger.debug("FullName: " + fullname)
            load = Image.open(fullname)
            #load.resize((50, 50), Image.ANTIALIAS)
            load.thumbnail((200, 200))
            render = ImageTk.PhotoImage(load)
            # img = Label(self.master, image = render)
            self.lbl_thumb = tk.Label(self.master, image=render, height=200, width=200)
            self.lbl_thumb.image = render
            self.lbl_thumb.grid(row=2, column=1, sticky='E', padx=2, pady=2)

        else:
            logger.info("Nada seleccionado.")
            self.img_name_var.set(None)

    def crea_widgets(self, master):
        # Controles de carpeta e imagen en un Frame
        self.frm_controls = tk.Frame(master)
        self.lbl_dir = tk.Label(self.frm_controls, text='Carpeta: ')
        self.ent_dir = tk.Entry(self.frm_controls, textvariable=self.dir_name_var, width=45)
        self.btn_dir = tk.Button(self.frm_controls, text='...', command=self.select_carpeta)
        self.lbl_dir.grid(row=0, column=0, sticky='W', padx=2, pady=2)
        self.ent_dir.grid(row=0, column=1, sticky='W', pady=2)
        self.btn_dir.grid(row=0, column=2, sticky='E', padx=2, pady=2)
        # Controles de Imagen
        self.lbl_img = tk.Label(self.frm_controls, text='Imagen:')
        self.ent_img = tk.Entry(self.frm_controls, textvariable=self.img_name_var, width=45)
        self.btn_img = tk.Button(self.frm_controls, text='...', command=self.select_imagen)
        self.lbl_img.grid(row=1, column=0, sticky='W', padx=2, pady=2)
        self.ent_img.grid(row=1, column=1, sticky='W', padx=2, pady=2)
        self.btn_img.grid(row=1, column=2, sticky='E', padx=2, pady=2)

        self.frm_controls.grid(row=0, column=0, columnspan=2, sticky='W', padx=2, pady=2)

        # Listado de ficheros en su propio panel
        self.frm_lst_images = tk.Frame(self.master)
        self.lst_images = tk.Listbox(self.frm_lst_images, height=10, width=40)#, yscrollcommand=self.scrollbar.set)
        # activestyle='dotbox')
        #self.lst_images.grid(row=2, column=0, columnspan=2, sticky='W', padx=2, pady=2)
        self.lst_images.pack(side=tk.LEFT)#, padx=2, pady=2)
        self.lst_images.bind("<<ListboxSelect>>", self.lst_callback)
        # Crear una barra de deslizamiento con orientación vertical.
        self.scrollbar = ttk.Scrollbar(self.frm_lst_images, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.lst_images.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lst_images.yview)
        #self.scrollbar.grid(row=2, column=2, sticky='E')
        self.frm_lst_images.grid(row=2, column=0, sticky='W')


    def crea_menu(self, master):
        # Creamos la barra
        self.barramenu = Menu(master)
        master.config(menu=self.barramenu)

        # Creamos el menu de fichero
        self.menu_fichero = Menu(self.barramenu, tearoff=0)

        self.menu_fichero.add_command(label='Carpeta...',
                                 command=self.select_carpeta)
        self.menu_fichero.add_command(label='Imagen...',
                                 command=self.select_imagen)
        self.menu_fichero.add_separator()

        self.menu_fichero.add_command(label='Salir', command=master.destroy)
        self.barramenu.add_cascade(label='Fichero', menu=self.menu_fichero)

        # Creamos el menu de ayuda
        self.menu_ayuda = Menu(self.barramenu, tearoff=0)
        self.menu_ayuda.add_command(label='Acerca de...', command=self.acerca_de)

        self.barramenu.add_cascade(label='Ayuda', menu=self.menu_ayuda)

    def select_carpeta(self):
        imgdir = fd.askdirectory()
        if imgdir:
            self.dir_name_var.set(imgdir)
            #self.populate_dir_images()
        else:
            print("Carpeta: no seleccionada")
            self.dir_name_var.set("")
        logger.info("New dir: " + self.dir_name_var.get())
        self.populate_dir_images()

    def populate_dir_images(self):
        self.lst_images.delete(0,'end')
        sufijos_imagen = ['.jpg', '.JPG', ".jpeg"]
        for fichero in Path(self.dir_name_var.get()).iterdir():
            if fichero.suffix in sufijos_imagen:
                fich_sin_path = os.path.basename(fichero)
                self.lst_images.insert('end', fich_sin_path)
        # Activar la barra de desplazamiento
        self.lst_images.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lst_images.yview)

    def select_imagen(self):
        logger.info(self.img_name_var.get())
        #TODO: seleccionar una imágen concreta

    def acerca_de(self):
        popup1 = tk.Toplevel(self.master)
        popup1.geometry("400x300")
        popup1.title("Acerca de...")
        tk.Label(popup1, text="(c) by Juxmix", font=('Mistral 18 bold')).place(x=90,y=50)
        #print("(c) by Juxmix")
