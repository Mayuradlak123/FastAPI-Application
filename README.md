# Online Test Management System

## Overview

The **Online Test Management System** is a FastAPI application that allows for managing quizzes and user interactions. It includes APIs for both admin and user functionalities.
![Screenshot 2024-08-07 at 11 53 40 PM](https://github.com/user-attachments/assets/41ab6311-7017-457c-a542-70399dbb0d40)

### Project Structure

- `app/`: Contains the main application code including routes, database models, schemas, and CRUD operations.
- `tests/`: Contains test cases for the admin and user APIs.
- `requirements.txt`: Lists project dependencies.

## Getting Started

### Prerequisites

Ensure you have Python 3.7+ and `pip` installed on your machine.

### Installation

1. **Clone the Repository:**

    ```sh
    git clone <repository-url>
    cd online_test_management_system
    ```

2. **Create and Activate a Virtual Environment:**

    On Unix or MacOS:

    ```sh
    python -m venv venv
    source venv/bin/activate
    ```

    On Windows:

    ```sh
    python -m venv venv
    venv\Scripts\activate
    ```

3. **Install Dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

### Configuration

**Database Setup:**

Ensure you have a PostgreSQL database. Update the `SQLALCHEMY_DATABASE_URL` in `app/database.py` with your database credentials:

```python
SQLALCHEMY_DATABASE_URL = "postgresql://username:password@host:port/database"
```

### Running the Application

Start the FastAPI application using:

```sh
uvicorn app.main:app --reload
```

This will start the server on http://127.0.0.1:8000.

### API Documentation

The API documentation is available at http://127.0.0.1:8000/docs.

### Admin User Credentials

For testing and using admin APIs:
Only this is the credintials of admin. so Use this will checking the code.

Username: admin
Password: password


I have already posted the question in the data base so you can read them from the read api of admin.

### API Endpoints


**Admin APIs**

**Create Question**

Endpoint: /admin/create_question
Method: POST
Description: Allows admin to create a new question.
Parameters: admin_username, question, answer
Limit: Up to 10 questions.

**Read Questions**

Endpoint: /admin/read_questions
Method: GET
Description: Retrieves all questions in the quiz.

**Update Question**

Endpoint: /admin/update_question
Method: PUT
Description: Updates an existing question by ID.
Parameters: id, question

**Delete Question**

Endpoint: /admin/delete_question
Method: DELETE
Description: Deletes a question by ID.

**User APIs**

**Sign Up**

Endpoint: /user/create_user
Method: POST
Description: Allows a user to sign up.
Parameters: username, password

**Get Questions**

Endpoint: /user/take_test
Method: GET
Description: Retrieves all questions for the user to answer.
Parameters: username

**Submit Answer**

Endpoint: /user/submit_answer
Method: POST
Description: Allows a user to submit an answer to a question.
Parameters: username, question_id, answer
Limit: Maximum of 10 submissions.

**Check Score**

Endpoint: /user/get_score
Method: GET
Description: Retrieves the score of the user.
Parameters: username

### Database Schema

![Screenshot 2024-08-07 at 11 54 03 PM](https://github.com/user-attachments/assets/a90b2580-64ed-4694-8b34-8eb84ce741e8)

**quiz Table**

- id: Integer, Primary Key
- admin_username: String
- question: String
- answer: String
- marks: Integer (default 10)

**user Table**
![Screenshot 2024-08-07 at 11 55 00 PM](https://github.com/user-attachments/assets/aa99d885-6097-43f4-8055-5fd93d1cba5b)

- id: Integer, Primary Key
- username: String
- password: String
- score: Integer

### Running Tests

To run the test cases, use:

```sh
pytest tests/
```

Ensure you have pytest installed:

```sh
pip install pytest
```

### Troubleshooting

- Database Connection Issues: Verify your database URL in `app/database.py`.
- API Not Accessible: Ensure the server is running and you are accessing the correct port.
