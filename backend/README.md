# Full Stack Trivia API Backend

This is the backend API code for the Full Stack Trivia API project.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 

    - **NOTE: This was implemented as a GET request since a request payload is not used.**
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## Testing
In order to run tests navigate to the backend folder and run the following commands:
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling
Error response bodies will be in the following JSON format:
```
{
  "success": False,
  "error": <HTTP response status code>,
  "message": <HTTP response status message>
}
```
The API uses these standard HTTP response status codes when describing call results:
- 200: OK
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable
- 500: Internal Server Error

### Endpoints
#### GET /categories
- **Description:**
  - Returns a dictionary of categories where keys are the ids and values are the category names.
  - Returns success indicator.
- **Arguments:**
  - None

- **Sample Request:**
   ```
   curl http://127.0.0.1:5000/categories
   ```
- **Sample Response:**
  ```
  {
    "categories": {
      "1": "Science",
      "2": "Art",
      "3": "Geography",
      "4": "History",
      "5": "Entertainment",
      "6": "Sports"
    },
    "success": true
  }
  ```
#### GET /categories/{category_id}/questions?page={page_number}
- **Description:**
  - Returns an array of question objects for a given category id.
  - Returns success indicator, current category id and total number of questions in the category.
- **Arguments:**
  - category_id: (integer) id of the requested category
  - page_number: (integer) number of the requested page
- **Sample Request:**
   ```
   curl http://127.0.0.1:5000/categories/1/questions

   ```
- **Sample Response:**
  ```
  {
    "current_category": 1,
    "questions": [
      {
        "answer": "The Liver",
        "category": 1,
        "difficulty": 4,
        "id": 20,
        "question": "What is the heaviest organ in the human body?"
      },
      {
        "answer": "Alexander Fleming",
        "category": 1,
        "difficulty": 3,
        "id": 21,
        "question": "Who discovered penicillin?"
      },
      {
        "answer": "Blood",
        "category": 1,
        "difficulty": 4,
        "id": 22,
        "question": "Hematology is a branch of medicine involving the study of what?"
      }
    ],
    "success": true,
    "total_questions": 3
  }
  ```
#### GET /questions?page={page_number}
- **Description:**
  - Returns an array of question objects for a given page number.
  - Returns a dictionary of categories where keys are the ids and values are the category names.
  - Returns success indicator, current category id and total number of questions in the database.
- **Arguments:**
  - page_number: (integer) number of the requested page

- **Sample Request:**
   ```
   curl http://127.0.0.1:5000/questions?page=1
   ```
- **Sample Response:**
  ```
  {
    "categories": {
      "1": "Science",
      "2": "Art",
      "3": "Geography",
      "4": "History",
      "5": "Entertainment",
      "6": "Sports"
    },
    "current_category": null,
    "questions": [
      {
        "answer": "Maya Angelou",
        "category": 4,
        "difficulty": 2,
        "id": 5,
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      },
      {
        "answer": "Muhammad Ali",
        "category": 4,
        "difficulty": 1,
        "id": 9,
        "question": "What boxer's original name is Cassius Clay?"
      },
      {
        "answer": "Apollo 13",
        "category": 5,
        "difficulty": 4,
        "id": 2,
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
      },
      {
        "answer": "Edward Scissorhands",
        "category": 5,
        "difficulty": 3,
        "id": 6,
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
      },
      {
        "answer": "Brazil",
        "category": 6,
        "difficulty": 3,
        "id": 10,
        "question": "Which is the only team to play in every soccer World Cup tournament?"
      },
      {
        "answer": "Uruguay",
        "category": 6,
        "difficulty": 4,
        "id": 11,
        "question": "Which country won the first ever soccer World Cup in 1930?"
      },
      {
        "answer": "George Washington Carver",
        "category": 4,
        "difficulty": 2,
        "id": 12,
        "question": "Who invented Peanut Butter?"
      },
      {
        "answer": "Lake Victoria",
        "category": 3,
        "difficulty": 2,
        "id": 13,
        "question": "What is the largest lake in Africa?"
      },
      {
        "answer": "The Palace of Versailles",
        "category": 3,
        "difficulty": 3,
        "id": 14,
        "question": "In which royal palace would you find the Hall of Mirrors?"
      },
      {
        "answer": "Agra",
        "category": 3,
        "difficulty": 2,
        "id": 15,
        "question": "The Taj Mahal is located in which Indian city?"
      }
    ],
    "success": true,
    "total_questions": 19
  }
  ```
#### DELETE /questions/{question_id}
- **Description:**
  - Deletes a question using a question id.
  - Returns success indicator and id of the deleted question.
- **Arguments:**
  - question_id: (integer) id of the question to be deleted

- **Sample Request:**
   ```
   curl -X DELETE http://127.0.0.1:5000/questions/24
   ```
- **Sample Response:**
  ```
  {
    "deleted": 24,
    "success": true
  }
  ```
#### POST /questions
- **Description:**
  - Creates a new question object.
  - Returns success indicator and id of the new question.
- **Arguments:**
  - question: (string) question text
  - answer: (string) ansewer text
  - category: (integer) id of the category or the new question
  - difficulty: (integer) difficulty level of the new question

- **Sample Request:**
   ```
   curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" --data {"question":"Who wrote Fahrenheit 451?","answer":"Ray Bradbury","difficulty":1,"category":"4"}
   ```
- **Sample Response:**
  ```
  {
    "created": 25,
    "success": true
  }
  ```
#### POST /questions?page={page_number}
- **Description:**
  - Searches for questions containing a search term.
  - Returns an array of question objects that contain the serch term.
  - Returns success indicator, current category id and total number of questions in the search results.
- **Arguments:**
  - searchTerm: (string) search term
  - page_number: (integer) number of the requested page

- **Sample Request:**
   ```
   curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" --data {"searchTerm":"beetle"}
   ```
- **Sample Response:**
  ```
  {
    "current_category": null,
    "questions": [
      {
        "answer": "Scarab",
        "category": 4,
        "difficulty": 4,
        "id": 23,
        "question": "Which dung beetle was worshipped by the ancient Egyptians?"
      }
    ],
    "success": true,
    "total_questions": 1
  }
  ```
#### POST /quizzes
- **Description:**
  - Gets the next question to use when playing the quiz.
  - Uses the quiz_category and previous_questions parameters to return a random question within the given category, if provided, that is not one of the previous questions.
  - Returns success indicator and a question object.

- **Arguments:**
  - previous_questions: (list) ids of questions that have already been used in the quiz
  - quiz_category: (dictionary) category object containing the current category id and description

- **Sample Request:**
   ```
   curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" --data {"previous_questions":[20],"quiz_category":{"type":"Science","id":"1"}}
   ```
- **Sample Response:**
  ```
  {
    "question": {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    "success": true
  }
  ```

## Authors

* **Abe Feinberg** - *Initial work* - [AbeFeinberg](https://github.com/AbeFeinberg)
* **Several others...**
* **Rafael Benitez** - *Customized application for Full Stack Nanodegree Project* - [rafbenitez](https://github.com/rafbenitez)

## Acknowledgments

* This is a project for the Udacity Full Stack Web Developer Nanodegree Program
