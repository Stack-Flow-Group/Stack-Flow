# Stack-Flow

## BACKEND API
## Schema
![Stack Flow (1)](https://github.com/user-attachments/assets/ccc4394b-50bd-4d74-bc60-56d06f9f6af7)

## Auth
### All apis that require authentication
All apis that require a current logged in user.

* Request: apis that require authentication
* Error Response: Require authentication
  * Status Code: 401
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "errors":
      {
        "message": "Unauthorized"
      }
    }
    ```

### All apis that require proper authorization
All apis that require authentication and the current user does not have the
correct permission to view.

* Request: apis that require proper authorization
* Error Response: Require proper authorization
  * Status Code: 403
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Forbidden"
    }
    ```

### Get all Users
Returns the information about the all users

* Require Authentication: true
* Request
  * Method: GET
  * URL: /api/users
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "users": [
        {
          "id": 1,
          "email": "john.smith@gmail.com",
          "username": "JohnSmith"
        }
      ]
    }
    ```

### Get an User with Specific id
Returns the information about a user of a specific id

* Require Authentication: true
* Request
  * Method: GET
  * URL: /api/users/:userId
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "id": 1,
      "email": "john.smith@gmail.com",
      "username": "JohnSmith"
    }
    ```

### Log In a User
Logs in a current user with email and password and returns the user's information.

* Require Authentication: false
* Request
  * Method: POST
  * URL: /api/auth/login
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "email": "john.smith@gmail.com",
      "password": "secret password"
    }
    ```

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "id": 1,
      "email": "john.smith@gmail.com",
      "username": "JohnSmith"
    }
    ```

* Error Response: Invalid credentials
  * Status Code: 401
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "error": "No such user exists.",
      // or
      "error": "Password was incorrect."
    }
    ```

* Error response: Body validation errors
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Bad Request",
      "errors": {
        "email": "email is required" /*or*/ "Email provided not found.",
        "password": "password is required"
      }
    }
    ```

### Log out
Log the current user out.

* Require Authentication: false
* Request
  * Method: GET
  * URL: /api/auth/logout
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "User logged out"
    }
    ```

### Sign Up a User
Create a new user, log in, and return the user's information.

* Require Authentication: false
* Request
  * Method: POST
  * URL: /api/auth/signup
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "username": "JohnSmith",
      "email": "john.smith@gmail.com",
      "password": "secret password"
    }
    ```

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "id": 1,
      "email": "john.smith@gmail.com",
      "username": "JohnSmith"
    }
    ```

* Error response: Validation Errors
  * Status Code: 401
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "errors": {
        "username": [
          "This field is required", // or
          "Username is already in use."
        ], // and/or
        "email": [
          "This field is required", // or
          "Email address is already in use."
        ], // and/or
        "password": [
          "This field is required"
        ]
      }
    }
    ```

## Questions
### Get all questions
* Require Authentication: false
* Request
  * Method: GET
  * URL: /api/questions
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
	"questions":[
		{
			"id": 1,
			"question": "How do I write API's?",
			"subject": "How do you make a readme",
			"User": {
				"username": "testUser"
			}
		},
		{
			"id": 2,
			"question": "How do I finish a project?",
			"subject": "What should I do?",
			"User": {
				"username": "testUser"
			}
		}
	]
    }
    ```

### Get all questions of current user
* Require Authentication: true
* Request
  * Method: GET
  * URL: /api/questions/current
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
			"id": 1,
			"question": "How do I write API's?",
			"subject": "How do you make a readme",
			"User": {
        "id": 1,
				"username": "testUser"
		  }
    }
    ```

### Get a Question with Specific id
Return details of a question with given question id

* Require Authentication: false
* Request
  * Method: GET
  * URL: /api/questions/:id
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

