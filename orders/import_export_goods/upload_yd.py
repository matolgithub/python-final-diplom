import os
from orders.settings import BASE_DIR
import requests
from datetime import datetime


# Upload method photos getting from aplications move to Disk.Yandex
# https://disk.yandex.ru/d/FNp_7YIE7GJN-Q - link to result folder in Disk.Yandex
def upload_data():
    """This is the upload method photos getting from aplications move to Disk.Yandex."""
    with open('token_yd.txt', 'r') as file:
        token_ya = file.read().strip()
    time_start = datetime.now()
    folder_path = f"{BASE_DIR}/import_export_goods/export_files"
    file_path = os.listdir(folder_path)
    count_files = 0
    count_percent = 0
    for item in file_path:
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {token_ya}'}
        params = {'path': f'diplom_export_yd/{item}', 'overwrite': 'true'}
        response = requests.get(upload_url, params=params, headers=headers)
        href_json = response.json()
        data = {"file": open(f'{folder_path}/{item}', "rb")}
        _ = requests.post(url=href_json['href'], files=data)
        count_files += 1
        count_percent += round((100 / len(file_path)), 5)
        print("*" * 10, f' {count_percent}% ', end='')
    time_end = datetime.now()
    period = time_end - time_start
    print(f"\nCopying files to Disk.Yandex - complete! Start: {time_start}, end: {time_end}, total run time: {period}.")


if __name__ == "__main__":
    upload_data()
