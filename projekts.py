from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from colorama import Fore, Style

while True:
    print("Select the section that interests you:")
    print("1. Stocks")
    print("2. Funds")
    print("3. Futures")
    print("4. Forex")
    print("5. Crypto")
    print("6. Index")
    print("7. Bonds")
    print("8. Economic")

    choice = input("Enter the number of the section you want to explore: ").strip()
    name = input("Enter the title (only short name): ").strip()

    if choice == "1":
        choice = "stocks"
    elif choice == "2":
        choice = "funds"
    elif choice == "3":
        choice = "futures"
    elif choice == "4":
        choice = "forex"
    elif choice == "5":
        choice = "bitcoin,crypto"
        name = (name + "USD")
    elif choice == "6":
        choice = "index"
    elif choice == "7":
        choice = "bond"
    elif choice == "8":
        choice = "economic"
    else:
        print("SELECT A NUMBER FROM 1 TO 8")
        continue

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    url = "https://ru.tradingview.com/markets/cryptocurrencies/"
    driver.get(url)

    time.sleep(2)

    try:
        find = driver.find_element(By.CLASS_NAME, "tv-header-search-container__button")
    except NoSuchElementException:
        print("Element not found. Exiting.")
        driver.quit()
        break

    find.click()

    time.sleep(1)
    find = driver.find_element(By.ID, choice)
    find.click()
    find = driver.find_element(By.NAME, "query")
    find.click()
    find.send_keys(name)
    find.click()
    find = driver.find_element(By.CLASS_NAME, "icon-KLRTYDjH")
    find.click()
    time.sleep(5)

    try:
        find = driver.find_element(By.CLASS_NAME, "highlight-maJ2WnzA.price-qWcO4bp9")
        span_element = driver.find_element(By.CLASS_NAME, "currency-qWcO4bp9")
        span_element_change = driver.find_element(By.CLASS_NAME, 'change-SNvPvlJ3')
        span_element2 = driver.find_element(By.CLASS_NAME, 'text-d1N3lNBX')
    except NoSuchElementException:
        print(Fore.YELLOW,"Elements not found. Exiting.",Style.RESET_ALL)
        driver.quit()
        break

    temp = float(find.text)
    change_value_text = span_element_change.text
    change_value_text = change_value_text.replace('−', '-')
    currency_text = span_element.text
    active = span_element2.text

    change_value = float(change_value_text)
    if change_value > 0:
        percent = (change_value * 100) / (temp - change_value)
    elif change_value < 0:
        minval = change_value * (-1) + temp
        percent = (change_value * 100) / minval
    percent_str = float("{:.2f}".format(percent))
    print("-" * 30)
    print(name.upper())
    print("-" * 30)
    print("CURRENT PRICE:", temp, currency_text)
    if percent_str < 0:
        print("CHANGES IN THE LAST 24 HOURS:", Fore.RED, change_value, currency_text, Style.RESET_ALL, "(",
              Fore.RED, percent_str, "%", Style.RESET_ALL, ")")
    else:
        print("CHANGES IN THE LAST 24 HOURS:", Fore.GREEN, change_value, currency_text, Style.RESET_ALL, "(",
              Fore.GREEN, percent_str, "%", Style.RESET_ALL, ")")
    print("-" * 30)
    if active == "РЫНОК ОТКРЫТ":
        active = "MARKET IS OPEN"
        print(Fore.GREEN + active + Style.RESET_ALL)
    elif active == "РЫНОК ЗАКРЫТ":
        active = "MARKET IS CLOSED"
        print(Fore.RED + active + Style.RESET_ALL)
    else:
        print(Fore.YELLOW, "IT WAS NOT ABLE TO DETERMINE THE STATE OF THE MARKET", Style.RESET_ALL)
    print("-" * 30)
    user_input = input("Do you want to continue? ({}/{}): ".format(Fore.GREEN + "yes" + Style.RESET_ALL,
                                                                        Fore.RED + "no" + Style.RESET_ALL))

    if user_input.lower() not in ['yes', 'y']:
        break

    driver.quit()