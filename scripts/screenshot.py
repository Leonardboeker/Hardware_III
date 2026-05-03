from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto('file:///C:/Users/Rafik/Documents/GitHub/Hardware/proposal.html')
    page.wait_for_load_state('networkidle')

    # Screenshot each slide
    page.screenshot(path='screenshot_slide1.png', full_page=False)

    page.evaluate('window.scrollTo(0, window.innerHeight)')
    page.wait_for_timeout(300)
    page.screenshot(path='screenshot_slide2.png', full_page=False)

    page.evaluate('window.scrollTo(0, window.innerHeight * 2)')
    page.wait_for_timeout(300)
    page.screenshot(path='screenshot_slide3.png', full_page=False)

    browser.close()
    print("Screenshots saved")
