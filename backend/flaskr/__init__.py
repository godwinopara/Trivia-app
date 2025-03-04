from crypt import methods
import json
import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginated_questions(selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers",
                             "Content-Type, Authorization, true")

        response.headers.add("Access-Control-Allow-Methods",
                             "GET, PATCH, POST, DELETE, OPTION")
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():

        try:
            categories = Category.query.order_by(Category.id).all()
            formated_categories = {}
            for category in categories:
                formated_categories[category.id] = category.type

            return jsonify({
                "success": True,
                "categories": formated_categories,
            })
        except:
            abort(404)
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions')
    def get_questions():

        questions = Question.query.order_by(Question.id).all()
        categories = Category.query.order_by(Category.id).all()
        current_questions = paginated_questions(questions)

        # format_question = [question.format() for question in questions]

        """ DICTIONARY THAT HOLDS ALL CATEGORIES """
        formated_categories = {}

        """ 
        RETURN ALL THE CATEGORIES IN DICTIONARY WITH
        ID AS KEY AND TYPE AS VALUE
        """
        for category in categories:
            formated_categories[category.id] = category.type

        if len(current_questions) == 0:
            abort(404)
        else:
            return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": len(questions),
                "categories": formated_categories,
                "current_category": "All Question"
            })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        try:
            question = Question.query.get(question_id)

            if question is None:
                abort(400)

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginated_questions(selection)

            question.delete()

            return({
                "success": True,
                "deleted_question": question.id,
                "questions": current_questions,
                "total_questions": len(current_questions)
            })
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=["POST"])
    def search_question_or_add_question():

        data = request.get_json()

        question = data.get('question', None)
        answer = data.get('answer', None)
        category = data.get('category', None)
        difficulty = data.get('difficulty', None)
        search = data.get('searchTerm')
        print(data)

        try:
            if search:
                questions = Question.query.filter(
                    Question.question.ilike(f'%{search}%'))
                current_questions = paginated_questions(questions)

                return jsonify({
                    "success": True,
                    "questions": current_questions
                })
            else:
                new_question = Question(
                    question=question, answer=answer, category=category, difficulty=difficulty)

                new_question.insert()

                all_questions = Question.query.order_by(Question.id).all()
                current_questions = paginated_questions(all_questions)
                return jsonify({
                    "success": True,
                    "created": new_question.id,
                    "questions": current_questions,
                    "total_questions": len(all_questions)
                })
        except:
            abort(405)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):

        try:
            category = Category.query.get(category_id)
            questions = Question.query.filter(Question.category == category.id)
            format_questions = [question.format() for question in questions]

            return({
                "success": True,
                "questions": format_questions,
                "totalQuestions": len(format_questions),
                "current_category": category.type
            })

        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=["POST"])
    def get_quizzes():

        try:
            """ GET THE QUIZ CATEGORY THE USER SELECTED """
            data = request.get_json()

            """ THE PREVIOUS QUESTION THE USER HAVE ATTEMPTED """
            previous_questions = data.get('previous_questions')

            """ THE CATEGORY OF QUESTIONS THE USER SELECTED """
            quiz_category = data.get('quiz_category')

            """
                    FILTER OUT QUESTIONS BASED ON THE CATEGORY
                    THE USER SELECTED
                """
            questions_based_on_current_quiz_category = Question.query.filter(
                Question.category == quiz_category.get('id'))

            """
                    RANDOMLY SELECT A QUESTIONS FROM THE FILTERED QUESTIONS
                    THAT THE USER HAVE NOT ATTEMPTED
                """
            current_question = random.choice(
                [question for question in questions_based_on_current_quiz_category if question.category not in previous_questions])

            random_question = {
                'id': current_question.id,
                'question': current_question.question,
                'answer': current_question.answer,
                'category': current_question.category,
                'difficulty': current_question.difficulty
            }

            return jsonify({
                'success': True,
                'question': random_question
            })
        except:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @ app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found",
        }), 404

    @ app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    @ app.errorhandler(405)
    def method_not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405

    @ app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    return app
