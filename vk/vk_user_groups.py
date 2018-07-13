import pandas as pd
import vk.vk_group as groups
import vk.vk_settings as settings

from time import sleep


def main_user_groups(id, target_name, token_ranges):
    sleep(0.2)

    path_friends_similar = settings.path + '/' + target_name + '/groups'

    settings.path_set(path_friends_similar)

    person_id = id
    fields = 'city, country, place, description, wiki_page, members_count, counters, start_date, finish_date, can_post, can_see_all_posts, activity, status, contacts, links, fixed_post, verified, site, can_create_topic'
    offset = 0
    count = 5

    params = {
        'user_id': person_id,
        'extended': True,
        'filter': 0,
        'fields': fields,
        'offset': offset,
        'count': count,
        'v': 5.74,
        'access_token': token_ranges
    }

    user_groups = settings.get_vk_data('https://api.vk.com/method/groups.get', params)

    id_list = []
    name_list = []
    url_list = []
    admin_list = []
    member_list = []
    type_list = []

    for group in user_groups['items']:
        id = group['id']
        name = group['name']
        url = 'vk.com/' + str(group['screen_name'])
        admin = 'Yes'
        member = 'Yes'
        type = 'Open'

        if group['is_admin'] is 0:
            admin = 'No'

        if group['is_member'] is 0:
            member = 'No'

        if group['is_closed'] is 1:
            type = 'Closed'

        id_list.append(id)
        name_list.append(name)
        url_list.append(url)
        admin_list.append(admin)
        member_list.append(member)
        type_list.append(type)

        groups.main_group(id, name, path_friends_similar, token_ranges)

    user_groups_csv = pd.DataFrame(data={
        'id': id_list,
        'name': name_list,
        'url': url_list,
        'user is admin': admin_list,
        'user is member': member_list,
        'type group': type_list
    })

    user_groups_csv.to_csv(path_friends_similar + '/vk_user_groups_' + target_name + '.csv')


if __name__ == '__main__':
    main_user_groups()