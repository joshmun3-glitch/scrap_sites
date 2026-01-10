"""HTML 스크래핑 서비스"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from datetime import datetime
from urllib.parse import urljoin
import logging
import re

logger = logging.getLogger(__name__)


def scrape_html(
    url: str,
    list_container_selector: Optional[str] = None,
    title_selector: Optional[str] = None,
    link_selector: Optional[str] = None,
    date_selector: Optional[str] = None,
    author_selector: Optional[str] = None,
    excerpt_selector: Optional[str] = None,
    image_selector: Optional[str] = None,
    date_format: Optional[str] = None,
    custom_headers: Optional[Dict[str, str]] = None,
) -> List[Dict]:
    """
    HTML 페이지에서 CSS 셀렉터를 사용하여 글 목록을 스크래핑합니다.

    Args:
        url: 스크래핑할 URL
        list_container_selector: 글 목록 컨테이너 셀렉터
        title_selector: 제목 셀렉터
        link_selector: 링크 셀렉터
        date_selector: 날짜 셀렉터
        author_selector: 저자 셀렉터
        excerpt_selector: 요약 셀렉터
        image_selector: 이미지 셀렉터
        date_format: 날짜 형식 (strptime 형식)
        custom_headers: 사용자 정의 HTTP 헤더

    Returns:
        스크래핑된 글 목록

    Raises:
        ValueError: 스크래핑 실패 시
    """
    try:
        logger.info(f"Scraping HTML: {url}")

        # HTTP 요청
        headers = custom_headers or {}
        if 'User-Agent' not in headers:
            headers['User-Agent'] = (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/91.0.4472.124 Safari/537.36'
            )

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        response.encoding = response.apparent_encoding

        # HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # 글 목록 컨테이너 찾기
        if list_container_selector:
            containers = soup.select(list_container_selector)
            if not containers:
                logger.warning(f"No containers found with selector: {list_container_selector}")
                return []
        else:
            # 컨테이너 셀렉터가 없으면 전체 페이지를 대상으로
            containers = [soup]

        posts = []
        for container in containers:
            post = _extract_post_data(
                container,
                url,
                title_selector,
                link_selector,
                date_selector,
                author_selector,
                excerpt_selector,
                image_selector,
                date_format,
            )
            if post:
                posts.append(post)

        logger.info(f"Successfully scraped {len(posts)} posts")
        return posts

    except requests.RequestException as e:
        logger.error(f"HTTP request failed for {url}: {str(e)}")
        raise ValueError(f"페이지 요청 실패: {str(e)}")
    except Exception as e:
        logger.error(f"HTML scraping failed for {url}: {str(e)}")
        raise ValueError(f"HTML 스크래핑 실패: {str(e)}")


def _extract_post_data(
    container,
    base_url: str,
    title_selector: Optional[str],
    link_selector: Optional[str],
    date_selector: Optional[str],
    author_selector: Optional[str],
    excerpt_selector: Optional[str],
    image_selector: Optional[str],
    date_format: Optional[str],
) -> Optional[Dict]:
    """컨테이너에서 글 데이터를 추출합니다."""
    try:
        # 제목 추출
        title = None
        if title_selector:
            title_elem = container.select_one(title_selector)
            if title_elem:
                title = title_elem.get_text(strip=True)

        # 링크 추출
        link = None
        if link_selector:
            link_elem = container.select_one(link_selector)
            if link_elem:
                if link_elem.name == 'a':
                    link = link_elem.get('href')
                else:
                    link_tag = link_elem.find('a')
                    if link_tag:
                        link = link_tag.get('href')

                # 상대 URL을 절대 URL로 변환
                if link:
                    link = urljoin(base_url, link)

        # 필수 필드 검증
        if not title or not link:
            return None

        # 날짜 추출
        published_at = None
        if date_selector:
            date_elem = container.select_one(date_selector)
            if date_elem:
                date_text = date_elem.get_text(strip=True)
                published_at = _parse_date(date_text, date_format)

        # 저자 추출
        author = None
        if author_selector:
            author_elem = container.select_one(author_selector)
            if author_elem:
                author = author_elem.get_text(strip=True)

        # 요약 추출
        excerpt = None
        if excerpt_selector:
            excerpt_elem = container.select_one(excerpt_selector)
            if excerpt_elem:
                excerpt = excerpt_elem.get_text(strip=True)[:500]

        # 이미지 추출
        image_url = None
        if image_selector:
            image_elem = container.select_one(image_selector)
            if image_elem:
                if image_elem.name == 'img':
                    image_url = image_elem.get('src')
                else:
                    img_tag = image_elem.find('img')
                    if img_tag:
                        image_url = img_tag.get('src')

                # 상대 URL을 절대 URL로 변환
                if image_url:
                    image_url = urljoin(base_url, image_url)

        return {
            'title': title,
            'url': link,
            'author': author,
            'published_at': published_at.isoformat() if published_at else None,
            'excerpt': excerpt,
            'image_url': image_url,
        }

    except Exception as e:
        logger.error(f"Failed to extract post data: {str(e)}")
        return None


def _parse_date(date_text: str, date_format: Optional[str] = None) -> Optional[datetime]:
    """날짜 문자열을 datetime 객체로 파싱합니다."""
    if not date_text:
        return None

    try:
        # 사용자 지정 형식 사용
        if date_format:
            return datetime.strptime(date_text, date_format)

        # 일반적인 날짜 형식들 시도
        common_formats = [
            '%Y-%m-%d',
            '%Y.%m.%d',
            '%Y/%m/%d',
            '%Y-%m-%d %H:%M:%S',
            '%Y.%m.%d %H:%M:%S',
            '%Y/%m/%d %H:%M:%S',
            '%d-%m-%Y',
            '%d.%m.%Y',
            '%d/%m/%Y',
        ]

        for fmt in common_formats:
            try:
                return datetime.strptime(date_text, fmt)
            except ValueError:
                continue

        # ISO 형식 시도
        try:
            return datetime.fromisoformat(date_text.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            pass

        logger.warning(f"Could not parse date: {date_text}")
        return None

    except Exception as e:
        logger.error(f"Date parsing error: {str(e)}")
        return None


def validate_html_selectors(
    url: str,
    list_container_selector: Optional[str],
    title_selector: Optional[str],
    link_selector: Optional[str],
) -> Dict:
    """
    HTML 셀렉터의 유효성을 검사합니다.

    Args:
        url: 테스트할 URL
        list_container_selector: 컨테이너 셀렉터
        title_selector: 제목 셀렉터
        link_selector: 링크 셀렉터

    Returns:
        검증 결과 {'valid': bool, 'message': str, 'posts_count': int}
    """
    try:
        posts = scrape_html(
            url=url,
            list_container_selector=list_container_selector,
            title_selector=title_selector,
            link_selector=link_selector,
        )
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
