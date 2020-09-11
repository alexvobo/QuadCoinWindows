from selenium import webdriver

# * Parameters for dual monitor setup in configuration: [Monitor2, Monitor1]
# * Monitor2: 1920x1080
# * This will likely need to be adjusted depending on system
X_MIN_POS = -2100
X_MAX_POS = -970
Y_MAX_POS = 800

WIDTH = 970
HEIGHT = 580

if __name__ == "__main__":
    default_coins = ["BITCOIN", "ETHEREUM", "LOOPRING", "DUSK"]
    default_coins_binance = ["BTC", "ETH", "LRC", "DUSK"]

    default_urls = []

    # * Select binance or CoinTrader charts.
    # ! Binance uses tickers |  CoinTrader uses full names | Kucoin to be added...
    preference = ["binance", "cmc", "kucoin"]
    choice = preference[1]

    # ! Each chart source has different quirks we need to address (i.e. how url is formed)
    if choice == "binance":
        for coin in default_coins_binance:
            if coin in ["BTC", "ETH"]:
                quote = "USDT"
            else:
                quote = "BTC"
            default_urls.append(
                "https://www.binance.com/en/trade/{}_{}?layout=pro".format(coin, quote))
    elif choice == "cmc":
        for coin in default_coins:
            if coin in ["BITCOIN", "ETHEREUM"]:
                quote = "USD"
            else:
                quote = "BTC"
            default_urls.append(
                "https://charts.cointrader.pro/charts.html?coin={}%3A{}".format(coin, quote))
    else:
        #!
        #! Add KuCoin code here
        #!
        pass

    # * Loop through reversed list because of the way the windows stack
    for i, url in enumerate(reversed(default_urls)):
        # * Create web window, navigate to a url in list
        driver = webdriver.Firefox()
        driver.get(url)

        # ! Each chart source has different elements to search for
        if choice == "binance":
            # * Wait for content to load so we can locate with xpath
            driver.implicitly_wait(5)

            # * Full Screen
            fs = driver.find_element_by_xpath(
                "/html/body/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[4]").click()

        # * Resize window, adjust positioning based on index
        driver.set_window_size(WIDTH, HEIGHT)
        if i == 3:
            driver.set_window_position(X_MIN_POS, 0)
        elif i == 2:
            driver.set_window_position(X_MAX_POS, 0)
        elif i == 1:
            driver.set_window_position(X_MIN_POS, Y_MAX_POS)
        elif i == 0:
            driver.set_window_position(X_MAX_POS, Y_MAX_POS)
        else:
            break

        #! Due to how binance's page works the only way to get trading view selected is to put this in at the end of the script
        if choice == "binance":
            driver.find_element_by_css_selector(
                "div.css-4xvi8k:nth-child(2)").click()

    #! Empty while True loop allows us to exit all windows at once when terminating code (stop code shortcut)
    while True:
        pass
    #! Remove if calling from cmd
