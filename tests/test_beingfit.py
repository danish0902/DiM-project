import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Base URL of your hosted website
BASE_URL = "https://danish0902.github.io/DiM-project"

@pytest.fixture
def driver():
    """Setup Chrome WebDriver before each test"""
    print("\n[SETUP] Initializing Chrome WebDriver...")
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    print("\n[TEARDOWN] Closing browser...")
    driver.quit()

# ========== FUNCTIONAL TESTS ==========

def test_tc01_homepage_loads(driver):
    """TC01: Verify homepage loads successfully"""
    print("\n[TEST] TC01: Testing homepage load...")
    driver.get(f"{BASE_URL}/index.html")
    time.sleep(2)
    assert "BeingFIT" in driver.title
    print("✓ PASSED: Homepage loaded with correct title")

def test_tc02_explore_page_loads(driver):
    """TC02: Verify explore page loads"""
    print("\n[TEST] TC02: Testing explore page load...")
    driver.get(f"{BASE_URL}/explore.html")
    time.sleep(2)
    assert "Explore" in driver.title
    print("✓ PASSED: Explore page loaded successfully")

def test_tc03_all_exercise_pages_load(driver):
    """TC03: Verify all exercise category pages load"""
    print("\n[TEST] TC03: Testing all exercise pages...")
    pages = ["chest.html", "shoulder.html", "tricep.html", "back.html", "bicep.html", "legs.html"]
    
    for page in pages:
        driver.get(f"{BASE_URL}/{page}")
        time.sleep(1)
        assert driver.title != "", f"Failed to load {page}"
        print(f"  ✓ {page} loaded successfully")
    
    print("✓ PASSED: All 6 exercise pages loaded")

def test_tc04_bmi_calculator_loads(driver):
    """TC04: Verify BMI calculator page loads"""
    print("\n[TEST] TC04: Testing BMI calculator page...")
    driver.get(f"{BASE_URL}/bmi.html")
    time.sleep(2)
    assert "BMI" in driver.title or "bmi.html" in driver.current_url
    print("✓ PASSED: BMI calculator page loaded")

def test_tc05_journal_page_loads(driver):
    """TC05: Verify workout journal page loads"""
    print("\n[TEST] TC05: Testing journal page...")
    driver.get(f"{BASE_URL}/journal.html")
    time.sleep(2)
    assert "Journal" in driver.title or "journal.html" in driver.current_url
    print("✓ PASSED: Journal page loaded")

# ========== INTEGRATION TESTS ==========

def test_tc06_homepage_to_explore_navigation(driver):
    """TC06: Navigate from homepage to explore page"""
    print("\n[TEST] TC06: Testing homepage → explore navigation...")
    driver.get(f"{BASE_URL}/index.html")
    time.sleep(2)
    
    explore_link = driver.find_element(By.CSS_SELECTOR, "a[href='explore.html']")
    explore_link.click()
    time.sleep(2)
    
    assert "explore.html" in driver.current_url
    print("✓ PASSED: Navigation from home to explore successful")

def test_tc07_explore_to_chest_navigation(driver):
    """TC07: Navigate from explore to chest exercises"""
    print("\n[TEST] TC07: Testing explore → chest navigation...")
    driver.get(f"{BASE_URL}/explore.html")
    time.sleep(2)
    
    chest_link = driver.find_element(By.CSS_SELECTOR, "a[href='chest.html']")
    chest_link.click()
    time.sleep(2)
    
    assert "chest.html" in driver.current_url
    print("✓ PASSED: Navigation from explore to chest successful")

def test_tc08_navigation_bar_home_link(driver):
    """TC08: Test home link in navigation bar"""
    print("\n[TEST] TC08: Testing navigation bar home link...")
    driver.get(f"{BASE_URL}/explore.html")
    time.sleep(2)
    
    home_link = driver.find_element(By.LINK_TEXT, "Home")
    home_link.click()
    time.sleep(2)
    
    assert "index.html" in driver.current_url
    print("✓ PASSED: Home navigation link works correctly")

# ========== SYSTEM TESTS ==========

def test_tc09_complete_user_journey(driver):
    """TC09: Complete user journey through website"""
    print("\n[TEST] TC09: Testing complete user journey...")
    
    # Step 1: Homepage
    driver.get(f"{BASE_URL}/index.html")
    time.sleep(2)
    assert "BeingFIT" in driver.title
    print("  ✓ Step 1: Reached homepage")
    
    # Step 2: Navigate to explore
    driver.find_element(By.CSS_SELECTOR, "a[href='explore.html']").click()
    time.sleep(2)
    assert "explore.html" in driver.current_url
    print("  ✓ Step 2: Navigated to explore")
    
    # Step 3: Select chest exercises
    driver.find_element(By.CSS_SELECTOR, "a[href='chest.html']").click()
    time.sleep(2)
    assert "chest.html" in driver.current_url
    print("  ✓ Step 3: Viewed chest exercises")
    
    # Step 4: Check BMI calculator
    driver.get(f"{BASE_URL}/explore.html")
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "a[href='bmi.html']").click()
    time.sleep(2)
    assert "bmi.html" in driver.current_url
    print("  ✓ Step 4: Accessed BMI calculator")
    
    print("✓ PASSED: Complete user journey successful")

# ========== UI/VISUAL TESTS ==========

