import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  '''
  Setup CORS. Allow '*' for origins.
  '''
  CORS(app, resources={'/': {'origins': '*'}})

  '''
  Set Access-Control-Allow
  '''
  # CORS Headers
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  '''
  Handle GET requests for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.get_all()

    if len(categories) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': categories
    })

  '''
  Handle GET requests for questions, including pagination (every 10 questions).
  '''
  @app.route('/questions')
  def get_questions():
    selection = Question.query.all()
    current_questions = paginate_questions(request, selection)

    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(selection),
      'categories': Category.get_all(),
      'current_category': None
    })

  '''
  Handle DELETE requests for a question using a question ID.
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()

      return jsonify({
        'success': True,
        'deleted': question_id
      })

    except:
      abort(422)

  '''
  Handle POST requests for new questions and search requests.
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()

    search_term = body.get('searchTerm', None)

    if search_term:
      selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search_term))).all()
      if len(selection) == 0:
        abort(404)

      current_questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(selection),
        'current_category': None
      })

    else:
      new_question = body.get('question', None)
      new_answer = body.get('answer', None)
      new_category = body.get('category', None)
      new_difficulty = body.get('difficulty', None)

      if new_question is None or new_answer is None or new_category is None or new_difficulty is None:
        abort(422)

      try:
        question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
        question.insert()

        return jsonify({
          'success': True,
          'created': question.id
        })
      except:
        abort(422)

  '''
  Handle GET requests for questions based on a category ID.
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):
    selection = Question.query.filter(Question.category == category_id).all()
    current_questions = paginate_questions(request, selection)

    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(selection),
      'current_category': category_id
    })

  '''
  Handle POST requests for questions to play the quiz.
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_quiz_questions():
    body = request.get_json()

    previous_questions = body.get('previous_questions', None)
    quiz_category = body.get('quiz_category', None)

    try:
      if quiz_category['id']:
        questions = Question.query.filter(Question.category == quiz_category['id'])
      else:
        questions = Question.query
      new_questions = questions.filter(Question.id.notin_(previous_questions)).all()

      if len(new_questions):
        next_question = new_questions[random.randrange(0, len(new_questions))].format()
      else:
        next_question = None

      return jsonify({
        'success': True,
        'question': next_question
      })
    except:
      abort(400)

  '''
  Error handlers for all expected errors.
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request'
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Not Found'
    }), 404

  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable Entity'
    }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal Server Error'
    }), 500

  return app
