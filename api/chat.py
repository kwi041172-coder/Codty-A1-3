import os

from openai import APIConnectionError, APIError, AuthenticationError, OpenAI, RateLimitError
from flask import Flask, jsonify, request, send_from_directory


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
app = Flask(__name__, static_folder=PROJECT_ROOT, static_url_path="")


def get_openai_api_key():
    value = os.getenv("OPENAI_API_KEY", "").strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1].strip()
    if value.lower().startswith("bearer "):
        value = value[7:].strip()
    return value


@app.get("/")
def home():
    return send_from_directory(PROJECT_ROOT, "index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    api_key = get_openai_api_key()
    if not api_key:
        return jsonify(error="OPENAI_API_KEY 환경 변수가 설정되지 않았습니다."), 500

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="JSON 형식의 요청이 필요합니다."), 400

    user_message = data.get("message", "")
    if not isinstance(user_message, str) or not user_message.strip():
        return jsonify(error="메시지를 입력하세요."), 400

    try:
        client = OpenAI(api_key=api_key, timeout=30.0, max_retries=1)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
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
    except AuthenticationError as error:
        app.logger.warning("OpenAI authentication failed (request_id=%s)", error.request_id)
        return jsonify(
            error=(
                "OpenAI 인증에 실패했습니다. Vercel 환경 변수에 "
                "OpenAI Platform API 키가 등록되어 있고 재배포되었는지 확인해주세요."
            )
        ), 502
    except RateLimitError:
        return jsonify(error="OpenAI 사용량 한도를 초과했습니다. 잠시 후 다시 시도해주세요."), 429
    except APIConnectionError:
        return jsonify(error="OpenAI 서버에 연결할 수 없습니다. 잠시 후 다시 시도해주세요."), 502
    except APIError:
        return jsonify(error="OpenAI 요청을 처리하지 못했습니다. 잠시 후 다시 시도해주세요."), 502

    reply = response.choices[0].message.content or "응답을 받지 못했습니다."
    return jsonify(reply=reply)


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify(error=error.description or "POST 요청만 허용됩니다."), 405