```json
 {
	"id": 1,
	"question": "How do I write API's?",
	"subject": "How do you make a readme",
	"User": {
		"username": "testUser",
	},
	"QuestionComments": [
		{
			"id": 3,
			"comment": "This is a comment under the question",
			"User":{
				"username": "commentUser"
			}
    }
	],
	"Answers":[
		{
			"id": 3,
			"answer": "By writing a backend",
			"User": {
				"username": "answerUser"
			},
			"AnswerComments": [
				{
					"comment": "This is the right answer",
					"User":{
						"username": "answerCommentUser"
					}
				}
			]
		}
	]

  }
 ```
* Error response: Couldn't find question
* Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
	     "message": "Question couldn't be found"
    }
    ```

### Edit Question
Change and return details of a question with given id

* Require Authentication: true
* Require proper authorization: Question must belong to the logged in user
* Request
  * Method: PUT
  * URL: /api/questions/:id/edit
  * Body:
    ```json
    {
        "id": 1,
	"question": "How do I write API's?",
	"subject": "How do you make a readme",
	"userId": 1
    }
    ```

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

   ```json
   {
	"message": "Question update"
   }
    ```

* Error response: Couldn't find question
* Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
	"message": "Question couldn't be found"
    }
    ```

### Delete Question
Delete a question with given question id

* Require Authentication: true
* Require proper authorization: Question must belong to the logged in user
* Request
  * Method: DELETE
  * URL: /api/questions/:id
  * Body: none

* Successful Response
  * Status Code: 204
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Question deleted"
    }
    ```

* Error response: Couldn't find question
* Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
	"message": "Question couldn't be found"
    }
    ```

### Create Question
Create a new question with given details

* Require Authentication: true
* Request
  * Method: POST
  * URL: /api/questions/new
  * Body:
 ```json
    {
	"id": 1,
	"question": "How do I write API's?",
	"subject": "How do you make a readme",
	"user_id": 2
    }
 ```

* Successful Response
  * Status Code: 204
  * Headers:
    * Content-Type: application/json
  * Body:
 ```json
    {
	"message": "Question created"
    }
 ```

### Delete a Tag of a Question
Remove a tag from a question's tags.

* Require Authentication: true
* Require proper authorization: Question must belong to the logged in user
* Request
  * Method: DELETE
  * URL: /api/questions/tags/:questionId/:tagId
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Successfully Removed"
    }
    ```

* Error response: Couldn't find a Question with the specified id
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Question couldn't be found"
    }
    ```

* Error response: Couldn't find the specified Tag under the Question
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Tag couldn't be found"
    }
    ```

### Get all questions of a specific tag
Get all questions associated to a specific tag

* Require Authentication: false
* Request
  * Method: GET
  * URL: /api/questions/tags/:tagId
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "tagName": "javascript",
      "Questions": [
        {
          "Tags": [
            {
              "id": 1,
              "tag_name": "javascript"
            }
          ],
          "id": 1,
          "question": "This is a Question",
          "subject": "First Seed Question"
        }
      ]
    }
    ```

### Create an Answer for a Question
Create and return a new answer for a question specified by id.

* Require Authentication: true
* Require proper authorization: Question must NOT belong to the logged in user
* Request
  * Method: POST
  * URL: /api/questions/:questionId/answers
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "answer": "This is the answer to your question!",
    }
    ```

* Successful Response
  * Status Code: 201
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "id": 1,
      "userId": 1,
      "questionId": 1,
      "answer": "This is the answer to your question!",
      "createdAt": "2021-11-19 20:39:36",
      "updatedAt": "2021-11-19 20:39:36"
    }
    ```

* Error Response: Body validation errors
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Bad Request", // (or "Validation error" if generated by Sequelize),
      "errors": {
        "answer": "Answer text is required",
      }
    }
    ```

* Error response: Couldn't find a Question with the specified id
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Question couldn't be found"
    }
    ```

* Error response: Answer from the current user already exists for the Question
  * Status Code: 500
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "User already has a Answer for this Question"
    }
    ```



### Get all Question Comments of the Current User
Returns all the question comments that belong to the current user specified by answer id.

* Require Authentication: true
* Request
  * Method: GET
  * URL: /api/questions/comments/current
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "QuestionComments": [
        {
          "id": 1,
          "userId": 1,
          "questionId": 1,
          "comment": "Your question is neat!",
          "User": {
            "id": 1,
            "firstName": "John",
            "lastName": "Smith"
          },
        }
      ]
    }
    ```

