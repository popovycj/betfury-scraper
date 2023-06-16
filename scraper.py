import pandas as pd
import undetected_chromedriver as uc
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from fake_useragent import UserAgent
import time
import random
from config import proxies

# Function to create driver with specified proxy
def create_driver_with_proxy(proxy):
    options = uc.ChromeOptions()

    # Adding argument to disable the AutomationControlled flag
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Set browser size to Full HD
    options.add_argument("window-size=1920,1080")

    # Set proxy server
    if proxy:
        options.add_argument('--proxy-server=%s' % proxy)

    # Set up the Selenium WebDriver (this example uses Chrome)
    driver = uc.Chrome(options=options)

    # Changing the property of the navigator value for webdriver to undefined
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    return driver

# Load the CSV file
df = pd.read_csv('games.csv')

# Initialize the UserAgent object
ua = UserAgent()

proxy = proxies[1]

# Start without a proxy
driver = create_driver_with_proxy(None)

# Iterate over each URL and corresponding slug
for _, row in df.iterrows():
    url = row['url']
    slug = row['slug']
    driver.get(url)
    time.sleep(random.randint(10, 15))  # wait for 10 to 15 seconds

    # Set the user agent
    user_agent = ua.random
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": user_agent})

    # Try to find the button and click it
    try:
        demo_button = driver.find_element('id', 'demo_button')
        demo_button.click()
    except NoSuchElementException:
        print(f'Demo button not found on page {url}')
        continue
    except ElementNotInteractableException:
        # If button is not interactable, change the proxy and try again
        driver.close()  # close current driver

        # Choose a random proxy from the list
        proxy = random.choice([p for p in proxies if p != proxy])

        driver = create_driver_with_proxy(proxy)  # create new driver with updated proxy
        time.sleep(60)  # wait for 1 minute

        driver.get(url)  # load the URL in the new driver instance
        try:
            demo_button.click()
        except ElementNotInteractableException:
            # If still not interactable, wait for 5 minutes
            time.sleep(300)  # wait for 5 minutes
            continue

    # Take a screenshot
    driver.save_screenshot(f'screenshot_{slug}.png')

# Close the browser
driver.quit()
