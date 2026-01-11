"""
End-to-end tests for the AI Data Cleaning Assistant using Playwright.
Tests the complete flow: upload → process → download
"""
import os
import time
from pathlib import Path
from playwright.sync_api import Page, expect
import pytest


# Base URL for the application
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


@pytest.fixture(scope="session")
def test_csv_file():
    """Provide path to test CSV file"""
    return Path(__file__).parent / "fixtures" / "dirty_data.csv"


def test_landing_page_loads(page: Page):
    """Test that the landing page loads correctly"""
    page.goto(BASE_URL)
    
    # Check title
    expect(page).to_have_title("AI Data Cleaning Assistant")
    
    # Check main heading
    heading = page.locator("h1")
    expect(heading).to_contain_text("AI Data Cleaning Assistant")
    
    # Check upload button is disabled initially
    upload_button = page.locator("button#upload-btn")
    expect(upload_button).to_be_disabled()


def test_file_selection_enables_button(page: Page, test_csv_file: Path):
    """Test that selecting a file enables the upload button"""
    page.goto(BASE_URL)
    
    # Initially button should be disabled
    upload_button = page.locator("button#upload-btn")
    expect(upload_button).to_be_disabled()
    
    # Select file
    file_input = page.locator("input#file-input")
    file_input.set_input_files(str(test_csv_file))
    
    # Check file name is displayed
    file_name_display = page.locator("#file-name")
    expect(file_name_display).to_contain_text("dirty_data.csv")
    
    # Button should now be enabled
    expect(upload_button).to_be_enabled()


def test_complete_cleaning_flow(page: Page, test_csv_file: Path):
    """Test the complete flow: upload → clean → download"""
    page.goto(BASE_URL)
    
    # Select file
    file_input = page.locator("input#file-input")
    file_input.set_input_files(str(test_csv_file))
    
    # Click upload button
    upload_button = page.locator("button#upload-btn")
    upload_button.click()
    
    # Wait for processing status to appear
    status_div = page.locator("#status")
    expect(status_div).to_contain_text("Processing", timeout=10000)
    
    # Wait for success status (may take a few seconds)
    # The processing includes profiling, suggesting, and applying
    expect(status_div).to_contain_text("cleaned successfully", timeout=30000)
    
    # Check that download link appears
    download_link = page.locator('a[href*="/download"]')
    expect(download_link).to_be_visible()
    
    # Check that report link appears
    report_link = page.locator('a[href*="/report"]')
    expect(report_link).to_be_visible()


def test_download_cleaned_file(page: Page, test_csv_file: Path):
    """Test downloading the cleaned file"""
    page.goto(BASE_URL)
    
    # Upload file
    file_input = page.locator("input#file-input")
    file_input.set_input_files(str(test_csv_file))
    
    upload_button = page.locator("button#upload-btn")
    upload_button.click()
    
    # Wait for completion
    status_div = page.locator("#status")
    expect(status_div).to_contain_text("cleaned successfully", timeout=30000)
    
    # Start waiting for download
    with page.expect_download() as download_info:
        download_link = page.locator('a[href*="/download"]')
        download_link.click()
    
    download = download_info.value
    
    # Verify download
    assert download.suggested_filename.endswith("_cleaned.csv")
    
    # Save and check content
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
        download_path = Path(tmp_file.name)
    
    try:
        download.save_as(download_path)
        
        # Verify file exists and has content
        assert download_path.exists()
        content = download_path.read_text()
        
        # Check that cleaned data has expected structure
        assert "name,age,city,salary,email" in content
        assert "Alice" in content
        assert "Bob" in content
    finally:
        # Clean up
        if download_path.exists():
            download_path.unlink()


def test_health_endpoint(page: Page):
    """Test the health check endpoint"""
    response = page.request.get(f"{BASE_URL}/health")
    assert response.status == 200
    data = response.json()
    assert data["status"] == "ok"


def test_error_handling_no_file(page: Page):
    """Test that uploading without selecting a file shows an error"""
    page.goto(BASE_URL)
    
    # Button should be disabled without file selection
    upload_button = page.locator("button#upload-btn")
    expect(upload_button).to_be_disabled()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
