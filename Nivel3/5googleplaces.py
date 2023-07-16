import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def getScrollingScript(iteration):
    scrollingScript = "document.getElementsByClassName('m6QErb DxyBCb kA9KIf dS8AEf')[0]"

    return scrollingScript + f".scroll(0, {20000 * (iteration + 1)})"


opts = Options()
opts.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
driver.get(
    'https://www.google.com/maps/place/Casa+Caf%C3%A9+Cultor/@4.6549367,-74.058282,17z/data=!4m18!1m9!3m8!1s0x8e3f9a43d4c55d2b:0x9d270b51da5e090e!2sCasa+Caf%C3%A9+Cultor!8m2!3d4.6549367!4d-74.058282!9m1!1b1!16s%2Fg%2F11dxdn_txc!3m7!1s0x8e3f9a43d4c55d2b:0x9d270b51da5e090e!8m2!3d4.6549367!4d-74.058282!9m1!1b1!16s%2Fg%2F11dxdn_txc?entry=ttu'
)

sleep(random.uniform(3, 5.0))

SCROLLS = 0
MAX_SCROLLS = 3
while SCROLLS < MAX_SCROLLS:
    driver.execute_script(getScrollingScript(SCROLLS))
    sleep(random.uniform(3, 5.0))
    SCROLLS += 1

restaurantsReviews = driver.find_elements(By.XPATH, '//div[@data-review-id and not(@aria-label)]')

for review in restaurantsReviews:
    sleep(1)
    userLink = review.find_element(By.XPATH, "//div[contains(@class, 'WNx')]//button")

    try:
        userLink.click()

        driver.switch_to.window(driver.window_handles[1])

        userReviews = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '//div[@data-review-id and not(@aria-label)]'))
        )
        USER_SCROLLS = 0
        while (USER_SCROLLS < 2):
            driver.execute_script(getScrollingScript(USER_SCROLLS))
            sleep(random.uniform(4, 5))
            USER_SCROLLS += 1

        userReviews = driver.find_elements(By.XPATH, '//div[@data-review-id and not(@aria-label)]')

        for userReview in userReviews:
            print("*********************")
            reviewRating = userReview.find_element(By.XPATH, './/span[@class="kvMYJc"]').get_attribute('aria-label')
            userParsedRating = float(''.join(filter(str.isdigit or str.isspace,
                                                    reviewRating)))
            reviewText = userReview.find_element(By.XPATH, './/span[@class="wiI7pd"]').text

            print(userParsedRating)
            print(reviewText)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    except Exception as e:
        print(e)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
