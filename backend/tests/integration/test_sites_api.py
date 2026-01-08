"""
Integration tests for Sites API
"""
import pytest
from fastapi import status


class TestCreateSite:
    """Tests for POST /api/v1/sites"""

    def test_create_rss_site_success(self, client, sample_site_data):
        """Test creating a new RSS site"""
        response = client.post("/api/v1/sites/", json=sample_site_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == sample_site_data["name"]
        assert data["url"] == sample_site_data["url"]
        assert data["site_type"] == sample_site_data["site_type"]
        assert data["is_active"] is True
        assert "id" in data
        assert "scraping_rule" in data
        assert data["scraping_rule"]["rule_type"] == "rss"

    def test_create_html_site_success(self, client, sample_html_site_data):
        """Test creating a new HTML site with CSS selectors"""
        response = client.post("/api/v1/sites/", json=sample_html_site_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == sample_html_site_data["name"]
        assert data["scraping_rule"]["rule_type"] == "css_selector"
        assert data["scraping_rule"]["title_selector"] == "h2.title"

    def test_create_site_duplicate_url(self, client, sample_site_data):
        """Test creating a site with duplicate URL fails"""
        # Create first site
        client.post("/api/v1/sites/", json=sample_site_data)

        # Try to create another site with same URL
        response = client.post("/api/v1/sites/", json=sample_site_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already exists" in response.json()["detail"].lower()

    def test_create_site_invalid_data(self, client):
        """Test creating a site with invalid data fails"""
        invalid_data = {
            "name": "",  # Empty name
            "url": "not-a-url",  # Invalid URL format
            "site_type": "invalid",  # Invalid type
        }

        response = client.post("/api/v1/sites/", json=invalid_data)

        assert response.status_code in [
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            status.HTTP_400_BAD_REQUEST
        ]


class TestGetSites:
    """Tests for GET /api/v1/sites"""

    def test_get_sites_empty(self, client):
        """Test getting sites when none exist"""
        response = client.get("/api/v1/sites/")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_get_sites_multiple(self, client, sample_site_data, sample_html_site_data):
        """Test getting multiple sites"""
        # Create two sites
        client.post("/api/v1/sites/", json=sample_site_data)
        client.post("/api/v1/sites/", json=sample_html_site_data)

        response = client.get("/api/v1/sites/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == sample_site_data["name"]
        assert data[1]["name"] == sample_html_site_data["name"]

    def test_get_sites_filter_active(self, client, sample_site_data):
        """Test filtering sites by active status"""
        # Create a site
        create_response = client.post("/api/v1/sites/", json=sample_site_data)
        site_id = create_response.json()["id"]

        # Toggle it to inactive
        client.patch(f"/api/v1/sites/{site_id}/toggle")

        # Filter for active sites
        response = client.get("/api/v1/sites/", params={"is_active": True})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 0

        # Filter for inactive sites
        response = client.get("/api/v1/sites/", params={"is_active": False})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1


class TestGetSite:
    """Tests for GET /api/v1/sites/{site_id}"""

    def test_get_site_success(self, client, sample_site_data):
        """Test getting a specific site"""
        create_response = client.post("/api/v1/sites/", json=sample_site_data)
        site_id = create_response.json()["id"]

        response = client.get(f"/api/v1/sites/{site_id}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == site_id
        assert data["name"] == sample_site_data["name"]

    def test_get_site_not_found(self, client):
        """Test getting a non-existent site"""
        response = client.get("/api/v1/sites/999")

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateSite:
    """Tests for PUT /api/v1/sites/{site_id}"""

    def test_update_site_success(self, client, sample_site_data):
        """Test updating a site"""
        # Create a site
        create_response = client.post("/api/v1/sites/", json=sample_site_data)
        site_id = create_response.json()["id"]

        # Update it
        update_data = {
            "name": "Updated Blog Name",
            "description": "Updated description"
        }
        response = client.put(f"/api/v1/sites/{site_id}", json=update_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Updated Blog Name"
        assert data["description"] == "Updated description"
        # URL should remain unchanged
        assert data["url"] == sample_site_data["url"]

    def test_update_site_not_found(self, client):
        """Test updating a non-existent site"""
        update_data = {"name": "Updated Name"}
        response = client.put("/api/v1/sites/999", json=update_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteSite:
    """Tests for DELETE /api/v1/sites/{site_id}"""

    def test_delete_site_success(self, client, sample_site_data):
        """Test deleting a site"""
        # Create a site
        create_response = client.post("/api/v1/sites/", json=sample_site_data)
        site_id = create_response.json()["id"]

        # Delete it
        response = client.delete(f"/api/v1/sites/{site_id}")

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify it's gone
        get_response = client.get(f"/api/v1/sites/{site_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_site_not_found(self, client):
        """Test deleting a non-existent site"""
        response = client.delete("/api/v1/sites/999")

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestToggleSiteActive:
    """Tests for PATCH /api/v1/sites/{site_id}/toggle"""

    def test_toggle_site_active(self, client, sample_site_data):
        """Test toggling site active status"""
        # Create a site (starts as active)
        create_response = client.post("/api/v1/sites/", json=sample_site_data)
        site_id = create_response.json()["id"]
        assert create_response.json()["is_active"] is True

        # Toggle to inactive
        response = client.patch(f"/api/v1/sites/{site_id}/toggle")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["is_active"] is False

        # Toggle back to active
        response = client.patch(f"/api/v1/sites/{site_id}/toggle")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["is_active"] is True
