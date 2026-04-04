import requests
import re

URL = "https://tgftp.nws.noaa.gov/data/forecasts/recreation/reno.txt"
NTFY_TOPIC = "Rileys-tahoe-surf-alert-841"

def get_value(pattern, text):
    match = re.search(pattern, text)
    return match.group(1).strip() if match else "N/A"

def check_waves():
    try:
        response = requests.get(URL)
        text = response.text.lower()
        
        # Look for 4, 5, or 6 feet/ft
        match = re.search(r"([1-6]\s*(feet|foot|ft))", text)
        
        if match:
            wave_height = match.group(1)
            # Extracting other conditions using simple regex
            wind = get_value(r"winds?\s*(.*?)\.", text)
            air = get_value(r"air temperature\s*(.*?)\.", text)
            water = get_value(r"water temperature\s*(.*?)\.", text)

            message = (
                f"Tahoe is ON! 🏄\n"
                f"Waves: {wave_height}\n"
                f"Wind: {wind}\n"
                f"Air: {air} | Water: {water}\n"
                f"Get after it!"
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
