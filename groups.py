from API import access_token, v
from time import sleep
import csv
import requests

groups = ["hse_university", "thevyshka", "hse_case_school", "iqhse", "hseofficial"]


def get_group_members(group):  # groups/{group}.csv (id, last_name + first_name
    global access_token, v
    count = 1000
    params = {
        'access_token': access_token,
        'v': v,
        'group_id': group,
        'sort': 'id_asc',
        'offset': 0,
        'count': count,
        'fields': 'description'
    }
    response = requests.get('https://api.vk.com/method/groups.getMembers', params=params).json()
    print(group, 'upload_members')
    sleep(0.334)
    path = 'C:/Users/User/PycharmProjects/Culture_Centre/groups/{group}.csv'.format(group=group)
    file = open(path, 'w', newline='', encoding='utf-8')
    writer = csv.writer(file)
    for offset in range(0, response['response']['count'], count):
        params['offset'] = offset
        print(round(offset / response['response']['count'] * 100, 3), '%')
        response = requests.get('https://api.vk.com/method/groups.getMembers', params=params).json()
        sleep(0.334)
        for item in response['response']['items']:
            if not item.get('deactivated'):
                if not item['is_closed']:
                    data = [item['id'], item['first_name'] + ' ' + item['last_name']]
                    writer.writerow(data)
    file.close()


for group in groups:
    get_group_members(group)