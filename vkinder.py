import requests
import time
from datetime import date, datetime
import vk


def start_program():
    # спрашиваем у пользователя ник или id аккаунта, записываем в параметры запроса
    account = input('Введите id аккаунта или ник: ')
    try:
        vk.params['user_id'] = int(account)
    except ValueError:
        print("введен ник")
        vk.params['screen_name'] = account

    user_info = vk.get_user_info()
    user_id = user_info['id']
    users = vk.search_users(user_info)
    result = vk.compare_groups(users)
    top10_users = vk.find_top10(result)
    top10_users_with_photos = vk.find_top3_photos(top10_users)
    final_list = vk.create_output_file(top10_users_with_photos)
    vk.write_output_file(final_list)


if __name__ == '__main__':
    start_program()
