import { useState } from 'react';
import { usePosts, useTogglePostRead, useTogglePostStar } from '@/hooks/usePosts';
import { PostFilters as PostFiltersType } from '@/types/post.types';
import PostCard from '@/components/features/posts/PostCard';
import PostFilters from '@/components/features/posts/PostFilters';

export default function Posts() {
  const [filters, setFilters] = useState<PostFiltersType>({
    skip: 0,
    limit: 20,
  });

  const { data, isLoading, error } = usePosts(filters);
  const toggleRead = useTogglePostRead();
  const toggleStar = useTogglePostStar();

  const handleToggleRead = (id: number) => {
    toggleRead.mutate(id);
  };

  const handleToggleStar = (id: number) => {
    toggleStar.mutate(id);
  };

  const handleLoadMore = () => {
    if (data) {
      setFilters((prev) => ({
        ...prev,
        skip: (prev.skip || 0) + (prev.limit || 20),
      }));
    }
  };

  if (isLoading && !data) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p className="mt-4 text-gray-600">글 목록을 불러오는 중...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">
            오류가 발생했습니다: {error instanceof Error ? error.message : '알 수 없는 오류'}
          </p>
        </div>
      </div>
    );
  }

  const posts = data?.posts || [];
  const total = data?.total || 0;
  const hasMore = (filters.skip || 0) + posts.length < total;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">글 목록</h1>
        <p className="mt-1 text-sm text-gray-600">
          총 {total}개의 글{filters.isRead === false && ' (읽지 않음)'}
        </p>
      </div>

      {/* Filters */}
      <div className="mb-6">
        <PostFilters filters={filters} onFiltersChange={setFilters} />
      </div>

      {/* Posts List */}
      {posts.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-lg border border-gray-200">
          <svg
            className="mx-auto h-12 w-12 text-gray-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
          <h3 className="mt-2 text-sm font-medium text-gray-900">글이 없습니다</h3>
          <p className="mt-1 text-sm text-gray-500">
            사이트를 추가하고 스크래핑을 실행하세요
          </p>
        </div>
      ) : (
        <>
          <div className="space-y-4">
            {posts.map((post) => (
              <PostCard
                key={post.id}
                post={post}
                onToggleRead={handleToggleRead}
                onToggleStar={handleToggleStar}
              />
            ))}
          </div>

          {/* Load More */}
          {hasMore && (
            <div className="mt-6 text-center">
              <button
                onClick={handleLoadMore}
                disabled={isLoading}
                className="px-6 py-2 bg-white border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors disabled:opacity-50"
              >
                {isLoading ? '로딩 중...' : '더 보기'}
              </button>
              <p className="mt-2 text-sm text-gray-500">
                {posts.length} / {total}개 표시 중
              </p>
            </div>
          )}
        </>
      )}
    </div>
  );
}
