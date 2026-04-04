import requests

# Configuration
URL = "https://tgftp.nws.noaa.gov/data/forecasts/recreation/reno.txt"
NTFY_TOPIC = "Rileys-tahoe-surf-alert-841"
KEYWORD = "1 foot"

def check_waves():
    try:
        response = requests.get(URL)
        text = response.text.lower()
        
        # This will now trigger for '1 foot' as seen in today's forecast
        if "1 foot" in text:
            msg = "Waves are forecasted for Tahoe!"
            requests.post(f"https://ntfy.sh/{NTFY_TOPIC}", 
                          data=msg,
                          headers={"Title": "Tahoe Surf Alert", "Priority": "high"})
            print("Alert sent!")
        else:
            print(f"Conditions not met. Current text: {text[:100]}...")
            
    except Exception as e:
        print(f"Error: {e}")
        
if __name__ == "__main__":
    check_waves
    ()
