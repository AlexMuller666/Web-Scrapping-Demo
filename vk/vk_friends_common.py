import pandas as pd
import vk.vk_settings as settings

from time import sleep


def common_friends(id, ids, token_ranges, file_name, target_name):
    sleep(0.2)

    friends_ids = ','.join(str(elem) for elem in ids)

    person_id = id
    count = 50
    offset = 0

    params = {
        'source_uid': person_id,
        'target_uids': friends_ids,
        'count': count,
        'offset': offset,
        'v': 5.74,
        'access_token': token_ranges
    }

    common_dict = settings.get_vk_data('https://api.vk.com/method/friends.getMutual', params)

    id_list = []
    common_list = []
    common_count_list = []
    url_friends_list = []
    url_common_list = []

    for common in common_dict:
        url_common = []
        id_friend = common['id']
        url_friend = 'vk.com/id' + str(id_friend)

        id_commons = settings.try_except('common_friends', common)

        for id_common in id_commons:
            url = 'vk.com/id' + str(id_common)

            url_common.append(url)

        count_common = settings.try_except('common_count', common)

        id_commons = ', '.join(str(elem) for elem in id_commons)

        url_common = ', '.join(str(elem) for elem in url_common)

        id_list.append(id_friend)
        common_list.append(id_commons)
        common_count_list.append(count_common)
        url_friends_list.append(url_friend)
        url_common_list.append(url_common)

    path_common = settings.path + '/' + target_name + '/friends_common'

    settings.path_set(path_common)

    common_elems = {
        'id': id_list,
        'url id': url_friends_list,
        'common friends': common_list,
        'common count': common_count_list,
        'url common friends': url_common_list
    }

    common_to_csv = pd.DataFrame(data=common_elems)
    common_to_csv.to_csv(path_common + '/vk_common_friends.csv')

if __name__ == '__main__':
    common_friends()