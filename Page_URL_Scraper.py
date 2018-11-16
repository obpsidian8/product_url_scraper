from selenium import webdriver
from bs4 import BeautifulSoup
import traceback
import re
import pprint


def Page_URL_Scraper(url_link, driver, pages):
    '''
    Takes as its input a url from certain online merchants (currently Amazon, bestbuy, Newegg and buydig) and extracts a
    list of product urls from the page.
    Function returns a list of product urls on the given page
    '''

    driver.get(url_link)

    print(
        f"\n***************************************************************************************\nGetting site name.")
    site_name_regex = re.compile(r"www.(.+?).com")
    try:
        site_name = site_name_regex.search(url_link).group(1).strip()
        print(f"Site Name: {site_name}")
    except:
        print("Cannot determine site name from regex")
        site_name = " "
        traceback.print_exc()

    print("\nChecking for additional links")
    # Will limit to 3 pages.

    all_links_to_process = [url_link]
    for page in range(2, pages + 1):

        if site_name.lower() == 'amazon':
            additional_page = f"{url_link}&page={page}"

            print("Checking page to see if same as previous page")
            driver.get(additional_page)
            current_page = driver.current_url

            previous_page_url = f"{url_link}&page={page-1}"
            driver.get(previous_page_url)
            previous_page = driver.current_url

            if current_page.lower() != previous_page.lower():
                print(f"Additional page\n {additional_page}")
                all_links_to_process.append(additional_page)
            else:
                print("Last page encountered")

        elif site_name.lower() == 'bestbuy':
            additional_page = f"{url_link}&cp={page}"
            print(f"Additional page\n {additional_page}")
            all_links_to_process.append(additional_page)

        elif site_name.lower() == 'newegg':
            additional_page = f"{url_link}&page={page}"
            print(f"Additional page\n {additional_page}")
            all_links_to_process.append(additional_page)

        elif site_name.lower() == 'buydig':
            additional_page = f"{url_link}?pn={page}"
            print(f"Additional page\n {additional_page}")
            all_links_to_process.append(additional_page)

    # After getting all links to process

    print("Commencing scraping for all links collected from all pages.")
    product_links = []
    for link in all_links_to_process:
        # perform the scraping procedure.
        driver.get(link)

        html_source = driver.page_source
        # print(html_source)

        soup = BeautifulSoup(html_source, 'html.parser')
        page_links = soup.find_all('a')

        number_of_links_found = len(page_links)
        print(f"Number of links found {number_of_links_found}")

        # tag = soup.a
        #
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(page_links)

        # print(page_links)

        print("\nGetting all links")
        print(
            "********************************************************************************************************************************************************************************")
        print(
            "********************************************************************************************************************************************************************************")

        url_regex = re.compile(r"//(.+)")

        for page in page_links:
            try:
                href_link = page['href']
            except:
                href_link = None
                # traceback.print_exc()

            if href_link is not None:
                if "product/product" in href_link.lower():
                    print("Newegg Product Links:")
                    try:
                        url = url_regex.search(href_link).group(1).strip()
                        if "https://" not in url:
                            url = f"https://{url}"
                        print(url)
                        product_links.append(url)
                    except:
                        pass

                elif "/site/" in href_link and "https:" not in href_link.lower() and "skuid" in href_link.lower():
                    print("Bestbuy Product Links:")
                    try:
                        url = f"https://www.bestbuy.com{href_link}"
                        print(url)
                        product_links.append(url)
                    except:
                        print("\n")

                elif "https://www.amazon.com" in href_link and "/dp" in href_link.lower():
                    print("Amazon Product Links")
                    try:
                        print(href_link)
                        product_links.append(href_link)
                    except:
                        print(href_link)

                elif "buydig.com/shop/product" in href_link:
                    print("Buydig Product Links")
                    try:
                        print(href_link)
                        product_links.append(href_link)
                    except:
                        print(href_link)

                elif "https://" in href_link and site_name in href_link.lower():
                    print("Other Links")
                    print(href_link)
                    pass
            else:
                # print("No href in \"a\" tag")
                pass

    # number_of_cleaned_up_links = (len(product_links))
    number_of_cleaned_up_links = (len(list(set(product_links))))

    print(f"Cleaned up links: {number_of_cleaned_up_links}")

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(list(set(product_links)))

    return list(set(product_links))


def SetupChrome():

    """Sets up a new data directory and profile for chrome separate from your regular browser profile."""

    path_to_dir = "C:/Chromeprofiles"
    profile_folder = "Ultron"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--user-data-dir=' + path_to_dir)
    chrome_options.add_argument('--profile-directory=' + profile_folder)

    print("\nSetting Chrome Options.")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.set_window_size(1200, 2270)
    return driver


def test_run():
    driver = SetupChrome()

    #Example urls that can be used with this function.

    # url_link = "https://www.bestbuy.com/site/tv-home-theater/tv-sale-page/pcmcat359600050007.c?id=pcmcat359600050007"
    # url_link = "https://www.amazon.com/s/ref=nb_sb_ss_c_1_9?url=search-alias%3Daps&field-keywords=spiderman+ps4&sprefix=spiderman%2Caps%2C154&crid=1MU5I52309VMS"
    # url_link = "https://www.amazon.com/gp/offer-listing/B00ZQC73O8/"
    # url_link = "https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&N=8000&IsNodeId=1&Description=PPSSQCGZHBPXSO&bop=And&PageSize=60&order=BESTMATCH"
    # url_link = "https://www.amazon.com/s/ref=nb_sb_ss_i_4_13?url=search-alias%3Daps&field-keywords=android+phone&sprefix=android+phone%2Caps%2C182&crid=25S96U1WRL5V8&rh=i%3Aaps%2Ck%3Aandroid+phone"
    # url_link = "https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&id=pcat17071&iht=y&keys=keys&ks=960&list=n&qp=category_facet%3Dpcmcat311200050005&sc=Global&st=android%20phone&type=page&usc=All%20Categories"
    # url_link = "https://www.buydig.com/shop/list/category/2014/Digital-Cameras"
    #url_link = "https://www.buydig.com/shop/list/category/1082/Tablet%20PCs"

    # Email link sent as input tp the function
    url_link = "https://promotions.newegg.com/NEemail/Oct-0-2018/RedTagSale_7du5un_09/index-landing.html?"

    # A category of items can span several pages on a site. We can cycle through as many pages as we define.
    number_of_pages_to_check = 3

    Page_URL_Scraper(url_link, driver, number_of_pages_to_check)

if __name__ == '__main__':
    test_run()

