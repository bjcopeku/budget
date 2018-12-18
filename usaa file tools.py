# GOALS:
# 1.  Add list of imported files - DONE
# 2.  Add function to check if imported - DONE
# 3.  Not sure I have correctly handled missing data, but think so - DONE
# 4.  Way to handle corrupted location and category entries
# 5.  Delete/edit location, category
# 6.  Delete/edit bad individual transaction
# 7.  Currently nothing catches for a known location + group location w/o known category for that group location
# 8.  Check for duplicate data


import csv
import os
from decimal import Decimal

# os.chdir(os.pardir)
os.chdir('CSV')

with open('parsed_file_list.csv', 'r') as parsed_files:
    parsed_files_reader = csv.DictReader(parsed_files, delimiter=',')
    files = {}
    for row in parsed_files_reader:
        files[row['file']] = ''

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


def fix_date(date):
    if len(date) < 8:
        print("Error in file date formatting:  " + date + ".  Expecting MM/DD/YYYY")
        return date

    if len(date) == 8:
        date = "0"+date

    if (date[2]=='/' and len(date)<10):
        date = date[:3]+"0"+date[3:]
        # print(date)

    if len(date) == 9:
        date = "0"+date

    newdate = date[6]+date[7]+date[8]+date[9] +'-'+ date[0]+date[1] +'-'+ date[3]+date[4]
    # print(newdate)

    return newdate  # transform to ISO_8601 standard


def loc_aggregator(location, amt):
    if location in bank_locations_dict:                      # instant escape for known locations
        return bank_locations_dict[location]

    grouped_location = input('Enter group name for NEW location:  ' + location + '($' + amt + ')  ')
    if grouped_location == "":  # this prevents logging entry when I want to specify the group later
        return None

    bank_locations_dict[location] = grouped_location
    with open('Locations.csv', 'a') as locs_writer:                        # remember the new group
        locs_writer.write(location + ',' + grouped_location + '\n')

    if grouped_location in group_to_category:                              # instant escape for new branch of a group
        return grouped_location

    new_cat = input('Enter a category for:  ' + grouped_location + '  ')
    group_to_category[grouped_location] = new_cat
    with open('Categories.csv', 'a') as cats_writer:                       # remember the new category
            cats_writer.write(grouped_location + ',' + new_cat + '\n')

    return grouped_location  # normalize data from bank locations


def parse_file(filename):
    if filename.find('CC') > 0:
        source_account = 'CC'
    elif filename.find('CHECKING') > 0:
        source_account = 'CHECKING'
    else: source_account = None

    with open(filename, 'r') as parsefile, open('trans_Master.csv', 'a') as trans_master_file:
        parsefile = csv.reader(parsefile, delimiter=',')
        trans_master_file = csv.writer(trans_master_file, dialect='excel', lineterminator='\n')
        for row in parsefile:                                                        # iterate over file to be entered
            if len(row[2]) < 10:
                fixed_date = fix_date(row[2])
            else:
                fixed_date = row[2]
            parsed_loc = loc_aggregator(row[4], row[6])
            if parsed_loc is None:
                parsed_cat = None
            else:
                parsed_cat = group_to_category[parsed_loc]
            # print(row)
            trans_master_file.writerow([None, source_account, fixed_date, row[3], row[4], row[5], Decimal(row[6]),
                                        parsed_loc, parsed_cat])
            # print(None, source_account, fixed_date, row[3], row[4], row[5], Decimal(row[6]), parsed_loc, parsed_cat)
            # 0,1,2-6/1/2017,3-USAA CC,4-TACO BELL,5-,6: -10.07           USAA FORMAT
        # trans_master_file.writerow('\r')

    with open('parsed_file_list.csv', 'a') as list_writer:
        list_writer.write(filename + '\n')
    print('Finished parsing:  ', filename)


if __name__ == "__main__":
    for row in files:
        print('Already parsed: ', [row])

    try:
        working_file = input('What file needs to be parsed?  ')
        if working_file.find(".csv") == -1:                             # catches missing extension
            working_file = working_file + ".csv"

        while working_file in files:                                    # checks for possible duplication
            print('File already processed.\n')
            working_file = input('What file needs to be parsed?')

        print("Parsing:  ", working_file)
        parse_file(working_file)

    except FileNotFoundError:
        print('Requested Parse File Not Found.')
else:
    print('usaa_file_tools.py was imported')

# with open("Locations.csv", 'w', newline='') as csvfile:
#     fieldnames = ['statement', 'grouping']
#     w = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     w.writeheader()
#     for key,value in bank_locations_dict.items():
#         # print(key, "corresponds to", d[key])
#         w.writerow({'statement' : key, 'grouping' : bank_locations_dict[key]})
