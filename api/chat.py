import os

import openai
from flask import Flask, jsonify, request, send_from_directory


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
app = Flask(__name__, static_folder=PROJECT_ROOT, static_url_path="")
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.get("/")
def home():
    return send_from_directory(PROJECT_ROOT, "index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    if not openai.api_key:
        return jsonify(error="OPENAI_API_KEY 환경 변수가 설정되지 않았습니다."), 500

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="JSON 형식의 요청이 필요합니다."), 400

    user_message = data.get("message", "")
    if not isinstance(user_message, str) or not user_message.strip():
        return jsonify(error="메시지를 입력하세요."), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "당신은 초보자를 위한 친절한 영어 선생님입니다. "
                        "요청한 상황에 맞는 짧은 영어 문장 3개와 한글 해석, "
                        "그리고 한국어 발음을 적어주세요."
                    ),
                },
                {"role": "user", "content": user_message.strip()},
            ],
        )
    except openai.error.OpenAIError:
        return jsonify(error="AI 서비스에 연결할 수 없습니다. 잠시 후 다시 시도해주세요."), 502

    reply = response.choices[0].message.content
    return jsonify(reply=reply)


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify(error=error.description or "POST 요청만 허용됩니다."), 405
