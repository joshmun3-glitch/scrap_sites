# Site Monitor Backend

블로그/뉴스 사이트 모니터링 애플리케이션의 백엔드 API

## 기술 스택

- **FastAPI**: Python 웹 프레임워크
- **PostgreSQL**: 데이터베이스
- **SQLAlchemy**: ORM
- **Alembic**: 데이터베이스 마이그레이션
- **Celery**: 비동기 작업 큐
- **Redis**: 캐시 및 메시지 브로커
- **pytest**: 테스트 프레임워크

## 설치

### 1. 가상 환경 생성 및 활성화

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정

`.env.example`을 복사하여 `.env` 파일을 생성하고 필요한 값을 설정하세요.

```bash
cp .env.example .env
```

### 4. 데이터베이스 시작 (Docker)

```bash
# 프로젝트 루트에서
docker-compose up -d
```

### 5. 데이터베이스 마이그레이션

```bash
alembic upgrade head
```

## 실행

### 개발 서버

```bash
uvicorn app.main:app --reload --port 8000
```

API 문서: http://localhost:8000/docs

### Celery Worker (별도 터미널)

```bash
celery -A app.tasks.celery_app worker --loglevel=info
```

### Celery Beat (스케줄러, 별도 터미널)

```bash
celery -A app.tasks.celery_app beat --loglevel=info
```

## 테스트

### 모든 테스트 실행

```bash
pytest
```

### 커버리지와 함께 실행

```bash
pytest --cov=app --cov-report=html
```

커버리지 리포트: `htmlcov/index.html`

### 특정 테스트만 실행

```bash
# 통합 테스트만
pytest tests/integration/

# 특정 파일
pytest tests/integration/test_sites_api.py

# 특정 테스트
pytest tests/integration/test_sites_api.py::TestCreateSite::test_create_rss_site_success
```

## API 엔드포인트

### Sites

- `POST /api/v1/sites` - 새 사이트 생성
- `GET /api/v1/sites` - 사이트 목록 조회
- `GET /api/v1/sites/{id}` - 특정 사이트 조회
- `PUT /api/v1/sites/{id}` - 사이트 수정
- `DELETE /api/v1/sites/{id}` - 사이트 삭제
- `PATCH /api/v1/sites/{id}/toggle` - 활성 상태 토글

## 프로젝트 구조

```
backend/
├── app/
│   ├── api/v1/         # API 라우터
│   ├── models/         # SQLAlchemy 모델
│   ├── schemas/        # Pydantic 스키마
│   ├── services/       # 비즈니스 로직
│   ├── tasks/          # Celery 작업
│   ├── utils/          # 유틸리티 함수
│   ├── config.py       # 설정
│   ├── database.py     # 데이터베이스 설정
│   └── main.py         # FastAPI 앱
├── tests/
│   ├── unit/           # 유닛 테스트
│   ├── integration/    # 통합 테스트
│   └── fixtures/       # 테스트 픽스처
├── alembic/            # 마이그레이션 파일
├── requirements.txt    # Python 의존성
└── pytest.ini          # pytest 설정
```

## 개발 가이드

### 데이터베이스 마이그레이션 생성

```bash
alembic revision --autogenerate -m "설명"
alembic upgrade head
```

### 코드 스타일

- 코드 작성 시 PEP 8 스타일 가이드를 따릅니다
- 함수와 클래스에 docstring을 작성합니다

## 문제 해결

### 데이터베이스 연결 오류

PostgreSQL과 Redis가 실행 중인지 확인하세요:

```bash
docker-compose ps
```

### 마이그레이션 오류

데이터베이스를 초기화하고 다시 마이그레이션:

```bash
docker-compose down -v
docker-compose up -d
alembic upgrade head
```
