import os


def remaner(link_names_file):
    files = os.listdir('Videos/')
    if len(files) == 0:
        print('Videos Directory is Empty!!!')
        return
    names = open(link_names_file, 'r', encoding="utf-8")
    for line in names:
        name = line.strip().split("|")
        old_name = name[0]
        new_name = name[1]
        if os.path.exists('Videos/{}'.format(old_name)):
            os.rename('Videos/{}'.format(old_name), 'Videos/{}'.format(new_name))


link_names = [
        "link_names_1.txt",
        "link_names_2.txt"
    ]
quality = "720"
itr = 0
for link_name in link_names:
    remaner(link_name)
