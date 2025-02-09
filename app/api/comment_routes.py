# Need to verify: are the routes below used or not

## Overrided by /api/questions/comments/:commentId

from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required

from app.forms import QuestionCommentForm
from app.models import QuestionComment, db

comments_routes = Blueprint('comments', __name__)


# Get a comment
@comments_routes.route('/<int:comment_id>', methods=['GET'])
@login_required
def get_comment(comment_id):
    comment = QuestionComment.query.get(comment_id)

    # Check if comment exists
    if not comment:
        return jsonify({"error": "Comment couldn't be found"}), 404

    print(comment.comment)

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
    })

# Update a question comment
@comments_routes.route('/<int:comment_id>', methods=['PUT'])
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

# Delete a question comment
@comments_routes.route('/<int:comment_id>', methods=['DELETE'])
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
