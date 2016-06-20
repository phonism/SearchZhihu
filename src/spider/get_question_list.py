# -*- encoding=utf-8 -*-
# Author: Qi Lu (luqi.code@gmail.com)


import requests
from bs4 import BeautifulSoup

class QuestionList(object):
    
    def __init__(self, topic_id):
        self.topic_id = topic_id
        self.headers = {
                'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36",
                'Host': "www.zhihu.com",
                'Origin': "http://www.zhihu.com",
                'Pragma': "no-cache",
                'Referer': "http://www.zhihu.com/",
                "Cookie": 'r_c=1; _za=5a838480-e92e-4cec-a300-01de9b2cf8aa; c_c=4bd857b815e311e58107b083fee92c52; tc=AQAAAEnyR0VOKQ0A8kZ+ew/uMPaUv2UJ; aliyungf_tc=AQAAAM0NfiVxVg0Abia13Khluyqrx3LY; _alicdn_sec=56cc3a296f529329d7ebd0fd69755293ac59ec50; udid="AEDA5kuAlAmPTntYPSHWE6x1uTcQQgiYqK0=|1457507407"; _zap=af241c14-18d5-45a6-b130-13958d9db095; d_c0="AJAAtVpaoQmPTvyH8ucUqDWFOKAIGUzAbkc=|1461294954"; _ga=GA1.2.636417043.1420000878; q_c1=539237b6a1f54e8da7abbd9001757b08|1463817813000|1418220969000; login="ODFjOGQ3MTdiNDA4NGJhZTkyMjc0YjIyMzEzYmZhYjc=|1464521339|b80197261688878c4cdda76f8503e9620e503bf4"; z_c0=Mi4wQUJDS2k4Q3NaUWdBa0FDMVdscWhDUmNBQUFCaEFsVk5lMTl5VndDdUxUZUZTZ2JzcU41aHUwMTB0OGNGaGU3N1Nn|1464521339|9ddc16021b2707314e339522e3b0eb5367143a6b; s-t=autocomplete; _xsrf=6b67eabba1eefce57a0ef72074772954; s-q=deep%20learning%20%E6%9C%BA%E5%99%A8%E9%85%8D%E7%BD%AE; s-i=6; sid=nhvavaao; l_cap_id="MDQ1YTI0NjA3YWI0NDNhMWFkNTViNWU3ZDU2NjRhMzM=|1466140910|d45f94add7e8e2cdebdc13fbb6621d4fb0dd63d5"; cap_id="ZDcwZTlhZWQ1ZjhhNDY3MTliODY0MzI1YThkODM4NGI=|1466140910|1401b008eda51fd5b70c871b7b9bd435816e0ab4"; n_c=1; a_t="2.0ABCKi8CsZQgXAAAAv5mMVwAQiovArGUIAJAAtVpaoQkXAAAAYQJVTXtfclcAri03hUoG7KjeYbtNdLfHBYXu-0oI2af5MtzghomP2EJygGT8JlIapg=="; __utma=51854390.636417043.1420000878.1466239449.1466240203.3; __utmb=51854390.29.9.1466241331913; __utmc=51854390; __utmz=51854390.1466240203.3.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=51854390.100-1|2=registration_date=20150716=1^3=entry_date=20141210=1'
        }


    def get_question_list(self):
        base_url = "https://www.zhihu.com/topic/%s/questions?page=%s"
        page_num = 1
        question_list = []

        while True:
            url = base_url % (self.topic_id, page_num)
            r = requests.get(url, headers=self.headers, verify=False)
            if r.status_code != 200:
                break
            soup = BeautifulSoup(r.content)
            for question in soup.find_all("a", {"class": "question_link"}):
                yield "https://www.zhihu.com" + question["href"]
            page_num += 1
