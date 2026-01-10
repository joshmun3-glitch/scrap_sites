import { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useSite, useCreateSite, useUpdateSite } from '@/hooks/useSites';
import { CreateSiteInput } from '@/types/site.types';

interface SiteFormDialogProps {
  isOpen: boolean;
  onClose: () => void;
  siteId?: number;
}

// Zod 스키마 정의
const siteSchema = z.object({
  name: z.string().min(1, '사이트 이름을 입력하세요'),
  url: z.string().url('올바른 URL을 입력하세요'),
  siteType: z.enum(['rss', 'html'], {
    required_error: '사이트 타입을 선택하세요',
  }),
  description: z.string().optional(),
  scrapeIntervalMinutes: z.number().min(1, '최소 1분 이상이어야 합니다').default(60),
  scrapingRule: z.object({
    ruleType: z.enum(['rss', 'css_selector', 'xpath']),
    rssUrl: z.string().url().optional().or(z.literal('')),
    listContainerSelector: z.string().optional(),
    titleSelector: z.string().optional(),
    linkSelector: z.string().optional(),
    dateSelector: z.string().optional(),
    excerptSelector: z.string().optional(),
    imageSelector: z.string().optional(),
  }),
});

type SiteFormData = z.infer<typeof siteSchema>;

export default function SiteFormDialog({ isOpen, onClose, siteId }: SiteFormDialogProps) {
  const { data: site } = useSite(siteId!);
  const createSite = useCreateSite();
  const updateSite = useUpdateSite();
  const isEditing = !!siteId;

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    watch,
  } = useForm<SiteFormData>({
    resolver: zodResolver(siteSchema),
    defaultValues: {
      siteType: 'rss',
      scrapeIntervalMinutes: 60,
      scrapingRule: {
        ruleType: 'rss',
      },
    },
  });

  const ruleType = watch('scrapingRule.ruleType');

  // 사이트 데이터 로드 (수정 모드)
  useEffect(() => {
    if (site && isEditing) {
      reset({
        name: site.name,
        url: site.url,
        siteType: site.siteType,
        description: site.description || '',
        scrapeIntervalMinutes: site.scrapeIntervalMinutes,
        scrapingRule: {
          ruleType: site.scrapingRule?.ruleType || 'rss',
          rssUrl: site.scrapingRule?.rssUrl || '',
          listContainerSelector: site.scrapingRule?.listContainerSelector || '',
          titleSelector: site.scrapingRule?.titleSelector || '',
          linkSelector: site.scrapingRule?.linkSelector || '',
          dateSelector: site.scrapingRule?.dateSelector || '',
          excerptSelector: site.scrapingRule?.excerptSelector || '',
          imageSelector: site.scrapingRule?.imageSelector || '',
        },
      });
    }
  }, [site, isEditing, reset]);

  // 다이얼로그 닫을 때 폼 초기화
  useEffect(() => {
    if (!isOpen) {
      reset();
    }
  }, [isOpen, reset]);

  const onSubmit = async (data: SiteFormData) => {
    try {
      if (isEditing) {
        await updateSite.mutateAsync({ id: siteId, data });
      } else {
        await createSite.mutateAsync(data as CreateSiteInput);
      }
      onClose();
    } catch {
      // 에러는 hook에서 toast로 처리됨
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex min-h-screen items-center justify-center p-4">
        {/* Backdrop */}
        <div
          className="fixed inset-0 bg-black bg-opacity-50 transition-opacity"
          onClick={onClose}
        />

        {/* Dialog */}
        <div className="relative bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
          <div className="p-6">
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">
                {isEditing ? '사이트 수정' : '사이트 추가'}
              </h2>
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              {/* Basic Info */}
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    사이트 이름 *
                  </label>
                  <input
                    {...register('name')}
                    type="text"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="예: TechCrunch"
                  />
                  {errors.name && (
                    <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    사이트 URL *
                  </label>
                  <input
                    {...register('url')}
                    type="url"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="https://example.com"
                  />
                  {errors.url && (
                    <p className="mt-1 text-sm text-red-600">{errors.url.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    설명
                  </label>
                  <textarea
                    {...register('description')}
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="사이트에 대한 설명을 입력하세요"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      사이트 타입 *
                    </label>
                    <select
                      {...register('siteType')}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="rss">RSS</option>
                      <option value="html">HTML</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      스크래핑 간격 (분) *
                    </label>
                    <input
                      {...register('scrapeIntervalMinutes', { valueAsNumber: true })}
                      type="number"
                      min="1"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    {errors.scrapeIntervalMinutes && (
                      <p className="mt-1 text-sm text-red-600">
                        {errors.scrapeIntervalMinutes.message}
                      </p>
                    )}
                  </div>
                </div>
              </div>

              {/* Scraping Rules */}
              <div className="border-t pt-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">스크래핑 규칙</h3>

                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      규칙 타입 *
                    </label>
                    <select
                      {...register('scrapingRule.ruleType')}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="rss">RSS</option>
                      <option value="css_selector">CSS Selector</option>
                      <option value="xpath">XPath</option>
                    </select>
                  </div>

                  {ruleType === 'rss' && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        RSS Feed URL *
                      </label>
                      <input
                        {...register('scrapingRule.rssUrl')}
                        type="url"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="https://example.com/feed"
                      />
                      {errors.scrapingRule?.rssUrl && (
                        <p className="mt-1 text-sm text-red-600">
                          {errors.scrapingRule.rssUrl.message}
                        </p>
                      )}
                    </div>
                  )}

                  {ruleType === 'css_selector' && (
                    <div className="space-y-3 bg-gray-50 p-4 rounded-md">
                      <p className="text-sm text-gray-600">
                        CSS 셀렉터를 사용하여 HTML에서 데이터를 추출합니다
                      </p>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          목록 컨테이너 셀렉터
                        </label>
                        <input
                          {...register('scrapingRule.listContainerSelector')}
                          type="text"
                          className="w-full px-3 py-2 border border-gray-300 rounded-md"
                          placeholder=".post-list > article"
                        />
                      </div>

                      <div className="grid grid-cols-2 gap-3">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            제목 셀렉터
                          </label>
                          <input
                            {...register('scrapingRule.titleSelector')}
                            type="text"
                            className="w-full px-3 py-2 border border-gray-300 rounded-md"
                            placeholder=".title"
                          />
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            링크 셀렉터
                          </label>
                          <input
                            {...register('scrapingRule.linkSelector')}
                            type="text"
                            className="w-full px-3 py-2 border border-gray-300 rounded-md"
                            placeholder="a.permalink"
                          />
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-3">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            날짜 셀렉터
                          </label>
                          <input
                            {...register('scrapingRule.dateSelector')}
                            type="text"
                            className="w-full px-3 py-2 border border-gray-300 rounded-md"
                            placeholder=".date"
                          />
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            이미지 셀렉터
                          </label>
                          <input
                            {...register('scrapingRule.imageSelector')}
                            type="text"
                            className="w-full px-3 py-2 border border-gray-300 rounded-md"
                            placeholder="img.thumbnail"
                          />
                        </div>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          요약 셀렉터
                        </label>
                        <input
                          {...register('scrapingRule.excerptSelector')}
                          type="text"
                          className="w-full px-3 py-2 border border-gray-300 rounded-md"
                          placeholder=".excerpt"
                        />
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* Actions */}
              <div className="flex gap-3 pt-6 border-t">
                <button
                  type="button"
                  onClick={onClose}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors"
                >
                  취소
                </button>
                <button
                  type="submit"
                  disabled={createSite.isPending || updateSite.isPending}
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors disabled:bg-blue-300"
                >
                  {createSite.isPending || updateSite.isPending
                    ? '처리 중...'
                    : isEditing
                    ? '수정'
                    : '추가'}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
