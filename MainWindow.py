#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter import Menu
import os
from pathlib import Path

class MainWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        master.title("Utilidades de fotos")

        # Tamaño inicial de la ventana
        master.geometry('550x300')

        self.crea_menu(master)

        # Variables
        self.dir_name_var=tk.StringVar()
        self.img_name_var=tk.StringVar()

        self.crea_widgets(master)

    def lst_callback(self, evento):
        seleccion = evento.widget.curselection()
        if seleccion:
            index = seleccion[0]
            nombre = evento.widget.get(index)
            print("nombre: ", nombre)
        else:
            print("Nada seleccionado.")

    def crea_widgets(self, master):
        # Controles de carpeta
        self.lbl_dir = tk.Label(master, text='Carpeta: ')
        self.ent_dir = tk.Entry(master, textvariable=self.dir_name_var, width=45)
        self.btn_dir = tk.Button(master, text='...', command=self.select_carpeta)
        self.lbl_dir.grid(row=0, column=0, sticky='W', padx=2, pady=2)
        self.ent_dir.grid(row=0, column=1, sticky='W', pady=2)
        self.btn_dir.grid(row=0, column=2, sticky='E', padx=2, pady=2)
        # Controles de Imagen
        self.lbl_img = tk.Label(master, text='Imagen:')
        self.ent_img = tk.Entry(master, textvariable=self.img_name_var, width=45)
        self.btn_img = tk.Button(master, text='...', command=self.select_imagen)
        self.lbl_img.grid(row=1, column=0, sticky='W', padx=2, pady=2)
        self.ent_img.grid(row=1, column=1, sticky='W', padx=2, pady=2)
        self.btn_img.grid(row=1, column=2, sticky='E', padx=2, pady=2)
        # Listado de ficheros
        # Crear una barra de deslizamiento con orientación vertical.
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.lst_images = tk.Listbox(master, height=10, width=40, yscrollcommand=self.scrollbar.set)
        # activestyle='dotbox')
        self.scrollbar.config(command=self.lst_images.yview)
        self.lst_images.grid(row=2, column=0, columnspan=2,
                             sticky='W', padx=2, pady=2)
        self.lst_images.bind("<<ListboxSelect>>", self.lst_callback)

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
            self.populate_dir_images()
        else:
            print("Carpeta: no seleccionada")
            #self.dir_name_var.set("")
        self.populate_dir_images()

    def populate_dir_images(self):
        self.lst_images.delete(0,'end')
        sufijos_imagen = ['.jpg', '.JPG']
        for fichero in Path(self.dir_name_var.get()).iterdir():
            if fichero.suffix in sufijos_imagen:
                fich_sin_path = os.path.basename(fichero)
                self.lst_images.insert('end', fich_sin_path)
        # Activar la barra de desplazamiento

    def select_imagen(self):
        print("Imagen: "+self.img_name_var.get())

    def acerca_de(self):
        print("(c) by Juxmix")

'''
if __name__ == "__main__":
    root = tk.Tk()
    myapp = MainWindow(root)
    myapp.mainloop()
'''