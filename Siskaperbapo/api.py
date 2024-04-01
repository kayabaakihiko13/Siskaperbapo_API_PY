from datetime import datetime
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


class CommuditiyEastJava(object):
    def __init__(self) -> None:
        self.url_harga = "https://siskaperbapo.jatimprov.go.id/"
        self.driver = webdriver.Chrome()
        self.excuteJS = self.driver.execute_script
        # initial webDriver
        self.driver.get(self.url_harga)
        self.html = self.driver.page_source
        self.soup = BeautifulSoup(self.html, "html.parser")

    def __get_options(self) -> list | None:
        # parsing webpage using bs4
        if city_selected := self.soup.find("select", {"id": "kabkota"}):
            city_options = city_selected.find_all("option")
            options_list = [option.get_text(strip=True) for option in city_options]
            return options_list
        return None

    def see_options(self):
        return self.__get_options()

    def __get_commodity_list(self):
        # parsing webpage using bs4
        select_element = self.soup.find("select", {"id": "komoditas"})
        options = select_element.find_all("option")
        commodities_list = []
        for option in options:
            commodities_list.append(option.text.strip())

        return commodities_list

    def see_commodity_list(self):
        return self.__get_commodity_list()

    def get_price_cities(self, komoditas_text: str, tanggal: str):
        try:
            # Set tanggal menggunakan JavaScript karena elemen bersifat readonly
            self.driver.execute_script(
                "arguments[0].value = arguments[1];",
                self.driver.find_element(By.ID, "tanggal"),
                tanggal,
            )

            # Pilih komoditas
            select_element = self.driver.find_element(By.ID, "komoditas")
            select_element.click()
            option_element = self.driver.find_element(
                By.XPATH, f"//option[text()='{komoditas_text}']"
            )
            option_element.click()

            # Klik refresh
            refresh_button = self.driver.find_element(By.ID, "refresh")
            refresh_button.click()

            # Tunggu beberapa saat untuk proses refresh
            time.sleep(2)

            # Dapatkan harga kota setelah refresh
            table_element = self.driver.find_element(By.ID, "datatbl")
            rows = table_element.find_elements(By.TAG_NAME, "tr")
            data = []
            for row in rows[1:]:  # Mulai dari indeks 1 untuk melewati baris header
                columns = row.find_elements(By.TAG_NAME, "td")
                if len(columns) == 2:
                    kabupaten_kota = columns[0].text.strip()
                    harga_mean = columns[1].text.strip()
                    data.append(
                        {
                            "Tanggal": tanggal,
                            "Kabupaten/Kota": kabupaten_kota,
                            "Harga Mean": harga_mean,
                        }
                    )
            return data
        finally:
            self.driver.quit()

    def get_price_province(self, tanggal: str):
        try:
            table_element = self.driver.find_element(
                By.CSS_SELECTOR, "div#harga table.table-bordered"
            )
            tanggal_parsed = datetime.strptime(tanggal, "%Y-%m-%d")
            data = []
            rows = table_element.find_elements(By.TAG_NAME, "tr")[1:]
            for row in rows:
                columns = row.find_elements(By.TAG_NAME, "td")
                if len(columns) == 4:
                    no = columns[0].text.strip()
                    nama_bahan_pokok = columns[1].text.strip()
                    satuan = columns[2].text.strip()
                    harga = columns[3].text.strip().split()[0]
                    data.append(
                        {
                            "No": no,
                            "Nama Bahan Pokok": nama_bahan_pokok,
                            "Satuan": satuan,
                            "Harga": harga,
                            "Tanggal": tanggal_parsed,
                        }
                    )
            return data
        except Exception as e:
            print("An error occurred:", e)
            return None
        finally:
            self.driver.quit()


if __name__ == "__main__":
    east_java = CommuditiyEastJava()
    price_cities = east_java.get_price_cities("Beras Medium / kg", "2024-04-01")
    print(price_cities)
    # options_list = east_java.see_options()
    # commodity_list = east_java.see_commodity_list()
    # print("Options:", options_list)
    # print("Commodity:", commodity_list)

    # Example usage of get_data method
    # data = east_java.get_price_province("2024-04-01")
    # print("Data:", data)
