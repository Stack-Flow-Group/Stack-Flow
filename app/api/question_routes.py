from flask import Blueprint, request, jsonify

from app.models import Question, Answer, Tag, QuestionTag, QuestionComment, User, QuestionFollowing, db, AnswerComment
from app.forms import AnswerForm, QuestionCommentForm, QuestionFollowingForm, QuestionForm

from flask_login import current_user, login_required



question_routes = Blueprint('questions', __name__)


@question_routes.route('/')
def index():
    questions = Question.query.join(User).all()
    question_list = []

    for question in questions:
    # We're going to just do this one step at a time to get it done faster
    # Get question
        tags = []
        comments = []
        question_id = question.id
        question_res = {
            'id': question.id,
            'subject': question.subject,
            'question': question.question,
            'user_id': question.user_id,
            'User': {
                'id': question.user.id,
                'username': question.user.username
            }
        }

        #########
        # Get question comments
        questionComment_res = QuestionComment.query.filter(QuestionComment.question_id == question_id).all()
        questionComments = []
        for row in questionComment_res:
            # Get user
            user_res = u = User.query.get(row.user_id)
            user_obj = {
                'id': u.id,
                'username': u.username
            }
            questionComments.append({
                'id': row.id,
                'comment': row.comment,
                'User': user_obj
            })

        question_res["QuestionComment"] = questionComments

        ################
        # Get Ansers
        answer_res = Answer.query.filter_by(question_id = question_id)
        answers = []
        for row in answer_res:
            answer_dict = {
                'answer': row.answer,
                'id': row.id,
                'User': row.user.to_dict(),
                'question_id': row.question_id,
                'AnswerComments': []
            }
            for row in row.answer_comments:
                user_res = u = User.query.get(row.user_id)
                user_obj = {
                    'id': u.id,
                    'username': u.username
                }
                answer_dict["AnswerComments"].append({
                    'id': row.id,
                    'comment': row.comment,
                    'User': user_obj,
                    'answer_id': row.answer_id
                })
            answers.append(answer_dict)
        question_res["Answer"] = answers
            # answers.append()

        ###
        # Get Comments

        questiontags = QuestionTag.query.filter(QuestionTag.question_id == question_id).all()

        tag_res = {
            'id': question_id,
            'Tags': [
            {
                'id': questiontag.tag.id,
                'tagName': questiontag.tag.tag_name
            }
            for questiontag in questiontags]
        }

        question_res["Tags"] =  [
            {
                'id': questiontag.tag.id,
                'tag_name': questiontag.tag.tag_name
            }
            for questiontag in questiontags]

        question_list.append(question_res)

    return jsonify({"Questions": question_list})


# Get current user's questions
@question_routes.route('/current')
@login_required
def get_user_questions():
    questions = Question.query.join(User).filter(Question.user_id == current_user.id).all()

    question_res = { 'Questions': [
        {
            'id': question.id,
            'question': question.question,
            'subject': question.subject,
            'User': {
                'id': question.user.id,
                'username': question.user.username
            }
        } for question in questions]
    }

    return jsonify(question_res)

# Refractor required
###########
# Get Question
@question_routes.route('/<int:id>')
def get_question(id):
    question_res = Question.query.get(id)

    if not question_res:
        return jsonify({"error": "Question couldn't be found"}), 404


# We're going to just do this one step at a time to get it done faster
# Get question
    question = {
        'id': question_res.id,
        'subject': question_res.subject,
        'question': question_res.question,
        'user_id': question_res.user_id
    }

    user_res = User.query.get(id)
    question["User"] = {'id':user_res.id, 'username':user_res.username}

    #########
    # Get question comments
    questionComment_res = QuestionComment.query.filter(QuestionComment.question_id == question.id).all()
    questionComments = []
    for row in questionComment_res:
        # Get user
        user_res = u = User.query.get(row.user_id)
        user_obj = {
            'id': u.id,
            'username': u.username
        }
        questionComments.append({
            'id': row.id,
            'comment': row.comment,
            'User': user_obj
        })

    question["QuestionComment"] = questionComments

    ################
    # Get Ansers
    answer_res = Answer.query.filter_by(question_id = id).join(AnswerComment)
    answers = []
    for row in answer_res:
        answer_dict = {
            'answer': row.answer,
            'id': row.id,
            'question_id': row.question_id,
            'AnswerComments': []
        }
        for row in row.answer_comments:
            user_res = u = User.query.get(row.user_id)
            user_obj = {
                'id': u.id,
                'username': u.username
            }
            answer_dict["AnswerComments"].append({
                'id': row.id,
                'comment': row.comment,
                'User': user_obj,
                'answer_id': row.answer_id
            })
        answers.append(answer_dict)
    question["Answer"] = answers
        # answers.append()

    return jsonify(question)

