import argparse
import requests
import json
import os.path
from termcolor import colored

QB_URL = "https://hezuo.btime.com/question/getquestion?page="
PAGES = 40
BASE_DIR = "./data"


def download_raw_answers():
    questionBank = []
    for page in range(PAGES):
        try:
            source = requests.get(QB_URL + str(page + 1), timeout=20)
            questionBank += json.loads(source.text)["data"]["data"]
            print(colored("Page {} loaded".format(page+1), "yellow"))
        except Exception:
            return 0

    print(colored("Writing to the file...", "green"))
    with open(BASE_DIR + "/question_bank.json", "w", encoding="utf-8") as f:
        json.dump(
            questionBank,
            f,
            indent=4,
            separators=(',', ': '),
            sort_keys=False,
            ensure_ascii=False
        )
    print(colored("Done!", "green"))


download_raw_answers()
