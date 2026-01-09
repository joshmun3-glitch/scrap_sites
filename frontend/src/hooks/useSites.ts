import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { sitesService } from '@/services/sites.service';
import { CreateSiteInput, UpdateSiteInput } from '@/types/site.types';
import toast from 'react-hot-toast';

// 쿼리 키 상수
export const SITES_QUERY_KEY = ['sites'];

// 모든 사이트 조회
export function useSites() {
  return useQuery({
    queryKey: SITES_QUERY_KEY,
    queryFn: sitesService.getAll,
  });
}

// 특정 사이트 조회
export function useSite(id: number) {
  return useQuery({
    queryKey: [...SITES_QUERY_KEY, id],
    queryFn: () => sitesService.getById(id),
    enabled: !!id,
  });
}

// 사이트 생성
export function useCreateSite() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (siteData: CreateSiteInput) => sitesService.create(siteData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: SITES_QUERY_KEY });
      toast.success('사이트가 성공적으로 추가되었습니다.');
    },
    onError: (error: any) => {
      const message = error.response?.data?.detail || '사이트 추가에 실패했습니다.';
      toast.error(message);
    },
  });
}

// 사이트 수정
export function useUpdateSite() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: UpdateSiteInput }) =>
      sitesService.update(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: SITES_QUERY_KEY });
      queryClient.invalidateQueries({ queryKey: [...SITES_QUERY_KEY, variables.id] });
      toast.success('사이트가 성공적으로 수정되었습니다.');
    },
    onError: (error: any) => {
      const message = error.response?.data?.detail || '사이트 수정에 실패했습니다.';
      toast.error(message);
    },
  });
}

// 사이트 삭제
export function useDeleteSite() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => sitesService.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: SITES_QUERY_KEY });
      toast.success('사이트가 삭제되었습니다.');
    },
    onError: (error: any) => {
      const message = error.response?.data?.detail || '사이트 삭제에 실패했습니다.';
      toast.error(message);
    },
  });
}

// 사이트 활성/비활성 토글
export function useToggleSiteActive() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => sitesService.toggleActive(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: SITES_QUERY_KEY });
      toast.success('사이트 상태가 변경되었습니다.');
    },
    onError: (error: any) => {
      const message = error.response?.data?.detail || '상태 변경에 실패했습니다.';
      toast.error(message);
    },
  });
}

// 스크래핑 규칙 테스트
export function useTestScrapingRule() {
  return useMutation({
    mutationFn: (id: number) => sitesService.testScrapingRule(id),
    onSuccess: (data) => {
      if (data.success) {
        toast.success(`테스트 성공! ${data.posts_found || 0}개의 글을 발견했습니다.`);
      } else {
        toast.error(data.message || '테스트에 실패했습니다.');
      }
    },
    onError: (error: any) => {
      const message = error.response?.data?.detail || '테스트에 실패했습니다.';
      toast.error(message);
    },
  });
}

// 수동 스크래핑 실행
export function useScrapeNow() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => sitesService.scrapeNow(id),
    onSuccess: (data) => {
      if (data.success) {
        queryClient.invalidateQueries({ queryKey: ['posts'] });
        toast.success(`스크래핑 완료! ${data.new_posts || 0}개의 새 글을 발견했습니다.`);
      } else {
        toast.error(data.message || '스크래핑에 실패했습니다.');
      }
    },
    onError: (error: any) => {
      const message = error.response?.data?.detail || '스크래핑에 실패했습니다.';
      toast.error(message);
    },
  });
}
