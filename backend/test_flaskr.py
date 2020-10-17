import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
  """This class represents the trivia test case"""

  def setUp(self):
    """Define test variables and initialize app."""
    self.app = create_app()
    self.client = self.app.test_client
    self.database_name = "trivia_test"
    self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
    setup_db(self.app, self.database_path)

    self.new_question = {
      'question': 'Such a great question',
      'answer': 'this is the answer',
      'category': 4,
      'difficulty': 3
    }

    # binds the app to the current context
    with self.app.app_context():
      self.db = SQLAlchemy()
      self.db.init_app(self.app)
      # create all tables
      self.db.create_all()

  def tearDown(self):
    """Executed after reach test"""
    pass

  """
  TODO
  Write at least one test for each test for successful operation and for expected errors.
  """

  """
  Tests for /categories GET endpoint
  """
  def test_get_gategories(self):
    res = self.client().get('/categories')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['categories'])
    self.assertTrue(len(data['categories']))

  def test_404_if_no_gategories_exist(self):
    res = self.client().get('/categories/999')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['error'], 404)
    self.assertEqual(data['message'], 'Not Found')

  """
  Tests for /categories/<int:category_id>/questions GET endpoint
  """
  def test_get_paginated_questions_by_category(self):
    res = self.client().get('/categories/1/questions')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['questions'])
    self.assertTrue(len(data['questions']))
    self.assertTrue(data['total_questions'])
    self.assertTrue(data['current_category'])
    self.assertEqual(data['current_category'], 1)

  def test_404_sent_requesting_by_category_beyond_valid_page(self):
    res = self.client().get('/categories/1/questions?page=1000')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['error'], 404)
    self.assertEqual(data['message'], 'Not Found')

  """
  Tests for /questions GET endpoint
  """
  def test_get_paginated_questions(self):
    res = self.client().get('/questions')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['questions'])
    self.assertTrue(len(data['questions']))
    self.assertTrue(data['total_questions'])
    self.assertTrue(data['categories'])
    self.assertTrue(len(data['categories']))
    self.assertIn('current_category', data)

  def test_404_sent_requesting_beyond_valid_page(self):
    res = self.client().get('/questions?page=1000')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['error'], 404)
    self.assertEqual(data['message'], 'Not Found')

  """
  Tests for /questions DELETE endpoint
  """
  def test_delete_question(self):
    question = Question(question='delete me', answer='delete me', difficulty=1, category=1)
    question.insert()
    new_question_id = question.id

    res = self.client().delete('/questions/{}'.format(new_question_id))
    data = json.loads(res.data)

    question = Question.query.filter(Question.id == new_question_id).one_or_none()

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(data['deleted'], new_question_id)
    self.assertEqual(question, None)

  def test_422_if_question_does_not_exist(self):
    res = self.client().delete('/questions/1000')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 422)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['error'], 422)
    self.assertEqual(data['message'], 'Unprocessable Entity')

  """
  Tests for /questions POST endpoint
  """
  def test_create_new_question(self):
    res = self.client().post('/questions', json=self.new_question)
    data = json.loads(res.data)
    pass

  def test_422_if_question_creation_fails(self):
    res = self.client().post('/questions', json=self.new_question)
    data = json.loads(res.data)
    pass

  def test_post_question_search_with_results(self):
    res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': {'type': '', 'id': 0}})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['question'])

  def test_post_question_search_without_results(self):
    res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': {'type': '', 'id': 100}})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(data['question'], None)

  def test_400_if_post_question_search_fails(self):
    res = self.client().post('/quizzes', json={})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 400)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['error'], 400)
    self.assertEqual(data['message'], 'Bad Request')

# Make the tests conveniently executable
if __name__ == "__main__":
  unittest.main()