import tkinter as tk
from tkinter import filedialog, ttk
import threading
from americium4peaky import americium4peaky
from settings_cache import get, set, get_initial_dir, get_calibration_data, set_calibration_data, get_calibration_curves_data, set_calibration_curves_data
from custom_function import custom_function
from multithreadingFitting import multithreadingFitting, zapisCalibDoSuboru
import printHistogramCalibrated
import rawDataToCalibrationData
import printHistogram
import matplotlib.pyplot as plt
import numpy as np
from globals import MAX_TOT, RESOLUTION, THRESHOLD

class Application(tk.Frame):
    _stop_event = None
    _calib_thread = None

    def __init__(self, root=None):
        tk.Frame.__init__(self, root)
        self.grid()
        if Application._stop_event is None:
            Application._stop_event = threading.Event()
        root = self.winfo_toplevel()
        root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self):
        if hasattr(self, '_save_calibration_curves_state') and hasattr(self, 'overlay_files'):
            self._save_calibration_curves_state()
        Application._stop_event.set()
        if Application._calib_thread and Application._calib_thread.is_alive():
            Application._calib_thread.join(timeout=3)
        self.winfo_toplevel().destroy()

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

    def openFileExplorer(self, event, button, setting_key=None, placeholder="zadaj sem súbor", on_change=None):
        if event.num == 3:
            button.config(text=placeholder)
            if setting_key:
                set(setting_key, "")
            if on_change:
                on_change()
            return
        event.widget.focus_force()
        if setting_key:
            initialdir = get_initial_dir(setting_key)
        else:
            initialdir = get_initial_dir("output_folder") or get_initial_dir("totkanaly")
        file_path = filedialog.askopenfilename(initialdir=initialdir)
        if file_path:
            button.config(text=file_path)
            if setting_key:
                set(setting_key, file_path)
            if on_change:
                on_change()

    def openFolderExplorer(self, event, button, setting_key=None, placeholder="zadaj sem priečinok", on_change=None):
        if event.num == 3:
            button.config(text=placeholder)
            if setting_key:
                set(setting_key, "")
            if on_change:
                on_change()
            return
        event.widget.focus_force()
        initialdir = get_initial_dir(setting_key) if setting_key else None
        folder_path = filedialog.askdirectory(initialdir=initialdir)
        if folder_path:
            button.config(text=folder_path)
            if setting_key:
                set(setting_key, folder_path)
            if on_change:
                on_change()

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
        if hasattr(self, 'overlay_files'):
            self._save_calibration_curves_state()
        self.destroy()
        new_app = Application()
        new_app.rawDataWidget()
        new_app.mainloop()

    def histogramWidget(self):
        self.topRow()
        row = 2

        hist_frame = tk.LabelFrame(self, text="Histogramy", padx=10, pady=5)
        hist_frame.grid(row=row, column=0, columnspan=3, sticky="ew", padx=5, pady=3)
        row += 1
        r = 0
        tk.Label(hist_frame, text=".totKanaly súbor:").grid(row=r, column=0, sticky="w", pady=2)
        self.file_label = tk.Label(hist_frame, text=get("totkanaly") or "zadaj sem súbor")
        self.file_label.grid(row=r, column=1, sticky="ew", pady=2)
        self.file_label.bind("<ButtonRelease>", lambda e: self.openFileExplorer(e, self.file_label, "totkanaly", on_change=self._save_calibration_curves_state))
        r += 1
        tk.Label(hist_frame, text="číslo pixela:").grid(row=r, column=0, sticky="w", pady=2)
        self.text_entrypixel = tk.Entry(hist_frame)
        self.text_entrypixel.grid(row=r, column=1, sticky="w", pady=2)
        self.text_entrypixel.bind("<FocusOut>", lambda e: self._save_calibration_curves_state())
        r += 1
        self.vytvorMiestoNaCalibSuboryFrame(hist_frame, r, on_change=self._save_calibration_curves_state)
        r += 4
        btn_frame = tk.Frame(hist_frame)
        btn_frame.grid(row=r, column=0, columnspan=2, pady=5)
        tk.Button(btn_frame, text='vykresli', command=lambda: self.vykresliHistogramButtonOnClick(False)).pack(side="left", padx=2)
        tk.Button(btn_frame, text='vykresli s porovnaním', command=lambda: self.vykresliHistogramButtonOnClick(True)).pack(side="left", padx=2)
        r += 1
        self.hist_file_text2 = tk.Label(hist_frame, text="")
        self.hist_file_text2.grid(row=r, column=0, columnspan=2)
        hist_frame.columnconfigure(1, weight=1)

        sep = tk.Frame(self, height=2, bg="gray75", relief="sunken")
        sep.grid(row=row, column=0, columnspan=3, sticky="ew", pady=8, padx=5)
        row += 1

        calib_frame = tk.LabelFrame(self, text="Kalibračné krivky", padx=10, pady=5)
        calib_frame.grid(row=row, column=0, columnspan=3, sticky="ew", padx=5, pady=3)
        self.calib_frame = calib_frame
        pixel_frame = tk.Frame(calib_frame)
        pixel_frame.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        self.pixel_frame = pixel_frame
        self.calib_row = 0
        tk.Label(pixel_frame, text="číslo pixela:").grid(row=self.calib_row, column=0, sticky="w", pady=2)
        self.pixely = []
        self.text_entry = tk.Entry(pixel_frame)
        self.text_entry.grid(row=self.calib_row, column=1, sticky="w", pady=2)
        self.pixely.append(self.text_entry)
        self.calib_row += 1
        self.addButton = tk.Button(pixel_frame, text='ďalší pixel', command=self.pridajRadKalibracnychKriviek)
        self.addButton.grid(row=self.calib_row, column=0, pady=2)
        self.vykresliButton = tk.Button(pixel_frame, text='vykresli', command=self.vykresliKalibKrivkyButtonOnClick)
        self.vykresliButton.grid(row=self.calib_row, column=1, pady=2)
        self.calib_row += 1
        self.file_text2 = tk.Label(pixel_frame, text="")
        self.file_text2.grid(row=self.calib_row, column=0, columnspan=2)
        self.calib_row += 1

        overlay_frame = tk.LabelFrame(calib_frame, text="Overlay súbory", padx=5, pady=5)
        overlay_frame.grid(row=1, column=0, sticky="ew", pady=(0, 5))
        self.overlay_frame = overlay_frame
        self.overlay_row = 0
        self.overlay_files = []
        self.addOverlayBtn = tk.Button(overlay_frame, text='Pridaj overlay súbor', command=lambda: self.pridajOverlaySubor(on_change=self._save_calibration_curves_state))
        curves_data = get_calibration_curves_data()
        overlay_inits = curves_data.get("overlay_files") or [{"path": "", "americium": False, "energy": ""}]
        for init in overlay_inits:
            self.pridajOverlaySubor(init=init, on_change=self._save_calibration_curves_state)
        curve_pixels = curves_data.get("curve_pixels") or [""]
        if curve_pixels:
            self.pixely[0].insert(0, curve_pixels[0])
        for px in curve_pixels[1:]:
            self.pridajRadKalibracnychKriviek()
            self.pixely[-1].insert(0, px)
        for p in self.pixely:
            p.bind("<FocusOut>", lambda e: self._save_calibration_curves_state())
        if curves_data.get("hist_pixel"):
            self.text_entrypixel.insert(0, curves_data["hist_pixel"])
        calib_frame.columnconfigure(0, weight=1)
        overlay_frame.columnconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

    def _is_placeholder_path(self, path):
        return not path or str(path).strip().lower().startswith("zadaj sem")

    def _save_calibration_curves_state(self):
        if not hasattr(self, 'overlay_files') or not hasattr(self, 'pixely'):
            return
        overlay_files = []
        for file_lbl, is_am, _tbtn, energy_entry in self.overlay_files:
            path = file_lbl.cget("text").strip() or ""
            if self._is_placeholder_path(path):
                continue
            energy = energy_entry.get().strip() if not is_am[0] else ""
            if not is_am[0] and not energy:
                continue
            overlay_files.append({
                "path": path,
                "americium": bool(is_am[0]),
                "energy": energy
            })
        curve_pixels = [p.get().strip() for p in self.pixely if p.get().strip()]
        hist_pixel = self.text_entrypixel.get().strip() if hasattr(self, 'text_entrypixel') else ""
        set_calibration_curves_data({
            "hist_pixel": hist_pixel,
            "curve_pixels": curve_pixels,
            "overlay_files": overlay_files
        })

    def vytvorMiestoNaCalibSuboryFrame(self, parent, start_row, on_change=None):
        cb = on_change or (lambda: None)
        self.file_text = tk.Label(parent, text="calib_a.txt súbor:")
        self.file_text.grid(row=start_row, column=0, sticky="w", pady=2)
        self.file_labela = tk.Label(parent, text=get("calib_a") or "zadaj sem calib_a subor")
        self.file_labela.grid(row=start_row, column=1, sticky="ew", pady=2)
        self.file_labela.bind("<ButtonRelease>", lambda e: self.openFileExplorer(e, self.file_labela, "calib_a", "zadaj sem calib_a subor", on_change=cb))
        self.file_text = tk.Label(parent, text="calib_b.txt súbor:")
        self.file_text.grid(row=start_row+1, column=0, sticky="w", pady=2)
        self.file_labelb = tk.Label(parent, text=get("calib_b") or "zadaj sem calib_b subor")
        self.file_labelb.grid(row=start_row+1, column=1, sticky="ew", pady=2)
        self.file_labelb.bind("<ButtonRelease>", lambda e: self.openFileExplorer(e, self.file_labelb, "calib_b", "zadaj sem calib_b subor", on_change=cb))
        self.file_text1 = tk.Label(parent, text="calib_c.txt súbor:")
        self.file_text1.grid(row=start_row+2, column=0, sticky="w", pady=2)
        self.file_labelc = tk.Label(parent, text=get("calib_c") or "zadaj sem calib_c subor")
        self.file_labelc.grid(row=start_row+2, column=1, sticky="ew", pady=2)
        self.file_labelc.bind("<ButtonRelease>", lambda e: self.openFileExplorer(e, self.file_labelc, "calib_c", "zadaj sem calib_c subor", on_change=cb))
        self.file_text1 = tk.Label(parent, text="calib_t.txt súbor:")
        self.file_text1.grid(row=start_row+3, column=0, sticky="w", pady=2)
        self.file_labelt = tk.Label(parent, text=get("calib_t") or "zadaj sem calib_t subor")
        self.file_labelt.grid(row=start_row+3, column=1, sticky="ew", pady=2)
        self.file_labelt.bind("<ButtonRelease>", lambda e: self.openFileExplorer(e, self.file_labelt, "calib_t", "zadaj sem calib_t subor", on_change=cb))

    def pridajOverlaySubor(self, init=None, on_change=None):
        j = len(self.overlay_files)
        row = self.overlay_row + j * 2
        f = self.overlay_frame
        init = init or {}
        cb = on_change or (lambda: None)
        path = init.get("path", "") or "zadaj sem súbor"
        file_lbl = tk.Label(f, text=path if path else "zadaj sem súbor")
        file_lbl.grid(row=row, column=1, sticky="w", pady=2)
        file_lbl.bind("<ButtonRelease>", lambda e, fl=file_lbl: self.openFileExplorer(e, fl, on_change=cb))
        type_lbl = tk.Label(f, text="Amerícium?")
        type_lbl.grid(row=row+1, column=0, sticky="w", pady=2)
        am = init.get("americium", False)
        is_am = [am]
        energy_entry = tk.Entry(f, width=8)
        if init.get("energy"):
            energy_entry.insert(0, init["energy"])
        toggle_btn = tk.Button(f, text="Ano" if am else "Nie")
        def _toggle():
            is_am[0] = not is_am[0]
            toggle_btn.config(text="Ano" if is_am[0] else "Nie")
            if is_am[0]:
                energy_entry.grid_forget()
            else:
                energy_entry.grid(row=row+1, column=2, sticky="w", pady=2)
            cb()
        toggle_btn.config(command=_toggle)
        toggle_btn.grid(row=row+1, column=1, sticky="w", pady=2)
        if am:
            energy_entry.grid_forget()
        else:
            energy_entry.grid(row=row+1, column=2, sticky="w", pady=2)
        energy_entry.bind("<FocusOut>", lambda e: cb())
        self.addOverlayBtn.grid(row=row+2, column=1, pady=2)
        self.overlay_files.append((file_lbl, is_am, toggle_btn, energy_entry))

    def pridajRadKalibracnychKriviek(self):
        f = self.pixel_frame
        tk.Label(f, text="číslo pixela:").grid(row=self.calib_row, column=0, sticky="w", pady=2)
        entry = tk.Entry(f)
        entry.bind("<FocusOut>", lambda e: self._save_calibration_curves_state())
        self.pixely.append(entry)
        self.pixely[-1].grid(row=self.calib_row, column=1, sticky="w", pady=2)
        self.calib_row += 1
        self.addButton.grid(row=self.calib_row, column=0, pady=2)
        self.vykresliButton.grid(row=self.calib_row, column=1, pady=2)
        self.file_text2.grid(row=self.calib_row+1, column=0, columnspan=2)

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
        
        am_cache = {}
        tot_cache = {}
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

            x_fit = np.linspace(THRESHOLD, 100, 200)
            y_fit = custom_function(x_fit, *params)
            colors = ['red', 'blue', 'green', 'black', 'purple', 'orange',  'brown', 'cyan', 'pink', 'yellow']
            c = colors[i]
            plt.plot(x_fit, y_fit, label='Pixel ' + pixel.get(), color=c)

            pixel_idx = int(pixel.get())
            for file_lbl, is_am, _tbtn, energy_entry in getattr(self, 'overlay_files', []):
                path = file_lbl.cget("text").strip()
                if not path or path in ("zadaj sem subor", "zadaj sem súbor"):
                    continue
                ext = path.split(".")[-1] if "." in path else ""
                if ext not in ("totKanaly", "rudolf"):
                    continue
                try:
                    if is_am[0]:
                        if path not in am_cache:
                            am_cache[path] = americium4peaky(path)
                        am_array = am_cache[path]
                        if pixel_idx < len(am_array):
                            peaks = am_array[pixel_idx]
                            x_pts = np.array([17.7, 20.7, 26.3, 59.5])
                            y_pts = np.array([float(x) if x is not None else np.nan for x in peaks])
                            valid = ~np.isnan(y_pts)
                            if np.any(valid):
                                plt.scatter(x_pts[valid], y_pts[valid], color=c, marker='o', s=40, zorder=5)
                    else:
                        energy_str = energy_entry.get().strip()
                        if not energy_str:
                            continue
                        en = float(energy_str)
                        if path not in tot_cache:
                            with open(path, 'r', encoding='utf-8') as f:
                                tot_cache[path] = f.readlines()
                        lines = tot_cache[path]
                        if pixel_idx < len(lines):
                            row = [float(x) if "." in str(x) else int(x) for x in lines[pixel_idx].strip().split() if x]
                            if row and max(row) > 0:
                                tot = row.index(max(row))
                                plt.scatter([en], [tot], color=c, marker='o', s=40, zorder=5)
                except Exception as ex:
                    print(f"[Chyba] Overlay {path}: {ex}")


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
            self.hist_file_text2.config(text="Zlý vstupný súbor")
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
        if hasattr(self, 'overlay_files'):
            self._save_calibration_curves_state()
        self.destroy()
        new_app = Application()
        new_app.histogramWidget()
        new_app.mainloop()

    def kalibrujOnClick(self):
        energie = [THRESHOLD]
        file_data = []

        for i in range(len(self.labels)):
            file_path = self.labels[i].cget("text").strip()
            if self._is_placeholder_path(file_path):
                continue

            if self.toggle_states[i]:
                file_energies = [17.7, 20.7, 26.3, 59.5]
                energie.extend(file_energies)
                array = americium4peaky(self.labels[i].cget("text"))
                file_data.append(("am", file_energies, array))
            else:
                energy_str = self.energie[i].get().strip()
                if not energy_str:
                    continue
                try:
                    e = float(energy_str)
                except ValueError:
                    continue
                energie.append(e)
                with open(self.labels[i].cget("text"), 'r', encoding='utf-8') as file:
                    array = []
                    for line in file:
                        riadok = line.strip().split(" ")
                        riadok = [float(x) if "." in str(x) else int(x) for x in riadok if x]
                        array.append(riadok)
                    tots = []
                    for j in range(len(array)):
                        if max(array[j]) == 0:
                            tots.append(None)
                        else:
                            tots.append(array[j].index(max(array[j])))
                    file_data.append(("single", [e], tots))

        n_pixels = len(file_data[0][2]) if file_data else 0
        casy = []
        for j in range(n_pixels):
            row = []
            for kind, en_list, data in file_data:
                if kind == "am":
                    row.extend([float(x) if x is not None else 0 for x in data[j]])
                else:
                    v = data[j]
                    row.append(float(v) if v is not None else 0)
            casy.append(row)

        if not casy:
            self.file_text2.config(text="Pridajte aspoň jeden platný súbor")
            return
        print("[Kalibrácia] Peaky zistené, spúšťam fitovanie")
        self.progress_bar['value'] = 0
        self.parseButton.config(state='disabled')
        self.file_text2.config(text="Kalibrácia...")

        def run_calibration():
            def on_progress(percent):
                def _update():
                    if not Application._stop_event.is_set():
                        self.progress_bar.config(value=percent)
                self.master.after(0, _update)

            try:
                Application._stop_event.clear()
                multithreadingFitting(casy, energie, self.file_label.cget("text"), progress_callback=on_progress, stop_event=Application._stop_event)
                self.master.after(0, lambda: (Application._stop_event.is_set() or self.file_text2.config(text="Hotovo")))
            except Exception as e:
                self.master.after(0, lambda: (Application._stop_event.is_set() or self.file_text2.config(text=f"Chyba: {e}")))
                print(f"[Chyba] {e}")
            finally:
                self.master.after(0, lambda: (Application._stop_event.is_set() or self.parseButton.config(state='normal')))

        Application._calib_thread = threading.Thread(target=run_calibration, daemon=True)
        Application._calib_thread.start()
        
    def _on_toggle(self, i, toggle_button):
        self.toggle(i, toggle_button)
        self._save_calibration_state()

    def toggle(self, i, toggle_button):
        if self.toggle_states[i]:
            self.energie[i].grid(row=5+(4*i), column=2)
            self.toggle_states[i] = False
            toggle_button.config(text="Nie")
        else:
            self.energie[i].grid_forget()
            self.toggle_states[i] = True
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

        cal_data = get_calibration_data()
        print(f"[Konfigurácia] calibration_data: {cal_data}")
        self.file_label = tk.Label(self, text=cal_data.get("output_folder") or "zadaj sem priečinok")
        self.file_label.grid(row=self.i, column=2)
        self.file_label.bind("<ButtonRelease>", lambda e: self.openFolderExplorer(e, self.file_label, "output_folder", on_change=self._save_calibration_state))

        self.parseButton = tk.Button(self, text='kalibruj', command=self.kalibrujOnClick)
        self.pridajRad = tk.Button(self, text='Pridaj ďalsie súbory', command=self.pridajRadKalibracnychSuborov)

        self.i = self.i + 2
        self.file_text2 = tk.Label(self)
        self.progress_bar = ttk.Progressbar(self, length=300, mode='determinate')
        files = cal_data.get("files", [])
        if files:
            for f in files:
                self.pridajRadKalibracnychSuborov(init=f)
        else:
            self.pridajRadKalibracnychSuborov()
        
    def _save_calibration_state(self):
        files = []
        for i in range(len(self.labels)):
            path = self.labels[i].cget("text").strip() or ""
            if not path or str(path).lower().startswith("zadaj sem"):
                continue
            am = bool(self.toggle_states[i])
            energy = self.energie[i].get().strip() if not am else ""
            files.append({"path": path, "americium": am, "energy": energy})
        output = self.file_label.cget("text").strip() or ""
        if str(output).lower().startswith("zadaj sem"):
            output = ""
        set_calibration_data({"output_folder": output, "files": files})

    def pridajRadKalibracnychSuborov(self, init=None):
        self.file_text = tk.Label(self, text=".totKanaly súbor:")
        self.file_text.grid(row=self.i, column=0)

        path = (init.get("path") or "") if init else (get("totkanaly") if len(self.labels) == 0 else "")
        self.labels.append(tk.Label(self, text=path or "zadaj sem súbor"))
        j = len(self.labels) - 1
        self.labels[j].grid(row=self.i, column=2)
        self.labels[j].bind("<ButtonRelease>", lambda e: self.openFileExplorer(e, self.labels[j], on_change=self._save_calibration_state))

        self.file_text = tk.Label(self, text="Je to Amerícium?")
        self.file_text.grid(row=self.i+1, column=0)

        am = init.get("americium", False) if init else False
        self.toggle_states.append(am)
        toggle_button = tk.Button(self, text="Ano" if am else "Nie", command=lambda: self._on_toggle(j, toggle_button))
        self.toggle_buttons.append(toggle_button)
        toggle_button.grid(row=self.i+1, column=1)

        energia = tk.Entry(self)
        if init and init.get("energy"):
            energia.insert(0, init["energy"])
        if am:
            energia.grid_forget()
        else:
            energia.grid(row=self.i+1, column=2)
        energia.bind("<FocusOut>", lambda e: self._save_calibration_state())
        self.energie.append(energia)
        
        self.parseButton.grid(row=self.i+2, column=1)
        self.pridajRad.grid(row=self.i+2, column=0)
        self.progress_bar.grid(row=self.i+3, column=0, columnspan=3, sticky='ew', padx=5, pady=2)
        self.file_text2.grid(row=self.i+4, column=1)

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
        if hasattr(self, 'overlay_files'):
            self._save_calibration_curves_state()
        self.destroy()
        new_app = Application()
        new_app.calibrationWidget()
        new_app.mainloop()


if __name__ == "__main__":
    app = Application()
    app.rawDataWidget()
    app.mainloop()