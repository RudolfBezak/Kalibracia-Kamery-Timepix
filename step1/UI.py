import tkinter as tk
from tkinter import filedialog
from custom_function import custom_function
import rawDataToCalibrationData
import printHistogramFromLineOfData
import matplotlib.pyplot as plt
import numpy as np
from globals import MAX_TOT, TRESHOLD

class Application(tk.Frame):

    def __init__(self, root=None):
        tk.Frame.__init__(self, root)
        self.grid()

    def topRow(self):
        self.master.title('Timepix Kalibracia')
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

        # Create a label for displaying the dropped file name
        self.file_label = tk.Label(self, text="zadaj sem subor")
        self.file_label.grid(row=2, column=2)

        # Bind drag and drop events
        self.file_label.bind("<ButtonRelease>", lambda event: self.openFileExplorer(event, self.file_label))

        self.file_text1 = tk.Label(self, text="názov výstupného súboru:	")
        self.file_text1.grid(row=3, column=0)

        self.text_entry = tk.Entry(self)
        self.text_entry.grid(row=3, column=2)

        self.parseButton = tk.Button(self, text='spracuj', command=self.spracujButtonOnClick)
        self.parseButton.grid(row=4, column=1)  # Specify the row and column for the button

        self.file_text2 = tk.Label(self)
        self.file_text2.grid(row=5, column=1)

    def openFileExplorer(self, event, button):
        event.widget.focus_force()  # Give focus to the widget receiving the drop
        file_path = filedialog.askopenfilename()  # Use filedialog to ask for file path
        button.config(text=file_path)  # Update the file label with the dropped file path

    def openFolderExplorer(self, event, button):
        event.widget.focus_force()
        folder_path = filedialog.askdirectory()
        button.config(text=folder_path)

    def spracujButtonOnClick(self):
        if (self.file_label.cget("text") == "Drop .clog file here" or self.file_label.cget("text").split(".")[-1] != "clog"):
            self.file_text2.config(text="Zlý vstupný súbor")
            print("No file selected")
            return
        if (self.text_entry.get() == ""):
            self.file_text2.config(text="Zlý výstupný súbor")
            print("No text entered")
            return
        rawDataToCalibrationData.rawDataToCalibrationData(self.file_label.cget("text"), self.text_entry.get(), self.file_text2)

    def renderRawDataWidget(self):
        # Destroy the current frame
        self.destroy()
        new_app = Application()
        new_app.rawDataWidget()
        new_app.mainloop()

    def histogramWidget(self):
        self.topRow()
        self.i = 3
        self.file_text2 = tk.Label(self, text="Histogramy")
        self.file_text2.grid(row=self.i-1, column=1)
        self.file_text = tk.Label(self, text=".totKanaly súbor:")
        self.file_text.grid(row=self.i, column=0)

        # Create a label for displaying the dropped file name
        self.file_label = tk.Label(self, text="zadaj sem subor")
        self.file_label.grid(row=self.i, column=2)

        self.file_label.bind("<ButtonRelease>", lambda event: self.openFileExplorer(event, self.file_label))

        self.file_text1 = tk.Label(self, text="číslo pixela:	")
        self.file_text1.grid(row=self.i+1, column=0)

        self.text_entrypixel = tk.Entry(self)
        self.text_entrypixel.grid(row=self.i+1, column=2)

        self.vykresliButton = tk.Button(self, text='vykresli', command=self.vykresliKalibButtonOnClick)
        self.vykresliButton.grid(row=self.i+2, column=1)  # Specify the row and column for the button

        self.file_text2 = tk.Label(self)
        self.file_text2.grid(row=self.i+3, column=1)

        self.i = self.i+5

        self.file_text2 = tk.Label(self, text="Kalibračné krivky")
        self.file_text2.grid(row=self.i-1, column=1)
        self.file_text = tk.Label(self, text="calib_a.txt súbor:")
        self.file_text.grid(row=self.i, column=0)

        # Create a label for displaying the dropped file name
        self.file_labela = tk.Label(self, text="zadaj sem calib_a subor")
        self.file_labela.grid(row=self.i, column=2)

        self.file_labela.bind("<ButtonRelease>", lambda event: self.openFileExplorer(event, self.file_labela))

        self.file_text = tk.Label(self, text="calib_b.txt súbor:")
        self.file_text.grid(row=self.i+1, column=0)

        # Create a label for displaying the dropped file name
        self.file_labelb = tk.Label(self, text="zadaj sem calib_b subor")
        self.file_labelb.grid(row=self.i+1, column=2)

        self.file_labelb.bind("<ButtonRelease>", lambda event: self.openFileExplorer(event, self.file_labelb))

        self.file_text1 = tk.Label(self, text="calib_c.txt súbor:")
        self.file_text1.grid(row=self.i+2, column=0)

        # Create a label for displaying the dropped file name
        self.file_labelc = tk.Label(self, text="zadaj sem calib_c subor")
        self.file_labelc.grid(row=self.i+2, column=2)

        self.file_labelc.bind("<ButtonRelease>", lambda event: self.openFileExplorer(event, self.file_labelc))

        self.file_text1 = tk.Label(self, text="calib_t.txt súbor:")
        self.file_text1.grid(row=self.i+3, column=0)

        # Create a label for displaying the dropped file name
        self.file_labelt = tk.Label(self, text="zadaj sem calib_t subor")
        self.file_labelt.grid(row=self.i+3, column=2)

        self.file_labelt.bind("<ButtonRelease>", lambda event: self.openFileExplorer(event, self.file_labelt))

        self.file_text1 = tk.Label(self, text="číslo pixela:	")
        self.file_text1.grid(row=self.i+4, column=0)

        self.pixely = []
        self.text_entry = tk.Entry(self)
        self.text_entry.grid(row=self.i+4, column=2)
        self.pixely.append(self.text_entry)
  
        self.addButton = tk.Button(self, text='dalsi pixel', command=self.pridajRadKalibracnychKriviek)
        self.addButton.grid(row=self.i+5, column=0)

        self.vykresliButton = tk.Button(self, text='vykresli', command=self.vykresliKalibKrivkyButtonOnClick)
        self.vykresliButton.grid(row=self.i+5, column=1)  # Specify the row and column for the button

        self.file_text2 = tk.Label(self)
        self.file_text2.grid(row=self.i+6, column=1)

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
            print("No file selected")
            return
        
        if (not (self.file_labelb.cget("text").split(".")[-1] == "txt" )):
            self.file_text2.config(text="Zlý vstupný súbor")
            print("No file selected")
            return
        
        if (not (self.file_labelc.cget("text").split(".")[-1] == "txt" )):
            self.file_text2.config(text="Zlý vstupný súbor")
            print("No file selected")
            return
        
        if (not (self.file_labelt.cget("text").split(".")[-1] == "txt" )):
            self.file_text2.config(text="Zlý vstupný súbor")
            print("No file selected")
            return
        
        i = -1
        for pixel in self.pixely:
            i += 1
            if (pixel.get() == ""):
                continue

            filea = open(self.file_labela.cget("text"), 'r', encoding='utf-8')
            riadokCislo = 0
            hladanyRiadok = int(pixel.get())//256
            hladanyStlpec = int(pixel.get())%256
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
            hladanyRiadok = int(pixel.get())//256
            hladanyStlpec = int(pixel.get())%256
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
            hladanyRiadok = int(pixel.get())//256
            hladanyStlpec = int(pixel.get())%256
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
            hladanyRiadok = int(pixel.get())//256
            hladanyStlpec = int(pixel.get())%256
            for riadok in filet:
                if riadokCislo == hladanyRiadok:
                    riadok = riadok.strip()
                    riadok = riadok.split(" ")
                    t = riadok[hladanyStlpec-1]
                    break
                riadokCislo += 1
            
            filet.close()

            params = (float(a), float(b), float(c), float(t))

            x_fit = np.linspace(TRESHOLD, MAX_TOT)
            y_fit = custom_function(x_fit, *params)

            print(params)
            colors = ['red', 'blue', 'green', 'black', 'purple', 'orange',  'brown', 'cyan', 'pink', 'yellow']
            plt.plot(x_fit, y_fit, label='Pixel ' + pixel.get(), color=colors[i])

        x_data = np.array([TRESHOLD, 17.7, 20.7, 26.3, 59.5])
        fileData = open("am4peaks.rudolf", 'r', encoding='utf-8')
        riadokCislo = 1
        for riadok in fileData:
            if riadokCislo == int(self.pixely[0].get()):
                riadok = riadok.strip()
                riadok = riadok.split(" ")
                print("riadok", riadok)
                for i in range(len(riadok)):
                    riadok[i] = int(riadok[i])
                riadok.insert(0, 0)
                print("riadok", riadok)
                y_data = np.array(riadok)
                print("y_data", y_data)
                break
            riadokCislo += 1

        print("x", x_data, "y", y_data)
        plt.scatter(x_data, y_data, label='Namerané hodnoty', color='black')
          
        plt.xlabel('Energia (KeV)')
        plt.ylabel('ToT (ADU)')
        plt.legend()
        plt.show()


    def vykresliKalibButtonOnClick(self):
        if (self.file_label.cget("text") == "Drop .totKanaly file here" or not (self.file_label.cget("text").split(".")[-1] == "totKanaly" or self.file_label.cget("text").split(".")[-1] == "rudolf")):
            self.file_text2.config(text="Zlý vstupný súbor")
            print("No file selected")
            return
        if (self.text_entrypixel.get() == ""):
            self.file_text2.config(text="Zlé číslo pixela")
            print("wrong pixel entered")
            return
        printHistogramFromLineOfData.printHistogramFromLineOfData(self.file_label.cget("text"), self.text_entrypixel.get())

    def renderHistogramWidget(self):
        # Destroy the current frame
        self.destroy()
        new_app = Application()
        new_app.histogramWidget()
        new_app.mainloop()

    def calibrationWidget(self):
        self.topRow()
        self.labels=[]
        self.file_text = tk.Label(self, text="precinok na vystup:")
        self.file_text.grid(row=2, column=0)

        # Create a label for displaying the dropped file name
        self.file_label = tk.Label(self, text="zadaj sem priecinok")
        self.file_label.grid(row=2, column=2)

        self.file_label.bind("<ButtonRelease>", lambda event: self.openFolderExplorer(event, self.file_label))

        self.file_text = tk.Label(self, text=".totKanaly súbor:")
        self.file_text.grid(row=3, column=0)

        self.labels.append(tk.Label(self, text="zadaj sem subor"))
        self.labels[0].grid(row=3, column=2)

        self.labels[0].bind("<ButtonRelease>", lambda event: self.openFileExplorer(event, self.labels[0]))


        self.addButton = tk.Button(self, text='dalsi subor', command=self.pridajRadSuborov)
        self.addButton.grid(row=len(self.labels) + 4, column=0)
        self.parseButton = tk.Button(self, text='vykresli', command=self.vykresliKalibKrivkyButtonOnClick)
        self.parseButton.grid(row=len(self.labels) + 4, column=1)

        self.file_text2 = tk.Label(self)
        self.file_text2.grid(row=6, column=1)

    def pridajRadSuborov(self):
        self.text = tk.Label(self, text=".totKanaly súbor:")
        self.text.grid(row=4+len(self.labels), column=0)

        self.labels.append(tk.Label(self, text="zadaj sem subor"))
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