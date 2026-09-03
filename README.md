# 🌟 Easy English Buddy
초보자를 위한 AI 맞춤형 영어 회화 문장 추천 서비스

## 1. 서비스 소개
- 사용자가 원하는 상황을 입력하면 AI가 즉석에서 영어 문장과 해석, 발음을 제공합니다.
- 5060 세대를 고려한 큰 글씨와 직관적인 UI, 다크모드를 지원합니다.

## 2. 기술 스택
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla JS)
- **Backend**: Python (Vercel Serverless Functions)
- **AI API**: OpenAI GPT-3.5-turbo
- **Deployment**: Vercel

## 3. 환경 변수 설정
Vercel 프로젝트 설정에서 아래 키를 반드시 추가해야 합니다:
- `OPENAI_API_KEY`: OpenAI에서 발급받은 API 키

## 4. 실행 방법
1. 이 저장소를 Clone 합니다.
2. `requirements.txt`에 명시된 패키지를 설치합니다 (`pip install -r requirements.txt`).
3. Vercel 프로젝트 환경 변수에 `OPENAI_API_KEY`를 등록합니다.
4. Vercel CLI를 통해 `vercel dev`로 로컬에서 테스트하거나 GitHub 푸시로 자동 배포합니다.

> `index.html`을 파일로 직접 열면 브라우저 보안 정책 때문에 `/api/chat` 요청이 동작하지 않을 수 있습니다. API 기능은 `vercel dev` 또는 배포된 URL에서 확인하세요.

### API 동작
- `POST /api/chat`: `{ "message": "카페에서 주문할 때" }` 형식으로 요청합니다.
- 빈 입력, 잘못된 JSON, API 키 누락, 서버 오류에 대해 JSON 오류 응답을 반환합니다.
- 브라우저에서는 요청 중 중복 제출을 막고, 응답 오류를 화면에 표시합니다.

## 5. 배포 URL
- [여기에 본인의 Vercel URL 삽입]