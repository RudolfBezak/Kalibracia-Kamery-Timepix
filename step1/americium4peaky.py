from globals import MAX_TOT


inputFile = f"calibrationData.rudolf"
outputFile = f"am4peaks.rudolf"
start = 0
koniec = 50

treshold = 0.5

riadokCislo=0

print("start")

def najdiSekundarnyPeak(row, main_peak_index, left=False):
    data = [int(x) for x in row.split()]

    # Define the direction to search for the secondary peak
    shift = -1 if left else 1

    # Determine the range of indices to search
    start_index = main_peak_index + shift if left else main_peak_index
    end_index = -1 if left else len(data)

    # Iterate from the main peak index in the specified direction
    changeTrigger = False
    steepnessStepBack = 0
    for i in range(start_index, end_index - 1, shift):
        currentSteepness = data[i] - data[i + shift]

        if (changeTrigger and (currentSteepness > 0)):
            if left:
                return i
            return i + 1

        if (currentSteepness < (steepnessStepBack * treshold)):
            changeTrigger = True

        steepnessStepBack = currentSteepness

    return None  # Secondary peak not found

file = open(inputFile, 'r', encoding='utf-8')
file2 = open(outputFile, 'w', encoding='utf-8')
for riadok in file:
    data = [int(x) for x in riadok.split()]
    sublist = data[start:koniec + 1]
    
    max_value = sublist.index(max(sublist)) + start



    file2.write(str(najdiSekundarnyPeak(riadok, max_value, True)) + " " + str(max_value + 1) + " " + str(najdiSekundarnyPeak(riadok, max_value)) + " ")


    #posledny peak
    data = [int(x) for x in riadok.split()]
    sublist = data[koniec:MAX_TOT + 1]
    
    max_value = sublist.index(max(sublist)) + koniec
    file2.write(str(max_value + 1))

    file2.write("\n")

file.close()
file2.close()

print("done")


