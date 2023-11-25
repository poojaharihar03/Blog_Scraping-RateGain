import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_blog_data(driver, url):
    # Navigate to the initial page
    driver.get(url)

    def get_titles():
        h6_elements = driver.find_elements(By.XPATH, "//h6/a")
        titles = [element.text for element in h6_elements]
        return titles

    def get_likes():
        like_ele = driver.find_elements(By.CLASS_NAME, "zilla-likes")
        likes = [element.text for element in like_ele]
        return likes

    def get_date():
        blog_detail_ele = driver.find_elements(By.CLASS_NAME, "blog-detail")
        dates = [blog_detail.find_element(By.CLASS_NAME, "bd-item").text for blog_detail in blog_detail_ele]
        return dates

    def get_images():
        anchor_elements = driver.find_elements(By.CSS_SELECTOR, "a[data-bg]")
        data_bg_values = [element.get_attribute("data-bg") for element in anchor_elements]
        return data_bg_values

    # List to store all data
    all_data = []

    while True:
        try:
            current_titles = get_titles()
            current_likes = get_likes()
            current_date = get_date()
            current_images = get_images()

            # Combine all data into a dictionary
            page_data = {'Title': current_titles, 'Likes': current_likes, 'Date': current_date, 'Images': current_images}
            all_data.append(page_data)
            
            next_page_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[@class='next page-numbers']"))
            )
            driver.execute_script("arguments[0].click();", next_page_button)

        except Exception as e:
            print("Error:", e)
            break

    return all_data

def write_to_csv(data, filename='output.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['titles', 'likes', 'date', 'images']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Write the data
        for page_data in data:
            writer.writerow(page_data)

# Example usage
driver = webdriver.Chrome()
url = "https://rategain.com/blog/"
result_data = scrape_blog_data(driver, url)

# Write data to CSV
write_to_csv(result_data)

# Close the browser window
driver.quit()
