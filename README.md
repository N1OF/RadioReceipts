# RadioReceipts

Python program that pulls relevant Amateur Radio information from the internet, and outputs information to a file.
The .txt file output is then designed to be printed to a thermal receipt printer, and may be scheduled via Windows
Task Manager or Cron on Linux to automatically run once a day via a Batch file or Bash Script.

This program will pull Band Conditions from HamQSL's Solar XML file, Solar Weather Predictions from NOAA Space Weather Prediction Center,
and Satellite passes from N2YO's API.

CONFIGURATION

Open the radioprint.py script, and go to "def calculate_iss_passes". You will need to edit the URL to include relevant information for use with N2YO's 
API. Comments will guide you through how to format the URL.

RUNNING

Run the python script. A file named "output.txt" will appear in the same directory as the Python Script. I have uploaded an example output.txt file.
