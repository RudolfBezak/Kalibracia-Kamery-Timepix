import tkinter as tk
from tkinter import filedialog
from americium4peaky import americium4peaky
from settings_cache import get, set, get_initial_dir
from custom_function import custom_function
from multithreadingFitting import calibLine, multithreadingFitting, zapisCalibDoSuboru
import printHistogramCalibrated
import rawDataToCalibrationData
import printHistogram
import matplotlib.pyplot as plt
import numpy as np
from globals import MAX_TOT, RESOLUTION, THRESHOLD

class Application(tk.Frame):

    def __init__(self, root=None):
        tk.Frame.__init__(self, root)
        self.grid()

    def topRow(self):
        self.master.title('Timepix Kalibrácia')
        self.rawData = tk.Button(self, text='Per pixel spektrá', command=self.renderRawDataWidget)
        self.rawData.grid(row=1, column=0)

        self.rawData = tk.Button(self, text='Zobrazenie dát', command=self.renderHistogramWidget)
        self.rawData.grid(row=1, column=1)

        self.rawData = tk.Button(self, text='Kalibrovanie', command=self.renderCalibrationWidget)
        self.rawData.grid(row=1, column=2)

    def rawDataWidget(self):
        
        self.topRow()

        self.file_text = tk.Label(self, text=".clog súbor:")
        self.file_text.grid(row=2, column=0)

        self.file_label = tk.Label(self, text=get("clog") or "zadaj sem súbor")
        self.file_label.grid(row=2, column=2)

        self.file_label.bind("<ButtonRelease>", lambda event: self.openFileExplorer(event, self.file_label, "clog"))

        self.file_text1 = tk.Label(self, text="názov výstupného súboru:	")
        self.file_text1.grid(row=3, column=0)

        self.text_entry = tk.Entry(self)
        self.text_entry.insert(0, get("output_name"))
        self.text_entry.grid(row=3, column=2)

        self.parseButton = tk.Button(self, text='spracuj', command=self.spracujButtonOnClick)
        self.parseButton.grid(row=4, column=1)  # Specify the row and column for the button

        self.file_text2 = tk.Label(self)
        self.file_text2.grid(row=5, column=1)

    def openFileExplorer(self, event, button, setting_key=None, placeholder="zadaj sem súbor"):
        if event.num == 3:
            button.config(text=placeholder)
            if setting_key:
                set(setting_key, "")
            return
        event.widget.focus_force()
        initialdir = get_initial_dir(setting_key) if setting_key else None
        file_path = filedialog.askopenfilename(initialdir=initialdir)
        if file_path:
            button.config(text=file_path)
            if setting_key:
                set(setting_key, file_path)

    def openFolderExplorer(self, event, button, setting_key=None, placeholder="zadaj sem priečinok"):
        if event.num == 3:
            button.config(text=placeholder)
            if setting_key:
                set(setting_key, "")
            return
        event.widget.focus_force()
        initialdir = get_initial_dir(setting_key) if setting_key else None
        folder_path = filedialog.askdirectory(initialdir=initialdir)
        if folder_path:
            button.config(text=folder_path)
            if setting_key:
                set(setting_key, folder_path)

    def spracujButtonOnClick(self):
        if (self.file_label.cget("text") == "Drop .clog file here" or self.file_label.cget("text").split(".")[-1] != "clog"):
            self.file_text2.config(text="Zlý vstupný súbor")
            print("[Chyba] Nebol vybraný žiadny .clog súbor")
            return
        if (self.text_entry.get() == ""):
            self.file_text2.config(text="Zlý výstupný súbor")
            print("[Chyba] Nebol zadaný názov výstupného súboru")
            return
        set("output_name", self.text_entry.get())
        rawDataToCalibrationData.rawDataToCalibrationData(self.file_label.cget("text"), self.text_entry.get(), self.file_text2)

    def renderRawDataWidget(self):
        # Destroy the current frame
        self.destroy()
        new_app = Application()
        new_app.rawDataWidget()
        new_app.mainloop()

    def vytvorMiestoNaCalibSubory(self):
          self.file_text = tk.Label(self, text="calib_a.txt súbor:")
          self.file_text.grid(row=self.i, column=0)

          self.file_labela = tk.Label(self, text=get("calib_a") or "zadaj sem calib_a subor")
          self.file_labela.grid(row=self.i, column=2)

          self.file_labela.bind("<ButtonRelease>", lambda event: self.openFileExplorer(event, self.file_labela, "calib_a", "zadaj sem calib_a subor"))

          self.file_text = tk.Label(self, text="calib_b.txt súbor:")
          self.file_text.grid(row=self.i+1, column=0)

          self.file_labelb = tk.Label(self, text=get("calib_b") or "zadaj sem calib_b subor")
          self.file_labelb.grid(row=self.i+1, column=2)

          self.file_labelb.bind("<ButtonRelease>", lambda event: self.openFileExplorer(event, self.file_labelb, "calib_b", "zadaj sem calib_b subor"))

          self.file_text1 = tk.Label(self, text="calib_c.txt súbor:")
          self.file_text1.grid(row=self.i+2, column=0)

          self.file_labelc = tk.Label(self, text=get("calib_c") or "zadaj sem calib_c subor")
          self.file_labelc.grid(row=self.i+2, column=2)

          self.file_labelc.bind("<ButtonRelease>", lambda event: self.openFileExplorer(event, self.file_labelc, "calib_c", "zadaj sem calib_c subor"))

          self.file_text1 = tk.Label(self, text="calib_t.txt súbor:")
          self.file_text1.grid(row=self.i+3, column=0)

          self.file_labelt = tk.Label(self, text=get("calib_t") or "zadaj sem calib_t subor")
          self.file_labelt.grid(row=self.i+3, column=2)

          self.file_labelt.bind("<ButtonRelease>", lambda event: self.openFileExplorer(event, self.file_labelt, "calib_t", "zadaj sem calib_t subor"))

    def histogramWidget(self):
        self.topRow()
        self.i = 3
        self.file_text2 = tk.Label(self, text="Histogramy")
        self.file_text2.grid(row=self.i-1, column=1)
        self.file_text = tk.Label(self, text=".totKanaly súbor:")
        self.file_text.grid(row=self.i, column=0)

        self.file_label = tk.Label(self, text=get("totkanaly") or "zadaj sem súbor")
        self.file_label.grid(row=self.i, column=2)

        self.file_label.bind("<ButtonRelease>", lambda event: self.openFileExplorer(event, self.file_label, "totkanaly"))

        self.file_text1 = tk.Label(self, text="číslo pixela:	")
        self.file_text1.grid(row=self.i+1, column=0)

        self.text_entrypixel = tk.Entry(self)
        self.text_entrypixel.grid(row=self.i+1, column=2)

        self.i = self.i+7

        self.vytvorMiestoNaCalibSubory()


        self.vykresliButton = tk.Button(self, text='vykresli', command=lambda: self.vykresliHistogramButtonOnClick(False))
        self.vykresliButton.grid(row=self.i+4, column=1)  # Specify the row and column for the button

        self.vykresliVsetkoButton = tk.Button(self, text='vykresli s porovnaním', command=lambda: self.vykresliHistogramButtonOnClick(True))
        self.vykresliVsetkoButton.grid(row=self.i+4, column=2)  # Specify the row and column for the button

        self.file_text2 = tk.Label(self)
        self.file_text2.grid(row=self.i+5, column=1)

        self.i = self.i+6

        self.file_text2 = tk.Label(self, text="Kalibračné krivky")
        self.file_text2.grid(row=self.i-1, column=1)
        # self.vytvorMiestoNaCalibSubory()
        # self.i = self.i+4

        self.file_text1 = tk.Label(self, text="číslo pixela:	")
        self.file_text1.grid(row=self.i, column=0)

        self.pixely = []
        self.text_entry = tk.Entry(self)
        self.text_entry.grid(row=self.i, column=2)
        self.pixely.append(self.text_entry)
  
        self.addButton = tk.Button(self, text='ďalší pixel', command=self.pridajRadKalibracnychKriviek)
        self.addButton.grid(row=self.i+1, column=0)

        self.vykresliButton = tk.Button(self, text='vykresli', command=self.vykresliKalibKrivkyButtonOnClick)
        self.vykresliButton.grid(row=self.i+1, column=1)  # Specify the row and column for the button

        self.file_text2 = tk.Label(self)
        self.file_text2.grid(row=self.i+2, column=1)

        self.i = self.i + 7

    def pridajRadKalibracnychKriviek(self):
        self.pixely.append(tk.Entry(self))
        self.pixely[-1].grid(row=self.i, column=2)

        self.file_text = tk.Label(self, text="číslo pixela:	")
        self.file_text.grid(row=self.i, column=0)

        self.i = self.i + 1
        self.addButton.grid(row=self.i, column=0)
        self.vykresliButton.grid(row=self.i, column=1)

        self.i = self.i + 1
        self.file_text2.grid(row=self.i, column=1)

    def vykresliKalibKrivkyButtonOnClick(self):
        if (not (self.file_labela.cget("text").split(".")[-1] == "txt" )):
            self.file_text2.config(text="Zlý vstupný súbor")
            print("[Chyba] Nebol vybraný calib_a.txt súbor")
            return
        
        if (not (self.file_labelb.cget("text").split(".")[-1] == "txt" )):
            self.file_text2.config(text="Zlý vstupný súbor")
            print("[Chyba] Nebol vybraný calib_b.txt súbor")
            return
        
        if (not (self.file_labelc.cget("text").split(".")[-1] == "txt" )):
            self.file_text2.config(text="Zlý vstupný súbor")
            print("[Chyba] Nebol vybraný calib_c.txt súbor")
            return
        
        if (not (self.file_labelt.cget("text").split(".")[-1] == "txt" )):
            self.file_text2.config(text="Zlý vstupný súbor")
            print("[Chyba] Nebol vybraný calib_t.txt súbor")
            return
        
        i = -1
        for pixel in self.pixely:
            i += 1
            if (pixel.get() == ""):
                continue

            filea = open(self.file_labela.cget("text"), 'r', encoding='utf-8')
            riadokCislo = 0
            hladanyRiadok = int(pixel.get())//RESOLUTION
            hladanyStlpec = int(pixel.get())%RESOLUTION
            for riadok in filea:
                if riadokCislo == hladanyRiadok:
                    riadok = riadok.strip()
                    riadok = riadok.split(" ")
                    a = riadok[hladanyStlpec-1]
                    break
                riadokCislo += 1
            
            filea.close()

            fileb = open(self.file_labelb.cget("text"), 'r', encoding='utf-8')
            riadokCislo = 0
            hladanyRiadok = int(pixel.get())//RESOLUTION
            hladanyStlpec = int(pixel.get())%RESOLUTION
            for riadok in fileb:
                if riadokCislo == hladanyRiadok:
                    riadok = riadok.strip()
                    riadok = riadok.split(" ")
                    b = riadok[hladanyStlpec-1]
                    break
                riadokCislo += 1
            
            fileb.close()

            
            filec = open(self.file_labelc.cget("text"), 'r', encoding='utf-8')
            riadokCislo = 0
            hladanyRiadok = int(pixel.get())//RESOLUTION
            hladanyStlpec = int(pixel.get())%RESOLUTION
            for riadok in filec:
                if riadokCislo == hladanyRiadok:
                    riadok = riadok.strip()
                    riadok = riadok.split(" ")
                    c = riadok[hladanyStlpec-1]
                    break
                riadokCislo += 1
            
            filec.close()

            
            filet = open(self.file_labelt.cget("text"), 'r', encoding='utf-8')
            riadokCislo = 0
            hladanyRiadok = int(pixel.get())//RESOLUTION
            hladanyStlpec = int(pixel.get())%RESOLUTION
            for riadok in filet:
                if riadokCislo == hladanyRiadok:
                    riadok = riadok.strip()
                    riadok = riadok.split(" ")
                    t = riadok[hladanyStlpec-1]
                    break
                riadokCislo += 1
            
            filet.close()

            params = (float(a), float(b), float(c), float(t))
            print(f"[Kalibračné krivky] Pixel {pixel.get()}: a={params[0]:.2f}, b={params[1]:.2f}, c={params[2]:.2f}, t={params[3]:.2f}")

            x_fit = np.linspace(THRESHOLD, MAX_TOT)
            y_fit = custom_function(x_fit, *params)
            colors = ['red', 'blue', 'green', 'black', 'purple', 'orange',  'brown', 'cyan', 'pink', 'yellow']
            plt.plot(x_fit, y_fit, label='Pixel ' + pixel.get(), color=colors[i])


        # testovacie body
        # x_data = np.array([THRESHOLD, 17.7, 20.7, 26.3, 59.5])
        # fileData = open("am4peaks.rudolf", 'r', encoding='utf-8')
        # riadokCislo = 1
        # for riadok in fileData:
        #     if riadokCislo == int(self.pixely[0].get()):
        #         riadok = riadok.strip()
        #         riadok = riadok.split(" ")
        #         print("riadok", riadok)
        #         for i in range(len(riadok)):
        #             riadok[i] = int(riadok[i])
        #         riadok.insert(0, 0)
        #         print("riadok", riadok)
        #         y_data = np.array(riadok)
        #         print("y_data", y_data)
        #         break
        #     riadokCislo += 1

        # print("x", x_data, "y", y_data)
        # plt.scatter(x_data, y_data, label='Namerané hodnoty', color='black')
          
        plt.xlabel('Energia (keV)')
        plt.ylabel('ToT (ADU)')
        plt.legend()
        plt.show()

    def vykresliHistogramButtonOnClick(self, porovnanie):
        kalibKrivy = True
        if ((self.file_label.cget("text") == "zadaj sem subor" or self.file_label.cget("text") == "") or not (self.file_label.cget("text").split(".")[-1] == "totKanaly" or self.file_label.cget("text").split(".")[-1] == "rudolf")):
            self.file_text2.config(text="Zlý vstupný súbor")
            print("[Chyba] Nebol vybraný .totKanaly súbor pre histogram")
            return
      
        if (not (self.file_labela.cget("text").split(".")[-1] == "txt" )):
            kalibKrivy = False
        
        if (not (self.file_labelb.cget("text").split(".")[-1] == "txt" )):
            kalibKrivy = False
        
        if (not (self.file_labelc.cget("text").split(".")[-1] == "txt" )):
            kalibKrivy = False
        
        if (not (self.file_labelt.cget("text").split(".")[-1] == "txt" )):
            kalibKrivy = False

        if (kalibKrivy):
            printHistogramCalibrated.printHistogramCalibrated(self.file_label.cget("text"), self.text_entrypixel.get(), self.file_labela.cget("text"), self.file_labelb.cget("text"), self.file_labelc.cget("text"), self.file_labelt.cget("text"), porovnanie)
        else:
            printHistogram.printHistogramFromLineOfData(self.file_label.cget("text"), self.text_entrypixel.get())

    def renderHistogramWidget(self):
        # Destroy the current frame
        self.destroy()
        new_app = Application()
        new_app.histogramWidget()
        new_app.mainloop()

    def kalibrujOnClick(self):
        energie = [THRESHOLD]
        casy = []

        for i in range(len(self.labels)):
            if (self.labels[i].cget("text") == "zadaj sem subor"):
                continue

            if (self.toggle_states[i] == "Ano"):
                energie.append(17.7)
                energie.append(20.7)
                energie.append(26.3)
                energie.append(59.5)
                array = americium4peaky(self.labels[i].cget("text"))
                for j in range(len(array)):
                    casy.append(array[j])
            else:
                energie.append(float(self.energie[i].get()))
                with open(self.labels[i].cget("text"), 'r', encoding='utf-8') as file:
                    array = []
                    for line in file:
                        riadok = line.strip()
                        riadok = riadok.split(" ")
                        for i in range(len(riadok)):
                            riadok[i] = int(riadok[i])
                        array.append(riadok)

                    for j in range(len(array)):
                        if max(array[j]) == 0:
                            casy.append(None)
                        else:
                            casy.append(array[j].index(max(array[j])))

        print("[Kalibrácia] Peaky zistené, spúšťam fitovanie")

        multithreadingFitting(casy, energie, self.file_label.cget("text"))
        
    def toggle(self, i, toggle_button):

        if self.toggle_states[i] == "Ano":
            self.energie[i].grid(row=5+(4*i), column=2)
            self.toggle_states[i] = "Nie"
            toggle_button.config(text="Nie")
        else:
            self.energie[i].grid_forget()
            self.toggle_states[i] = "Ano"
            toggle_button.config(text="Ano")

    def calibrationWidget(self):
        self.toggle_states = []
        self.toggle_buttons = []
        self.labels=[]
        self.energie = []
        self.i = 2
        self.topRow()
        self.file_text = tk.Label(self, text="prečinok na výstup:")
        self.file_text.grid(row=self.i, column=0)

        self.file_label = tk.Label(self, text=get("output_folder") or "zadaj sem priečinok")
        self.file_label.grid(row=self.i, column=2)

        self.file_label.bind("<ButtonRelease>", lambda event: self.openFolderExplorer(event, self.file_label, "output_folder"))

        self.parseButton = tk.Button(self, text='kalibruj', command=self.kalibrujOnClick)

        self.pridajRad = tk.Button(self, text='Pridaj ďalsie súbory', command=self.pridajRadKalibracnychSuborov)

        self.i = self.i + 2
        self.file_text2 = tk.Label(self)
        self.pridajRadKalibracnychSuborov()
        
    def pridajRadKalibracnychSuborov(self):
        self.file_text = tk.Label(self, text=".totKanaly súbor:")
        self.file_text.grid(row=self.i, column=0)

        cached = get("totkanaly") if len(self.labels) == 0 else ""
        self.labels.append(tk.Label(self, text=cached or "zadaj sem súbor"))
        j = len(self.labels) - 1
        self.labels[j].grid(row=self.i, column=2)

        self.labels[j].bind("<ButtonRelease>", lambda event: self.openFileExplorer(event, self.labels[j], "totkanaly"))

        self.file_text = tk.Label(self, text="Je to Amerícium?")
        self.file_text.grid(row=self.i+1, column=0) 

        self.toggle_states.append(False)
        toggle_button = tk.Button(self, text="Nie", command=lambda: self.toggle(j, toggle_button))
        self.toggle_buttons.append(toggle_button)
        toggle_button.grid(row=self.i+1, column=1)

        energia = tk.Entry(self)
        energia.grid(row=self.i+1, column=2)
        self.energie.append(energia) 
        
        self.parseButton.grid(row=self.i+2, column=1)
        self.pridajRad.grid(row=self.i+2, column=0)
        
        self.file_text2.grid(row=self.i+3, column=1)

        self.i = self.i + 4
        
    def pridajRadSuborov(self):
        
        self.text = tk.Label(self, text=".totKanaly súbor:")
        self.text.grid(row=4+len(self.labels), column=0)

        self.labels.append(tk.Label(self, text="zadaj sem súbor"))
        self.labels[-1].grid(row=3+len(self.labels), column=2)
        
        i = len(self.labels) - 1

        self.labels[-1].bind("<ButtonRelease>", lambda event: self.openFileExplorer(event, self.labels[i]))

        self.addButton.grid(row=len(self.labels) + 4, column=0)
        self.parseButton.grid(row=len(self.labels) + 4, column=1)
        self.file_text2.grid(row=len(self.labels) + 5, column=1)

    def renderCalibrationWidget(self):
        # Destroy the current frame
        self.destroy()
        new_app = Application()
        new_app.calibrationWidget()
        new_app.mainloop()
         

app = Application()
app.rawDataWidget()
app.mainloop()