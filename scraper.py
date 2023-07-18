import pandas as pd
import undetected_chromedriver as uc
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from fake_useragent import UserAgent
import time
import random
from bs4 import BeautifulSoup
from config import openai_key, proxies
import openai

def chatgpt_response(title, provider=None):
    prompt = f"Write a creative and informative description of the casino slot game {title}"
    if provider:
        prompt += f" provided by {provider}"
    prompt += ". The description should be approximately 1200-1500 words long and should engage the readers in an informal style. Markup text with <p> tags."

    prompt += " Up to 5 sentences"

    print(f'[PROMPT]: {prompt}')

    openai.api_key = openai_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are online casino player"},
                {"role": "user", "content": prompt},
            ]
    )
    result = ''
    for choice in response.choices:
        result += choice.message.content
    return result

# def create_driver_with_proxy(proxy):
#     options = uc.ChromeOptions()
#     options.add_argument("--disable-blink-features=AutomationControlled")
#     options.add_argument("window-size=1920,1080")
#     options.add_argument("--headless")
#     if proxy:
#         options.add_argument('--proxy-server=%s' % proxy)
#     driver = uc.Chrome(options=options)
#     driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
#     return driver

# df = pd.read_csv('games.csv')
# ua = UserAgent()
# proxy = proxies[0]
# driver = create_driver_with_proxy(None)

# all_data = []

# for index, row in df.iterrows():
#     url = row['url']
#     slug = row['slug']
#     image = row['image']
#     driver.get(url)
#     time.sleep(random.randint(10, 15))
#     user_agent = ua.random
#     driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": user_agent})
#     try:
#         demo_button = driver.find_element('id', 'demo_button')
#         demo_button.click()
#     except NoSuchElementException:
#         print(f'Demo button not found on page {url}')
#         continue
#     except ElementNotInteractableException:
#         print('Timeout 60')
#         time.sleep(60)
#         # proxy = random.choice([p for p in proxies if p != proxy])
#         # driver = create_driver_with_proxy(proxy)
#         # driver.get(url)
#         try:
#             demo_button.click()
#         except ElementNotInteractableException:
#             print(f'Timeout 300, skipping page {url}')
#             time.sleep(300)
#             continue

#     soup = BeautifulSoup(driver.page_source, 'lxml')
#     title = title.text if (title := soup.find('title')) else None
#     description = soup.find('meta', attrs={'name': 'description'})
#     description = description['content'] if description else None
#     info_title = info_title.text if (info_title := soup.find('h1', class_='slot__info-title')) else None
#     table = soup.find('table', class_='slot__table')
#     labels_values = {}
#     if table:
#         rows = table.find_all('tr')
#         for row in rows:
#             labels = row.find_all('p', class_='slot__label')
#             values = row.find_all(['a', 'p'], class_='slot__value')
#             for label, value in zip(labels, values):
#                 labels_values[label.text] = value.text
#     # chatgpt_output = chatgpt_response(info_title, None if labels_values['Software:'] == '-' else labels_values['Software:'])

#     data = {
#         'meta_title': title,
#         'meta_description': description,
#         'title': info_title,
#         'slug': slug,
#         'url': url,
#         'image': image,
#         # 'chatgpt_output': chatgpt_output
#     }
#     data.update(labels_values)
#     all_data.append(data)

#     driver.save_screenshot(f'screenshot_{slug}.png')

#     # Save to CSV after every iteration
#     df = pd.DataFrame(all_data)
#     df.to_csv('data.csv', index=False)

#     print(f'Saved {index}th page')prompt

# driver.quit()

data = pd.read_csv('result.csv')

data['gpt_response'] = ''

# Iterate through each row
for index, row in data.iterrows():
    # Extract 'title' and 'Software' columns
    title = row['title']
    software = row['Software:']

    # Generate response using ChatGPT
    response = chatgpt_response(title, software)

    print(f'[RESPONSE]: {response}')

    # Store the response in the 'response' column
    data.at[index, 'gpt_response'] = response

    # Save the modified data to a new CSV file
    data.to_csv('output.csv', index=False)
    print(f'Saved {index}th row')
    print('=' * 50)

# Optional: Print a message when saving is completed
print("Data saved to output.csv")
