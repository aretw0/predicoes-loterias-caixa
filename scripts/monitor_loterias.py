
import requests
import json
import datetime

API_BASE_URL = "https://loteriascaixa-api.herokuapp.com/api/"

def fetch_latest_result(lottery_name):
    try:
        response = requests.get(f"{API_BASE_URL}{lottery_name}/latest")
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {lottery_name} latest result: {e}")
        return None

def log_observation(lottery_name, result, prediction=None):
    log_file = f"{lottery_name}_observations.log"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] Latest {lottery_name} Result:\n")
        f.write(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
        if prediction:
            f.write(f"  Prediction: {prediction}\n")
        f.write("\n")

def main():
    lotteries = ["megasena", "lotofacil", "maismilionaria"]

    for lottery in lotteries:
        print(f"Fetching latest result for {lottery}...")
        latest_result = fetch_latest_result(lottery)
        if latest_result:
            print(f"Latest {lottery} result fetched. Logging observation.")
            log_observation(lottery, latest_result)
        else:
            print(f"Could not fetch latest result for {lottery}.")

if __name__ == "__main__":
    main()


