# -*- encoding=utf-8 -*-
# Author: Qi Lu (luqi.code@gmail.com)

from question import Question

with open("./question_url_list") as f:
    for line in f:
        line = line.strip()
        q = Question(line.split("/")[-1])
        print q.get_question_info()
