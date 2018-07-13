import re
import pandas as pd
import vk.vk_friends as friends
import vk.vk_user_groups as user_groups
import vk.vk_settings as settings
import random


class VkMain:
    def __init__(self, page_ranges):
        token_ranges = (random.choice(settings.token))

        path = settings.path

        settings.path_set(path)

        reg = re.compile('[^a-zA-Zа-яА-Я]')

        fields = 'photo_id, verified, sex, bdate, city, country, home_town, has_photo, photo_50, photo_100, photo_200_orig, photo_200, photo_400_orig, photo_max, photo_max_orig, online, domain, has_mobile, contacts, site, education, universities, schools, status, last_seen, followers_count, common_count, occupation, nickname, relatives, relation, personal, connections, exports, wall_comments, activities, interests, music, movies, tv, books, games, about, quotes, can_post, can_see_all_posts, can_see_audio, can_write_private_message, can_send_friend_request, is_favorite, is_hidden_from_feed, timezone, screen_name, maiden_name, crop_photo, is_friend, friend_status, career, military, blacklisted, blacklisted_by_me'

        params = {
            'user_ids': page_ranges,
            'fields': fields,
            'name_case': 'Nom',
            'v': 5.74,
            'access_token': token_ranges
        }

        person_dict = settings.get_vk_data('https://api.vk.com/method/users.get', params)

        id = settings.try_except('id', person_dict[0])
        first_name = settings.try_except('first_name', person_dict[0])
        last_name = settings.try_except('last_name', person_dict[0])
        bdate = settings.try_except('bdate', person_dict[0])
        city = settings.try_except('city', person_dict[0])
        city_title = 'None'

        if city != 'None':
            city_title = city['title']

        url_name = settings.try_except('screen_name', person_dict[0])
        url = 'vk.com/' + str(url_name)

        country = settings.try_except('country', person_dict[0])
        country_title = 'None'

        if country != 'None':
            country_title = country['title']

        followers = settings.try_except('followers_count', person_dict[0])

        company = settings.try_except('career', person_dict[0])
        company_name = 'None'

        if company:
            company_name = company[0]['company']

        company_position = settings.try_except('career', person_dict[0])
        company_pos = 'None'

        if company_position:
            company_pos = company_position[0]['position']

        university_name = person_dict[0]['university_name']
        faculty_name = person_dict[0]['faculty_name']
        music = person_dict[0]['music']
        sex = person_dict[0]['sex']

        if sex == 1:
            sex = 'Female'

        elif sex == 2:
            sex = 'Male'

        else:
            sex = 'None'

        path_user = path + '/' + str(url_name)

        settings.path_set(path_user)

        person_csv = pd.DataFrame(data={
            'id_user': [id],
            'url_user': [url],
            'first_name_user': [first_name],
            'last_name_user': [last_name],
            'bdate_user': [bdate],
            'city_user': [city_title],
            'country_user': [country_title],
            'followers_user': [followers],
            'company_user': [company_name],
            'company_position_user': [company_pos],
            'university_name_user': [university_name],
            'faculty_name_user': [faculty_name],
            'music_user': [music],
            'sex_user': [sex]
        })

        correct_user = reg.sub('', str(url_name))

        file_name = path + '/' + str(url_name) + '/vk_user_' + correct_user + '.csv'

        person_csv.to_csv(file_name)

        friends.main_friends(str(id), url_name, token_ranges, file_name)
        user_groups.main_user_groups(str(id), url_name, token_ranges)


if __name__ == '__main__':
    app = VkMain()