import os
from tqdm import tqdm
import requests as req
from bs4 import BeautifulSoup as bs
import progressbar


def main(file_index, link):
    print("initialing Connection to apart URL ...")
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
    print("fetching download list ...")
    i = 1
    for name, videoLink in links.items():
        origin_url = videoLink.split("?")[0]
        file_name = origin_url.split('/')[4]
        r = req.get(videoLink, stream=True)
        # -------------------------------------
        total_size_in_bytes = int(r.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, ncols=75, ascii=True)

        CHECK_FOLDER = os.path.isdir('Videos/' + main_name.decode('utf-8'))
        if not CHECK_FOLDER:
            os.makedirs('Videos/' + main_name.decode('utf-8'))

        with open('Videos/{}/{:03d}_{}.mp4'.format(main_name.decode('utf-8'), i, name.decode('utf-8')), 'wb') as f:
            for data in r.iter_content(block_size):
                progress_bar.set_description("\tDownload {}/{} file:{}".format(i, len(links.items()), file_name))
                progress_bar.update(len(data))
                f.write(data)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("ERROR, something went wrong")

        # -------------------------------------
        i += 1


if __name__ == "__main__":
    links_file = open('links.txt', 'r', encoding="utf-8")
    quality = "720"
    itr = 0
    for pls_link in links_file:
        print("\n---------------------------------------")
        print('working on List {}'.format(pls_link))
        itr += 1
        main(itr, pls_link)
