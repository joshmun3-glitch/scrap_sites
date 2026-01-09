import { useState } from 'react';
import { useSites, useDeleteSite, useToggleSiteActive } from '@/hooks/useSites';
import SiteCard from '@/components/features/sites/SiteCard';
import SiteFormDialog from '@/components/features/sites/SiteFormDialog';

export default function Sites() {
  const { data: sites, isLoading, error } = useSites();
  const deleteSite = useDeleteSite();
  const toggleActive = useToggleSiteActive();
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingSiteId, setEditingSiteId] = useState<number | undefined>();

  const handleEdit = (id: number) => {
    setEditingSiteId(id);
    setIsFormOpen(true);
  };

  const handleDelete = (id: number) => {
    if (confirm('정말로 이 사이트를 삭제하시겠습니까?')) {
      deleteSite.mutate(id);
    }
  };

  const handleToggleActive = (id: number) => {
    toggleActive.mutate(id);
  };

  const handleFormClose = () => {
    setIsFormOpen(false);
    setEditingSiteId(undefined);
  };

  if (isLoading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p className="mt-4 text-gray-600">사이트 목록을 불러오는 중...</p>
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

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">사이트 관리</h1>
            <p className="mt-1 text-sm text-gray-600">
              모니터링할 블로그/뉴스 사이트를 추가하고 관리하세요
            </p>
          </div>
          <button
            onClick={() => setIsFormOpen(true)}
            className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition-colors"
          >
            + 사이트 추가
          </button>
        </div>
      </div>

      {/* Sites Grid */}
      {sites && sites.length === 0 ? (
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
              d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
            />
          </svg>
          <h3 className="mt-2 text-sm font-medium text-gray-900">사이트가 없습니다</h3>
          <p className="mt-1 text-sm text-gray-500">
            첫 번째 사이트를 추가하여 모니터링을 시작하세요
          </p>
          <div className="mt-6">
            <button
              onClick={() => setIsFormOpen(true)}
              className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
            >
              + 사이트 추가
            </button>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {sites?.map((site) => (
            <SiteCard
              key={site.id}
              site={site}
              onEdit={handleEdit}
              onDelete={handleDelete}
              onToggleActive={handleToggleActive}
            />
          ))}
        </div>
      )}

      {/* Site Form Dialog */}
      <SiteFormDialog
        isOpen={isFormOpen}
        onClose={handleFormClose}
        siteId={editingSiteId}
      />
    </div>
  );
}
