import requests
import re

URL = "https://tgftp.nws.noaa.gov/data/forecasts/recreation/reno.txt"
NTFY_TOPIC = "Rileys-tahoe-surf-alert-841"

def check_waves():
    try:
        response = requests.get(URL)
        full_text = response.text.lower()
        
        # 1. Isolate the Lake Tahoe specific section to avoid global warnings
        # This looks for text between 'lake tahoe at lake level' and the next '$$' separator
        tahoe_section = re.search(r"lake tahoe at lake level-.*?\$\$", full_text, re.DOTALL)
        if not tahoe_section:
            print("Could not find Lake Tahoe section.")
            return
            
        text = tahoe_section.group(0)

        # 2. Look for wave heights (4-9 ft for testing)
        match = re.search(r"wave heights (([4-9]|\d{2,})\s*(feet|foot|ft))", text)
        
        if match:
            wave_height = match.group(1)
            
            # 3. Targeted extraction for Tahoe-specific conditions
            # Finds winds specifically in the '.TONIGHT' or '.SATURDAY' lines
            wind_match = re.search(r"winds?\s+(.*?)\.", text)
            wind = wind_match.group(1) if wind_match else "Light"
            
            # Finds highs/lows
            temp_match = re.search(r"(highs|lows)\s+(\d+\s+to\s+\d+)", text)
            air_temp = temp_match.group(2) if temp_match else "N/A"
            
            # Finds water temp from the specific 'Mid Lake Buoys' line
            water_match = re.search(r"buoys\.+(\d+\.?\d*)", text)
            water_temp = water_match.group(1) if water_match else "N/A"

            message = (
                f"🏄 TAHOE IS ON!\n"
                f"Swell: {wave_height}\n"
                f"Wind: {wind}\n"
                f"Air: {air_temp}°\n"
                f"Water: {water_temp}°\n"
                f"You'll be fine! 🤙🥶🤙"
            )
            
            requests.post(f"https://ntfy.sh/{NTFY_TOPIC}", 
                          data=message,
                          headers={"Title": "Swell Alert: Tahoe", "Priority": "high"})
            print("Surf alert sent!")
        else:
            print("Flat spells continue...")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_waves()
