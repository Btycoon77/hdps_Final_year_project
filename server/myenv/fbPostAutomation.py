from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from time import sleep

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


# Initialize Chrome WebDriver
def init_driver():
    service = Service("C:\\Driver\\chromedriver-win64\\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    return driver


# Function to login to Facebook
def login_to_facebook(driver, email_address, password_value):
    driver.get("https://www.facebook.com")

    try:
        # Find email, password fields, and login button
        email = driver.find_element(By.ID, "email")
        password = driver.find_element(By.ID, "pass")
        login_button = driver.find_element(By.NAME, "login")

        # Input email and password, then click login
        email.send_keys(email_address)
        password.send_keys(password_value)
        login_button.click()
        sleep(3)  # Allow time for the page to load

    except Exception as e:
        print("Error during login:", e)
        driver.quit()


# Function to post a message
def post_message(driver, message):
    try:
        # Find and click the post area

        post_area = driver.find_element(
            By.CLASS_NAME, "x1ed109x x1iyjqo2 x5yr21d x1n2onr6 xh8yej3"
        )
        post_area.click()
        sleep(3)

        # Switch to active post area and type message
        active_post_area = driver.switch_to.active_element
        active_post_area.send_keys(message)

        # Find and click the "Post" button
        post_buttons = driver.find_elements(
            By.TAG_NAME,
            "x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz x9f619 x3nfvp2 xdt5ytf xl56j7k x1n2onr6 xh8yej3",
        )
        for button in post_buttons:
            if button.text == "Post":
                button.click()
                break

        print("Message posted successfully!")

    except Exception as e:
        print("Error during posting:", e)


# Main function
def main():
    email_address = "btycoon84@gmail.com"
    password_value = "9192631770"
    message = "Hello Programmer"

    # Initialize driver
    driver = init_driver()

    # Login and post message
    login_to_facebook(driver, email_address, password_value)
    post_message(driver, message)

    # Close the driver
    driver.quit()


if __name__ == "__main__":
    main()
