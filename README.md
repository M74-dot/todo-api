# TODO REST API Application

## How to use it

### Clone the repository
> git clone https://github.com/M74-dot/todo-api.git

### Run requirements.txt file to get all modules installed
> pip install -r requirements.txt

### Run the app.py file
> flask run

### It will run on localhost (127.0.0.1:5000)

### Postman for testing API's
> create 2 collections in postman _1.todo_ _2.user_

#### todo API route

> GET / : Home route

> GET /todo : Get todo list

> POST /todo : Create todo list

> PUT /todo/<int:id> : Update specific todo list

> DEL /todo/<int:id> : Delete specific todo list

> GET /swagger-ui : OPEN API Documentation

#### user API route

> POST /register : Register the user

> POST /login : Authenticate user

> POST /logout : Logout the user


>> THANK YOU! 