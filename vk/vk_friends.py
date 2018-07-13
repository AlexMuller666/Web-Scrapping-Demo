import pandas as pd
import vk.vk_settings as settings

from time import sleep
from vk.vk_friends_common import common_friends


def main_friends(id, target_name, token_ranges, file_name):
    sleep(0.2)
    user_info = pd.read_csv(file_name, encoding='utf-8')

    person_id = id
    count = 50
    offset = 0

    fields = 'nickname, domain, sex, bdate, city, country, timezone, photo_50, photo_100, photo_200_orig, has_mobile, contacts, education, online, relation, last_seen, status, can_write_private_message, can_see_all_posts, can_post, universities'

    params = {
        'user_id': person_id,
        'order': 'hints',
        'count': count,
        'offset': offset,
        'fields': fields,
        'name_case': 'nom',
        'v': 5.74,
        'access_token': token_ranges
    }

    friends_dict = settings.get_vk_data('https://api.vk.com/method/friends.get', params)

    count = friends_dict['count']

    ids = []
    urls = []
    first_names = []
    last_names = []
    bdates = []
    cities = []
    countries = []
    universities = []
    faculties = []
    f_m = []

    similar_first_list = []
    similar_last_list = []
    similar_bdates_list = []
    similar_cities_list = []
    similar_countries_list = []
    similar_un_list = []
    similar_fac_list = []
    similar_f_m_list = []

    for friend in friends_dict['items']:
        if settings.try_except('first_name', friend) == 'DELETED' or settings.try_except('deactivated', friend) == 'deleted':
            print('Friend are DELETED', friend['id'])
            continue

        id_friend = friend['id']
        url_friend = 'vk.com/id' + str(id_friend)

        first_name = settings.try_except('first_name', friend)

        last_name = settings.try_except('last_name', friend)

        bdate = settings.try_except('bdate', friend)

        city = settings.try_except('city', friend)
        title_city = 'None'

        if city != 'None':
            title_city = city['title']

        country = settings.try_except('country', friend)
        title_country = 'None'

        if country != 'None':
            title_country = country['title']

        university = settings.try_except('university_name', friend)
        faculty = settings.try_except('faculty_name', friend)

        sex = settings.try_except('sex', friend)

        if len(bdate) < 6 and bdate != 'None':
            bdate = str(friend['bdate']) + ' year is unknown'

        if sex == 2:
            sex = 'Male'

        elif sex == 1:
            sex = 'Female'

        else:
            sex = 'Female'

        ids.append(id_friend)
        urls.append(url_friend)
        first_names.append(first_name)
        last_names.append(last_name)
        bdates.append(bdate)
        cities.append(title_city)
        countries.append(title_country)
        universities.append(university)
        faculties.append(faculty)
        f_m.append(sex)

        similar_search(similar_first_list, first_name, user_info.first_name_user)
        similar_search(similar_last_list, last_name, user_info.last_name_user)
        similar_search(similar_bdates_list, bdate, user_info.bdate_user)
        similar_search(similar_cities_list, title_city, user_info.city_user)
        similar_search(similar_countries_list, title_country, user_info.country_user)
        similar_search(similar_un_list, university, user_info.university_name_user)
        similar_search(similar_fac_list, faculty, user_info.faculty_name_user)
        similar_search(similar_f_m_list, sex, user_info.sex_user)

    path_friends = settings.path + '/' + target_name + '/friends'

    settings.path_set(path_friends)

    friends_elems = {
            'id': ids,
            'url friend': urls,
            'first name': first_names,
            'last name': last_names,
            'sex': f_m,
            'bdate': bdates,
            'city': cities,
            'country': countries,
            'university': universities,
            'faculty': faculties
    }

    friends_csv = pd.DataFrame(data=friends_elems)
    friends_csv.to_csv(path_friends + '/vk_friends_user_' + target_name + '.csv')

    path_friends_similar = settings.path + '/' + target_name + '/friends_similar'

    settings.path_set(path_friends_similar)

    friends_similar_csv = pd.DataFrame(data={
        'id': ids,
        'url friend': urls,
        'first name': similar_first_list,
        'last name': similar_last_list,
        'sex': similar_f_m_list,
        'bdate': similar_bdates_list,
        'city': similar_cities_list,
        'country': similar_countries_list,
        'university': similar_un_list,
        'faculty': similar_fac_list
    })

    friends_similar_csv.to_csv(path_friends_similar + '/friends_similar_user_' + target_name + '.csv')

    common_friends(person_id, ids, token_ranges, file_name, target_name)


def similar_search(similar_list, similar_item, user_info_item):
    similar = 'Similar' if user_info_item.item() == similar_item else 'No similar'

    similar_list.append(similar)


if __name__ == '__main__':
    main_friends()
