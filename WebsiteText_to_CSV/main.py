import requests # download the website content.
from bs4 import BeautifulSoup # Used to parse the downloaded HTML content.
import csv
from urllib.parse import urljoin # combine base URL with relative URLs found on the website.

base_url = "https://ezra.com/conditions"
with open('dataset.csv', mode='w', newline='') as file: # Opens a CSV file ("dataset.csv") for writing and creates a CSV writer object.
    writer = csv.writer(file)
    writer.writerow(["Name", "Description", "Category"]) # Writes the header row with column names ("Name", "Description", "Category").

    while True:
        response = requests.get(base_url) # Makes a GET request to the current URL (starts with base_url).
        if response.status_code == 200: # 200 means successful
            soup = BeautifulSoup(response.content, 'html.parser') # If request is successful Parses the downloaded content with BeautifulSoup.
            cards = soup.find_all('div', class_='conditions-card') # Finds all elements with class "conditions-card" (likely containing condition details).
            if not cards:
                print("Error.")
                break
            for card in cards:
                try: 
                    name = card.find('h4', attrs={'fs-cmsfilter-field': 'Name'}).get_text().strip() # from an h4 element attribute (fs-cmsfilter-field: Name).
                    description_div = card.find('div', attrs={'fs-cmsfilter-field': 'Description'})
                    if description_div and description_div.find('p'):
                        description_text = description_div.find('p').get_text().strip()
                    else:
                        description_text = "No description available"
                    category_div = card.find('div', attrs={'fs-cmsfilter-field': 'Categories'})
                    category = category_div.get_text().strip() if category_div else "No category available"

                    writer.writerow([name, description_text, category])
                except AttributeError as e:
                    print(f"A card was missing expected fields, skipping it. Error: {e}")

            next_button = soup.find('a', class_='w-pagination-next') # Checks for a "next page" button.

            if next_button:
                next_page_url = next_button['href']
                urljoin(base_url, next_page_url) # Extracts the URL for the next page using urljoin.
                print(f"Moving to next page: {base_url}")
            else:
                print("No more pages to scrape.")
                break

        else:
            print("Failed to retrieve the website's content")
            break

print("Data extracted and saved to dataset.csv")

next_button = soup.find('a', class_='w-pagination-next')

if next_button:
    next_page_url = next_button['href']
    next_url = urljoin(base_url, next_page_url)  # Extracts the URL for the next page using urljoin
    base_url = next_url  # Updates the base_url for the next iteration
    print(f"Moving to next page: {base_url}")