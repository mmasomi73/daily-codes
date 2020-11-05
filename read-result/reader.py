import os
import csv

entries = os.listdir('outs/')
for entry in entries:
    file = open('outs/'+entry, 'r')
    row = []
    data = []
    for line in file:
        # print("{}\n".format(line.strip()))
        lists = line.strip().split("=")

        if len(lists) == 2:
            if lists[0].find('Label Percentage') != -1:
                row.append(lists[1].strip())
            elif lists[0].find('Final Time') != -1:
                row.append(lists[1].strip())
            elif lists[0].find('Final Accuracy') != -1:
                row.append(lists[1].strip())
                data.append(row)
                row = []
    name = entry.split('.')
    with open('res/'+name[0]+'.csv', mode='w+', newline='') as data_file:
        data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for row in data:
            if  len(row) > 0:
                data_writer.writerow(row)

    file.close()

