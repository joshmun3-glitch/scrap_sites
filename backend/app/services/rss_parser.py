"""RSS 피드 파싱 서비스"""
import feedparser
from typing import List, Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def parse_rss_feed(rss_url: str) -> List[Dict]:
    """
    RSS 피드를 파싱하여 글 목록을 반환합니다.

    Args:
        rss_url: RSS 피드 URL

    Returns:
        파싱된 글 목록 (dict 리스트)

    Raises:
        ValueError: RSS 피드 파싱 실패 시
    """
    try:
        logger.info(f"Parsing RSS feed: {rss_url}")
        feed = feedparser.parse(rss_url)

        if feed.bozo:
            # 파싱 오류가 있지만 일부 데이터를 가져올 수 있을 수도 있음
            logger.warning(f"RSS feed parsing warning: {feed.bozo_exception}")

        if not feed.entries:
            logger.warning(f"No entries found in RSS feed: {rss_url}")
            return []

        posts = []
        for entry in feed.entries:
            post = _parse_rss_entry(entry)
            if post:
                posts.append(post)

        logger.info(f"Successfully parsed {len(posts)} posts from RSS feed")
        return posts

    except Exception as e:
        logger.error(f"Failed to parse RSS feed {rss_url}: {str(e)}")
        raise ValueError(f"RSS 피드 파싱 실패: {str(e)}")


def _parse_rss_entry(entry) -> Optional[Dict]:
    """
    개별 RSS 엔트리를 파싱합니다.

    Args:
        entry: feedparser entry 객체

    Returns:
        파싱된 글 데이터 (dict) 또는 None
    """
    try:
        # 필수 필드
        title = entry.get('title', '').strip()
        link = entry.get('link', '').strip()

        if not title or not link:
            logger.warning(f"Skipping entry with missing title or link")
            return None

        # 날짜 파싱
        published_at = None
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            try:
                published_at = datetime(*entry.published_parsed[:6])
            except:
                pass

        if not published_at and hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            try:
                published_at = datetime(*entry.updated_parsed[:6])
            except:
                pass

        # 저자 추출
        author = None
        if hasattr(entry, 'author'):
            author = entry.author
        elif hasattr(entry, 'author_detail') and entry.author_detail:
            author = entry.author_detail.get('name')

        # 요약/내용 추출
        excerpt = None
        if hasattr(entry, 'summary'):
            excerpt = entry.summary
        elif hasattr(entry, 'description'):
            excerpt = entry.description

        # HTML 태그 제거 (간단한 방법)
        if excerpt:
            import re
            excerpt = re.sub(r'<[^>]+>', '', excerpt)
            excerpt = excerpt.strip()[:500]  # 최대 500자

        # 이미지 URL 추출
        image_url = None

        # media:thumbnail 또는 media:content
        if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
            image_url = entry.media_thumbnail[0].get('url')
        elif hasattr(entry, 'media_content') and entry.media_content:
            for media in entry.media_content:
                if media.get('medium') == 'image' or media.get('type', '').startswith('image/'):
                    image_url = media.get('url')
                    break

        # enclosure (팟캐스트 등)
        if not image_url and hasattr(entry, 'enclosures') and entry.enclosures:
            for enclosure in entry.enclosures:
                if enclosure.get('type', '').startswith('image/'):
                    image_url = enclosure.get('href')
                    break

        # content 내 이미지 추출
        if not image_url and hasattr(entry, 'content') and entry.content:
            import re
            content_html = entry.content[0].get('value', '')
            img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', content_html)
            if img_match:
                image_url = img_match.group(1)

        return {
            'title': title,
            'url': link,
            'author': author,
            'published_at': published_at.isoformat() if published_at else None,
            'excerpt': excerpt,
            'image_url': image_url,
        }

    except Exception as e:
        logger.error(f"Failed to parse RSS entry: {str(e)}")
        return None


def validate_rss_feed(rss_url: str) -> Dict:
    """
    RSS 피드의 유효성을 검사합니다.

    Args:
        rss_url: 검사할 RSS 피드 URL

    Returns:
        검증 결과 {'valid': bool, 'message': str, 'posts_count': int}
    """
    try:
        posts = parse_rss_feed(rss_url)
        return {
            'valid': True,
            'message': f'{len(posts)}개의 글을 찾았습니다.',
            'posts_count': len(posts)
        }
    except Exception as e:
        return {
            'valid': False,
            'message': str(e),
            'posts_count': 0
        }
