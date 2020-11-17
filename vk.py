import requests
import time
from datetime import date, datetime
import json
from db import datingdb as db

token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'

params = {
    'access_token': token,
    'v': 5.124
}

# Информация о пользователе

def get_user_info():
    print('-')
    params['fields'] = ['sex, city, bdate, music, books, interests']
    user_info = (requests.get(
        'https://api.vk.com/method/users.get', params)).json()['response'][0]
    print(user_info)
    return user_info

# Вычисляем возраст пользователя

def calculate_age_user(bdate):
    today = date.today()
    age = today.year - bdate.year
    if today.month < bdate.month:
        age -= 1
    elif today.month == bdate.month and today.day < bdate.day:
        age -= 1

    return age

# Устанавливаем параметры (город, пол, возрастной диапозон) поиска и запускаем поиск

def search_users(user_info):
    try:
        city_id = user_info['city']['id']
    except KeyError:
        print("У подьзователя не указан id городa")
        city_id = int(input('Введите id города: '))

    sex = 2 if user_info['sex'] == 1 else 1

    try:
        bdate_str = user_info['bdate']
        bdate = datetime.strptime(bdate_str, "%d.%m.%Y")
        age = calculate_age_user(bdate)
        age_from = age - 2
        age_to = age + 2
    except (KeyError, ValueError):
        print("У подьзователя не указан год рождения")
        age = int(input('Введите ваш возраст: '))
        age_from = age - 2
        age_to = age + 2

    params['age_from'] = [age_from]
    params['age_to'] = [age_to]
    params['count'] = [1000]
    params['city'] = [city_id]
    params['sex'] = [sex]
    params['status'] = [1, 6]

    response = requests.get('https://api.vk.com/method/users.search', params)
    search_info = response.json()['response']['items']

    search_list = []
    for item in search_info:
        search_list.append(item['id'])
        
    #Убираем совпадения с прошлыми результатами
    list_ids_saved_to_db = []
    list_users_saved_to_db = list(db['users'].find())

    for user_saved in list_users_saved_to_db:
        list_ids_saved_to_db.append(user_saved.get('id'))

    update_search_list = list(set(search_list) - set(list_ids_saved_to_db))

    #Получаем отфильтрованный результат поиска
    update_search_info = []
    for item_list in update_search_list:
        for item in search_info:
            if item_list == item['id']:
                update_search_info.append(item)

    return update_search_info

# функция запроса списка сообществ пользователя

def get_user_groups():
    response = requests.get('https://api.vk.com/method/groups.get', params)
    print('-')
    groups_list = response.json()#['response']['items']

    return groups_list

# функция запроса списка друзей пользователя

def get_user_friends():
    response = requests.get('https://api.vk.com/method/friends.get', params)
    print('-')
    friends_list = response.json()['response']['items']

    return friends_list

# У пользователей собираем список групп и сравниваем с группами основного пользователя
# записываем в новый словарь совпадения

def compare_groups(users_list):
    result = []
    user_list_groups = get_user_groups()

    for user in users_list:
        params['user_id'] = user['id']
        groups_list = get_user_groups()
        for key in groups_list:
            if key == 'response':
                
                user_coincidences = {
                    'id': user['id'],
                    'matching_groups': [],
                    'number_matching_groups': 0
                }
                for group in groups_list:
                    if group in user_list_groups:
                        user_coincidences['matching_groups'].append(group)
                    user_coincidences['number_matching_groups'] = len(
                        user_coincidences['matching_groups'])

                result.append(user_coincidences)
                time.sleep(0.3)

    return result

# сортировка по кол-ву совпавших групп

def find_top10(list):
    users_sorted = sorted(list, key=lambda x: x['number_matching_groups'])

    top10_users = users_sorted[len(users_sorted) - 10:len(users_sorted)]

    return top10_users

# cортировка топ3 фото

def find_top3(list):
    photos_sorted = sorted(list, key=lambda x: x['likes']['count'])

    top3_photos = photos_sorted[len(photos_sorted) - 3:len(photos_sorted)]

    return top3_photos

# у топ-10 запрашиваем фото и ищем топ3 фото

def find_top3_photos(top10_users):
    for user in top10_users:
        params['user_id'] = user['id']
        params['album_id'] = ['profile']
        params['extended'] = [1]

        response = requests.get('https://api.vk.com/method/photos.get', params)
        profile_photos = response.json()['response']['items']

        top3 = find_top3(profile_photos)
        user['top3_photos'] = top3

        time.sleep(0.3)

    return top10_users

#  подготавливаем данные для записи

def create_output_file(top10_users):
    output = []

    for user in top10_users:

        user_vk = {
            'vk_link': f"https://vk.com/id{user['id']}",
            'photos': []
        }

        for photo in user['top3_photos']:
            user_vk['photos'].append(photo['sizes'][-1]['url'])

        output.append(user_vk)

    return output

# записываем результат в файл JSON

def write_output_file(output):
    with open('top_users.json', 'w') as json_file:
        data = json.dumps(output, sort_keys=False, indent=4,
                          ensure_ascii=False, separators=(',', ': '))

        json_file.write(data)
        db['users'].insert_many(output)
