import { Site } from '@/types/site.types';

interface SiteCardProps {
  site: Site;
  onEdit: (id: number) => void;
  onDelete: (id: number) => void;
  onToggleActive: (id: number) => void;
}

export default function SiteCard({ site, onEdit, onDelete, onToggleActive }: SiteCardProps) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
      <div className="p-6">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-1">
              <h3 className="text-lg font-semibold text-gray-900">{site.name}</h3>
              <span
                className={`px-2 py-1 text-xs font-medium rounded-full ${
                  site.isActive
                    ? 'bg-green-100 text-green-800'
                    : 'bg-gray-100 text-gray-800'
                }`}
              >
                {site.isActive ? '활성' : '비활성'}
              </span>
            </div>
            <a
              href={site.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-blue-600 hover:text-blue-800 hover:underline break-all"
            >
              {site.url}
            </a>
          </div>
        </div>

        {/* Description */}
        {site.description && (
          <p className="text-sm text-gray-600 mb-4 line-clamp-2">{site.description}</p>
        )}

        {/* Info */}
        <div className="space-y-2 text-sm text-gray-600 mb-4">
          <div className="flex items-center justify-between">
            <span>타입:</span>
            <span className="font-medium">
              {site.siteType === 'rss' ? 'RSS' : 'HTML'}
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span>스크래핑 간격:</span>
            <span className="font-medium">{site.scrapeIntervalMinutes}분</span>
          </div>
          {site.lastScrapedAt && (
            <div className="flex items-center justify-between">
              <span>마지막 스크래핑:</span>
              <span className="font-medium">
                {new Date(site.lastScrapedAt).toLocaleDateString('ko-KR')}
              </span>
            </div>
          )}
          {site.scrapeErrors > 0 && (
            <div className="flex items-center justify-between text-red-600">
              <span>오류 횟수:</span>
              <span className="font-medium">{site.scrapeErrors}</span>
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex gap-2 pt-4 border-t border-gray-200">
          <button
            onClick={() => onToggleActive(site.id)}
            className={`flex-1 px-3 py-2 text-sm font-medium rounded-md transition-colors ${
              site.isActive
                ? 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                : 'bg-green-100 text-green-700 hover:bg-green-200'
            }`}
          >
            {site.isActive ? '비활성화' : '활성화'}
          </button>
          <button
            onClick={() => onEdit(site.id)}
            className="flex-1 px-3 py-2 text-sm font-medium text-blue-700 bg-blue-50 rounded-md hover:bg-blue-100 transition-colors"
          >
            수정
          </button>
          <button
            onClick={() => onDelete(site.id)}
            className="px-3 py-2 text-sm font-medium text-red-700 bg-red-50 rounded-md hover:bg-red-100 transition-colors"
          >
            삭제
          </button>
        </div>
      </div>
    </div>
  );
}
