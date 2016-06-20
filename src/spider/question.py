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
                "Cookie": 'r_c=1; _za=5a838480-e92e-4cec-a300-01de9b2cf8aa; c_c=4bd857b815e311e58107b083fee92c52; tc=AQAAAEnyR0VOKQ0A8kZ+ew/uMPaUv2UJ; aliyungf_tc=AQAAAM0NfiVxVg0Abia13Khluyqrx3LY; _alicdn_sec=56cc3a296f529329d7ebd0fd69755293ac59ec50; udid="AEDA5kuAlAmPTntYPSHWE6x1uTcQQgiYqK0=|1457507407"; _zap=af241c14-18d5-45a6-b130-13958d9db095; d_c0="AJAAtVpaoQmPTvyH8ucUqDWFOKAIGUzAbkc=|1461294954"; _ga=GA1.2.636417043.1420000878; q_c1=539237b6a1f54e8da7abbd9001757b08|1463817813000|1418220969000; login="ODFjOGQ3MTdiNDA4NGJhZTkyMjc0YjIyMzEzYmZhYjc=|1464521339|b80197261688878c4cdda76f8503e9620e503bf4"; z_c0=Mi4wQUJDS2k4Q3NaUWdBa0FDMVdscWhDUmNBQUFCaEFsVk5lMTl5VndDdUxUZUZTZ2JzcU41aHUwMTB0OGNGaGU3N1Nn|1464521339|9ddc16021b2707314e339522e3b0eb5367143a6b; _xsrf=6b67eabba1eefce57a0ef72074772954; s-t=autocomplete; s-q=%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E5%A4%84%E7%90%86; s-i=27; sid=84e0ld18; l_cap_id="MTlmMzg2MWRiMDA5NGUwOGJkODlhYWI1NWJkOWQ5Njc=|1466404566|f30c1e5f4644a0ad611f1aa5205729005cca4796"; cap_id="YTlkODM1MjBmZjExNDhlOThiOTkxNTFiODY0N2Y4OTk=|1466404566|510327b492a94d4b7f04442c1977314770e59705"; n_c=1; a_t="2.0ABCKi8CsZQgXAAAAz2GPVwAQiovArGUIAJAAtVpaoQkXAAAAYQJVTXtfclcAri03hUoG7KjeYbtNdLfHBYXu-0omrrDFAr0nGW1iI67NRxtD_G-Wlg=="; __utma=51854390.636417043.1420000878.1466422483.1466418482.4; __utmb=51854390.26.9.1466431520521; __utmc=51854390; __utmz=51854390.1466418482.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.100-1|2=registration_date=20150716=1^3=entry_date=20141210=1'
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
        tags = []
        for a in self.soup.find_all("a", {"class": "zm-item-tag"}):
            tags.append(a.text.strip().encode("utf-8"))
        return tags

    def get_collapsed(self):
        if self.soup is None:
            self._get_soup()
        collapsed = self.soup.find("span", {"id": "zh-question-collapsed-num"})
        if collapsed is None:
            return "0"
        return collapsed.text.strip()

    def get_question_comment_num(self):
        if self.soup is None:
            self._get_soup()
        div = self.soup.find("div", {"id": "zh-question-meta-wrap"})
        comment = div.find("a", {"name": "addcomment"}).text.encode("utf-8")
        if comment.find("条评论") != -1:
            return comment.split("条评论")[0].strip()
        return "0"


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
        q_json["title"] = self.soup.find("title").text.split("-")[0].strip().encode("utf-8")
        q_json["detail"] = self.soup.find("div", {"id": "zh-question-detail"}).find("div", {"class": "zm-editable-content"}).text.strip().encode("utf-8")
        q_json["comment_num"] = int(self.get_question_comment_num())
        q_json["answer_num"] = int(self.get_answer_num())
        q_json["follower_num"] = int(self.soup.find("a", {"href": "/question/" + self.question_id + "/followers"}).find("strong").text.strip())
        q_json["tags"] = self.get_tags()
        q_json["recent_modify"] = self.soup.find_all("div", {"class": "zg-gray-normal"})[-2].find("span", {"class": "time"}).text.strip().encode("utf-8")
        q_json["view_num"] = int(self.soup.find_all("div", {"class": "zg-gray-normal"})[-1].find_all("strong")[0].text.strip())
        q_json["topic_follower_num"] = int(self.soup.find_all("div", {"class": "zg-gray-normal"})[-1].find_all("strong")[1].text.strip())
        q_json["collapsed_num"] = int(self.get_collapsed())
        return json.dumps(q_json, ensure_ascii=False)



