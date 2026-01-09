import api from './api';
import { Site, CreateSiteInput, UpdateSiteInput } from '@/types/site.types';

export const sitesService = {
  // 모든 사이트 조회
  getAll: async (): Promise<Site[]> => {
    const { data } = await api.get<Site[]>('/api/v1/sites/');
    return data;
  },

  // 특정 사이트 조회
  getById: async (id: number): Promise<Site> => {
    const { data } = await api.get<Site>(`/api/v1/sites/${id}`);
    return data;
  },

  // 사이트 생성
  create: async (siteData: CreateSiteInput): Promise<Site> => {
    const { data } = await api.post<Site>('/api/v1/sites/', siteData);
    return data;
  },

  // 사이트 수정
  update: async (id: number, siteData: UpdateSiteInput): Promise<Site> => {
    const { data } = await api.put<Site>(`/api/v1/sites/${id}`, siteData);
    return data;
  },

  // 사이트 삭제
  delete: async (id: number): Promise<void> => {
    await api.delete(`/api/v1/sites/${id}`);
  },

  // 사이트 활성/비활성 토글
  toggleActive: async (id: number): Promise<Site> => {
    const { data } = await api.patch<Site>(`/api/v1/sites/${id}/toggle`);
    return data;
  },

  // 스크래핑 규칙 테스트
  testScrapingRule: async (id: number): Promise<{ success: boolean; message: string; posts_found?: number }> => {
    const { data } = await api.post(`/api/v1/sites/${id}/test`);
    return data;
  },

  // 수동 스크래핑 실행
  scrapeNow: async (id: number): Promise<{ success: boolean; message: string; new_posts?: number }> => {
    const { data } = await api.post(`/api/v1/sites/${id}/scrape`);
    return data;
  },
};
