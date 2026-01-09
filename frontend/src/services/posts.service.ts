import api from './api';
import { Post, PostListResponse, PostFilters } from '@/types/post.types';

export const postsService = {
  // 글 목록 조회
  getAll: async (filters?: PostFilters): Promise<PostListResponse> => {
    const params = new URLSearchParams();

    if (filters?.siteId) params.append('site_id', filters.siteId.toString());
    if (filters?.isRead !== undefined) params.append('is_read', filters.isRead.toString());
    if (filters?.isStarred !== undefined) params.append('is_starred', filters.isStarred.toString());
    if (filters?.search) params.append('search', filters.search);
    if (filters?.skip) params.append('skip', filters.skip.toString());
    if (filters?.limit) params.append('limit', filters.limit.toString());

    const { data } = await api.get<PostListResponse>(`/api/v1/posts/?${params.toString()}`);
    return data;
  },

  // 특정 글 조회
  getById: async (id: number): Promise<Post> => {
    const { data } = await api.get<Post>(`/api/v1/posts/${id}`);
    return data;
  },

  // 읽음 상태 토글
  toggleRead: async (id: number): Promise<Post> => {
    const { data } = await api.patch<Post>(`/api/v1/posts/${id}/read`);
    return data;
  },

  // 별표 상태 토글
  toggleStar: async (id: number): Promise<Post> => {
    const { data } = await api.patch<Post>(`/api/v1/posts/${id}/star`);
    return data;
  },

  // 일괄 읽음 처리
  bulkMarkAsRead: async (postIds: number[], isRead: boolean = true): Promise<void> => {
    await api.post('/api/v1/posts/bulk-read', { post_ids: postIds, is_read: isRead });
  },

  // 글 삭제
  delete: async (id: number): Promise<void> => {
    await api.delete(`/api/v1/posts/${id}`);
  },
};
