import csv
import datetime
import sys

import dateutil
from dateutil import parser
import requests
from pytz import utc

api_url = "http://127.0.0.1:5000/players"
header = ['id', 'first_name', 'last_name', 'current_club', 'dob', 'nationality', 'last_modified', 'pull_time']


def write_all_players_csv(now, response):
    try:
        csv_file = open(r"players.csv", "r", encoding="UTF8")

        last_pulls = {}
        reader = csv.DictReader(csv_file, fieldnames=header)
        for row in reader:
            last_pulls[row['id']] = row['pull_time']

        csv_file.close()

        csv_file = open(fr"players.csv", "a+", encoding="UTF8", newline='')

        for entry in response.json():
            last_modified = entry['last_modified']
            last_modified = dateutil.parser.parse(last_modified)

            last_pull = last_pulls.get(f'{entry["id"]}', None)
            if last_pull:
                last_pull = dateutil.parser.parse(last_pull)

            if last_pull is None or last_modified > last_pull:
                writer = csv.DictWriter(csv_file, fieldnames=header)
                data = dict(entry)
                data['pull_time'] = f'{str(now)}'
                writer.writerow(data)

        csv_file.close()
    except FileNotFoundError:
        csv_file = open(r"players.csv", "w+", encoding="UTF8", newline='')
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writeheader()
        for entry in response.json():
            data = dict(entry)
            data['pull_time'] = f'{str(now)}'
            writer.writerow(data)
        csv_file.close()


def write_one_player_csv(now, response, player_id):
    last_modified = response.json()["last_modified"]
    last_modified = dateutil.parser.parse(last_modified)

    try:
        csv_file = open(fr"player_{player_id}.csv", "r", encoding="UTF8")
        reader = csv.DictReader(csv_file, fieldnames=header)

        for row in reader:
            last_pull = row['pull_time']

        last_pull = dateutil.parser.parse(last_pull)
        csv_file.close()

        if last_modified > last_pull:
            csv_file = open(fr"player_{player_id}.csv", "a+", encoding="UTF8", newline='')
            writer = csv.DictWriter(csv_file, fieldnames=header)
            data = dict(response.json())
            data['pull_time'] = f'{str(now)}'
            writer.writerow(data)
            csv_file.close()

    except FileNotFoundError:
        csv_file = open(fr"player_{player_id}.csv", "w+", encoding="UTF8", newline='')
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writeheader()
        data = dict(response.json())
        data['pull_time'] = f'{str(now)}'
        writer.writerow(data)
        csv_file.close()


if __name__ == '__main__':
    now = utc.localize(datetime.datetime.now())
    if len(sys.argv) == 2:
        response = requests.get(api_url + f"/{sys.argv[1]}")
        if response.status_code == 200:
            write_one_player_csv(now, response, sys.argv[1])
        else:
            print(response.text)
    else:
        response = requests.get(api_url)
        write_all_players_csv(now, response)
