# 🌟 Easy English Buddy
초보자를 위한 AI 맞춤형 영어 회화 문장 추천 서비스

## 1. 서비스 소개
- 사용자가 원하는 상황을 입력하면 AI가 즉석에서 영어 문장과 해석, 발음을 제공합니다.
- 5060 세대를 고려한 직관적인 UI, 반응형 화면, 다크모드를 지원합니다.

## 2. 기술 스택
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla JS)
- **Backend**: Python (Vercel Serverless Functions)
- **AI API**: Anthropic Claude Haiku 4.5 (`anthropic>=1.0.0,<2.0.0`)
- **Deployment**: Vercel

Vercel은 `pyproject.toml`의 `tool.vercel.entrypoint` 설정을 통해 `api.chat:app`을 Flask 애플리케이션 진입점으로 사용합니다. Flask가 `/`에서 `index.html`을 제공하고 `/api/chat`에서 AI 요청을 처리하므로 별도 `vercel.json` 재작성 설정이 필요하지 않습니다.
Python 실행 버전은 `.python-version`과 `pyproject.toml`에서 3.12로 고정하며, `project` 테이블은 Vercel의 `uv lock` 의존성 설치에 사용됩니다.

## 3. 환경 변수 설정
Vercel 프로젝트 설정에서 아래 키를 반드시 추가해야 합니다:
- `ANTHROPIC_API_KEY`: Anthropic Console에서 발급받은 API 키

## 4. 실행 방법
1. 이 저장소를 Clone 합니다.
2. `requirements.txt`에 명시된 패키지를 설치합니다 (`pip install -r requirements.txt`).
3. Vercel 프로젝트 환경 변수에 `ANTHROPIC_API_KEY`를 등록합니다.
4. Vercel CLI를 통해 `vercel dev`로 로컬에서 테스트하거나 GitHub 푸시로 자동 배포합니다.

> `index.html`을 파일로 직접 열면 브라우저 보안 정책 때문에 `/api/chat` 요청이 동작하지 않을 수 있습니다. API 기능은 `vercel dev` 또는 배포된 URL에서 확인하세요.

### API 동작
- `POST /api/chat`: `{ "message": "카페에서 주문할 때" }` 형식으로 요청합니다.
- `GET /api/chat`은 허용하지 않습니다.
- 빈 입력, 잘못된 JSON, 잘못된 요청 형식, API 키 누락, 서버 오류에 대해 JSON 오류 응답을 반환합니다.
- 브라우저에서는 요청 중 중복 제출을 막고, 응답 오류를 화면에 표시합니다.

## 5. 배포
1. GitHub 저장소를 Vercel에 연결합니다.
2. Vercel 프로젝트 설정의 **Environment Variables**에 `ANTHROPIC_API_KEY`를 등록합니다.
3. 프로젝트의 Root Directory가 이 폴더인지 확인합니다.
4. 배포 URL : https://codty-a1-3.vercel.app/
5. GitHub의 `main` 브랜치에 push하면 자동 배포되며, 수동 배포는 다음 명령으로 실행합니다.

```powershell
vercel --prod
```

배포 후 브라우저에서 `/api/chat` 기능을 확인합니다. API 키는 소스 코드나 GitHub에 저장하지 않습니다.

### Claude 인증 오류 점검
- 키는 Claude 웹사이트의 로그인·구독 비밀번호가 아니라 [Anthropic Console](https://console.anthropic.com/settings/keys)에서 만든 API 키여야 합니다.
- Vercel 값에는 키만 입력합니다. `Bearer` 접두사, 따옴표, 줄바꿈, 앞뒤 공백을 포함하지 않아야 합니다.
- `ANTHROPIC_API_KEY`의 대상 환경(Production)을 선택하고 저장한 뒤 반드시 새 배포를 실행합니다.
- 모델을 변경해야 하면 Vercel 환경 변수에 `ANTHROPIC_MODEL`을 추가할 수 있습니다. 기본값은 `claude-haiku-4-5-20251001`입니다.
- Claude 구독과 Anthropic API 결제·사용 한도는 별도이므로 Console의 Billing과 Limits도 확인합니다.
- 배포된 주소에서 `/api/health`를 열어 `configured: true`인지 확인할 수 있습니다. 이 경로는 키 원문을 반환하지 않습니다.
