import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Function to scrape water-related data from a URL
def scrape_water_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract relevant data from the webpage
    data = []
    for row in soup.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) > 0:
            row_data = [cell.text.strip() for cell in cells]
            data.append(row_data)
    
    return data

# Example usage: Scrape data from a government website
water_data_url = "https://www.un.org/"
raw_data = scrape_water_data(water_data_url)

# Clean and preprocess the data
df = pd.DataFrame(raw_data, columns=['Region', 'Water Availability', 'Water Consumption', 'Water Scarcity'])
df = df.dropna()  # Remove rows with missing values
df['Water Availability'] = df['Water Availability'].astype(float)
df['Water Consumption'] = df['Water Consumption'].astype(float)
df['Water Scarcity'] = df['Water Scarcity'].astype(float)

# Exploratory data analysis
print('Data Summary:')
print(df.describe())

print('\nCorrelation Matrix:')
print(df.corr())

# Visualize the data
plt.figure(figsize=(12, 6))
sns.scatterplot(x='Water Availability', y='Water Consumption', data=df, hue='Water Scarcity')
plt.xlabel('Water Availability')
plt.ylabel('Water Consumption')
plt.title('Water Availability vs. Consumption by Water Scarcity')
plt.show()