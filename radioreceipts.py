#Copyright (c) [2023] [Scott Sheets]
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#

import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from tabulate import tabulate

def fetch_calculated_conditions(url):
    try:
        response = requests.get(url)
        root = ET.fromstring(response.text)

        calculated_conditions = root.find(".//calculatedconditions")
        if calculated_conditions is not None:
            conditions_data = []
            for band in calculated_conditions.findall(".//band"):
                band_name = band.get("name")
                time = band.get("time")
                condition = band.text
                conditions_data.append([f"{band_name} ({time})", condition])

            # Use tabulate to format data into a table with reduced width
            table = tabulate(conditions_data, headers=["Band & Time", "Condition"], tablefmt="plain")
            return table
        else:
            return "No calculated conditions found in the XML."

    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        print(f"Raw XML content:\n{response.text}")
        return "Error parsing XML. See console for details."
    except Exception as e:
        print(f"Error fetching calculated conditions: {e}")
        return "Error fetching calculated conditions. See console for details."

def fetch_solar_weather_predictions():
    url = "https://services.swpc.noaa.gov/text/advisory-outlook.txt"
    response = requests.get(url)
    return response.text

def calculate_iss_passes():
    #Edit URL for your satellite. Variables should be set as follows:
    #25544 - ISS NORAD ID, or enter ID of satellite you want predictions for
    #LAT - Latitude (In Decimal Degrees)
    #LON - Longiture (In Decimal Degrees)
    #ELE - Elevation (In Meters)
    #DAY - How many days you want predictions for
    #DEG - Minimum Satellite Elevation you want passes for (In Degrees)
    #YOUR_API_KEY - N2YO API Key
    url = "https://api.n2yo.com/rest/v1/satellite/radiopasses/25544/LAT/LON/EVE/DAY/DEG/&apiKey=YOUR_API_KEY"
    response = requests.get(url)

    try:
        response_json = response.json()
        passes = response_json.get("passes", [])
        return passes
    except ValueError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Raw JSON content:\n{response.text}")
        return []

def format_iss_passes_for_table(passes):
    table_data = []
    for pass_info in passes:
        start_utc = datetime.fromtimestamp(pass_info['startUTC'], timezone.utc)
        end_utc = datetime.fromtimestamp(pass_info['endUTC'], timezone.utc)
        table_data.append([
            start_utc.strftime('%Y-%m-%d %H:%M:%S'),
            f"{pass_info['maxEl']:.2f} degrees",
            end_utc.strftime('%Y-%m-%d %H:%M:%S'),
        ])

    # Use tabulate to format data into a table with reduced width
    table = tabulate(table_data, headers=["Start UTC", "Max El", "End UTC"], tablefmt="plain")
    return table

def write_data_to_file(data):
    with open("output.txt", "w") as file:
        file.write(data)

def main():
    # Fetch data from HamQSL XML (calculated conditions only)
    hamqsl_url = "https://www.hamqsl.com/solarxml.php"
    calculated_conditions = fetch_calculated_conditions(hamqsl_url)

    # Fetch data from other sources
    solar_weather_predictions = fetch_solar_weather_predictions()
    iss_passes = calculate_iss_passes()

    formatted_iss_passes_table = format_iss_passes_for_table(iss_passes)

    # Get the current UTC time
    current_utc_time = datetime.now(timezone.utc)
    formatted_utc_time = current_utc_time.strftime('%Y-%m-%d %H:%M UTC')
    
    # Prepare data for printing
    data_to_print = (
    f"Amateur Radio Conditions for {formatted_utc_time}\n"
    f"{'*'*40}\n"  # Visual break line
    f"Calculated Conditions:\n{calculated_conditions}\n"
    f"{'*'*40}\n"  # Visual break line
    f"Solar Weather Predictions:\n{solar_weather_predictions}"
    f"{'*'*40}\n"  # Visual break line
    f"ISS Passes (Table Format):\n{formatted_iss_passes_table}"
)

    # Write data to a file
    write_data_to_file(data_to_print)

if __name__ == "__main__":
    # Run the program once
    main()
