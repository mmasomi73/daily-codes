import os
import codecs

# rename files in a directory /captivate to their original names

# 1- read all original names from titles.txt
titles = []
with codecs.open("titles.txt", "r", "utf-8") as f:
    lines = f.readlines()
    titles = []
    for line in lines:
        titles.append(line.strip())

# 2- read all download_links.txt file line by line
index = 0
with codecs.open("download_links.txt", "r", "utf-8") as f:
    lines = f.readlines()
    for line in lines:
        # 2-1- separate filename from url
        url = line.split("?")[0]
        filename = url.split("/")[-1]

        # 3- rename file
        os.rename("captivate/" + filename, "captivate/" + titles[index] + ".mp4")
        index += 1