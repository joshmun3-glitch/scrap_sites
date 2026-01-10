import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { postsService } from '@/services/posts.service';
import { PostFilters } from '@/types/post.types';
import toast from 'react-hot-toast';
import { AxiosError } from 'axios';

// 쿼리 키 상수
export const POSTS_QUERY_KEY = ['posts'];

// 글 목록 조회
export function usePosts(filters?: PostFilters) {
  return useQuery({
    queryKey: [...POSTS_QUERY_KEY, filters],
    queryFn: () => postsService.getAll(filters),
  });
}

// 특정 글 조회
export function usePost(id: number) {
  return useQuery({
    queryKey: [...POSTS_QUERY_KEY, id],
    queryFn: () => postsService.getById(id),
    enabled: !!id,
  });
}

// 읽음 상태 토글
export function useTogglePostRead() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => postsService.toggleRead(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: POSTS_QUERY_KEY });
    },
    onError: (error: AxiosError<{ detail?: string }>) => {
      const message = error.response?.data?.detail || '읽음 상태 변경에 실패했습니다.';
      toast.error(message);
    },
  });
}

// 별표 상태 토글
export function useTogglePostStar() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => postsService.toggleStar(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: POSTS_QUERY_KEY });
    },
    onError: (error: AxiosError<{ detail?: string }>) => {
      const message = error.response?.data?.detail || '별표 상태 변경에 실패했습니다.';
      toast.error(message);
    },
  });
}

// 일괄 읽음 처리
export function useBulkMarkAsRead() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ postIds, isRead }: { postIds: number[]; isRead?: boolean }) =>
      postsService.bulkMarkAsRead(postIds, isRead),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: POSTS_QUERY_KEY });
      const message = variables.isRead === false
        ? '읽지 않음으로 표시했습니다.'
        : `${variables.postIds.length}개의 글을 읽음으로 표시했습니다.`;
      toast.success(message);
    },
    onError: (error: AxiosError<{ detail?: string }>) => {
      const message = error.response?.data?.detail || '일괄 처리에 실패했습니다.';
      toast.error(message);
    },
  });
}

// 글 삭제
export function useDeletePost() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => postsService.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: POSTS_QUERY_KEY });
      toast.success('글이 삭제되었습니다.');
    },
    onError: (error: AxiosError<{ detail?: string }>) => {
      const message = error.response?.data?.detail || '글 삭제에 실패했습니다.';
      toast.error(message);
    },
  });
}
