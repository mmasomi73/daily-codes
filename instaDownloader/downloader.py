from datetime import datetime
from itertools import takewhile, count

from instaloader import *

def dateCondition(date, st, end):
    # date = datetime.strptime(date, '%m/%d/%y %H:%M:%S')
    st_date = datetime.strptime(st, '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
    return (st_date <= date) & (end_date >= date)


# reminiscence10
# sabrinaflowerphoto
# 'chelseatea.r'
i_username = 'xxxxxxx'
i_passsword = 'xxxxxxx'

post_limiter = 3

L = instaloader.Instaloader()
L.login(i_username, i_passsword)
# aida = Post(L.context,'https://www.instagram.com/p/CLXBzLjgIjP/')
mlist = ['chelseatea.r', 'aksgrafy', 'myflowergm', 'sabrinaflowerphoto', 'reminiscence10','kyoko29kyokolily']
SINCE = '2021-02-18 0:0:0'
UNTIL = '2021-02-21 0:0:0'

for m in mlist:
    profile = Profile.from_username(L.context, m)
    i = 0
    posts = profile.get_posts()
    # for post in posts:
    #     print(post.date)
    print('----------------= Working On {} Page'.format(m))
    for post in takewhile(lambda p: dateCondition(p.date, SINCE, UNTIL), posts):
        # print(post.comments)
        L.download_post(post, target=profile.username)
        i += 1
        if i > post_limiter:
            break
