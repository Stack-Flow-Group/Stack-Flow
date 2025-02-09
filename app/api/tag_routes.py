from flask import Blueprint, request, jsonify, current_app
from app.models import Question, QuestionTag, Tag, db
from app.forms import TagForm
from flask_login import current_user, login_required


tag_routes = Blueprint('tags', __name__)

@tag_routes.route('/')
def index():
    tags = Tag.query.all()
    tag_res = { 'Tags': [
        {
            'id': tag.id,
            'tagName': tag.tag_name,
            'numQuestions': len(tag.question_tags)
        } for tag in tags]
    }

    return jsonify(tag_res)




# Get all Tags of a Question Based on the Question's id
@tag_routes.route('/questions/<int:question_id>')
def get_tags(question_id):
  question = Question.query.get(question_id)
  if not question:
    return jsonify({"error": "Question not found"}), 404

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

  return jsonify(tag_res)

# Add a Tag For a Question Based on the Question's id
@tag_routes.route('/questions/<int:question_id>', methods=['POST'])
@login_required
def add_tags(question_id):
  question = Question.query.get(question_id)
  if not question:
    return jsonify({"error": "Question not found"}), 404
  elif current_user.id != question.user.id:
    return jsonify({"message": "Unauthorized"}), 401
  form = TagForm()
  form['csrf_token'].data = request.cookies['csrf_token']
  if form.validate_on_submit():
    tag_name = form.data['tagName'].lower()
    tag = Tag.query.filter_by(tag_name=tag_name).first()
    if not tag:
      newTag = Tag(
        tag_name = tag_name
      )
      db.session.add(newTag)
      db.session.commit()
      tag = newTag
    questiontag = QuestionTag(
      question_id = question_id,
      tag_id = tag.id
    )
    db.session.add(questiontag)
    db.session.commit()
    res = {
      "id": tag.id,
      "tagName": tag_name
    }
    return jsonify(res), 200
  else:
    return form.errors, 400

# Delete All Tags For a Question Based on the Question's id
@tag_routes.route('/questions/<int:question_id>', methods=['DELETE'])
@login_required
def delete_tags(question_id):
  question = Question.query.get(question_id)

  if not question:
    return jsonify({"error": "Question not found"}), 404

  elif current_user.id != question.user.id:
    return jsonify({"message": "Unauthorized"}), 401

  questiontags = QuestionTag.query.filter(QuestionTag.question_id == question_id).all()
  for tag in questiontags:
    db.session.delete(tag)

  db.session.commit()

  return jsonify({"message": "Successfully deleted"})
