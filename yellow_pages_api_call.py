import requests
from datetime import datetime
from bs4 import BeautifulSoup

class Scrape:
    def __init__(self, root_website):
        self.soup = ""
        self.html_file = ""
        self.root_website = root_website

    def get_website_html(self):
        self.html_file = requests.get(self.root_website).text
        self.soup = BeautifulSoup(self.html_file, "lxml")
        return self.soup

    def scrape_web(self, write_in_file=False):
        arr = []
        self.soup = self.get_website_html()
        restaurants = self.soup.find_all("div", class_="result")[1:]
        now = str(datetime.now()).replace(" ", "--").split(".")[0].replace(":", "-")

        with open(f"Yellow-pages/{now}.txt", "w") as f:
            for restaurant in restaurants:
                name = restaurant.find("a", class_="business-name")
                status = restaurant.find("div", class_="open-status")
                if (name != None) and (status != None):
                    categories = restaurant.find("div", class_="categories").find_all("a")
                    num = restaurant.find("h2", class_="n").text
                    ph_num = restaurant.find("div", class_="phone").text
                    info_website = name["href"]
                    website = restaurant.find("div", class_="links").a["href"]
                    address = restaurant.find("div", class_="adr").text

                    if write_in_file:
                        f.write(f"{num}\n")
                        f.write(f"Name: {name.text}\n")
                        f.write(f"Phone number: {ph_num}\n")
                        f.write(f"Categories: {[category.text for category in categories]}\n")
                        f.write(f"Status: {status.text}\n")
                        f.write(f"Address: {address}\n")
                        f.write(f"Restaurant Website: {website}\n")
                        f.write(f"More info: https://www.yellowpages.com{info_website}\n")
                        f.write("-------------------------------------------------\n")
                        f.write("\n")
                    
                    dict_ = {"Name": name.text,
                             "Phone-number": ph_num,
                             "Categories": [category.text for category in categories],
                             "Status": status.text,
                             "Address": address,
                             "Restaurant-Website": website,
                             "More-info": f"https://www.yellowpages.com{info_website}"}
                    
                    arr.append(dict_)

        return arr


if __name__ == "__main__":
    root_website = "https://www.yellowpages.com/las-vegas-nv/restaurants"
    scrape = Scrape(root_website)
    arr = scrape.scrape_web(write_in_file=False)
    print(arr)