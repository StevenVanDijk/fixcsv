import csv
import glob

# utility function to loop over csv files and invoke a function for each one
def for_all_csv(executeBeforeOpenFile, executeWithReader):
    for filename in glob.iglob("*.csv"):
        if (filename == "output.csv"):
            print("Skipping output.csv")
            continue
        executeBeforeOpenFile(filename)
        with open(filename,newline='') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',', quotechar='"', skipinitialspace=True)
            executeWithReader(reader, filename)

try:
    columns = set()
    for_all_csv(
        lambda filename: print(f"Scanning {filename} for columns"),
        lambda reader, filename: [columns.add(i) for i in reader.fieldnames]
    )

    if not columns:
        raise Exception("Did not find any columns, aborting")
    else:
        print(f"Using columns {columns}")

    total_data = []
    def collectrows(reader, filename):
        for row in reader:
            converted_row = dict.fromkeys(columns,'')
            for field in row:
                if field not in converted_row.keys():
                    raise Exception("Illegal field %s in file %s" % (field, filename))
                converted_row[field] = row[field]
            total_data.append(converted_row)

    for_all_csv(
        lambda filename: print(f"Processing {filename} and collecting rows"),
        collectrows
    )   

    print("All files read, writing to output.csv")
    with open('output.csv', 'w',newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(total_data)
except:
    print(
        """
        Something went wrong. Check: 
        1) all input files have extension csv and are in the current working directory
        2) the output file output.csv is writable
        """)
    print("The exception thrown was:\n")
    raise
