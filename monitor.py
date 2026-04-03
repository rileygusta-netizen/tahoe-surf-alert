import requests

# Configuration
URL = "https://tgftp.nws.noaa.gov/data/forecasts/recreation/reno.txt"
NTFY_TOPIC = "rileys-tahoe-surf-alert-841"
KEYWORD = "1 foot"

def check_waves():
    try:
        response = requests.get(URL)
        text = response.text.lower()
        
        if KEYWORD in text:
            # Send the push notification
            requests.post(f"https://ntfy.sh/{NTFY_TOPIC}", 
                          data=f"Alert: Wave heights of {KEYWORD} forecasted for Tahoe!",
                          headers={"Title": "Tahoe Surf Alert", "Priority": "high"})
            print("Alert sent!")
        else:
            print("Conditions not met.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_waves
    ()
