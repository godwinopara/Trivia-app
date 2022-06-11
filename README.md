# API Development and Documentation Final Project

## Trivia App

This project is a quiz game intended to create bonding experience for udacity employees and students. Students or employees are able to add questions and the answer to the question, delete questions, search for questions based on a text query string, play the quiz game, randomizing either all questions or within a specifi category.
As part of the Udacity Fullstack Nanodegree this project serves as the capstone project for the Api Development, Testing and Documentation. completing this trivia app give me the ability to structure plan, implement and test an API.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

## Local Development

The instructions below are meant for the local setup only.

#### Pre-requisites

- Developers using this project should already have Python3, pip and node installed on their local machines.

### Backend

The [backend](./backend/README.md) contains Flask and SQLAlchemy server, the various endpoints and neccessary installations. The `flaskr/__init__.py` contains the various endpoints while `models.py` contains the model for the database and SQLAlchemy setup.

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend your design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. to note where the api are consumed. These are the files that contains the api just incase you want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [Frontend README](./frontend/README.md) for more details.

