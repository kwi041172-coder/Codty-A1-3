# 🌟 Easy English Buddy
초보자를 위한 AI 맞춤형 영어 회화 문장 추천 서비스

## 1. 서비스 소개
- 사용자가 원하는 상황을 입력하면 AI가 즉석에서 영어 문장과 해석, 발음을 제공합니다.
- 5060 세대를 고려한 직관적인 UI, 반응형 화면, 다크모드를 지원합니다.

## 2. 기술 스택
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla JS)
- **Backend**: Python (Vercel Serverless Functions)
- **AI API**: OpenAI GPT-4o-mini (`openai>=1.0.0,<2.0.0`)
- **Deployment**: Vercel

Vercel은 `pyproject.toml`의 `tool.vercel.entrypoint` 설정을 통해 `api.chat:app`을 Flask 애플리케이션 진입점으로 사용합니다. Flask가 `/`에서 `index.html`을 제공하고 `/api/chat`에서 AI 요청을 처리하므로 별도 `vercel.json` 재작성 설정이 필요하지 않습니다.
Python 실행 버전은 `.python-version`과 `pyproject.toml`에서 3.12로 고정하며, `project` 테이블은 Vercel의 `uv lock` 의존성 설치에 사용됩니다.

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
- `GET /api/chat`은 허용하지 않습니다.
- 빈 입력, 잘못된 JSON, 잘못된 요청 형식, API 키 누락, 서버 오류에 대해 JSON 오류 응답을 반환합니다.
- 브라우저에서는 요청 중 중복 제출을 막고, 응답 오류를 화면에 표시합니다.

## 5. 배포
1. GitHub 저장소를 Vercel에 연결합니다.
2. Vercel 프로젝트 설정의 **Environment Variables**에 `OPENAI_API_KEY`를 등록합니다.
3. 프로젝트의 Root Directory가 이 폴더인지 확인합니다.
4. GitHub의 `main` 브랜치에 push하면 자동 배포되며, 수동 배포는 다음 명령으로 실행합니다.

```powershell
vercel --prod
```

배포 후 브라우저에서 `/api/chat` 기능을 확인합니다. API 키는 소스 코드나 GitHub에 저장하지 않습니다.