### Get all Question Comments of a Question
Create and return a new question comment for a question specified by question id.

* Require Authentication: false
* Request
  * Method: GET
  * URL: /api/questions/:questionId/comments
  * Body: none

* Successful Response
  * Status Code: 201
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
    "QuestionComments": [
        {
          "User": {
            "email": "demo@aa.io",
            "id": 1,
            "username": "Demo"
          },
          "comment": "Have you done a git pull?",
          "id": 1,
          "questionId": 2,
          "userId": 1
        },
      ]
    }
    ```

* Error response: Couldn't find a Question with the specified id
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Question couldn't be found"
    }
    ```

### Create a Question Comment
Create and return a new question comment for a question specified by question id.

* Require Authentication: true
* Request
  * Method: POST
  * URL: /api/questions/:questionId/comments
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "comment": "Your question is neat!",
    }
    ```

* Successful Response
  * Status Code: 201
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "id": 1,
      "userId": 1,
      "answerId": 1,
      "comment": "Your question is neat!"
    }
    ```

* Error Response: Body validation errors
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Bad Request", // (or "Validation error" if generated by Sequelize),
      "errors": {
        "comment": "Comment text is required",
      }
    }
    ```

* Error response: Couldn't find a Question with the specified id
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Question couldn't be found"
    }
    ```

## Answers
### Get all Answers of the Current User
Returns all the answers that belong to a question specified by id.

* Require Authentication: true
* Request
  * Method: GET
  * URL: /api/answers/current
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "Answers": [
        {
          "id": 1,
          "userId": 1,
          "questionId": 1,
          "answer": "This is my answer",
          "createdAt": "2021-11-19 20:39:36",
          "updatedAt": "2021-11-19 20:39:36" ,
          "User": {
            "id": 1,
            "firstName": "John",
            "lastName": "Smith"
          },
        }
      ]
    }
    ```

### Edit a Answer
Update and return an existing answer.

* Require Authentication: true
* Require proper authorization: Answer must belong to the current user
* Request
  * Method: PUT
  * URL: /api/answers/:answerId
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "answer": "This is the answer to your question!",
    }
    ```

* Successful Response
  * Status Code: 201
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "id": 1,
      "userId": 1,
      "questionId": 1,
      "answer": "This is an updated answer to your question!",
      "createdAt": "2021-11-19 20:39:36",
      "updatedAt": "2021-11-19 20:39:36"
    }
    ```

* Error Response: Body validation errors
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:
    ```json
    {
      "message": "Bad Request", // (or "Validation error" if generated by Sequelize),
      "errors": {
        "answer": "Answer text is required",
      }
    }
    ```

* Error response: Couldn't find a Answer with the specified id
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Answer couldn't be found"
    }


### Delete a Answer
Delete an existing Answer.

* Require Authentication: true
* Require proper authorization: Answer must belong to the current user
* Request
  * Method: DELETE
  * URL: /api/answers/:answerId
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Successfully deleted"
    }
    ```

* Error response: Couldn't find a Answer with the specified id
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Answer couldn't be found"
    }
    ```

### Get all Answer Comments of the Current User
Returns all the answer comments that belong to the current user specified by answer id.

* Require Authentication: true
* Request
  * Method: GET
  * URL: /api/answers/comments/current
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "AnswerComments": [
        {
          "id": 1,
          "userId": 1,
          "questionId": 1,
          "comment": "Your answer is correct!",
          "createdAt": "2021-11-19 20:39:36",
          "updatedAt": "2021-11-19 20:39:36" ,
          "User": {
            "id": 1,
            "firstName": "John",
            "lastName": "Smith"
          },
        }
      ]
    }
    ```

### Create an Answer Comment for a Answer
Create and return a new answer comment for an answer specified by answer id.

