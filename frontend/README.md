# 블로그/뉴스 모니터링 시스템 - Frontend

React + TypeScript + Vite 기반 프론트엔드 애플리케이션

## 기술 스택

- **React 19** - UI 라이브러리
- **TypeScript** - 타입 안정성
- **Vite** - 빌드 도구 및 개발 서버
- **TanStack Query** - 서버 상태 관리 및 캐싱
- **Zustand** - 클라이언트 상태 관리
- **Tailwind CSS** - 유틸리티 기반 CSS
- **shadcn/ui** - 재사용 가능한 UI 컴포넌트 (예정)
- **Axios** - HTTP 클라이언트
- **Vitest** - 유닛 테스트
- **React Testing Library** - 컴포넌트 테스트
- **Playwright** - E2E 테스트 (예정)

## 프로젝트 구조

```
frontend/
├── src/
│   ├── components/       # React 컴포넌트
│   │   ├── ui/          # shadcn/ui 기본 컴포넌트
│   │   ├── layout/      # 레이아웃 컴포넌트
│   │   ├── common/      # 공통 컴포넌트
│   │   └── features/    # 기능별 컴포넌트
│   ├── hooks/           # Custom hooks
│   ├── pages/           # 페이지 컴포넌트
│   ├── services/        # API 서비스
│   ├── store/           # Zustand stores
│   ├── types/           # TypeScript 타입 정의
│   ├── utils/           # 유틸리티 함수
│   └── tests/           # 테스트 파일
├── public/              # 정적 파일
└── ...
```

## 시작하기

### 1. 의존성 설치

```bash
npm install
```

### 2. 환경 변수 설정

`.env` 파일이 이미 생성되어 있습니다:

```env
VITE_API_URL=http://localhost:8000
```

### 3. 개발 서버 실행

```bash
npm run dev
```

브라우저에서 http://localhost:5173/ 열기

### 4. 백엔드 서버 실행

프론트엔드가 정상 작동하려면 백엔드 API 서버가 실행 중이어야 합니다:

```bash
cd ../backend
venv/Scripts/python.exe -m uvicorn app.main:app --reload
```

백엔드 서버: http://localhost:8000

## 사용 가능한 스크립트

```bash
npm run dev          # 개발 서버 시작
npm run build        # 프로덕션 빌드
npm run preview      # 프로덕션 빌드 미리보기
npm run lint         # ESLint 실행
npm run test         # Vitest 테스트 실행
npm run test:watch   # 테스트 watch 모드
npm run test:ui      # Vitest UI 모드
npm run test:coverage # 테스트 커버리지
```

## 현재 구현 상태

### ✅ 완료
- [x] React 프로젝트 초기화 (Vite + TypeScript)
- [x] 필수 라이브러리 설치
- [x] Tailwind CSS 설정
- [x] TypeScript 경로 별칭 설정 (`@/*`)
- [x] Vitest 테스트 환경 설정
- [x] API 서비스 기본 구조 (`services/api.ts`)
- [x] TypeScript 타입 정의 (`types/site.types.ts`)
- [x] QueryClient 설정 및 Provider
- [x] 백엔드 API 연결 확인 페이지

### 🚧 진행 예정
- [ ] shadcn/ui 컴포넌트 추가
- [ ] 사이트 관리 UI (목록, 추가, 수정, 삭제)
- [ ] 글 목록 UI
- [ ] 대시보드
- [ ] 실시간 알림
- [ ] 프론트엔드 테스트 작성

## API 연결

프론트엔드는 `src/services/api.ts`에 정의된 Axios 인스턴스를 통해 백엔드 API와 통신합니다.

```typescript
import api from '@/services/api';

// 예시: 사이트 목록 조회
const response = await api.get('/api/v1/sites');
```

## 타입 정의

TypeScript 타입은 `src/types/` 디렉토리에 정의되어 있습니다:

- `site.types.ts` - 사이트 및 스크래핑 규칙 관련 타입

## 개발 가이드

### 컴포넌트 작성

```typescript
// src/components/features/sites/SiteCard.tsx
import { Site } from '@/types/site.types';

interface SiteCardProps {
  site: Site;
  onDelete?: (id: number) => void;
}

export function SiteCard({ site, onDelete }: SiteCardProps) {
  return (
    <div className="border rounded-lg p-4">
      <h3 className="font-bold">{site.name}</h3>
      <p className="text-sm text-gray-600">{site.url}</p>
    </div>
  );
}
```

### API 호출 (TanStack Query)

```typescript
// src/hooks/useSites.ts
import { useQuery } from '@tanstack/react-query';
import api from '@/services/api';
import { Site } from '@/types/site.types';

export function useSites() {
  return useQuery({
    queryKey: ['sites'],
    queryFn: async () => {
      const { data } = await api.get<Site[]>('/api/v1/sites');
      return data;
    },
  });
}
```

### 테스트 작성

```typescript
// src/tests/unit/hooks/useSites.test.ts
import { renderHook, waitFor } from '@testing-library/react';
import { useSites } from '@/hooks/useSites';

describe('useSites', () => {
  it('should fetch sites', async () => {
    const { result } = renderHook(() => useSites());
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
  });
});
```

## 문제 해결

### 백엔드 연결 실패

프론트엔드 페이지에서 "연결 실패" 메시지가 표시되면:

1. 백엔드 서버가 실행 중인지 확인
2. `.env` 파일의 `VITE_API_URL` 확인
3. 브라우저 개발자 도구의 Network 탭에서 요청 확인

### CORS 오류

백엔드의 CORS 설정이 올바른지 확인하세요 (`backend/app/main.py`).

## 다음 단계

1. shadcn/ui 컴포넌트 추가
2. 사이트 관리 UI 구현
3. 글 목록 페이지 구현
4. 대시보드 구현
5. 프론트엔드 테스트 작성

## 라이선스

MIT
