import io
import argparse
import requests as req
from bs4 import BeautifulSoup as bs
import progressbar


def main(file_index, link):
    print("Please wait...")
    mainPage = req.get(link).content
    main_soup = bs(mainPage, 'html.parser')
    main_name = main_soup.find("span", attrs={"class": "d-in v-m"}).text.encode()

    playlist = main_soup.find('div', attrs={'class': 'playlist-body'})
    playListLinks = playlist.find_all('a', attrs={'class': 'title'})

    video_pages = [f"https://www.aparat.com{video.get('href')}" for video in playListLinks]
    count = len(video_pages)
    print(f"This playlist contains {count} videos")

    bar = progressbar.ProgressBar(maxval=count,
                                  widgets=[progressbar.Bar('=', '[', ']'), progressbar.Percentage()])
    bar.start()

    links = {}
    for index, page in enumerate(video_pages):
        bar.update(index + 1)
        html = req.get(page).content
        soup = bs(html, 'html.parser')
        name = soup.find("h1", attrs={"id": "videoTitle", "class": "title"}).text.encode()
        qualitys = soup.find('div', attrs={'class': 'dropdown-content'}).find_all('a')
        # TODO change this method
        for qual in qualitys:
            if quality in qual.get('aria-label'):
                links[name] = qual.get('href')
            elif "480" in qual.get('aria-label'):
                links[name] = qual.get('href')
    bar.finish()
    print("writing download list ...")

    with io.open('download_links_{}.txt'.format(file_index), "a", encoding="utf-8") as file:
        file.write("\n-----------------------=\n{}\n-----------------------=\n\n".format(main_name.decode('utf-8')))
        i = 1
        for name, videoLink in links.items():
            file.write('{}\n'.format(videoLink))
            i += 1
    with io.open('link_names_{}.txt'.format(file_index), "a", encoding="utf-8") as file:
        i = 1
        for name, videoLink in links.items():
            origin_url = videoLink.split("?")[0]
            file_name = origin_url.split('/')[4]
            file.write('{}|{:03d}_{}.mp4\n'.format(file_name, i, name.decode('utf-8')))
            i += 1
            # print(file_name)


if __name__ == "__main__":
    pls_links = [
        "https://www.aparat.com/v/n0Bot?playlist=574915",
        "https://www.aparat.com/v/YzTe7?playlist=623287"

    ]
    quality = "720"
    itr = 0
    for pls_link in pls_links:
        print('working on List {}'.format(pls_link))
        itr += 1
        main(itr, pls_link)
