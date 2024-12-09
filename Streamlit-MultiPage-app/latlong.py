## In Analytics module we want to build add Geomap that shows sector wise distribution of avg price per sqft.
## So to map sector into map , we rquired latitude and longitude of each sector. so will do web srapping from Google

from opencage.geocoder import OpenCageGeocode
import pandas as pd

# OpenCage API key (Sign up at https://opencagedata.com/ for your free API key)
API_KEY = "565031f3bbc14c24b492675a1aa0cdff"  # Replace with your API key
geocoder = OpenCageGeocode(API_KEY)

# List of sectors in Gurgaon
sectors = [f"Sector {i}" for i in range(1, 115)]  # Adjust range as needed

# Data storage
sector_data = []

# Fetch coordinates for each sector
for sector in sectors:
    query = f"{sector}, Gurgaon, India"
    result = geocoder.geocode(query)
    
    if result:  # If a result is found
        latitude = result[0]['geometry']['lat']
        longitude = result[0]['geometry']['lng']
        sector_data.append({"Sector": sector, "Latitude": latitude, "Longitude": longitude})
        print(f"{sector}: {latitude}, {longitude}")
    else:  # If no result is found
        sector_data.append({"Sector": sector, "Latitude": None, "Longitude": None})
        print(f"{sector}: Coordinates not found.")

# Save the data to a CSV file
df = pd.DataFrame(sector_data)
df.to_csv("gurgaon_sector_coordinates.csv", index=False)

print("Coordinates fetched and saved to 'gurgaon_sector_coordinates.csv'.")
