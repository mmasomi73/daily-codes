import os
import csv

entries = os.listdir('res/')
iteration = 1
acc = []
time = []
acc.append([1, 5, 10, 20, 30, 100])
time.append([1, 5, 10, 20, 30, 100])
for entry in entries:
    file = open('res/' + entry, 'r')
    row_acc = []
    row_time = []

    for line in file:
        # print("{}\n".format(line.strip()))
        lists = line.strip().split(",")
        if len(lists) > 0:
            row_time.append(lists[1].strip())
            row_acc.append(lists[2].strip())

    acc.append(row_acc)
    time.append(row_time)
    file.close()

acc_name = 'Accuracy'
time_name = 'Time'

with open('out/' + time_name + '.csv', mode='w+', newline='') as data_file:
    data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in time:
        if len(row) > 0:
            data_writer.writerow(row)

with open('out/' + acc_name + '.csv', mode='w+', newline='') as data_file:
    data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in acc:
        if len(row) > 0:
            data_writer.writerow(row)