#############
# Edit Question

@question_routes.route('/<int:id>', methods=["PUT"])
@login_required
def edit_question(id):
    question = Question.query.get(id)
    # If answer doesn't exist
    if not question:
        return jsonify({"message": "Question couldn't be found"}), 404

    # if not authorized
    # if question.user_id != current_user.id:
    #     return jsonify({"error": "Not Authorized to udpate question"}), 403

    form = QuestionForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        question.question = form.data['question']
        question.subject = form.data['subject']

        db.session.commit()

        res = {
            "id": question.id,
            "subject": question.subject,
            "question": question.question,
        }
        return jsonify(res), 201
    else:
        return form.errors, 401

###############
# Delete Question
@question_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_question(id):
    question = Question.query.get(id)

    if not question:
        return jsonify({"error": "Question couldn't be found"}), 404

    if question.user_id != current_user.id:
        return jsonify({"error": "Not Authorized to delete question"}), 403

    db.session.delete(question)
    db.session.commit()

    return jsonify({"message": "Successfully deleted"})

@question_routes.route('/', methods=["POST"])
@login_required
def create_question():
    # Create Question
    form = QuestionForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        question = Question(
            question=form.data['question'],
            subject=form.data['subject'],
            user_id=current_user.id
        )
        db.session.add(question)
        db.session.commit()
        res = {
            "id": question.id,
            "question": question.question,
            "subject": question.subject,
            "user_id": current_user.id
        }
        return jsonify(res), 201
    else:
        return form.errors, 401

# Create Answer Route
@question_routes.route('/<int:question_id>/answers', methods=['POST'])
@login_required
def create_answer(question_id):
    # Check to see if question exists
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    # Check to see if user has already answered
    existing_answer = Answer.query.filter_by(question_id=question_id, user_id=current_user.id).first()
    if existing_answer:
        return jsonify({"error": "User already has a answer for question"}), 400

    # Create Answer
    form = AnswerForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        answer = Answer(
            user_id=current_user.id,
            question_id=question_id,
            answer=form.data['answer']
        )
        db.session.add(answer)
        db.session.commit()
        res = {
            "id": answer.id,
            "userId": current_user.id,
            "questionId": answer.question_id,
            "answer": answer.answer
        }
        return jsonify(res), 201
    else:
        return form.errors, 401

# Delete a Tag of a Question Based on the Question's id
@question_routes.route('/tags/<int:question_id>/<int:tag_id>', methods=['DELETE'])
@login_required
def delete_tag(question_id, tag_id):
  question = Question.query.get(question_id)
  tag = Tag.query.get(tag_id)
  if not question:
    return jsonify({"message": "Question couldn't be found"}), 404
  elif not tag:
    return jsonify({"message": "Tag couldn't be found"}), 404
  elif current_user.id != question.user.id:
    return jsonify({"message": "Unauthorized"}), 401

  questiontag = QuestionTag.query.filter_by(question_id=question_id, tag_id=tag_id).first()
  if not questiontag:
    return jsonify({"message": "Tag not associated with Question"}), 404
  else:
    db.session.delete(questiontag)
    db.session.commit()

    return jsonify({"message": "Successfully Removed"}), 200

# # Get Current user's question comments
# @question_routes.route('/comments/current')
# @login_required
# def question_comments():
#     comments = QuestionComment.query.join(Question).filter(QuestionComment.question_id == current_user.id).all()
#
#     comments_res = { 'QuestionComments': [
#         {
#             'id': comment.id,
#             'userId': comment.user_id,
#             'questionId': comment.question_id,
#             'comment': comment.comment,
#             'User': {
#                 'id': comment.user.id,
#                 'username': comment.user.username,
#                 'email': comment.user.email
#             }
#         } for comment in comments]
#     }
#
#     return jsonify(comments_res)

@question_routes.route('/<int:question_id>/comments', methods=['GET'])
def question_comments(question_id):
    comments = QuestionComment.query.join(Question).filter(QuestionComment.question_id == question_id).all()

    comments_res = { 'QuestionComments': [
        {
            'id': comment.id,
            'userId': comment.user_id,
            'questionId': comment.question_id,
            'comment': comment.comment,
            'User': {
                'id': comment.user.id,
                'username': comment.user.username,
                'email': comment.user.email
            }
        } for comment in comments]
    }

    return jsonify(comments_res)

