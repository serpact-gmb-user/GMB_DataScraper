"""with open(end_csv_file_name, 'r') as final_empty:
    with open(csv_file_name, 'w') as output_data:
        writer = csv.writer(output_data, lineterminator='\n')
        reader = csv.reader(final_empty)

        data_output = []
        row = next(reader)
        # row.append('Date')
        # row.append('Group')
        # row.append('Project')
        data_output.append(row)

        for row in reader:
            data_output.append(row)"""

# Filter the data in initial .csv file before parsing process.
"""for row in reader:
    new_row = []
    for i in row:
        if i not in values_to_remove:
            num_matching_value = re.split("\s", i, 1)
            if re.findall(regEx, num_matching_value[0]):
                del num_matching_value[0]
                # new_row.append(num_matching_value[0])

    # Append data into .csv file row by row.
    csv.writer(open(new_csv_file_name, 'a')).writerow(new_row)
    messagebox.showinfo("Second Wait!")

# Force close reader sessions of initial .csv file.
del reader

# Create an emtpy .csv file to store the filtered data.
with open(final_csv_file_name, 'w') as my_empty_csv:
    pass

# Populate new .csv file with filtered data, NO headers included.
with open(new_csv_file_name) as input_file, open(final_csv_file_name, 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    logger.info(
        f"Create {new_csv_file_name} and pass it as input file; create {final_csv_file_name} and pass it as output file")
    for row in csv.reader(input_file):
        if any(field.strip() for field in row):
            writer.writerow(row)

# Read result .csv file, split first column data into two columns.
with open(final_csv_file_name) as file_to_read:
    lines = file_to_read.readlines()
    logger.info(f"Read contents of {final_csv_file_name} file before final filtering of data")

for line in range(len(lines)):
    # Stripping lines of whitespace characters/tabs; splitting string into a list of elements.
    output = lines[line].replace("\n", "")
    list_output = re.split("\s", output)

    # Add two additional columns to final_csv_file_name -- Keyword, Search times,
    # Date (dd-MM-yyyy), Project name (GMB Data Scraper), Location, Location Group, URL Weblink
    # Obtain keyword values and appearance time from split list, append values to global lists.
    keywords = " ".join(list_output[:-1])
    logger.info(f"Current keyword element after filtering: {keywords}")
    times = list_output[-1]
    logger.info(f"Current search time count after filtering: {times}")
    gl_keywords_list.append(keywords)
    gl_times_list.append(times)

# Saving values to EndCSVFileName.csv file
np.savetxt(end_csv_file_name, np.c_[gl_keywords_list, gl_times_list], fmt='%s', delimiter=",")
logger.info(f"Insert all filtered and parsed data into {end_csv_file_name}")

with open(end_csv_file_name, 'r', newline="") as file_to_read:
    r = csv.reader(file_to_read)
    data = [line for line in r]

with open(end_csv_file_name, 'w', newline="") as file_to_write:
    w = csv.writer(file_to_write)
    w.writerow(['Keywords', 'Search times', 'Location', 'Location group', 'URL Address'])
    w.writerows(data)
"""