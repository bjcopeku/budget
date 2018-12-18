import csv
import os

os.chdir(os.pardir)
os.chdir('CSV')

with open("Locations.csv", 'r') as locations_file:
    locations_reader = csv.DictReader(locations_file, delimiter=',')
    bank_locations_dict = {}
    for row in locations_reader:
        bank_locations_dict[row['statement']] = row['grouping']

with open("Categories.csv", 'r') as categories_file:
    categories_reader = csv.DictReader(categories_file, delimiter=',')
    group_to_category = {}
    for row in categories_reader:
        group_to_category[row['group']] = row['category']

for key, value in bank_locations_dict.items():
    oldValue = bank_locations_dict[key]
    # newValue = input("What category for key: " + value)
    bank_locations_dict[key] = [oldValue, group_to_category[oldValue]]

# with open("Locations.csv", 'w', newline='') as locations_file:
#     fieldnames = ['location', ['group', 'category']]
#     locations_writer = csv.DictWriter(locations_file, fieldnames=fieldnames)
#     locations_writer.writeheader()
#     for key, [value1, value2] in bank_locations_dict.items():
#         locations_writer.writerow({'location' : key, ['group' : value1, 'category' : value2]})

with open('Locations_test.csv', 'w') as csv_file:
    fieldnames = ['statement', 'grouping']
    w = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator='\n')
    w.writeheader()
    for k, v in bank_locations_dict.items():
        # print(key, "corresponds to", d[key])
        w.writerow({'statement': k, 'grouping': bank_locations_dict[k]})

print('saving is complete')

with open("Locations_test.csv", 'r') as test_file:
    test_reader = csv.DictReader(test_file, delimiter=',')
    mydict = {}
    for row in test_reader:
        mydict[row['statement']] = list(row['grouping'])

print(mydict)
