import argparse
import random
import re
import time
import requests
import json

from prettytable import PrettyTable
from termcolor import colored

BASE_DIR = "./data"
HOME_URL = "https://h5.btime.com/Page/jd100challenge?mobile="
BASE_URL = "https://hezuo.btime.com"
INFO_URL = BASE_URL + "/user/getinfo/?mobile="
QUIZ_URL = BASE_URL + "/question/challenge/?mobile="
POST_URL = BASE_URL + "/question/challengeverify/"
PARAM = "&is_new=2"
NUM_QUESTIONS = 5

# INPUT YOUR COOKIE
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.77 Mobile Safari/537.36",
    "Cookie": "",
    "Host": "hezuo.btime.com",
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate, br",
    "Origin": "https://h5.btime.com",
    "Connection": "keep-alive",
    "Referer": "https://h5.btime.com/"
}


class QuizChallenger():
    def __init__(self, phone_number, interval_sec, rounds):
        self.phone_number = phone_number
        self.interval_sec = interval_sec
        self.rounds = rounds
        self.home_url = HOME_URL + phone_number
        self.info_url = INFO_URL + phone_number
        self.quiz_url = QUIZ_URL + phone_number + PARAM
        self.token = ''
        self.questions = {}
        self.question_id = []
        self.question_answers = []
        self.session = requests.session()

    def request_questions(self):
        try:
            response_home = self.session.get(self.home_url, timeout=20, headers=HEADERS)
            response_info = self.session.get(self.info_url, timeout=20, headers=HEADERS)
            self.questions = json.loads(self.session.get(self.quiz_url, timeout=20, headers=HEADERS).text)
            self.token = self.questions["data"]["token"]
            for question in self.questions["data"]["questions"]:
                self.question_id.append(question["question_id"])
            print(colored("Quiz is captured.\nQuestion sheet:"
                          "\n\tToken: {}\n\tQuestions: {}".format(self.token, self.question_id), "green"))
        except Exception:
            print(colored("Error in Request for questions!", "red"))

    def check_answers(self):
        with open(BASE_DIR+"/question_bank.json", "r", encoding="utf-8") as f:
            question_bank = json.load(f)
            for q_id in self.question_id:
                self.question_answers.append(question_bank[int(q_id) - 1]['correct'])
            print(colored("The answers are: {}".format(self.question_answers), "green"))

    def submit_sheet(self):
        data = []
        for index in range(5):
            data.append({
                "question_id": self.question_id[index],
                "type": "1" if index < 3 else "2",
                "answer": self.question_answers[index]
            })
        sheet = {
            "mobile": self.phone_number,
            "data": data,
            "token": self.token
        }
        print(colored("Waiting for submission...", "yellow"))
        time.sleep(20 + random.randint(0, 15))
        receipt = requests.post(url=POST_URL, headers=HEADERS, data=json.dumps(sheet))
        receipt_json = json.loads(receipt.text)
        print(colored("Status:{}, Message:{}".format(receipt_json["status"], receipt_json["msg"]), "green"))
        table = PrettyTable()
        table.field_names = ["Question ID", "Type", "Answer", "Is_correct"]
        for question in receipt_json["data"]["data"]:
            table.add_row([question["question_id"], question["type"], question["answer"], question["is_correct"]])
        print(colored(table, "green"))

    def run(self):
        for i in range(self.rounds):
            self.request_questions()
            self.check_answers()
            self.submit_sheet()
            time.sleep(self.interval_sec)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Following the CCP\'s Lead - Quiz Challenger')
    parser.add_argument('--phone_number', type=str, default="00000000000", help='Input your phone number.')
    parser.add_argument('--interval_sec', type=int, default=0,
                        help='Input the interval between two attempts.')
    parser.add_argument('--rounds', type=int, default=1, help='Input how many rounds in sum you would like to pass.')
    parser.add_argument("--daily-challenge", action='store_true', help='Use to do daily challenge.')
    args = parser.parse_args()

    for attempt in range(3):
        if re.match(r'1[3,4,5,7,8]\d{9}', args.phone_number):
            print(colored("Your phone number is valid.\nYour configurations:"
                          "\n\tAccount: {}\n\tRounds: {}\n\tInterval: {}s"
                          .format(args.phone_number, args.rounds, args.interval_sec), "green"))
            challenger = QuizChallenger(args.phone_number, args.interval_sec, args.rounds)
            print(colored("Quiz Challenger is starting...", "yellow"))
            challenger.run()
            break
        else:
            args.phone_number = input("Your phone number is illegal, please re-input:")
