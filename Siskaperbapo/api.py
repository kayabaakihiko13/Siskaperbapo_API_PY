from bs4 import BeautifulSoup
from selenium import webdriver


class CommuditiyEastJava(object):
    def __init__(self) -> None:
        self.url_harga = "https://siskaperbapo.jatimprov.go.id/harga/tabel"
        self.driver = webdriver.Chrome()
        self.excuteJS = self.driver.execute_script

    def __get_options(self):
        # initial WebDriver
        self.driver.get(self.url_harga)
        # parsing webpage using bs4
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        if city_selected := soup.find("select", {"id": "kabkota"}):
            city_options = city_selected.find_all("option")
            options_list = [
                option.get_text(strip=True)
                for option in city_options
                if option.get_text(strip=True) != "Provinsi Jawa Timur"
            ]
        self.driver.quit()
        return options_list

    def see_options(self):
        return self.__get_options()


east_java = CommuditiyEastJava()
city_list = east_java.see_options()
if city_list:
    print("List of city names:")
    print(city_list)
else:
    print("Failed to retrieve city list.")
