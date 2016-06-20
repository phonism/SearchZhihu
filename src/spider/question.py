# -*- encoding=utf-8 -*-
# Author: Qi Lu (luqi.code@gmail.com)

import requests
import json
from bs4 import BeautifulSoup

def AnswerBase(object):

    def __init__(self, answer_id=None, question_id=None):
        self.answer_id = answer_id
        self.question_id = question_id

        


class Question(object):

    def __init__(self, question_id):
        self.question_id = question_id
        self.headers = {
                'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36",
                'Host': "www.zhihu.com",
                'Origin': "http://www.zhihu.com",
                'Pragma': "no-cache",
                'Referer': "http://www.zhihu.com/",
                "Cookie": 'r_c=1; _za=5a838480-e92e-4cec-a300-01de9b2cf8aa; c_c=4bd857b815e311e58107b083fee92c52; tc=AQAAAEnyR0VOKQ0A8kZ+ew/uMPaUv2UJ; aliyungf_tc=AQAAAM0NfiVxVg0Abia13Khluyqrx3LY; _alicdn_sec=56cc3a296f529329d7ebd0fd69755293ac59ec50; udid="AEDA5kuAlAmPTntYPSHWE6x1uTcQQgiYqK0=|1457507407"; _zap=af241c14-18d5-45a6-b130-13958d9db095; d_c0="AJAAtVpaoQmPTvyH8ucUqDWFOKAIGUzAbkc=|1461294954"; _ga=GA1.2.636417043.1420000878; q_c1=539237b6a1f54e8da7abbd9001757b08|1463817813000|1418220969000; login="ODFjOGQ3MTdiNDA4NGJhZTkyMjc0YjIyMzEzYmZhYjc=|1464521339|b80197261688878c4cdda76f8503e9620e503bf4"; z_c0=Mi4wQUJDS2k4Q3NaUWdBa0FDMVdscWhDUmNBQUFCaEFsVk5lMTl5VndDdUxUZUZTZ2JzcU41aHUwMTB0OGNGaGU3N1Nn|1464521339|9ddc16021b2707314e339522e3b0eb5367143a6b; s-t=autocomplete; _xsrf=6b67eabba1eefce57a0ef72074772954; s-q=deep%20learning%20%E6%9C%BA%E5%99%A8%E9%85%8D%E7%BD%AE; s-i=6; sid=nhvavaao; l_cap_id="MDQ1YTI0NjA3YWI0NDNhMWFkNTViNWU3ZDU2NjRhMzM=|1466140910|d45f94add7e8e2cdebdc13fbb6621d4fb0dd63d5"; cap_id="ZDcwZTlhZWQ1ZjhhNDY3MTliODY0MzI1YThkODM4NGI=|1466140910|1401b008eda51fd5b70c871b7b9bd435816e0ab4"; n_c=1; a_t="2.0ABCKi8CsZQgXAAAAv5mMVwAQiovArGUIAJAAtVpaoQkXAAAAYQJVTXtfclcAri03hUoG7KjeYbtNdLfHBYXu-0oI2af5MtzghomP2EJygGT8JlIapg=="; __utma=51854390.636417043.1420000878.1466239449.1466240203.3; __utmb=51854390.29.9.1466241331913; __utmc=51854390; __utmz=51854390.1466240203.3.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=51854390.100-1|2=registration_date=20150716=1^3=entry_date=20141210=1'
        }
        self.soup = None
        self.answer_num = None

    def _get_soup(self):
        r = requests.get("https://www.zhihu.com/question/%s" % self.question_id, headers=self.headers, verify=False)
        if r.status_code != 200:
            return "ERROR"
        self.soup = BeautifulSoup(r.content, "lxml")

    def get_xsrf(self):
        if self.soup is None:
            self._get_soup()
        return self.soup.find("input", {"name": "_xsrf"})["value"]

    def get_comment(self):
        r = requests.get("https://www.zhihu.com/r/answers/38011728/comments?page=2", headers=self.headers, verify=False)
        return r.content
        
    def get_answer_num(self):
        if self.soup is None:
            self._get_soup()
        if self.answer_num is None:
            if self.soup.find("h3", {"id": "zh-question-answer-num"}) is None:
                self.answer_num = "0"
            else:
                self.answer_num = self.soup.find("h3", {"id": "zh-question-answer-num"})["data-num"]
        return self.answer_num

    def get_tags(self):
        if self.soup is None:
            self._get_soup()

    def get_answer_list(self):
        base_url = "https://www.zhihu.com/node/QuestionAnswerListV2"
        if int(self.get_answer_num()) == 0:
            return []
        answer_list = []
        for offset in range((int(self.get_answer_num()) - 1) / 10 + 1):
            payload = {
                    "method": "next",
                    "params": '{"url_token": %s, "pagesize": %s, "offset": %s}' % (int(self.question_id), 10, 10 * offset),
                    "_xsrf": self.get_xsrf()
            }
            r = requests.post(base_url, data=payload, headers=self.headers, verify=False)
            js = json.loads(r.content)
            for ans in js["msg"]:
                answer_list.append(ans.encode("utf-8"))
            return answer_list
        return answer_list
    
    def get_question_info(self):
        q_json = {}
        if self.soup is None:
            self._get_soup()
        q_json["question_id"] = self.question_id
        q_json["url"] = "https://www.zhihu.com/question/" + self.question_id
        q_json["title"] = self.soup.find("title").text.strip().encode("utf-8")
        q_json["detail"] = self.soup.find("div", {"id": "zh-question-detail"}).text.strip().encode("utf-8")
        q_json["answer_num"] = int(self.get_answer_num())
        q_json["follower_num"] = int(self.soup.find("a", {"href": "/question/" + self.question_id + "/ollowers"}).find("strong").text.strip())
        q_json["tags"] = 

