import random
import os
import csv
import sys
import tkinter as tk
from tkinter import simpledialog
from tkinter.filedialog import askopenfilename


class Camper:
    def __init__(self, nickname, last_name, column):
        self.nickname = nickname
        self.last_name = last_name
        self.column = column


root = tk.Tk()
root.withdraw()

# Ask for file
filename = os.path.abspath(
    askopenfilename(initialdir="/", title="Select csv file", filetypes=(("CSV Files", "*.csv"),)))
# Set output file name
output_name = filename.rsplit('.', 1)
del output_name[len(output_name) - 1]
if not output_name:
    sys.exit()
output_name = "".join(output_name)
output_name += "_processed.csv"
# Ask for number of boards
number_of_boards_to_make = simpledialog.askinteger("Input", "How many boards do you want to make?", parent=root)
# Using the file that will be written to
csv_output_file = open(os.path.abspath(output_name), 'w', encoding='utf-8', newline='')
# Using the file is be read in
csv_file = open(filename, encoding='utf-8', errors='ignore')
# Define reader with , delimiter
csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
# Define writer to put quotes around input values with a comma in them
csv_writer = csv.writer(csv_output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


def generate_header_row():
    header_row = []
    for row_count in range(1, 6):
        num_for_col_name = 1
        for col_count in range(1, 11):
            if col_count % 2 == 0:
                header_row.append("Last" + str(row_count) + str(num_for_col_name))
                num_for_col_name += 1
            else:
                header_row.append("Nick" + str(row_count) + str(num_for_col_name))
    return header_row


camper_list = []
for idx, row in enumerate(csv_reader):
    if idx != 0:
        camper_list.append(Camper(row[0], row[1], row[2]))
    else:
        # Set headers for output file
        csv_writer.writerow(generate_header_row())
camper_list_col1_options = []
camper_list_col2_options = []
camper_list_col3_options = []
camper_list_col4_options = []
camper_list_col5_options = []

for camper in camper_list:
    if camper.column == "1":
        camper_list_col1_options.append(camper)
    elif camper.column == "2":
        camper_list_col2_options.append(camper)
    elif camper.column == "3":
        camper_list_col3_options.append(camper)
    elif camper.column == "4":
        camper_list_col4_options.append(camper)
    elif camper.column == "5":
        camper_list_col5_options.append(camper)


def flatten_campers(campers_to_flatten):
    flattened_campers = []
    for unflattened_camper in campers_to_flatten:
        flattened_campers.append(unflattened_camper.nickname)
        flattened_campers.append(unflattened_camper.last_name)
    return flattened_campers


options_for_each_col = 5
boards = []
# Make as many boards as desired
for idx in range(number_of_boards_to_make):
    col1_final_names = flatten_campers(random.sample(camper_list_col1_options, options_for_each_col))
    col2_final_names = flatten_campers(random.sample(camper_list_col2_options, options_for_each_col))
    col3_final_names = flatten_campers(random.sample(camper_list_col3_options, options_for_each_col))
    col3_final_names[4] = "FREE"  # Replace middle of col3 with FREE
    col3_final_names[5] = "FREE"  # Replace middle of col3 with FREE
    col4_final_names = flatten_campers(random.sample(camper_list_col4_options, options_for_each_col))
    col5_final_names = flatten_campers(random.sample(camper_list_col5_options, options_for_each_col))
    csv_writer.writerow(col1_final_names + col2_final_names + col3_final_names + col4_final_names + col5_final_names)
csv_file.flush()
csv_output_file.flush()
csv_file.close()
csv_output_file.close()
