import streamlit as st
import io

# Hàm đọc dữ liệu từ file và lưu vào dictionary
def read_exchange_rates(file):
    exchange_rates = {}
    currencies = []
    for line in file:
        parts = line.decode("utf-8").strip().split("\t")
        currency = parts[0]
        # Thay thế dấu phẩy bằng dấu chấm và chuyển đổi thành float
        rate = float(parts[1].replace(",", "."))
        exchange_rates[currency] = rate
        currencies.append(currency)  # Lưu loại tiền vào danh sách
    return exchange_rates, currencies
# def read_exchange_rates(file):
#     # Đọc dữ liệu từ file Excel
#     df = pd.read_excel(file, engine='openpyxl')  # Đảm bảo cài đặt openpyxl để đọc file Excel

#     # Khởi tạo dictionary và danh sách các loại tiền tệ
#     exchange_rates = {}
#     currencies = []

#     # Duyệt qua từng hàng trong DataFrame
#     for index, row in df.iterrows():
#         currency = row[0]  # Cột đầu tiên chứa mã tiền tệ
#         rate = float(str(row[1]).replace(",", "."))  # Cột thứ hai chứa tỷ giá, thay dấu phẩy bằng dấu chấm nếu có
#         exchange_rates[currency] = rate
#         currencies.append(currency)  # Lưu loại tiền vào danh sách

#     return exchange_rates, currencies
# Hàm chuyển đổi tiền tệ sang USD
def convert_to_usd(currency, amount, exchange_rates):
    currency = currency.upper()
    if currency in exchange_rates:
        rate = exchange_rates[currency]
        usd_amount = amount * rate
        return round(usd_amount, 2)
    else:
        return "Loại tiền không hợp lệ"

# Tiêu đề ứng dụng
st.title('Ứng Dụng Đổi Tiền Tệ Sang USD')

# Người dùng tải lên file
uploaded_file = st.file_uploader("Tải lên file tỷ giá (định dạng .xlsx)", type=["xlsx"])

# Nếu có file tải lên
if uploaded_file is not None:
    # Đọc dữ liệu từ file tải lên
    exchange_rates, currencies = read_exchange_rates(uploaded_file)

    # Tạo thanh tìm kiếm để chọn loại tiền
    currency = st.selectbox('Chọn loại tiền (hoặc nhập loại tiền):', currencies)

    # Sử dụng form để xử lý submit khi nhấn Enter
    with st.form(key='conversion_form'):
        # Ô nhập số tiền (dùng text_input để có thể xóa nội dung khi nhấp vào)
        amount_input = st.text_input('Nhập số tiền:', value='', placeholder='Nhập số tiền...')

        # Button để đổi sang USD
        submit_button = st.form_submit_button(label='Đổi sang USD')

        if submit_button or amount_input:  # Nếu nhấn nút hoặc nhấn Enter trong ô nhập
            if currency and amount_input:
                try:
                    # Thay thế dấu phẩy (,) bằng dấu chấm (.) trước khi chuyển đổi
                    cleaned_amount = amount_input.replace(',', '.')
                    amount = float(cleaned_amount)
                    result = convert_to_usd(currency, amount, exchange_rates)
                    if isinstance(result, float):
                        # Tô đỏ đen tối màu, in đậm và phóng to kết quả chỉ cho số tiền USD
                        st.markdown(f"""
                        Số tiền {amount} {currency} tương đương 
                        <span style="font-size: 24px; color: #8B0000; font-weight: bold;">
                            {result} 
                        </span>.
                        USD
                        """, unsafe_allow_html=True)
                    else:
                        st.write(result)  # Nếu loại tiền không hợp lệ
                except ValueError:
                    st.write("Vui lòng nhập số tiền hợp lệ!")
            else:
                st.write("Vui lòng nhập đầy đủ thông tin!")
else:
    st.write("Vui lòng tải lên file tỷ giá để bắt đầu.")
