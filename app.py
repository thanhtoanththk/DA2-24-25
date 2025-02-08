from flask import Flask, request, jsonify, render_template
from model_utils import T5TextCorrector, XRBTextPredictor
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
import re

# Initialize Flask app
app = Flask(__name__)

# Cấu hình URI kết nối tới cơ sở dữ liệu (thay bằng thông tin của bạn)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://nlp:secret@mysql/nlp'
Bootstrap(app)
# Khởi tạo các extension
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Định nghĩa mô hình CorrectedText
class CorrectedText(db.Model):
    __tablename__ = 'corrected_texts'

    id = db.Column(db.Integer, primary_key=True)
    original_text = db.Column(db.Text, nullable=False)
    corrected_text = db.Column(db.Text, nullable=False)

    def __init__(self, original_text, corrected_text):
        self.original_text = original_text
        self.corrected_text = corrected_text

    def __repr__(self):
        return f"<CorrectedText {self.id}>"

corrector = T5TextCorrector()
predictor = XRBTextPredictor()
@app.route('/correct', methods=['POST'])
def correct_text():
    # Get input text from the request
    input_data = request.form.get('incorrect_text')

    if not input_data:
        return jsonify({
            'status': 'error',
            'message': 'Bad request, missing data.'
        }), 400

    sentences, punctuation = split_sentences_and_punctuation(input_data)
    index = 0
    corrected_sentences = []
    # # Dự đoán và sửa từng câu
    for sentence in sentences:
        pred = predictor.predict_language(sentence + '.')
        if pred == 1:
            corrected_sentence = corrector.correct_text(sentence + '.')
            # Lưu kết quả vào cơ sở dữ liệu
            new_corrected_text = CorrectedText(original_text=sentence, corrected_text=corrected_sentence.rstrip('.'))
            db.session.add(new_corrected_text)

            corrected_sentences.append(corrected_sentence.rstrip('.') + punctuation[index])
        elif pred == 2:
            corrected_sentences.append(sentence + punctuation[index])
        else:
            return jsonify({
                'status': 'error',
                'message': 'Hệ thống chỉ xử lý tiếng việt.'
            }), 400
        index += 1

    # Commit các thay đổi vào DB
    db.session.commit()

    correct_texts = ' '.join(corrected_sentences)

    # Return the corrected text as a JSON response
    return jsonify({
        'status': 'success',
        'message': '',
        'data': {
            'corrected_text': f'{correct_texts}',
        }
    }), 200

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# app name
@app.errorhandler(404)

# inbuilt function which takes error as parameter
def not_found(e):
    # defining function
    return render_template("404.html")

def split_sentences_and_punctuation(text):
    # Biểu thức chính quy để tách câu và dấu câu (., ?, !)
    # Chúng ta thêm điều kiện để lấy câu cuối mà không có dấu câu kết thúc
    sentence_pattern = r'([^.!?]+)([.!?])|([^.!?]+)$'

    # Tìm tất cả các câu và dấu câu tương ứng
    matches = re.findall(sentence_pattern, text)

    # Tách câu và dấu câu thành hai mảng riêng biệt
    sentences = []
    punctuation = []

    for match in matches:
        # Kiểm tra phần tử không phải là chuỗi trống
        if match[0]:
            sentences.append(match[0].strip())  # Mảng các câu
            punctuation.append(match[1])  # Mảng các dấu câu
        elif match[2]:
            sentences.append(match[2].strip())  # Câu cuối không có dấu câu
            punctuation.append('')  # Không có dấu câu cho câu cuối

    return sentences, punctuation
