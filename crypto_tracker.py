import requests
import pandas as pd
import time

def fetch_prices(coin_list):
    """
    Fetch current prices and 24h changes for given cryptocurrencies from CoinGecko API.
    """
    ids = ",".join(coin_list)
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ids,
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, params=params)
    time.sleep(1.5)  # To avoid hitting API rate limits

    try:
        data = response.json()
    except Exception:
        print("⚠️ Failed to parse API response.")
        return None

    # Handle API rate limit error
    if "error" in data or "status" in data:
        print("⛔ API rate limit hit. Please wait and try again later.")
        return pd.DataFrame([{
            "Coin": coin.title(),
            "Price (USD)": "N/A",
            "24h Change (%)": "N/A"
        } for coin in coin_list])

    records = []
    for coin in coin_list:
        try:
            price = data[coin]["usd"]
            change = data[coin]["usd_24h_change"]
            records.append({
                "Coin": coin.title(),
                "Price (USD)": round(price, 2),
                "24h Change (%)": round(change, 2)
            })
        except KeyError:
            records.append({
                "Coin": coin.title(),
                "Price (USD)": "N/A",
                "24h Change (%)": "N/A"
            })

    return pd.DataFrame(records)

def show_summary(df):
    """
    Display price summary, top gainer, and top loser based on 24h price change.
    """
    print("\n📊 Price Summary:")
    print(df)

    valid_df = df[df["24h Change (%)"] != "N/A"]
    if valid_df.empty:
        print("No valid data available to determine gainers and losers.")
        return

    sorted_df = valid_df.sort_values(by="24h Change (%)", ascending=False)

    print("\n📈 Top Gainer:")
    print(sorted_df.head(1).to_string(index=False))

    print("\n📉 Top Loser:")
    print(sorted_df.tail(1).to_string(index=False))

def main():
    """
    Main CLI loop to interact with the user.
    """
    print("🚀 Welcome to Crypto Tracker CLI")

    coin_list = ["bitcoin", "ethereum", "solana", "cardano"]

    while True:
        print("\nMenu:")
        print("1. Track My Coins")
        print("2. Show Gainers & Losers")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            df = fetch_prices(coin_list)
            if df is not None:
                print(df)
        elif choice == "2":
            df = fetch_prices(coin_list)
            if df is not None:
                show_summary(df)
        elif choice == "3":
            print("👋 Exiting. See you again!")
            break
        else:
            print("⚠️ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
