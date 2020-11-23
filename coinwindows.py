from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


V = 1.0
if __name__ == "__main__":
    default_coins = ["ETHEREUM", "BONK", "DUSK", "AIRSWAP"]
    default_coins_binance = ["BTC", "BLZ", "LRC", "DUSK"]

    default_urls = []

    print("\nTrading Views", V, "\n")

    valid_ans = [2, 3, 4]
    print("How many windows: {} or {}?".format(
        str(valid_ans)[1:-3], valid_ans[-1]))

    windows = 0
    while True:
        inp = input(" > Enter # and press <Enter>: ")
        try:
            inp = int(inp)
            if inp in valid_ans:
                windows = inp
                break
            else:
                raise ValueError
        except ValueError:
            print("Invalid choice.\n")

    # * Select binance or CoinTrader charts.
    # ! Binance uses tickers |  CoinTrader uses full names | Kucoin to be added...
    preference = ["binance", "cmc", "kucoin"]
    exch_choice = ""

    [print("  {}. {}".format(i+1, p.upper()))
     for i, p in enumerate(preference)]

    while True:
        inp = input(" > Enter # and press <Enter>: ")
        try:
            inp = int(inp)-1

            if inp >= 0 and inp < len(preference):
                exch_choice = preference[inp]
                break
        except ValueError:
            print("Invalid choice.\n")
    print(exch_choice)
    # ! Each chart source has different quirks we need to address (i.e. how url is formed)
    if exch_choice == "binance":
        for coin in default_coins_binance:
            if coin in ["BTC", "ETH"]:
                quote = "USDT"
            else:
                quote = "BTC"
            default_urls.append(
                "https://www.binance.com/en/trade/{}_{}?layout=pro".format(coin, quote))
    elif exch_choice == "cmc":
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
    drivers = []
    # * Loop through reversed list because of the way the windows stack
    for i, url in enumerate(reversed(default_urls[:windows])):
        print(url)
        # * Create web window, navigate to a url in list
        driver = webdriver.Firefox()
        driver.get(url)
        drivers.append(driver)
        # ! Each chart source has different elements to search for
        if exch_choice == "binance":
            # * Wait for content to load so we can locate with xpath
            driver.implicitly_wait(5)

            # * Full Screen
            try:
                fs = driver.find_element_by_xpath(
                    "/html/body/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[4]").click()
            except NoSuchElementException:
                fs = driver.find_element_by_xpath(
                    '/html/body/div[1]/div[2]/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[4]').click()

        # * Resize window, adjust positioning based on index
        if windows == 2:
            # * Parameters for dual monitor setup in configuration: [Monitor2, Monitor1]
            # * Monitor2: 1920x1080
            # * This will need to be adjusted depending on system
            X_MIN_POS = -2100
            X_MAX_POS = X_MIN_POS/2 + 80

            WIDTH = 960
            HEIGHT = 1080
            driver.set_window_size(WIDTH, HEIGHT)

            if i == 1:
                driver.set_window_position(X_MIN_POS, 0)
            elif i == 0:
                driver.set_window_position(X_MAX_POS, 0)
        if windows == 3:
            # * Parameters for dual monitor setup in configuration: [Monitor2, Monitor1]
            # * Monitor2: 1920x1080
            # * This will need to be adjusted depending on system
            X_MIN_POS = -2100
            X_MAX_POS = -815

            WIDTH = 650
            HEIGHT = 1080
            driver.set_window_size(WIDTH, HEIGHT)
            if i == 2:
                driver.set_window_position(X_MIN_POS-X_MAX_POS, 0)
            elif i == 1:
                driver.set_window_position(X_MIN_POS, 0)
            elif i == 0:
                driver.set_window_position(X_MAX_POS+WIDTH/4, 0)
        elif windows == 4:
            # * Parameters for dual monitor setup in configuration: [Monitor2, Monitor1]
            # * Monitor2: 1920x1080
            # * This will need to be adjusted depending on system
            X_MIN_POS = -2100
            X_MAX_POS = -970
            Y_MAX_POS = 800

            WIDTH = 970
            HEIGHT = 580
            driver.set_window_size(WIDTH, HEIGHT)
            if i == 3:
                driver.set_window_position(X_MIN_POS, 0)
            elif i == 2:
                driver.set_window_position(X_MAX_POS, 0)
            elif i == 1:
                driver.set_window_position(X_MIN_POS, Y_MAX_POS)
            elif i == 0:
                driver.set_window_position(X_MAX_POS, Y_MAX_POS)

        #! Due to how binance's page works the only way to get trading view selected is to put this in at the end of the script
        # if choice == "binance":
        #     driver.find_element_by_css_selector(
        #         "div.css-4xvi8k:nth-child(2)").click()

    #! Empty while True loop allows us to exit all windows at once when terminating code (stop code shortcut)
    while True:
        try:
            pass
        except KeyboardInterrupt:
            break
    #! Remove if calling from cmd
