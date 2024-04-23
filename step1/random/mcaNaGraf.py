import matplotlib.pyplot as plt
import numpy as np

#sem sa pise nazov suboru
inputFile = f"GaAs8MeV0kGy1_aAm_350Vneg_600s_pt08_g2.mca"

arraySpocitany = []
file = open(inputFile, 'r', encoding='unicode_escape')

data = False
for riadok in file:
    if data == False and riadok.strip() == "<<DATA>>":
        data = True
        continue
    if  data == True and riadok.strip() == "<<END>>":
        data = False
        continue
    if data:
       arraySpocitany.append(riadok.strip())

print(arraySpocitany)
for i in range(len(arraySpocitany)):
  arraySpocitany[i] = int(arraySpocitany[i])


x = np.arange(1, len(arraySpocitany)+1)
y = np.array(arraySpocitany)

plt.title("Line graph")
plt.xlabel("X axis")
plt.ylabel("Y axis")

#tu sa to da prepinat medzi logaritmickym a normalnym grafom

plt.semilogy(x, y, color="red") #logaritmicky graf
# plt.plot(x, y, color ="red") #normalny graf


plt.show()
