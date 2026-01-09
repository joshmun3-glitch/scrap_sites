import { BrowserRouter, Routes, Route, Link, Navigate, useLocation } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Home from './pages/Home';
import Sites from './pages/Sites';
import Posts from './pages/Posts';

function Navigation() {
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <nav className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <Link to="/" className="flex items-center px-2 py-2 text-gray-900 font-semibold text-lg">
              블로그/뉴스 모니터링
            </Link>
            <div className="flex space-x-8 ml-10">
              <Link
                to="/"
                className={`inline-flex items-center px-1 pt-1 text-sm font-medium border-b-2 ${
                  isActive('/')
                    ? 'text-blue-600 border-blue-600'
                    : 'text-gray-500 hover:text-gray-900 hover:border-gray-300 border-transparent'
                }`}
              >
                홈
              </Link>
              <Link
                to="/posts"
                className={`inline-flex items-center px-1 pt-1 text-sm font-medium border-b-2 ${
                  isActive('/posts')
                    ? 'text-blue-600 border-blue-600'
                    : 'text-gray-500 hover:text-gray-900 hover:border-gray-300 border-transparent'
                }`}
              >
                글 목록
              </Link>
              <Link
                to="/sites"
                className={`inline-flex items-center px-1 pt-1 text-sm font-medium border-b-2 ${
                  isActive('/sites')
                    ? 'text-blue-600 border-blue-600'
                    : 'text-gray-500 hover:text-gray-900 hover:border-gray-300 border-transparent'
                }`}
              >
                사이트 관리
              </Link>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        {/* Navigation */}
        <Navigation />

        {/* Routes */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/posts" element={<Posts />} />
          <Route path="/sites" element={<Sites />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>

        {/* Toast notifications */}
        <Toaster position="top-right" />
      </div>
    </BrowserRouter>
  );
}

export default App;
