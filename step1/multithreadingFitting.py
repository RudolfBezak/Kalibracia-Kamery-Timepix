import numpy as np
from scipy.optimize import curve_fit
import concurrent.futures
import os

from custom_function import custom_function
from globals import RESOLUTION, THRESHOLD, DEBUG_MODE

arrayA = [0] * (RESOLUTION * RESOLUTION)
arrayB = [0] * (RESOLUTION * RESOLUTION)
arrayC = [0] * (RESOLUTION * RESOLUTION)
arrayT = [0] * (RESOLUTION * RESOLUTION)

_worker_x_data = None

def _init_worker(x_data):
    global _worker_x_data
    _worker_x_data = np.array(x_data)

def _calibLineWorker(item):
    idx, riadok = item
    global _worker_x_data
    
    # Data preparation
    if riadok is None:
        row = [0.0]
    elif isinstance(riadok, (int, float)):
        row = [0.0, float(riadok)]
    else:
        row = [0.0] + [float(x) if x is not None else 0.0 for x in riadok]
    y_data = np.array(row)
    x_data = _worker_x_data
    
    # 1. Better Initial Guessing
    if len(x_data) >= 2 and len(y_data) >= 2:
        # Gain estimate
        slope = (y_data[-1] - y_data[0]) / (x_data[-1] - x_data[0] + 1e-9)
        # c=20 provides a starting 'bend' to the curve
        p0 = [max(0.5, slope), -5, 20, 3.0]
    else:
        p0 = [1.5, -5, 20, 3.0]

    # 2. Priority Weighting
    # Smaller values in sigma = higher priority for that data point
    sigmas = np.ones_like(y_data)
    if len(sigmas) >= 2:
        sigmas[0] = 0.1  # Force the fit through (6keV, 0TOT)
        sigmas[-1] = 0.5 # Force the fit to reach the 60keV TOT value

    # 3. Robust Fitting
    try:
        params, _ = curve_fit(
            custom_function, x_data, y_data,
            p0=p0,
            sigma=sigmas, 
            method='trf', # More stable with bounds
            maxfev=1000000,
            bounds=([0.1, -500, 0, 0], [5.0, 500, 2000, THRESHOLD - 0.1])
        )
    except:
        params = p0 # Fallback to guess if fit fails

    return (idx, params)

def zapisCalibDoSuboru(priecinok):
    print(f"[Kalibrácia] Zapisujem do súborov ({len(arrayA)} pixelov)")
    riadokCislo = 0  # Inicializácia počítadla riadkov

    # Otvorenie štyroch súborov pre zápis
    with open(priecinok + "/calib_a.txt", "w") as filea, open(priecinok + "/calib_b.txt", "w") as fileb, \
         open(priecinok + "/calib_c.txt", "w") as filec, open(priecinok + "/calib_t.txt", "w") as filet:

        for i in range(len(arrayA)):
            riadokCislo += 1  # Zvýšenie počítadla riadkov
            # Zápis zaokrúhlených hodnôt do súborov
            filea.write(str(round(arrayA[i], 2)) + " ")
            fileb.write(str(round(arrayB[i], 2)) + " ")
            filec.write(str(round(arrayC[i], 2)) + " ")
            filet.write(str(round(arrayT[i], 2)) + " ")

            if riadokCislo == RESOLUTION:
                # Ak je počet riadkov rovný RESOLUTION, pridá nový riadok do súboru
                riadokCislo = 0
                filea.write("\n")
                fileb.write("\n")
                filec.write("\n")
                filet.write("\n")
  
def multithreadingFitting(casy, x_dataVstup, vystupnySuborCesta, progress_callback=None, stop_event=None):
  totalPixels = len(casy)
  n_workers = min(os.cpu_count() or 4, totalPixels)

  if progress_callback:
      progress_callback(0)
  executor = concurrent.futures.ProcessPoolExecutor(
      max_workers=n_workers,
      initializer=_init_worker,
      initargs=(x_dataVstup,)
  )
  try:
      work_items = list(enumerate(casy))
      if DEBUG_MODE:
          work_items = [(i, row) for i, row in work_items if 99 <= i <= 499]
      work_count = len(work_items)
      chunk = max(64, work_count // (n_workers * 32))
      results = executor.map(_calibLineWorker, work_items, chunksize=chunk)
      last_percent = -1
      stopped = False
      for idx, (i, params) in enumerate(results):
          if stop_event and stop_event.is_set():
              stopped = True
              break
          completed = idx + 1
          percent = int(completed / work_count * 100)
          if percent > last_percent:
              last_percent = percent
              if progress_callback:
                  progress_callback(percent)
              print(f"[Kalibrácia] {percent}%")
          arrayA[i] = params[0]
          arrayB[i] = params[1]
          arrayC[i] = params[2]
          arrayT[i] = params[3]

      if not stopped and progress_callback:
          progress_callback(100)
      if not stopped:
          zapisCalibDoSuboru(vystupnySuborCesta)
  finally:
      executor.shutdown(wait=not (stop_event and stop_event.is_set()))