# Create a question comment
@question_routes.route('/<int:question_id>/comments', methods=['POST'])
@login_required
def create_comment(question_id):
    # Check if question exists
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Question couldn't be found"}), 404

    # Create Question
    form = QuestionCommentForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        comment = QuestionComment(
            user_id=current_user.id,
            question_id=question_id,
            comment=form.data['comment']
        )

        db.session.add(comment)
        db.session.commit()
        res = {
            "id": comment.id,
            "userId": comment.user_id,
            "questionId": comment.question_id,
            "comment": comment.comment
        }
        return jsonify(res), 201
    else:
        return form.errors, 401

# Update a question comment
@question_routes.route('/comments/<int:comment_id>', methods=['PUT'])
@login_required
def update_comment(comment_id):
    comment = QuestionComment.query.get(comment_id)
    # Check if comment exists
    if not comment:
        return jsonify({"error": "Comment couldn't be found"}), 404

    # Check if authorized
    if comment.user_id != current_user.id:
        return jsonify({"error": "Not Authorized to update comment"}), 403

    form = QuestionCommentForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        comment.comment = form.data['comment']

        db.session.commit()

        res = {
            "id": comment.id,
            "userId": comment.user_id,
            "questionId": comment.question_id,
            "comment": comment.comment
        }
        return jsonify(res), 201
    else:
        return form.errors, 401

##Delete a question comment
@question_routes.route('/comments/<int:comment_id>', methods=['DELETE'])
@login_required
def delete_comment(comment_id):
    comment = QuestionComment.query.get(comment_id)

    # Check if comment exists
    if not comment:
        return jsonify({"error": "Comment couldn't be found"}), 404

    # Check if authorized
    if comment.user_id != current_user.id:
        return jsonify({"error": "Not Authorized to delete comment"}), 403

    db.session.delete(comment)
    db.session.commit()

    return jsonify({"message": "Successfully deleted"})


# Get all Saved Questions of Current User
@question_routes.route('/saved/current')
def questions_followed():
    following_questions = QuestionFollowing.query.join(Question).filter(QuestionFollowing.user_id == current_user.id).all()

    response = {
        'Following': [
            {
                # 'id': following_question.id,
                'userId': following_question.user_id,
                'questionId': following_question.question_id,
                'Question': {
                    'id': following_question.question.id,
                    'question': following_question.question.question,
                    'subject': following_question.question.subject
                }
            }
            for following_question in following_questions
        ]
    }
    # response = {
    #   'questions': [following.question.to_dict() for following in following_questions]
    #   }

    return jsonify(response)

# Save a Question for Later
@question_routes.route('/<int:question_id>/saved', methods=['POST'])
@login_required
def follow_question(question_id):
    following = QuestionFollowing(user_id = current_user.id, question_id = question_id)
    db.session.add(following)
    db.session.commit()
    res = {
       'message': 'Saved for Later'
    }
    return jsonify(res), 200

# Unsave a Question
@question_routes.route('/<int:question_id>/saved', methods=['DELETE'])
@login_required
def unfollow_question(question_id):
    following = QuestionFollowing.query.get([current_user.id, question_id])
    if not following:
       return jsonify({"message": "Question couldn't be found in your saved list"}), 404
    db.session.delete(following)
    db.session.commit()
    res = {
       'message': 'Question unsaved'
    }
    return jsonify(res), 200

@question_routes.route('/comments/<int:comment_id>', methods=['GET'])
@login_required
def get_comment(comment_id):
    comment = QuestionComment.query.get(comment_id)

    # Check if comment exists
    if not comment:
        return jsonify({"error": "Comment couldn't be found"}), 404


    return jsonify({
        'id': comment.id,
        'userId': comment.user_id,
        'questionId': comment.question_id,
        'comment': comment.comment,
        'User': {
            'id': comment.user.id,
            'username': comment.user.username,
            'email': comment.user.email
        }
    }), 200

# Get all questions of a specific tag
@question_routes.route('/tags/<int:tag_id>', methods=['GET'])
def get_questions_by_tag(tag_id):
  tag = Tag.query.filter(Tag.id == tag_id).first()

  if tag:
    questiontags = QuestionTag.query.filter(QuestionTag.tag_id == tag_id).all()

    return jsonify({
      "tagName": tag.tag_name,
      "Questions": [
        {
          'Tags': [questiontag.tag.to_dict() for questiontag in QuestionTag.query.filter(QuestionTag.question_id == questiontag.question_id).all()],
          'id': questiontag.question_id,
          'question': questiontag.question.question,
          'subject': questiontag.question.subject
        }
        for questiontag in questiontags
      ]
    }), 200
  else:
    return jsonify({
      "Questions": []
    }), 200
