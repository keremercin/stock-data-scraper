import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

def scrape_stock_data(base_url, output_excel_path):
    # Send a GET request to the website
    response = requests.get(base_url)

    # Parse the website content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Create an empty list to store the data
    data = []

    # Find all <li> elements with class 'cell064'
    li_elements = soup.find_all('li', class_='cell064')

    # Process each <li> element
    for li_element in li_elements:
        # Find the <a> element with target='_blank'
        a_element = li_element.find('a', target='_blank')
        
        if a_element:
            # Get the href attribute of the <a> element
            href = a_element.get('href')
            
            # Combine with the base URL
            full_url = urljoin(base_url, href)
            
            # Send a GET request to the full URL
            new_response = requests.get(full_url)
            
            # Parse the new page content using BeautifulSoup
            new_soup = BeautifulSoup(new_response.content, 'html.parser')
            
            # Find the <h1> element with class 'pageTitle'
            h1_element = new_soup.find('h1', class_='pageTitle')
            
            # Find the required text elements
            fk_ratio_element = new_soup.find('li', text='F/K Oranı')
            market_value_ratio_element = new_soup.find('li', text='Piyasa Değ. / Defter Değ.')
            
            if h1_element and fk_ratio_element and market_value_ratio_element:
                # Add the data to the list
                data.append([
                    h1_element.text.strip(),
                    fk_ratio_element.find_next('li').text.strip(),
                    market_value_ratio_element.find_next('li').text.strip()
                ])

    # Convert the data to a DataFrame
    df = pd.DataFrame(data, columns=["Company Name", "P/E Ratio", "Market Value/Book Value Ratio"])

    # Save the DataFrame to an Excel file
    df.to_excel(output_excel_path, index=False)
    print(f"Data has been successfully saved to {output_excel_path}")

if __name__ == "__main__":
    base_url = 'https://bigpara.hurriyet.com.tr/borsa/canli-borsa/tum-hisseler/'  # Change this to the URL of the website you want to scrape
    output_excel_path = "path/to/your/output_file.xlsx"  # Change this to the path where you want to save the Excel file

    scrape_stock_data(base_url, output_excel_path)
