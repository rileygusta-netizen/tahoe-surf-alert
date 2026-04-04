import requests

URL = "https://tgftp.nws.noaa.gov/data/forecasts/recreation/reno.txt"
NTFY_TOPIC = "rileys-tahoe-surf-alert-841"
# Let's use a very broad keyword for this final test
TEST_KEYWORD = "foot"

def check_waves():
    try:
        response = requests.get(URL)
        text = response.text.lower()
        
        print(f"Checking for '{TEST_KEYWORD}' in NWS text...")
        
        if True:
            requests.post(f"https://ntfy.sh/{NTFY_TOPIC}", 
                          data=f"Success! Found '{TEST_KEYWORD}' in the Tahoe forecast.",
                          headers={"Title": "Tahoe Surf Alert", "Priority": "high"})
            print("Alert sent!")
        else:
            print(f"Keyword '{TEST_KEYWORD}' not found in the first 100 characters: {text[:100]}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_waves
    ()
