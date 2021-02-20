from datetime import datetime
from instaloader import *
from itertools import dropwhile, takewhile


i_username = 'xxxxxxx'
i_passsword = 'xxxxxxx'

post_limiter = 3

L = instaloader.Instaloader()
L.login(i_username, i_passsword)

mlist = ['chelseatea.r','aksgrafy', 'myflowergm', 'sabrinaflowerphoto', 'reminiscence10']

SINCE = datetime(2021, 2, 18)
UNTIL = datetime(2015, 2, 21)

for m in mlist:
    profile = Profile.from_username(L.context, m)
    i = 0
    posts = profile.get_posts()
    for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, posts)):
        # print(post.comments)
        L.download_post(post, target=profile.username)
        i += 1
        if i >= post_limiter:
            break