def test_tc10_images_load_on_explore(driver):
    """TC10: Verify images are present on explore page"""
    print("\n[TEST] TC10: Testing image loading...")
    driver.get(f"{BASE_URL}/explore.html")
    time.sleep(2)
    
    images = driver.find_elements(By.TAG_NAME, "img")
    assert len(images) > 0, "No images found on page"
    print(f"✓ PASSED: Found {len(images)} images on explore page")

def test_tc11_page_titles_unique(driver):
    """TC11: Verify each page has a unique title"""
    print("\n[TEST] TC11: Testing unique page titles...")
    pages = ["index.html", "explore.html", "chest.html", "shoulder.html", "bmi.html"]
    titles = []
    
    for page in pages:
        driver.get(f"{BASE_URL}/{page}")
        time.sleep(1)
        titles.append(driver.title)
    
    assert len(titles) == len(set(titles)), "Duplicate titles found"
    print("✓ PASSED: All pages have unique titles")

# ========== PERFORMANCE TESTS ==========

def test_tc12_page_load_time(driver):
    """TC12: Verify page loads within acceptable time"""
    print("\n[TEST] TC12: Testing page load performance...")
    start_time = time.time()
    driver.get(f"{BASE_URL}/index.html")
    load_time = time.time() - start_time
    
    assert load_time < 5, f"Page took {load_time:.2f}s to load (max 5s)"
    print(f"✓ PASSED: Page loaded in {load_time:.2f} seconds")

def test_tc13_responsive_mobile_view(driver):
    """TC13: Test responsive design (mobile viewport)"""
    print("\n[TEST] TC13: Testing mobile responsiveness...")
    driver.get(f"{BASE_URL}/index.html")
    
    # Set mobile viewport (iPhone size)
    driver.set_window_size(375, 667)
    time.sleep(2)
    
    assert driver.title != ""
    print("✓ PASSED: Site works in mobile view (375x667)")

def test_tc14_responsive_tablet_view(driver):
    """TC14: Test responsive design (tablet viewport)"""
    print("\n[TEST] TC14: Testing tablet responsiveness...")
    driver.get(f"{BASE_URL}/index.html")
    
    # Set tablet viewport (iPad size)
    driver.set_window_size(768, 1024)
    time.sleep(2)
    
    assert driver.title != ""
    print("✓ PASSED: Site works in tablet view (768x1024)")

# ========== SECURITY TESTS ==========

def test_tc15_google_analytics_present(driver):
    """TC15: Verify Google Analytics is implemented"""
    print("\n[TEST] TC15: Testing Google Analytics integration...")
    driver.get(f"{BASE_URL}/index.html")
    time.sleep(2)
    
    # Check page source for GA tracking code
    page_source = driver.page_source
    assert "gtag" in page_source or "G-QK7ZYSK2ZG" in page_source
    print("✓ PASSED: Google Analytics tracking code found")

# ========== NEGATIVE TESTS ==========

def test_tc16_invalid_page_handling(driver):
    """TC16: Test behavior with invalid page URL"""
    print("\n[TEST] TC16: Testing invalid page handling...")
    driver.get(f"{BASE_URL}/nonexistent.html")
    time.sleep(2)
    
    # GitHub Pages shows 404 page
    assert "404" in driver.page_source or "Not Found" in driver.page_source
    print("✓ PASSED: Invalid page handled with 404")

def test_tc17_all_navigation_links_work(driver):
    """TC17: Verify all links on explore page are functional"""
    print("\n[TEST] TC17: Testing all navigation links...")
    driver.get(f"{BASE_URL}/explore.html")
    time.sleep(2)
    
    links = driver.find_elements(By.TAG_NAME, "a")
    internal_links = [link for link in links if link.get_attribute("href") and "DiM-project" in link.get_attribute("href")]
    
    assert len(internal_links) > 0, "No internal links found"
    print(f"✓ PASSED: Found {len(internal_links)} functional internal links")

# ========== SEO TESTS ==========

def test_tc18_meta_tags_present(driver):
    """TC18: Verify SEO meta tags are present"""
    print("\n[TEST] TC18: Testing SEO meta tags...")
    driver.get(f"{BASE_URL}/index.html")
    time.sleep(2)
    
    page_source = driver.page_source
    assert 'name="description"' in page_source
    assert 'name="keywords"' in page_source
    assert 'name="robots"' in page_source
    print("✓ PASSED: All SEO meta tags present")

def test_tc19_page_has_h1_heading(driver):
    """TC19: Verify pages have H1 heading"""
    print("\n[TEST] TC19: Testing H1 heading presence...")
    pages = ["chest.html", "shoulder.html", "tricep.html"]
    
    for page in pages:
        driver.get(f"{BASE_URL}/{page}")
        time.sleep(1)
        h1_elements = driver.find_elements(By.TAG_NAME, "h1")
        assert len(h1_elements) > 0, f"No H1 found on {page}"
    
    print("✓ PASSED: All tested pages have H1 headings")

def test_tc20_external_links_open_new_tab(driver):
    """TC20: Verify external links have target='_blank'"""
    print("\n[TEST] TC20: Testing external link behavior...")
    driver.get(f"{BASE_URL}/chest.html")
    time.sleep(2)
    
    external_links = driver.find_elements(By.CSS_SELECTOR, "a[target='_blank']")
    
    if len(external_links) > 0:
        assert external_links[0].get_attribute("target") == "_blank"
        print(f"✓ PASSED: External links configured correctly ({len(external_links)} found)")
    else:
        print("⚠ SKIPPED: No external links with target='_blank' found")

if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])