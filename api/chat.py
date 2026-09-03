# api/chat.py
from http.server import BaseHTTPRequestHandler
import json
import os
import openai

# 환경 변수에서 API 키 로드 (보안 준수)
openai.api_key = os.getenv("OPENAI_API_KEY")

class handler(BaseHTTPRequestHandler):
    def _send_json(self, status, payload):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(payload, ensure_ascii=False).encode('utf-8'))

    def do_GET(self):
        self._send_json(405, {"error": "POST 요청만 허용됩니다."})

    def do_POST(self):
        try:
            if not openai.api_key:
                self._send_json(500, {"error": "OPENAI_API_KEY 환경 변수가 설정되지 않았습니다."})
                return

            content_length_header = self.headers.get('Content-Length')
            if content_length_header is None:
                self._send_json(400, {"error": "요청 본문이 필요합니다."})
                return

            try:
                content_length = int(content_length_header)
            except ValueError:
                self._send_json(400, {"error": "잘못된 요청 본문입니다."})
                return

            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data)
            except json.JSONDecodeError:
                self._send_json(400, {"error": "JSON 형식의 요청이 필요합니다."})
                return

            if not isinstance(data, dict):
                self._send_json(400, {"error": "잘못된 요청 형식입니다."})
                return

            user_message = data.get("message", "")

            # 실패 처리 1: 빈 입력값
            if not isinstance(user_message, str) or not user_message.strip():
                self._send_json(400, {"error": "메시지를 입력하세요."})
                return

            # AI API 호출
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 초보자를 위한 친절한 영어 선생님입니다. 요청한 상황에 맞는 짧은 영어 문장 3개와 한글 해석, 그리고 한국어 발음을 적어주세요."},
                    {"role": "user", "content": user_message}
                ]
            )

            reply = response.choices[0].message.content
            
            self._send_json(200, {"reply": reply})

        except Exception:
            # 실패 처리 2: API 또는 서버 오류
            self._send_json(500, {"error": "서버 오류가 발생했습니다."})