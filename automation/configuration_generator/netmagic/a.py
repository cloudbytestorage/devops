import csv

count = 0
with open('smoketest.csv', 'rb') as f:
    mycsv = csv.reader(f)
    for row in mycsv:
        if count == 1:
            text = row[1]
            print text
            break
        count = count + 1
