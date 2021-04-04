import os
import re

path = 'files/'
ex_number = "02_"
counter = 0
for root, dirs, files in os.walk(path):
    for file in files:
        filename = re.findall("\s*9912358...*", file)
        if len(filename) > 0:
            new_file_name = "Ex_" + ex_number + filename[0].replace('-', '_').replace(' ', '')
            os.rename(path + file, path + new_file_name)
            print('\tRenamed file: {}'.format(new_file_name))
            counter += 1
print('----------------------------------------')
print('\t{} File Renamed!'.format(counter))
