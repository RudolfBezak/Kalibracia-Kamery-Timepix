from globals import MAX_TOT

# vstupnySuborCesta = f"calibrationData.rudolf"
# vystupnySuborCesta = f"am4peaks.rudolf"


# print("start")

def americium4peaky(vstupnySuborCesta):
  zaciatok = 0
  koniec = round(MAX_TOT/2)
  treshold = 0.5

  def najdiSekundarnyPeak(riadok, hlavnyPeakIndex, smer=False): 
      # Funkcia pre hľadanie sekundárneho "peak-u" v danom riadku hodnôt.
      # Parametre:
      #   - riadok: Reťazec obsahujúci čísla oddelené medzerami.
      #   - hlavnyPeakIndex: Index hlavného peaku, okolo ktorého hľadáme sekundárny peak.
      #   - smer: Boolovská hodnota určujúca smer hľadania sekundárneho peaku.
      #           True - hľadáme vpravo od hlavného peaku, False - hľadáme vľavo od hlavného peaku.
      
      # Rozdelenie reťazca na čísla a uloženie do zoznamu
      data = [int(x) for x in riadok.split()]
      
      # Určenie smeru posunu v závislosti od smeru hľadania peak-u
      posun = -1 if smer else 1
      
      # Určenie začiatočného indexu pre prechádzanie zoznamom
      zaciatocnyIndex = hlavnyPeakIndex + posun if smer else hlavnyPeakIndex
      end_index = -1 if smer else len(data)
      
      # Premenné pre sledovanie zmien
      najdenaZmena = False
      strmostKrokSpat = 0

      # Prechádzanie cez zoznam čísel
      for i in range(zaciatocnyIndex, end_index - 1, posun):
          # Vypočítanie strmosti medzi susednými číslami
          strmost = data[i] - data[i + posun]

          # Podmienka pre hľadanie sekundárneho peak-u
          if najdenaZmena and strmost > 0:
              if smer:
                  return i  # Vráti index nájdeného sekundárneho peak-u
              return i + 1  # Vráti index nájdeného sekundárneho peak-u

          # Podmienka pre zistenie zmeny v strmosti
          if strmost < (strmostKrokSpat * treshold):
              najdenaZmena = True

          strmostKrokSpat = strmost

      return None  # Ak nebol nájdený sekundárny peak

  vstupnySubor = open(vstupnySuborCesta, 'r', encoding='utf-8')
  vystupnyArray = []
  for riadok in vstupnySubor:
      data = [int(x) for x in riadok.split()]
      sublist = data[zaciatok:koniec + 1]
      
      max_value = sublist.index(max(sublist)) + zaciatok

      maximaArray = []
      maximaArray.append(najdiSekundarnyPeak(riadok, max_value, True)) 
      maximaArray.append(max_value + 1)
      maximaArray.append(najdiSekundarnyPeak(riadok, max_value))


      #posledny peak
      data = [int(x) for x in riadok.split()]
      sublist = data[koniec:MAX_TOT + 1]
      
      max_value = sublist.index(max(sublist)) + koniec
      maximaArray.append(max_value + 1)

      vystupnyArray.append(maximaArray)

  return vystupnyArray

# vstupnySubor.close()
# vystupnySubor.close()

# print("done")


