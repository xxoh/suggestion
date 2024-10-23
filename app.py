from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# SQLite 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///suggestions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 데이터베이스 모델 정의
class Suggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    response = db.Column(db.String(500), nullable=True)

# 데이터베이스 생성
with app.app_context():
    db.create_all()

# 모든 건의글 조회
@app.route('/api/suggestions', methods=['GET'])
def get_suggestions():
    suggestions = Suggestion.query.all()
    suggestions_list = [{'id': s.id, 'content': s.content, 'response': s.response} for s in suggestions]
    return jsonify(suggestions_list)

# 새로운 건의글 제출
@app.route('/api/suggestions', methods=['POST'])
def add_suggestion():
    data = request.get_json()
    new_suggestion = Suggestion(content=data['content'])
    db.session.add(new_suggestion)
    db.session.commit()
    return jsonify({'id': new_suggestion.id, 'content': new_suggestion.content, 'response': new_suggestion.response})

# 선생님이 건의글에 답변 추가
@app.route('/api/suggestions/<int:id>/response', methods=['POST'])
def add_response(id):
    data = request.get_json()
    suggestion = Suggestion.query.get_or_404(id)
    suggestion.response = data['response']
    db.session.commit()
    return jsonify({'id': suggestion.id, 'content': suggestion.content, 'response': suggestion.response})

if __name__ == '__main__':
    app.run(debug=True)
