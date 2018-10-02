import sys
from collections import defaultdict
from datetime import datetime

import requests
from pytz import timezone, utc


def load_attempts():
    page = 1
    number_of_pages = 1
    api_url = "http://devman.org/api/challenges/solution_attempts/"

    while page <= number_of_pages:
        url_params = {"page": page}
        response = requests.get(api_url, params=url_params)
        attempts_info = response.json()
        solution_attempts = attempts_info["records"]
        number_of_pages = attempts_info["number_of_pages"]
        page += 1

        yield from solution_attempts


def get_midnighters(solution_attempts):
    datetime_format = "%Y-%m-%d %H:%M %Z%z"
    since_hour = 0
    until_hour = 5

    midnighters = defaultdict(list)

    for solution_attempt in solution_attempts:
        user_timezone = timezone(solution_attempt["timezone"])
        user_time = datetime.fromtimestamp(
            solution_attempt["timestamp"], user_timezone
        )

        if user_time.hour in range(since_hour, until_hour):
            midnighters[solution_attempt["username"]].append(
                user_time.strftime(datetime_format)
            )

    return midnighters


if __name__ == "__main__":
    try:
        midnighters = get_midnighters(load_attempts())
        for username, submission_times in midnighters.items():
            print(username)
            for submission_time in submission_times:
                print("\t" + submission_time)
    except requests.RequestException as error:
        sys.exit(error)
