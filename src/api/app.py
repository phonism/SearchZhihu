# -*- encoding=utf-8 -*-

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import sys
sys.path.append('..')
from spider import question

app = Flask(__name__)
api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument("question_id")


class Question(Resource):
    def get(self, question_id):
        q = question.Question(question_id)
        answer_list = q.get_answer_list()
        return answer_list[0]


api.add_resource(Question, '/question/<question_id>')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8111, debug=True)
