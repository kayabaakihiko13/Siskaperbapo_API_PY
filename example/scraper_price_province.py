from Siskaperbapo.api import CommuditiyEastJava

east_java = CommuditiyEastJava()
# mengetahui harga dari rentang waktu di tentukan sesuai kebutuhan
print(east_java.get_price_province("2024-03-29", "2024-04-01"))
