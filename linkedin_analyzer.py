import csv
import time
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


service = Service('C:\\Users\\shara\\Downloads\\chromedriver-win64 (1)\\chromedriver-win64\\chromedriver.exe')

# Initialize WebDriver with the Service
driver = webdriver.Chrome(service=service)

# Log into LinkedIn
def login_to_linkedin(username, password):
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(10)

# Read profile URLs from CSV
def read_profile_urls(file_path):
    profile_urls = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            profile_urls.append(row['profile_url'])
    return profile_urls

# Analyze LinkedIn messages
def analyze_conversations(profile_urls):
    conversation_scores = {}
    
    for profile_url in profile_urls:
        try:
            driver.get(profile_url)
            time.sleep(5)  # Allow profile to load

            # Click the "Message" button
            message_button = driver.find_element(By.XPATH, "//*[@id='global-nav']/div/nav/ul/li[4]")
            message_button.click()
            time.sleep(3)  # Allow messaging window to open
            
            # Count messages in the conversation
            messages = driver.find_elements(By.XPATH, "//div[@class='msg-s-event__content']//p[contains(@class, 'msg-s-event-listitem__body')]")

            message_count = len(messages)
            
            # Extract the name from the profile
            name = driver.find_element(By.XPATH, "//*[@id='thread-detail-jump-target']").text
            
            # Add to the dictionary
            conversation_scores[name] = message_count
            print(f"{name}: {message_count} messages")

            # Close the messaging overlay (if needed)
            close_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Close')]")
            close_button.click()
            time.sleep(2)
        
        except Exception as e:
            print(f"Failed to analyze {profile_url}: {e}")
    
    return conversation_scores


# Calculate scores based on message count

def calculate_scores(conversation_scores):
    score_dict = {}
    for name, count in conversation_scores.items():
        score_dict[name] = count  # Example: score based on message count
    return score_dict

# Main script
if __name__ == "__main__":
    
    # Replace with your LinkedIn credentials
    username = "rambogaming121@gmail.com"
    password = "Sharan@7306624241"
    
    # Login to LinkedIn
    login_to_linkedin(username, password)
    
    # Read profile URLs
    profiles = read_profile_urls("connections.csv")
    
    # Analyze conversations
    conversation_scores = analyze_conversations(profiles)
    
    # Calculate scores and print results
    final_scores = calculate_scores(conversation_scores)
    print(final_scores,'final score')
    
    # Close WebDriver
    driver.quit()