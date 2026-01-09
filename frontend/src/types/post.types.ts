export interface Post {
  id: number;
  siteId: number;
  title: string;
  url: string;
  author?: string;
  publishedAt?: string;
  excerpt?: string;
  imageUrl?: string;
  isRead: boolean;
  isStarred: boolean;
  readAt?: string;
  discoveredAt: string;
  createdAt: string;
  updatedAt: string;
}

export interface PostListResponse {
  total: number;
  skip: number;
  limit: number;
  posts: Post[];
}

export interface PostFilters {
  siteId?: number;
  isRead?: boolean;
  isStarred?: boolean;
  search?: string;
  skip?: number;
  limit?: number;
}
