# 🎓 Ứng Dụng Quản Lý Tiến Độ Học Tập & Điểm Số (Web App Version)

## 🎯 1. Giới thiệu tổng quan về dự án
Dự án **Ứng dụng Quản lý Tiến độ Học tập & Điểm số** là một sản phẩm mã nguồn mở (Open Source) được xây dựng hoàn toàn bằng ngôn ngữ lập trình **Python** kết hợp với thư viện **Streamlit**. 

Ứng dụng được thiết kế ra nhằm giải quyết bài toán thực tế của sinh viên trong việc tự theo dõi, ghi chép nhật ký điểm số của các bài kiểm tra hằng ngày. Hệ thống tích hợp thuật toán xử lý dữ liệu thông minh để tự động tính toán điểm trung bình tích lũy (GPA) và trực quan hóa năng lực học tập của người dùng thông qua hệ thống biểu đồ tương tác thời gian thực.

---

## 🛠️ 2. Công nghệ và Thư viện sử dụng
Dự án tuân thủ tiêu chí tối ưu hóa hiệu năng, giao diện sạch đẹp và quản lý thư viện phụ thuộc chặt chẽ thông qua file `requirements.txt`:
- **Ngôn ngữ cốt lõi:** Python (Phiên bản 3.8 trở lên).
- **Giao diện người dùng (Frontend & Backend):** `Streamlit` - Thư viện mã nguồn mở giúp chuyển đổi kịch bản dữ liệu thành giao diện Web App tương tác chỉ bằng mã Python.
- **Xử lý dữ liệu:** `Pandas` - Thư viện cấu trúc dữ liệu hiệu năng cao hỗ trợ quản lý, lọc và phân tích bảng dữ liệu (Data Frame) điểm số một cách khoa học.

---

## 📥 3. Mô tả chi tiết Luồng Dữ liệu (Input / Output)

### 🔹 Đầu vào của hệ thống (Input Data)
Người dùng nhập liệu trực tiếp thông qua một Form biểu mẫu an toàn trên giao diện Web:
1. **Ngày đánh giá (`Date Input`):** Định dạng ngày hệ thống (Năm-Tháng-Ngày), tự động lấy ngày hiện tại làm mặc định.
2. **Môn học (`Select Box`):** Menu thả xuống chứa danh sách các môn học cốt lõi (Ngôn ngữ Python, Cấu trúc dữ liệu & Giải thuật, Cơ sở dữ liệu, Trí tuệ nhân tạo, Toán cao cấp, hoặc Môn học khác).
3. **Điểm số (`Number Input`):** Kiểu số thực (Float) giới hạn nghiêm ngặt trong thang điểm từ `0.0` đến `10.0`, bước tăng giảm `0.5`.
4. **Ghi chú/Đánh giá (`Text Input`):** Chuỗi ký tự tự do giúp phân loại bài kiểm tra (Ví dụ: Kiểm tra giữa kỳ, Bài tập lớn số 1, Thi cuối kỳ).

### 🔹 Đầu ra của hệ thống (Output Data)
Hệ thống tự động xử lý và kết xuất ra 3 khu vực trực quan trên màn hình:
1. **Chỉ số GPA Tích lũy (`st.metric`):** Điểm trung bình cộng của tất cả các môn học hiện tại, tự động tính toán lại sau mỗi lần người dùng thêm dữ liệu mới và hiển thị nổi bật kèm định dạng làm tròn 2 chữ số thập phân.
2. **Bảng điểm chi tiết (`st.dataframe`):** Cấu trúc bảng dữ liệu sạch (Data Table) hiển thị toàn bộ lịch sử học tập, hỗ trợ người dùng lọc dữ liệu hoặc sắp xếp thứ tự điểm số tăng/giảm dần trực tiếp trên giao diện web.
3. **Biểu đồ trực quan (`st.bar_chart`):** Biểu đồ cột (Bar Chart) tự động gom nhóm dữ liệu theo từng môn học và tính điểm trung bình riêng của môn đó, giúp sinh viên nhận biết ngay phong độ học tập của mình.

---

## 🚀 4. Hướng dẫn các bước khởi chạy dự án tại máy cục bộ (Local)

Để chạy thử nghiệm ứng dụng ngay trên máy tính cá nhân của bạn, hãy mở công cụ dòng lệnh (Terminal/CMD) lên và thực hiện chính xác 3 bước sau:

**Bước 1: Di chuyển đường dẫn Terminal vào đúng thư mục chứa dự án**
```bash
cd DUAN-main
```

**Bước 2: Tiến hành cài đặt đồng bộ các thư viện phụ thuộc bắt buộc**
```bash
pip install -r requirements.txt
```
*(Hệ thống sẽ tự động quét file cấu hình để tải chính xác phiên bản thư viện Streamlit và Pandas tương thích).*

**Bước 3: Khởi chạy Server và bật giao diện Web App**
```bash
streamlit run app.py
```
*Sau khi gõ lệnh, hệ thống sẽ tự động kích hoạt trình duyệt web của bạn và dẫn thẳng vào địa chỉ mạng nội bộ cục bộ:* `http://localhost:8501`

---

## 🧪 5. Hướng dẫn vận hành Hệ thống Kiểm thử Tự động (Automation Test)

Dự án được tích hợp sẵn một file kiểm thử độc lập `test_app.py` để xác minh độ chính xác của thuật toán tính điểm trung bình trước khi triển khai phần mềm lên hệ thống thật. 

Để thực hiện kiểm thử tự động, bạn gõ câu lệnh sau:
```bash
python test_app.py
```
- **Kịch bản kiểm thử (Test Case):** Hàm sẽ tự động tạo ra một bảng dữ liệu giả lập chứa điểm môn Python (`9.0`) và môn Cơ sở dữ liệu (`7.0`). Sau đó đối sánh kết quả tính toán đầu ra với giá trị kỳ vọng là `8.0`.
- **Kết quả thành công:** Terminal sẽ in ra thông báo đóng khung khẳng định logic cốt lõi đã **CHẠY ĐẠT (PASS 10/10)**.

---

## ☁️ 6. Hướng dẫn Triển khai lên Mạng Internet (Deploy to Cloud)

Ứng dụng hỗ trợ cơ chế đóng gói hoàn hảo để đưa lên nền tảng đám mây **Streamlit Community Cloud** miễn phí 24/7 chỉ với các bước sau:
1. Đẩy toàn bộ mã nguồn sạch của thư mục này lên một Repository công khai (Public) trên tài khoản **GitHub** cá nhân của bạn.
2. Truy cập vào trang web [share.streamlit.io](https://streamlit.io) và đăng nhập bằng tài khoản GitHub.
3. Bấm chọn nút **Create app** -> Chọn đúng tên Repository vừa đẩy lên -> Thiết lập ô `Main file path` là `app.py`.
4. Bấm nút **Deploy!** và hệ thống sẽ cấp cho bạn một đường link trang web trực tuyến công khai để chia sẻ cho mọi người.

---

## ⚖️ 7. Tuyên bố Đạo đức & An toàn Bảo mật Dữ liệu
- **Quyền riêng tư:** Ứng dụng hoạt động hoàn toàn dựa trên cơ chế bộ nhớ đệm phiên làm việc hiện tại (`st.session_state`). 
- **Cam kết an toàn:** Hệ thống hoàn toàn không lưu trữ vĩnh viễn dữ liệu học tập lên bất kỳ máy chủ cơ sở dữ liệu bên thứ ba nào, bảo mật tuyệt đối 100% bảng điểm cá nhân và không thu thập hành vi người dùng, đảm bảo các quy chuẩn đạo đức an toàn thông tin phần mềm.
