from flask import jsonify

from sourcerer import app, logger
from sourcerer.models import Answer


@app.route('/api/v1/answers/<answer_id>', methods=['GET'])
def get_answer(answer_id):
    answer = Answer.objects.get_or_404(id=answer_id)
    return jsonify(answer)
