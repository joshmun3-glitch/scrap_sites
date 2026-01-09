import { useState } from 'react';
import { PostFilters as PostFiltersType } from '@/types/post.types';
import { useSites } from '@/hooks/useSites';

interface PostFiltersProps {
  filters: PostFiltersType;
  onFiltersChange: (filters: PostFiltersType) => void;
}

export default function PostFilters({ filters, onFiltersChange }: PostFiltersProps) {
  const { data: sitesResponse } = useSites();
  const sites = sitesResponse || [];
  const [search, setSearch] = useState(filters.search || '');

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onFiltersChange({ ...filters, search: search || undefined });
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4 space-y-4">
      <div className="flex flex-wrap gap-4">
        {/* 사이트 필터 */}
        <div className="flex-1 min-w-[200px]">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            사이트
          </label>
          <select
            value={filters.siteId || ''}
            onChange={(e) =>
              onFiltersChange({
                ...filters,
                siteId: e.target.value ? Number(e.target.value) : undefined,
              })
            }
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">전체 사이트</option>
            {sites.map((site) => (
              <option key={site.id} value={site.id}>
                {site.name}
              </option>
            ))}
          </select>
        </div>

        {/* 읽음 상태 필터 */}
        <div className="flex-1 min-w-[150px]">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            읽음 상태
          </label>
          <select
            value={
              filters.isRead === undefined ? '' : filters.isRead ? 'read' : 'unread'
            }
            onChange={(e) => {
              const value = e.target.value;
              onFiltersChange({
                ...filters,
                isRead: value === '' ? undefined : value === 'read',
              });
            }}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">전체</option>
            <option value="unread">읽지 않음</option>
            <option value="read">읽음</option>
          </select>
        </div>

        {/* 별표 필터 */}
        <div className="flex-1 min-w-[150px]">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            별표
          </label>
          <select
            value={
              filters.isStarred === undefined
                ? ''
                : filters.isStarred
                ? 'starred'
                : 'not-starred'
            }
            onChange={(e) => {
              const value = e.target.value;
              onFiltersChange({
                ...filters,
                isStarred: value === '' ? undefined : value === 'starred',
              });
            }}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">전체</option>
            <option value="starred">별표 있음</option>
            <option value="not-starred">별표 없음</option>
          </select>
        </div>
      </div>

      {/* 검색 */}
      <form onSubmit={handleSearchSubmit} className="flex gap-2">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="제목 또는 내용 검색..."
          className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
        >
          검색
        </button>
        {filters.search && (
          <button
            type="button"
            onClick={() => {
              setSearch('');
              onFiltersChange({ ...filters, search: undefined });
            }}
            className="px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition-colors"
          >
            초기화
          </button>
        )}
      </form>

      {/* 활성 필터 표시 */}
      {(filters.siteId || filters.isRead !== undefined || filters.isStarred !== undefined || filters.search) && (
        <div className="flex items-center gap-2 pt-2 border-t">
          <span className="text-sm text-gray-600">활성 필터:</span>
          {filters.siteId && (
            <span className="inline-flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
              {sites.find((s) => s.id === filters.siteId)?.name}
              <button
                onClick={() => onFiltersChange({ ...filters, siteId: undefined })}
                className="hover:text-blue-900"
              >
                ×
              </button>
            </span>
          )}
          {filters.isRead !== undefined && (
            <span className="inline-flex items-center gap-1 px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
              {filters.isRead ? '읽음' : '읽지 않음'}
              <button
                onClick={() => onFiltersChange({ ...filters, isRead: undefined })}
                className="hover:text-green-900"
              >
                ×
              </button>
            </span>
          )}
          {filters.isStarred !== undefined && (
            <span className="inline-flex items-center gap-1 px-2 py-1 bg-yellow-100 text-yellow-800 text-xs rounded-full">
              {filters.isStarred ? '별표 있음' : '별표 없음'}
              <button
                onClick={() => onFiltersChange({ ...filters, isStarred: undefined })}
                className="hover:text-yellow-900"
              >
                ×
              </button>
            </span>
          )}
          {filters.search && (
            <span className="inline-flex items-center gap-1 px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded-full">
              검색: {filters.search}
              <button
                onClick={() => {
                  setSearch('');
                  onFiltersChange({ ...filters, search: undefined });
                }}
                className="hover:text-purple-900"
              >
                ×
              </button>
            </span>
          )}
        </div>
      )}
    </div>
  );
}
