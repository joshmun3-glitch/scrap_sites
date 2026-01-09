import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '@/services/api';

export default function Home() {
  const [apiStatus, setApiStatus] = useState<'checking' | 'connected' | 'error'>('checking');
  const [errorMessage, setErrorMessage] = useState<string>('');

  useEffect(() => {
    const checkBackend = async () => {
      try {
        await api.get('/api/v1/sites/');
        setApiStatus('connected');
      } catch (error) {
        setApiStatus('error');
        setErrorMessage(error instanceof Error ? error.message : 'Unknown error');
      }
    };

    checkBackend();
  }, []);

  return (
    <div className="flex items-center justify-center p-4 py-12">
      <div className="max-w-2xl w-full bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">
          블로그/뉴스 모니터링 시스템
        </h1>

        <div className="space-y-4">
          <div className="border-l-4 border-blue-500 bg-blue-50 p-4">
            <h2 className="font-semibold text-blue-900 mb-2">기술 스택</h2>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>• Frontend: React 19 + TypeScript + Vite</li>
              <li>• State: Zustand + TanStack Query</li>
              <li>• UI: Tailwind CSS + shadcn/ui</li>
              <li>• Backend: FastAPI + SQLAlchemy</li>
            </ul>
          </div>

          <div className={`border-l-4 p-4 ${
            apiStatus === 'connected'
              ? 'border-green-500 bg-green-50'
              : apiStatus === 'error'
              ? 'border-red-500 bg-red-50'
              : 'border-yellow-500 bg-yellow-50'
          }`}>
            <h2 className={`font-semibold mb-2 ${
              apiStatus === 'connected'
                ? 'text-green-900'
                : apiStatus === 'error'
                ? 'text-red-900'
                : 'text-yellow-900'
            }`}>
              백엔드 연결 상태
            </h2>
            <p className={`text-sm ${
              apiStatus === 'connected'
                ? 'text-green-800'
                : apiStatus === 'error'
                ? 'text-red-800'
                : 'text-yellow-800'
            }`}>
              {apiStatus === 'checking' && '연결 확인 중...'}
              {apiStatus === 'connected' && '✓ 백엔드 API에 정상적으로 연결되었습니다'}
              {apiStatus === 'error' && `✗ 연결 실패: ${errorMessage}`}
            </p>
            {apiStatus === 'error' && (
              <p className="text-xs text-red-700 mt-2">
                백엔드 서버가 실행 중인지 확인하세요: <code>uvicorn app.main:app --reload</code>
              </p>
            )}
          </div>

          <div className="border-l-4 border-gray-500 bg-gray-50 p-4">
            <h2 className="font-semibold text-gray-900 mb-2">구현 완료</h2>
            <ul className="text-sm text-gray-700 space-y-1">
              <li>✓ React 프로젝트 초기화</li>
              <li>✓ 필수 라이브러리 설치</li>
              <li>✓ Tailwind CSS 설정</li>
              <li>✓ 기본 구조 구현</li>
              <li>✓ React Router 설정</li>
              <li className="text-blue-600 font-medium">→ 사이트 관리 UI (진행 중)</li>
            </ul>
          </div>

          {apiStatus === 'connected' && (
            <div className="pt-4">
              <Link
                to="/sites"
                className="block w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-md text-center transition-colors"
              >
                사이트 관리 시작하기 →
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
