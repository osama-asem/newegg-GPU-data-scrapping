# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = "https://www.newegg.com/global/uk-en/p/pl?d=graphics+card&page=1"
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")

# grab total page container
container_num = page_soup.findAll("span", {"class": "list-tool-pagination-text"})
page_number = int(container_num[0].strong.text.replace("1/", ""))
# next page to load
next_page = 1
file_name = "gpu_data.tsv"
f = open(file_name, "w")
headers = "brand\tproduct_name\tprice \n"
f.write(headers)

# grab each item

while next_page <= 5:
    containers = page_soup.findAll("div", {"class": "item-container"})
    next_page += 1

    for container in containers:
        product_name = container.findAll("a", {"class", "item-title"})[0].text.replace(",", "|")
        if container.div.a.img is None:
            brand = product_name.split()[0]
        else:
            brand = container.div.a.img["title"]
        price = container.findAll("li", {"class", "price-current"})[0].strong.text
        f.write(brand + "\t" + product_name + "\t" + price + "$\n")

    my_url = "https://www.newegg.com/global/uk-en/p/pl?d=graphics+card&page=" + str(next_page)
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")

f.close()
