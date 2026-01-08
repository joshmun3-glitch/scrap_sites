export type SiteType = 'rss' | 'html';
export type RuleType = 'css_selector' | 'xpath' | 'rss';

export interface ScrapingRule {
  id?: number;
  siteId?: number;
  ruleType: RuleType;
  rssUrl?: string;
  listContainerSelector?: string;
  titleSelector?: string;
  linkSelector?: string;
  dateSelector?: string;
  authorSelector?: string;
  excerptSelector?: string;
  imageSelector?: string;
  dateFormat?: string;
  dateAttribute?: string;
  customHeaders?: Record<string, string>;
  useJavascript?: boolean;
  waitForSelector?: string;
}

export interface Site {
  id: number;
  name: string;
  url: string;
  siteType: SiteType;
  description?: string;
  faviconUrl?: string;
  isActive: boolean;
  scrapeIntervalMinutes: number;
  lastScrapedAt?: string;
  lastSuccessfulScrapeAt?: string;
  scrapeErrors: number;
  createdAt: string;
  updatedAt: string;
  scrapingRule?: ScrapingRule;
}

export interface CreateSiteInput {
  name: string;
  url: string;
  siteType: SiteType;
  description?: string;
  scrapeIntervalMinutes?: number;
  scrapingRule: Omit<ScrapingRule, 'id' | 'siteId'>;
}

export interface UpdateSiteInput extends Partial<CreateSiteInput> {
  isActive?: boolean;
}
