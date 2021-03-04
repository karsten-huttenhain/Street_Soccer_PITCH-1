import sqlite3
from models.test import TestModel

class TopicModel:
    def __init__(self, topic_id, is_unlocked, name, needed_credit):
        self.topic_id = topic_id
        self.is_unlocked = is_unlocked
        self.name = name
        self.needed_credit = needed_credit
    
    def json(self, withTests=False, withQuizzes=False, withAnswers=False, withFormativeAssessments=False):
        tests = []
        if withTests:
            for test in TestModel.query_db(TestModel, "SELECT * FROM tests WHERE topic_id=?", (self.topic_id,)):
                tests.append(TestModel(*test).json(withQuizzes=withQuizzes, withAnswers=withAnswers, withFormativeAssessments=withFormativeAssessments))

        return {
            'topic_id': self.topic_id,
            'is_unlocked': self.is_unlocked,
            'name': self.name,
            'needed_credit': self.needed_credit,
            'tests': tests
        }

    def query_db(self, query, args):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        result = cursor.execute(query, args)
        row = result.fetchone()

        connection.close()

        return row

    @classmethod
    def find_by_id(cls, topic_id):
        result = cls.query_db(cls, "SELECT * FROM topics WHERE topic_id=?", (topic_id,))

        if result:
            topic = cls(*result)
        else:
            topic = None
        
        return topic