* Require Authentication: true
* Request
  * Method: POST
  * URL: /api/answers/:answerId/comments
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "comment": "This answer is correct!",
    }
    ```

* Successful Response
  * Status Code: 201
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "id": 1,
      "userId": 1,
      "answerId": 1,
      "comment": "This answer is correct!",
      "createdAt": "2021-11-19 20:39:36",
      "updatedAt": "2021-11-19 20:39:36"
    }
    ```

* Error Response: Body validation errors
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Bad Request", // (or "Validation error" if generated by Sequelize),
      "errors": {
        "comment": "Comment text is required",
      }
    }
    ```

* Error response: Couldn't find an Answer with the specified id
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Answer couldn't be found"
    }
    ```

    ```

## Tags
### Add a Tag For a Question
Create if not exist and return all tags for a given question with id.

* Require Authentication: true
* Require proper authorization: Question must belong to the logged in user
* Request
  * Method: POST
  * URL: /api/tags/questions/:questionId
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "tagName": "javascript"
    }
    ```

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "id": 2,
      "tagName": "javascript"
    }
    ```

* Error response: Body validation errors
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      {
        "tagName": [
          "Tag name must be less than 20 characters",
          // and/or
          "Tag name must not have space",
          // and/or
          "This field is required"
        ]
      }
    }
    ```

* Error response: Couldn't find a Question with the specified id
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "error": "Question not found"
    }
    ```

### Get all Tags
Returns all the tags.

* Require Authentication: false
* Request
  * Method: GET
  * URL: /api/tags
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "Tags": [
        {
          "id": 1,
          "tagName": "java",
          "numQuestions": 1
        },
        {
          "id": 2,
          "tagName": "javascript",
          "numQuestions": 2
        },
        {
          "id": 3,
          "tagName": "reactjs",
          "numQuestions": 1
        }
      ]
    }
    ```

### Get all Tags of a Question
Returns all the tags of a specific question based on its id.

* Require Authentication: false
* Request
  * Method: GET
  * URL: /api/tags/questions/:questionId
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "id": 1,
      "Tags": [
        {
          "id": 2,
          "tagName": "javascript"
        },
        {
          "id": 3,
          "tagName": "reactjs"
        }
      ]
    }
    ```
* Error response: Couldn't find a Question with the specified id
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "error": "Question not found"
    }
    ```

### Delete All Tags For a Question Based on the Question's id
Removes all the tags of a specific question based on its id.

* Require Authentication: true
* Require proper authorization: Question must belong to the logged in user
* Request
  * Method: DELETE
  * URL: /api/tags/questions/:questionId
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Successfully deleted"
    }
    ```

* Error response: Couldn't find a Question with the specified id
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Question not found"
    }
    ```

## Follow/Save for Later
### Get all Saved Questions of Current User
Return all the questions saved by the current user.

* Require Authentication: true
* Request
  * Method: GET
  * URL: /api/questions/saved/current
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "Saved": [
        {
          "id": 1,
          "userId": 1,
          "question": "How can I do x, y and z?",
          "subject": "Python is crazy!",
          "createdAt": "2021-11-19 20:39:36",
          "updatedAt": "2021-11-19 20:39:36" ,
        }
      ]
    }
    ```

### Save a Question for Later
Save a question for later specified by id.

* Require Authentication: true
* Request
  * Method: POST
  * URL: /api/questions/:questionId/saved
  * Headers:
    * Content-Type: application/json

* Successful Response
  * Status Code: 201
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Saved for later"
    }
    ```

* Error response: Couldn't find a question with the specified id
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Question couldn't be found"
    }
    ```

* Error response: The current user has already saved this question
  * Status Code: 500
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "This question has already been saved"
    }
    ```

### Unsave a Question
Unsaves a question.

* Require Authentication: true
* Require proper authorization: Question must be saved by the current user
* Request
  * Method: DELETE
  * URL: /api/question/:questionId/saved
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Question unsaved"
    }
    ```

* Error response: Couldn't find a saved question with the specified id
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Question couldn't be found in your saved list"
    }
    ```

