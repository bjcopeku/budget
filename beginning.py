import csv
import os
import pandas as pd
from decimal import *

globals()

# os.chdir(os.pardir)
# os.chdir('CSV')


# with open("Categories.csv") as csvfile:
#     readCSV = csv.reader(csvfile, delimiter=',')
#     for row in readCSV:
#         c.execute("INSERT INTO cats (groupLocation, category) VALUES (?, ?)", (row[0], row[1]))
import time
start_time = time.time()

with open('test.gff', 'r') as testfile:
    print(testfile)





# x = 0.5
# getcontext().prec = 6
#
# print(x, " / 3 = ", Decimal(x/3))


print("--- %s ms ---" % (time.time() - start_time))  #assuming at least 0.1 seconds to run