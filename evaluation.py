import requests

from LogWriter import LogWriter

API_URL = "http://127.0.0.1:5000/players/"
SINGLE_INGEST_FILENAME = "log_single.txt"
LIST_INGEST_FILENAME = "log_list.txt"
LAST_PULL_FILENAME = "log_time.txt"
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
FIELD_NAMES = ["id",
               "first_name",
               "last_name",
               "current_club",
               "nationality",
               "date_of_birth",
               "preferred_position",
               "last_modified"]


def main():
    lws = LogWriter(SINGLE_INGEST_FILENAME, LAST_PULL_FILENAME, FIELD_NAMES, TIME_FORMAT)
    lwl = LogWriter(LIST_INGEST_FILENAME, LAST_PULL_FILENAME, FIELD_NAMES, TIME_FORMAT)
    while True:
        try:
            a = int(input('Enter 0 for exit, 1 for single pull, 2 for list pull: '))
            if a == 1:
                getid = int(input('Enter id: '))
                r = requests.get(API_URL + str(getid))
                list_of_dicts = [r.json()]
                lws.write_to_file(list_of_dicts)
            elif a == 2:
                r = requests.get(API_URL + "list")
                list_of_dicts = r.json()["players"]
                lwl.write_to_file(list_of_dicts)
            else:
                exit(0)
        except ValueError:
            print('Please only input digits')


if __name__ == "__main__":
    main()