## Answer Upvote
### Get all Upvoted Answers of Current User
Return all the answers upvoted by the current user.

* Require Authentication: true
* Request
  * Method: GET
  * URL: /api/answers/upvoted/current
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "Upvoted": [
        {
          "id": 1,
          "userId": 1,
          "questionId": 1,
          "answer": "This is the answer"
        }
      ]
    }
    ```

### Upvote an Answer
Upvote an answer specified by id using the current user

* Require Authentication: true
* Request
  * Method: POST
  * URL: /api/answers/:answerId/upvoted
  * Headers:
    * Content-Type: application/json

* Successful Response
  * Status Code: 201
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Upvoted"
    }
    ```

* Error response: Couldn't find an answer with the specified id
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Answer couldn't be found"
    }
    ```

* Error response: The current user has already upvoted this answer
  * Status Code: 500
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "This answer has already been upvoted"
    }
    ```

### Undo an Upvote to an Answer
DeUpvotes an answer.

* Require Authentication: true
* Require proper authorization: Answer must be upvoted by the current user
* Request
  * Method: DELETE
  * URL: /api/answer/:answerId/upvoted
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Answer no longer upvoted"
    }
    ```

* Error response: Couldn't find an upvoted answer with the specified id
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Answer couldn't be found in your upvoted list"
    }
    ```

## Question Comments
### Edit a Question Comment
Update and return an existing question comment.

* Require Authentication: true
* Request
  * Method: PUT
  * URL: /api/questions/comments/:commentId
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "comment": "This question is wrong!",
    }
    ```

* Successful Response
  * Status Code: 201
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "id": 1,
      "userId": 1,
      "questionId": 1,
      "comment": "This question is wrong!"
    }
    ```

* Error Response: Body validation errors
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:
    ```json
    {
      "message": "Bad Request", // (or "Validation error" if generated by Sequelize),
      "errors": {
        "comment": "Comment text is required",
      }
    }
    ```

* Error response: Couldn't find a Question Comment with the specified id
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Comment couldn't be found"
    }


### Delete a Question Comment
Delete an existing Question Comment.

* Require Authentication: true
* Request
  * Method: DELETE
  * URL: /api/questions/comments/:commentId
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Successfully deleted"
    }
    ```

* Error response: Couldn't find a Question Comment with the specified id
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Comment couldn't be found"
    }

### Get a question comment based on comment id
Returns the question comment of a specific comment id.

* Require Authentication: true
* Request
  * Method: GET
  * URL: /api/questions/comments/:commentId
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      {
        "id": 1,
        "userId": 1,
        "questionId": 1,
        "comment": "Your question is neat!",
        "User": {
          "id": 1,
          "firstName": "John",
          "lastName": "Smith"
        },
      }
    }
    ```

## Answer Comments
### Edit a Answer Comment
Update and return an existing answer comment.

* Require Authentication: true
* Require proper authorization: Answer comment must belong to the current user
* Request
  * Method: PUT
  * URL: /api/answers/comments/:commentId
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "comment": "This answer is wrong!",
    }
    ```

* Successful Response
  * Status Code: 201
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "id": 1,
      "userId": 1,
      "questionId": 1,
      "comment": "This answer is wrong!",
      "createdAt": "2021-11-19 20:39:36",
      "updatedAt": "2021-11-19 20:39:36"
    }
    ```

* Error Response: Body validation errors
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:
    ```json
    {
      "message": "Bad Request", // (or "Validation error" if generated by Sequelize),
      "errors": {
        "comment": "Comment text is required",
      }
    }
    ```

* Error response: Couldn't find a Answer Comment with the specified id
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Comment couldn't be found"
    }


### Delete a Answer Comment
Delete an existing Answer Comment.

* Require Authentication: true
* Require proper authorization: Answer Comment must belong to the current user
* Request
  * Method: DELETE
  * URL: /api/answers/comments/:commentId
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Successfully deleted"
    }
    ```

* Error response: Couldn't find a Answer Comment with the specified id
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "message": "Comment couldn't be found"
    }
