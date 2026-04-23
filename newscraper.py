import time
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By


BASE_URL = "https://www.bikedekho.com/electric-scooters"


# 🔥 Extract correct price (skip EMI)
def extract_price(soup):
    for tag in soup.find_all(True):
        txt = tag.get_text(strip=True)

        if txt.startswith("₹") and "emi" not in txt.lower():
            return txt
    return None


# 🔥 Extract ALL specs from ALL tables
def extract_specs(soup):
    specs = {}

    for table in soup.find_all("table"):
        for row in table.find_all("tr"):
            cols = row.find_all("td")

            if len(cols) == 2:
                key = cols[0].get_text(strip=True).lower()
                value = cols[1].get_text(strip=True)
                specs[key] = value

    return specs


# 🔥 Extract rating + reviews
def extract_rating_reviews(soup):
    rating = None
    review_count = None

    try:
        rating_tag = soup.find("span", string=lambda x: x and "." in x)
        if rating_tag:
            rating = rating_tag.text.strip()

        review_tag = soup.find(string=lambda x: x and "review" in x.lower())
        if review_tag:
            review_count = review_tag.strip()
    except:
        pass

    return rating, review_count


# 🔥 Get ALL scooter links (pagination)
def get_all_links():
    driver = webdriver.Chrome()

    all_links = set()
    page = 1

    while True:
        url = f"{BASE_URL}?pageno={page}"
        print(f"\nLoading Page {page}")

        driver.get(url)
        time.sleep(4)

        products = driver.find_elements(By.XPATH, "//li[.//h3]")

        if not products:
            break

        new_links = set()

        for p in products:
            try:
                link = p.find_element(By.TAG_NAME, "a").get_attribute("href")
                if link:
                    new_links.add(link)
            except:
                continue

        # stop when no new links
        if not new_links or new_links.issubset(all_links):
            print("🛑 No new links → stopping")
            break

        all_links.update(new_links)
        print(f"Total collected: {len(all_links)}")

        page += 1

    driver.quit()

    print(f"\n✅ Total scooter links: {len(all_links)}")
    return list(all_links)


# 🔥 Scrape all details
def scrape_details(links):
    all_data = []
    headers = {"User-Agent": "Mozilla/5.0"}

    def get_spec(specs, *keys):
        for k in specs:
            for target in keys:
                if target in k:
                    return specs[k]
        return None

    for i, link in enumerate(links):
        print(f"Scraping {i+1}/{len(links)}")

        try:
            # 🔹 MAIN PAGE
            res = requests.get(link, headers=headers)
            soup = BeautifulSoup(res.text, "lxml")

            name_tag = soup.find("h1")
            name = name_tag.text.strip() if name_tag else None
            brand = name.split()[0] if name else None

            price = extract_price(soup)

            rating, review_count = extract_rating_reviews(soup)

            # 🔥 SPEC PAGE (CRITICAL FIX)
            spec_url = link.rstrip("/") + "/specifications"
            res2 = requests.get(spec_url, headers=headers)
            soup2 = BeautifulSoup(res2.text, "lxml")

            specs = {}

            for table in soup2.find_all("table"):
                for row in table.find_all("tr"):
                    cols = row.find_all("td")
                    if len(cols) == 2:
                        key = cols[0].get_text(strip=True).lower()
                        value = cols[1].get_text(strip=True)
                        specs[key] = value

            # 🔥 FULL TEXT (for fallback)
            full_text = soup2.get_text().lower()

            data = {
                "name": name,
                "brand": brand,
                "price": price,

                # 🔥 NUMERIC / SPECS
                "charging_time_hr": get_spec(specs, "charging time"),
                "motor_power_kw": get_spec(specs, "motor power", "max power"),
                "weight_kg": get_spec(specs, "kerb weight", "weight"),

                # 🔥 FIXED: underseat storage VALUE (not yes/no)
                "underseat_storage": get_spec(specs, "underseat storage", "boot space", "storage"),

                "usb_charging_port": get_spec(specs, "usb charging"),
                "anti_theft_alarm": get_spec(specs, "anti theft"),

                "braking_type": get_spec(specs, "braking type"),
                "load_carrying_capacity": get_spec(specs, "load carrying capacity"),

                "top_speed_kmph": get_spec(specs, "top speed"),

                "battery_warranty": get_spec(specs, "battery warranty"),

                "rating": rating,
                "review_count": review_count,

                "status": "available",
                "link": link
            }

            all_data.append(data)

        except Exception as e:
            print("❌ Error:", e)

    return all_data


def main():
    links = get_all_links()

    data = scrape_details(links)

    df = pd.DataFrame(data)

    # save file
    filename = "electric_scooters.csv"
    df.to_csv(filename, index=False)

    print("\n📁 CSV saved at:", os.path.abspath(filename))


if __name__ == "__main__":
    main()