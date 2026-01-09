import { Post } from '@/types/post.types';
import { formatDistanceToNow } from 'date-fns';
import { ko } from 'date-fns/locale';

interface PostCardProps {
  post: Post;
  onToggleRead: (id: number) => void;
  onToggleStar: (id: number) => void;
}

export default function PostCard({ post, onToggleRead, onToggleStar }: PostCardProps) {
  const formattedDate = post.publishedAt
    ? formatDistanceToNow(new Date(post.publishedAt), { addSuffix: true, locale: ko })
    : formatDistanceToNow(new Date(post.discoveredAt), { addSuffix: true, locale: ko });

  return (
    <div
      className={`bg-white rounded-lg border shadow-sm hover:shadow-md transition-shadow ${
        post.isRead ? 'border-gray-200 opacity-75' : 'border-gray-300'
      }`}
    >
      <div className="p-4">
        {/* Header */}
        <div className="flex items-start justify-between mb-3">
          <div className="flex-1">
            <a
              href={post.url}
              target="_blank"
              rel="noopener noreferrer"
              className={`text-lg font-semibold hover:text-blue-600 transition-colors ${
                post.isRead ? 'text-gray-600' : 'text-gray-900'
              }`}
            >
              {post.title}
            </a>
            <div className="flex items-center gap-3 mt-2 text-sm text-gray-500">
              {post.author && <span>{post.author}</span>}
              <span>•</span>
              <span>{formattedDate}</span>
            </div>
          </div>

          {/* Image */}
          {post.imageUrl && (
            <img
              src={post.imageUrl}
              alt={post.title}
              className="ml-4 w-24 h-24 object-cover rounded-lg flex-shrink-0"
              onError={(e) => {
                (e.target as HTMLImageElement).style.display = 'none';
              }}
            />
          )}
        </div>

        {/* Excerpt */}
        {post.excerpt && (
          <p className="text-sm text-gray-600 mb-3 line-clamp-2">{post.excerpt}</p>
        )}

        {/* Actions */}
        <div className="flex items-center gap-2 pt-3 border-t border-gray-100">
          <button
            onClick={() => onToggleRead(post.id)}
            className={`flex items-center gap-1 px-3 py-1.5 text-sm rounded-md transition-colors ${
              post.isRead
                ? 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                : 'bg-blue-50 text-blue-700 hover:bg-blue-100'
            }`}
            title={post.isRead ? '읽지 않음으로 표시' : '읽음으로 표시'}
          >
            <svg
              className="w-4 h-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              {post.isRead ? (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M5 13l4 4L19 7"
                />
              ) : (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              )}
            </svg>
            {post.isRead ? '읽음' : '읽지 않음'}
          </button>

          <button
            onClick={() => onToggleStar(post.id)}
            className={`flex items-center gap-1 px-3 py-1.5 text-sm rounded-md transition-colors ${
              post.isStarred
                ? 'bg-yellow-50 text-yellow-700 hover:bg-yellow-100'
                : 'bg-gray-50 text-gray-600 hover:bg-gray-100'
            }`}
            title={post.isStarred ? '별표 제거' : '별표 추가'}
          >
            <svg
              className="w-4 h-4"
              fill={post.isStarred ? 'currentColor' : 'none'}
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"
              />
            </svg>
          </button>

          <a
            href={post.url}
            target="_blank"
            rel="noopener noreferrer"
            className="ml-auto flex items-center gap-1 px-3 py-1.5 text-sm text-blue-600 hover:text-blue-800 rounded-md hover:bg-blue-50 transition-colors"
          >
            원문 보기
            <svg
              className="w-4 h-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
              />
            </svg>
          </a>
        </div>
      </div>
    </div>
  );
}
