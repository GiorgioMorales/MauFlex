# -*- coding: utf-8 -*-
"""
Segmentación de aguajes en imágenes aéreas

@author: GIORGIO MORALES LUNA
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as FileDialog
from tkinter import messagebox as tkmb
import sys
import ntpath
from PIL import Image, ImageTk
from natsort import natsorted

from aguaje_functions import *

# Disable warnings
import threading
import queue
import warnings

warnings.filterwarnings("ignore")

# Declaration of global variables
global flag_able
global paths_check
global count_check
global L
global bandera
global ct
ct = True
global flag
flag = False
global main_ruta
the_file = os.path.realpath(__file__)
main_ruta, name = ntpath.split(the_file)
global checkbutton_list
checkbutton_list = []

######
i = 0
intvar_dict = {}


def alerta_msg(msg):
    """ Generates warning message"""
    tpl = tk.Toplevel(pwm)
    tpl.wm_title("ALERTA")
    etiq = tk.Label(tpl, text=msg)
    etiq.pack(side="top", fill="x", padx=50, pady=10)
    b1 = ttk.Button(tpl, text="OK", command=tpl.destroy)
    b1.pack()
    tpl.iconbitmap(os.path.join(main_ruta, 'los_logos', 'inictelico.ico'))
    tpl.mainloop()


class ScrollableFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        # create a canvas object and a vertical scrollbar for scrolling it
        self.vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.vscrollbar.pack(side='right', fill="y", expand="false")
        self.canvas = tk.Canvas(self,
                                bg='#EFEFEF', bd=0,
                                height=350,
                                highlightthickness=0,
                                yscrollcommand=self.vscrollbar.set)
        self.canvas.pack(side="left", fill="both", expand="true")
        self.vscrollbar.config(command=self.canvas.yview)

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = tk.Frame(self.canvas, **kwargs)
        self.canvas.create_window(0, 0, window=self.interior, anchor="nw")

        self.bind('<Configure>', self.set_scrollregion)

    def set_scrollregion(self, event=None):
        """ Set the scroll region on the canvas"""
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))


def select_all():
    global buttons
    global flag

    if not flag:
        for item in buttons:
            v, n = item
            v.set(1)
        flag = True
    else:
        for item in buttons:
            v, n = item
            v.set(0)
        flag = False


def manual():
    """User manual"""
    import webbrowser
    webbrowser.open('http://didt.inictel-uni.edu.pe/didt/MANUAL_DE_USUARIO_MauFlex.pdf')


class Mauflex(tk.Tk):

    def __init__(self, *args, **kwargs):
        self.queue = queue.LifoQueue()
        self.princ = tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "MauFlex: Software de Segmentación de Aguajes")

        self.TheCheckBoxValue = tk.IntVar()

        ###################################################################
        #                               FRAMES
        ###################################################################

        # Frame: Menu
        self.frame = tk.Frame(self, bd=4, relief=tk.SUNKEN)

        # Frame_tools: Para botones de acceso rapido a herramientas
        self.frame_tools = tk.Frame(self, bg="#D6DBE9", width=10, height=20, relief=tk.SUNKEN)
        self.frame_tools.pack(side="top", fill="both")

        self.w = tk.Frame(self, bg="#4682B4", height=30, relief=tk.SUNKEN)
        self.w.pack(side="top", fill="both")

        # Frame1: El lienzo donde se mostrara el preview
        self.frame1 = tk.Frame(self, bg="#293955", bd=4, width=300)
        self.frame1.pack(side="right", fill="both", expand=True)

        # Frame2: Explorador de Proyecto
        self.frame2 = ScrollableFrame(self, bg='#EFEFEF')
        self.frame2.pack(side="left", fill="both", expand=True)

        ###################################################################
        #                               MENU
        ###################################################################
        self.crearmenu()

        ###################################################################
        #                               TOOLS
        ###################################################################
        self.btn_importimg = tk.Button(self.frame_tools, font=('Arial', 9), text="Importar Imagenes", bg="white",
                                       command=self.call)
        self.btn_importimg.grid(row=0, column=0)
        self.btn_selectodo = tk.Button(self.frame_tools, font=('Arial', 9), text="Seleccionar todo", bg="white",
                                       command=select_all)
        self.btn_selectodo.grid(row=0, column=4)
        self.boton_process = tk.Button(self.frame_tools, font=('Arial', 9), text="Procesar", bg="white",
                                       command=self.process_perusat)
        self.boton_process.grid(row=0, column=5)

        ###################################################################
        #                               CLOSE
        ###################################################################
        self.protocol('WM_DELETE_WINDOW', self.cerrar_app)

    def progress(self):
        self.prog_bar = ttk.Progressbar(
            self.master, orient="horizontal",
            length=200, mode="indeterminate"
        )
        self.prog_bar.place(x=20, y=29, width=200)

    @staticmethod
    def cerrar_app():
        if tkmb.askokcancel("Salir", "¿Quiere salir de la aplicacion?"):
            pwm.destroy()
            sys.exit()

    def crearmenu(self):
        menu = tk.Menu(self.frame)

        # Opcion Archivos
        archivo = tk.Menu(menu, tearoff=0)
        archivo.add_command(label='Abrir', command=self.call)
        #        archivo.add_command(label='Guardar')
        archivo.add_separator()
        archivo.add_command(label='Salir', command=self.cerrar_app)
        menu.add_cascade(label='Archivo', menu=archivo)

        # Opción Ayuda
        ayuda = tk.Menu(menu, tearoff=0)
        ayuda.add_command(label='Acerca de', command=self.creditos)
        ayuda.add_command(label='Manual de Usuario', command=manual)
        menu.add_cascade(label='Ayuda', menu=ayuda)

        tk.Tk.config(self, menu=menu)

    def creditos(self):
        """Acerca de"""
        global main_ruta
        win_cr = tk.Toplevel(self.princ)
        win_cr.wm_title("Acerca de")
        iml = Image.open(os.path.join(main_ruta, 'los_logos', 'logo.png'))
        photo = ImageTk.PhotoImage(iml)
        canv = tk.Canvas(win_cr, height=200, width=200)

        lbl = tk.Label(win_cr, image=photo)
        lbl.image = photo
        lbl.pack([])
        tk.Label(win_cr, text="Autor: Área de Procesamiento Digital de Señales e Imágenes (Coordinación II)\n"
                              "Direccion de Investigacion y Desarrollo Tecnologico del INICTEL-UNI\n\n"
                              "E-mail: gmorales@inictel-uni.edu.pe\n"
                              "Home Page: http://didt.inictel-uni.edu.pe/didt/", width=70, wraplength=600,
                 justify=tk.CENTER).pack()
        tk.Button(win_cr, text="Salir", command=win_cr.destroy).pack()
        win_cr.iconbitmap(os.path.join(main_ruta, 'los_logos', 'inictelico.ico'))
        win_cr.mainloop()

    ##############################################################################
    ##############################################################################
    #                        LECTURA Y CORRECCION
    ##############################################################################
    ##############################################################################

    def call(self):

        global buttons
        global i
        global filez

        buttons = []
        # filez has the path
        filez = FileDialog.askdirectory(parent=self.frame2, initialdir="/",
                                        title="Seleccione la carpeta que contiene a la imagen satelital")

        if os.path.isdir(filez):
            dirs = os.listdir(filez)
            dirs = natsorted(dirs)
            intvar_dict.clear()

            # remove previous Checkboxes
            for cb in checkbutton_list:
                cb.destroy()
            checkbutton_list.clear()

            global j
            j = []
            idx = 0
            for filename in dirs:
                # create IntVar for filename and keep in dictionary
                if os.path.isfile(filez + "/" + filename) and (filename[-4:] == '.jpg' or filename[-4:] == '.JPG'
                                                               or filename[-4:] == '.tif'):
                    intvar_dict[filename] = tk.IntVar()

                    # create Checkbutton for filename and keep on list
                    c = tk.Checkbutton(self.frame2.interior, text=filename, variable=intvar_dict[filename],
                                       bg='#EFEFEF', command=lambda ind=idx, text=filename,
                                                                    var=intvar_dict[filename]: self.chkbox_checked(ind,
                                                                                                                   text,
                                                                                                                   var))
                    c.pack(anchor='nw')
                    checkbutton_list.append(c)
                    buttons.append((intvar_dict[filename], filename))

                    idx = idx + 1

        # check all
        if i == 0:
            var = tk.IntVar()
            i = i + 1

    def chkbox_checked(self, ind, text, var):

        name_check = checkbutton_list[ind].cget("text")
        if " (100% completo)" in name_check:
            name_check = name_check[0:-16]

        paths_check_i = filez + "/" + name_check

        for widget in self.frame1.winfo_children():
            widget.destroy()

        image = Image.open(paths_check_i)
        image = image.resize((400, 300), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        img_jpg = ImageTk.PhotoImage(image)
        panel = tk.Label(self.frame1, image=img_jpg)
        panel.image = img_jpg
        panel.pack(fill="none", expand=True)

    def process_queue(self):

        global ct
        global count_check
        dirs2 = natsorted(count_check)
        if ct:
            try:
                msg = self.queue.get(False)
                if msg == "END":
                    self.prog_bar.stop()
                    self.queue.task_done()
                    self.prog_bar.destroy()
                    ct = False
                    for u in range(0, len(checkbutton_list)):
                        if checkbutton_list[u].cget("text") == dirs2[len(count_check) - 1]:
                            name_text = checkbutton_list[u].cget("text")
                            checkbutton_list[u].config(text=name_text + " (100% completo)")
                else:
                    for u in range(0, len(checkbutton_list)):
                        if checkbutton_list[u].cget("text") == msg:
                            name_text = checkbutton_list[u].cget("text")
                            checkbutton_list[u].config(text=name_text + " (100% completo)")

            except queue.Empty:
                self.after(2500, self.process_queue)
            self.after(8000, self.process_queue)

    def process_perusat(self):

        global paths_check
        global count_check
        paths_check = []
        count_check = []
        global bandera
        global ct
        ct = True

        cnt = 0
        idp = 0
        for key, value in intvar_dict.items():
            if value.get() > 0:
                src_path = filez + "/" + key
                paths_check.append(src_path)
                count_check.append(key)
                cnt = cnt + 1
            idp = idp + 1

        if cnt == 0:
            alerta_msg("No se ha seleccionado ninguna imagen para procesar")
        else:
            msgbox = tk.messagebox.askquestion('Iniciando proceso', "Se van a procesar " + str(cnt) + " imágenes",
                                               icon='warning')
            if msgbox == 'yes':
                print("Procesando...................")
                self.progress()
                self.prog_bar.start(10)
                self.ThreadedTask(self.queue).start()
                self.after(100, self.process_queue)

    class ThreadedTask(threading.Thread):
        def __init__(self, queuei):
            threading.Thread.__init__(self)
            self.queue = queuei

        def run(self):
            self.process_aguaje()
            self.queue.put("END")

        def process_aguaje(self):
            global paths_check

            dirs = natsorted(paths_check)
            dirs2 = natsorted(count_check)
            cnt = 0
            for paths_check_i in dirs:
                detectaguaje(filez, paths_check_i)

                self.queue.put(dirs2[cnt])
                cnt = cnt + 1


##############################################################################
##############################################################################
##############################################################################
##############################################################################


if __name__ == '__main__':
    pwm = Mauflex()
    pwm.geometry("650x365")
    pwm.iconbitmap(os.path.join(main_ruta, 'los_logos', 'inictelico.ico'))
    pwm.mainloop()
