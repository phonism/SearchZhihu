# -*- encoding=utf-8 -*-
# Author: Qi Lu (luqi.code@gmail.com)

import sys
import os
from question import Question

question_list = {}

with open("./question_url_list") as f:
    for line in f:
        line = line.strip()
        question_list[line] = 1

os.system("rm -rf data")
os.system("mkdir data")

for question in question_list:
    question_id = question.split("/")[-1]
    q = Question(question_id)
    os.system("mkdir data/" + question_id)
    answer_list = q.get_answer_list()
    for cnt in range(len(answer_list)):
        f = open("data/" + question_id + "/" + str(cnt), "w+")
        f.write(answer_list[cnt])
        f.close()
