import numpy as np

loc_file = './locations.txt'
locations = []

with open(loc_file, "r") as lf:
    line = lf.readline()
    for line in lf:
        locations.append(line.strip())
print(locations)
        
