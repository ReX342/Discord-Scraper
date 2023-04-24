import csv
import json

data = []

# Read messages.csv file and create the list of dictionaries
with open('messages.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    prev_comment = ''
    for row in reader:
        if row:
            comment = row[2].strip()
            if comment and 'http' not in comment:  # filter out comments with URLs
                if prev_comment:
                    data.append({"prompt": prev_comment, "completion": comment})
                prev_comment = comment

# Write the list of dictionaries to a JSON file
with open('output.json', 'w', encoding='utf-8') as file:
    for i, d in enumerate(data):
        json.dump(d, file, ensure_ascii=False)
        if i < len(data) - 1:
            file.write('\n')
