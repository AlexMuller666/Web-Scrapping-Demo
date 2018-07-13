import pandas as pd
import re
import vk.vk_settings as settings

from time import sleep


def main_group(id, name, path_name, token_ranges):
    group_id = '-' + str(id)
    offset = 0
    count = 50

    reg = re.compile('[^a-zA-Zа-яА-Я]')

    all_posts = []

    sleep(0.2)

    params = {
            'owner_id': group_id,
            'count': count,
            'offset': offset,
            'v': 5.52,
            'access_token': token_ranges
    }

    posts_dict = settings.get_vk_data('https://api.vk.com/method/wall.get', params)

    all_posts.append(posts_dict)

    id_list = []
    likes_list = []
    reposts_list = []
    text_list = []
    url_material_list = []

    top_likes = 0
    top_likes_id = 0
    top_likes_reposts = 0
    top_likes_text = ''
    top_likes_url_material = ''

    for post in all_posts:
        try:
            url = post['items'][0]['attachments'][0]['link']
            url = url['url']

        except:
            url = 'None'

        if (post['items'][0]['likes']['count']) > top_likes:
            top_likes = post['items'][0]['likes']['count']
            top_likes_id = post['items'][0]['id']
            top_likes_reposts = post['items'][0]['reposts']['count']
            top_likes_text = post['items'][0]['text']
            top_likes_url_material = url

        try:
            post_id = post['items'][0]['id']

        except:
            post_id = 0

        try:
            likes = post['items'][0]['likes']['count']

        except:
            likes = 'zero'

        try:
            reposts = post['items'][0]['reposts']['count']

        except:
            reposts = 'zero'

        try:
            text = post['items'][0]['text']

        except:
            text = '*******'

        id_list.append(post_id)
        likes_list.append(likes)
        reposts_list.append(reposts)
        text_list.append(text.replace('\n', ' ').strip())
        url_material_list.append(url)

    group_csv = pd.DataFrame(data={
        'id': id_list,
        'likes': likes_list,
        'reposts': reposts_list,
        'text': text_list,
        'url material': url_material_list
    })

    top_likes_csv = pd.DataFrame(data={
        'top likes': [top_likes],
        'id top pos': [top_likes_id],
        'reposts top pos': [top_likes_reposts],
        'text top pos': [top_likes_text.replace('\n', ' ').strip()],
        'url material': [top_likes_url_material]
    })

    name_correct = reg.sub('', name)

    path_group = path_name + '/' + name_correct
    path_group_likes = path_name + '/' + name_correct + '/top_likes'

    settings.path_set(path_group)
    settings.path_set(path_group_likes  )

    group_csv.to_csv(path_group + '/vk_group_' + name_correct + '.csv')
    top_likes_csv.to_csv(path_group_likes + '/vk_top_likes_' + name_correct + '.csv')


if __name__ == '__main__':
    main_group()
