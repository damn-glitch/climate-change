# N.America temperatures
file_1 = open("*your repository*\\N.America Temperature 1967-2020.csv", "r")
data_1 = file_1.readlines()

years_1 = []
for line in data_1:
    years_1.append(int(line.split(',')[0]))

temp_1 = []
for line in data_1:
    numlist_1 = line.split(',')[1].split()
    num_1 = float(''.join(numlist_1))
    temp_1.append(num_1)
from matplotlib import pyplot as plt

plt.plot(years_1, temp_1)
plt.ylabel('temperature (C)')
plt.xlabel('years')
plt.show()
