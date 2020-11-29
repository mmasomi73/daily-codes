import os
import csv

directories = os.listdir('Results/')
for directory in directories:
    entries = os.listdir('Results/{}/'.format(directory))
    for entry in entries:
        # print('Results/{}/{}'.format(directory, entry))
        file = open('Results/{}/{}'.format(directory, entry), 'r')
        row = []
        data = []
        for line in file:
            # print("{}\n".format(line.strip()))
            lists = line.strip().split("=")

            if len(lists) == 2:
                # if lists[0].find('Label Percentage') != -1:
                #     row.append(lists[1].strip())
                # elif lists[0].find('Final Accuracy') != -1:
                #     row.append(lists[1].strip())
                #
                # elif lists[0].find('Total Time') != -1:
                #     row.append(lists[1].strip())
                #     data.append(row)
                #     row = []
                if lists[0].find('Label Percentage') != -1:
                    row.append(lists[1].strip())
                elif lists[0].find('Final Time') != -1:
                    row.append(lists[1].strip())

                elif lists[0].find('Final Accuracy') != -1:
                    row.append(lists[1].strip())
                    data.append(row)
                    row = []

        name = entry.split('.')
        CHECK_FOLDER = os.path.isdir('res/' + directory)
        if not CHECK_FOLDER:
            os.makedirs('res/' + directory)
        with open('res/' + directory + '/' + name[0] + '.csv', mode='w+', newline='') as data_file:
            data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for row in data:
                if len(row) > 0:
                    data_writer.writerow(row)

        file.close()

    # ------------------------------ Write Data
    entries = os.listdir('res/{}/'.format(directory))
    iteration = 1
    acc = []
    time = []
    acc.append([1, 5, 10, 20, 30, 100])
    time.append([1, 5, 10, 20, 30, 100])
    for entry in entries:
        file = open('res/' + directory + '/' + entry, 'r')
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

    acc_name = '{}-Accuracy'.format(directory)
    time_name = '{}-Time'.format(directory)

    with open('res/' + time_name + '.csv', mode='w+', newline='') as data_file:
        data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in time:
            if len(row) > 0:
                data_writer.writerow(row)

    with open('res/' + acc_name + '.csv', mode='w+', newline='') as data_file:
        data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in acc:
            if len(row) > 0:
                data_writer.writerow(row)

