# Đọc dữ liệu từ file và lưu vào dictionary
exchange_rates = {}
with open("switch.txt", "r") as file:
    
    for line in file:
        parts = line.strip().split("\t")
        currency = parts[0]
        # Thay thế dấu phẩy bằng dấu chấm và chuyển đổi thành float
        rate = float(parts[1].replace(",", "."))
        exchange_rates[currency] = rate

# Hàm chuyển đổi tiền tệ sang USD
def convert_to_usd(currency, amount):
    if currency in exchange_rates:
        rate = exchange_rates[currency]
        return amount * rate
    else:
        return "Loại tiền không hợp lệ"

# Nhập loại tiền và số tiền
currency = input("Nhập loại tiền: ").upper()
amount = float(input("Nhập số tiền: "))

# Tính và in ra kết quả
usd_amount = convert_to_usd(currency, amount)
print(f"Số tiền {amount} {currency} tương đương {usd_amount} USD")
