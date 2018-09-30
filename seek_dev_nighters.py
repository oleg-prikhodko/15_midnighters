import json
import sys
from datetime import datetime
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from pytz import timezone, utc


def load_attempts():
    page = 1
    number_of_pages = 1
    api_url = "http://devman.org/api/challenges/solution_attempts/?"

    while page <= number_of_pages:
        url_params = {"page": page}
        response = urlopen(api_url + urlencode(url_params))
        attempts_info = json.loads(response.read())
        solution_attempts = attempts_info["records"]
        number_of_pages = attempts_info["number_of_pages"]
        page += 1

        yield from solution_attempts


def get_midnighters():
    datetime_format = "%Y-%m-%d %H:%M %Z%z"
    since_hour = 0
    until_hour = 5

    for solution_attempt in load_attempts():
        user_timezone = timezone(solution_attempt["timezone"])
        utc_time = datetime.fromtimestamp(solution_attempt["timestamp"], utc)
        user_time = utc_time.astimezone(user_timezone)

        if user_time.hour in range(since_hour, until_hour):
            yield solution_attempt["username"], user_time.strftime(
                datetime_format
            )


if __name__ == "__main__":
    try:
        for midnighter, submission_time in get_midnighters():
            print(midnighter, submission_time)
    except URLError as error:
        sys.exit(error)
