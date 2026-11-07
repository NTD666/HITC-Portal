# 🎓 HITC Portal - Cổng Thông Tin & Quản Lý Tiến Độ Học Tập Sinh Viên

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Altair](https://img.shields.io/badge/Altair-4B8BBE?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Trạng_thái-Hoàn_thiện-success?style=for-the-badge)
![License](https://img.shields.io/badge/Giấy_phép-MIT-blue?style=for-the-badge)

<p align="center">
  <b>Hệ thống Web App theo dõi tiến độ, nhật ký điểm số và phân tích năng lực học tập dành cho sinh viên Trường Cao đẳng Công thương TP.HCM (HITC)</b>
</p>

[Tính Năng](#-tính-năng-nổi-bật) • [Công Nghệ](#-công-nghệ-sử-dụng) • [Cài Đặt & Chạy](#-hướng-dẫn-cài-đặt--khởi-chạy-cục-bộ) • [Kiểm Thử](#-hệ-thống-kiểm-thử-tự-động) • [Triển Khai Server](#-hướng-dẫn-triển-khai-lên-server-cloud) • [Tác Giả](#-tác-giả--bản-quyền)

</div>

---

## 📖 1. Giới thiệu tổng quan

**HITC Portal** là ứng dụng Web quản lý học tập thông minh được xây dựng bằng ngôn ngữ **Python** kết hợp với nền tảng **Streamlit**. 

Dự án ra đời nhằm giải quyết nhu cầu thực tế của sinh viên trong việc:
* Ghi chép nhật ký điểm số các học phần theo từng học kỳ.
* Tự động tính toán điểm trung bình tích lũy (GPA) và phân loại học lực tức thì.
* Trực quan hóa dữ liệu điểm qua biểu đồ phân tích năng lực học tập đa chiều.
* Trải nghiệm giao diện thân thiện, hiện đại mang đậm bản sắc thương hiệu của **Trường Cao đẳng Công thương TP.HCM (HITC)**.

---

## ✨ 2. Tính năng nổi bật

### 🔑 Xác thực & Thông tin Sinh viên
- Đăng nhập xác thực thông tin sinh viên với **Họ tên**, **Mã số sinh viên (MSSV)** và **Lớp sinh hoạt**.
- Bảng thông tin sinh viên (Profile Card) trực quan ngay tại Sidebar kèm chức năng Đăng xuất an toàn.
- Quản lý phiên làm việc thông qua `st.session_state`.

### 🎨 Bộ nhận diện HITC & Chế độ Sáng / Tối (Dark Mode)
- **Tùy biến giao diện linh hoạt:** Cho phép người dùng chuyển đổi tức thì giữa **Giao diện Sáng (Light)** và **Giao diện Tối (Dark Mode)** ngay tại thanh công cụ.
- **Phong cách thương hiệu đặc trưng:** Sử dụng bảng màu chuẩn của HITC với tone **Đỏ đô (#A31D1D)** kết hợp **Vàng ánh kim (#E8B86D)**, bo góc mềm mại, đổ bóng hiện đại.

### 📥 Quản lý & Cập nhật Điểm số Học phần
- Lựa chọn ngày đánh giá (tự động lấy ngày hiện tại).
- Phân loại theo **Học kỳ đào tạo** (từ Học kỳ I đến Học kỳ VI).
- Danh mục môn học chuẩn theo **khung chương trình đào tạo Khoa CNTT - HITC**:
  - *Nhóm Đại cương:* Triết học Mác - Lênin, Pháp luật đại cương, Tin học đại cương, Tiếng Anh giao tiếp...
  - *Nhóm Cơ sở ngành:* Toán ứng dụng CNTT, Kiến trúc máy tính & Hệ điều hành, Mạng máy tính, Cơ sở dữ liệu (SQL Server), Cấu trúc dữ liệu và Giải thuật...
  - *Nhóm Chuyên ngành:* Lập trình Python, OOP, Thiết kế Web (HTML/CSS/JS), Lập trình Di động, Kiểm thử phần mềm, Đồ án tốt nghiệp...
- Phân loại trọng số điểm đánh giá:
  - Điểm chuyên cần (10%)
  - Điểm kiểm tra giữa kỳ (30%)
  - Điểm thi kết thúc học phần (60%)

### 📊 Thống kê & Đánh giá Năng lực Tự động
- **Tính toán GPA tự động:** Cập nhật điểm trung bình cộng tích lũy theo thời gian thực (làm tròn 2 chữ số thập phân).
- **Phân loại học lực theo chuẩn:**
  - `GPA >= 8.5`: Xuất sắc 🏆
  - `GPA >= 8.0`: Giỏi 🥇
  - `GPA >= 6.5`: Khá 🥈
  - `GPA >= 5.0`: Trung bình 🥉
  - `GPA < 5.0`: Yếu
- **Bảng điểm chi tiết:** Trình bày dạng bảng (`st.dataframe`) hỗ trợ tìm kiếm, lọc và sắp xếp trực tiếp trên web.

### 📈 Biểu đồ trực quan tương tác
- Tích hợp biểu đồ phân tích năng lực môn học bằng thư viện **Altair**.
- Thiết kế nhãn trục ngang cố định (`labelAngle=0`) giúp sinh viên dễ dàng quan sát điểm số từng môn mà không bị rối mắt.
- Hỗ trợ tooltip xem chi tiết điểm số khi rê chuột.

### 🤖 Trợ lý AI Cố vấn Học tập Đa tác nhân (Powered by CrewAI)
- **Tích hợp phi đội Multi-Agent tự hành:** 
  - **Chuyên viên Phân tích Học lực HITC:** Đánh giá điểm mạnh, môn yếu và cảnh báo rủi ro học vụ.
  - **Cố vấn Lộ trình & Hướng nghiệp CNTT:** Đưa ra kế hoạch hành động 3-5 bước, gợi ý phương pháp tự học và định hướng chuyên ngành (Web, Mobile, Network, Security, AI/Data).
- **Hỗ trợ linh hoạt mô hình:** OpenAI (GPT-4o-mini, GPT-4o) và Google Gemini (Gemini 1.5 Flash/Pro, Gemini 2.0).

---

## 🛠️ 3. Công nghệ sử dụng

| Công nghệ / Thư viện | Phiên bản | Vai trò trong hệ thống |
| :--- | :--- | :--- |
| **Python** | 3.8+ | Ngôn ngữ lập trình cốt lõi |
| **Streamlit** | Latest | Framework xây dựng giao diện Web tương tác cao |
| **Pandas** | Latest | Xử lý cấu trúc bảng dữ liệu điểm (DataFrame), tổng hợp số liệu |
| **Altair** | Latest | Xây dựng đồ thị trực quan hóa dữ liệu tương tác chuyên sâu |
| **CrewAI** | Latest | Nền tảng điều phối Multi-Agent AI phân tích và tư vấn học tập |

---

## 📂 4. Cấu trúc thư mục dự án

```text
DUAN-main/
│
├── .gitignore              # Danh sách các file/thư mục bỏ qua khi đẩy lên Git
├── README.md               # Tài liệu hướng dẫn sử dụng và giới thiệu dự án
├── requirements.txt        # Danh mục thư viện phụ thuộc bắt buộc
├── chay_ung_dung.bat       # Phím tắt 1-click tự động chạy trên Windows máy trường
├── app.py                  # Mã nguồn chính của ứng dụng HITC Portal
├── grade_calculator.py     # Module chuẩn hóa và tính điểm trọng số học phần (10%-30%-60%)
├── ai_advisor.py           # Module điều phối phi đội AI Agents (CrewAI)
└── test_app.py             # Kịch bản kiểm thử tự động thuật toán tính điểm
```

---

## 🚀 5. Hướng dẫn Cài đặt & Khởi chạy cục bộ

Để chạy ứng dụng trên máy tính của bạn, hãy thực hiện tuần tự các bước sau:

### Bước 1: Sao chép (Clone) hoặc Tải dự án
```bash
git clone https://github.com/NTD666/HITC-Portal.git
cd HITC-Portal
```
*(Nếu bạn đã tải sẵn thư mục `DUAN-main`, chỉ cần mở Terminal/PowerShell và trỏ vào thư mục này).*

### Bước 2: Tạo môi trường ảo (Khuyến nghị)
```bash
# Trên Windows
python -m venv venv
.\venv\Scripts\activate

# Trên macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Bước 3: Cài đặt các thư viện phụ thuộc
```bash
pip install -r requirements.txt
```

### Bước 4: Khởi chạy ứng dụng Web
```bash
streamlit run app.py
```

Sau khi khởi chạy thành công, trình duyệt web sẽ tự động mở trang:
```text
Local URL: http://localhost:8501
```

---

## 🧪 6. Hệ thống Kiểm thử Tự động (Automated Testing)

Dự án đi kèm bộ kiểm thử độc lập trong file `test_app.py` nhằm xác minh tính chính xác của thuật toán tính điểm trung bình trước khi bàn giao hoặc đưa lên máy chủ.

Chạy kiểm thử bằng lệnh:
```bash
python test_app.py
```

**Kịch bản kiểm thử (Test Case):**
- Giả lập bảng dữ liệu với điểm môn *Ngôn ngữ Python (9.0)* và môn *Cơ sở dữ liệu (7.0)*.
- Thuật toán xử lý tính trung bình: `(9.0 + 7.0) / 2 = 8.0`.
- Đối sánh qua `assert`. Khi đạt chuẩn, hệ thống xuất thông báo xác nhận:
```text
============================================================
 Chúc mừng! Hệ thống kiểm thử tự động đã CHẠY ĐẠT (PASS 10/10).
============================================================
```

---

## ☁️ 7. Hướng dẫn Triển khai lên Server (Cloud)

### Cách 1: Triển khai miễn phí qua Streamlit Community Cloud (Khuyên dùng)
1. Đẩy mã nguồn lên tài khoản GitHub của bạn tại repository: `https://github.com/NTD666/HITC-Portal`.
2. Truy cập [share.streamlit.io](https://share.streamlit.io) và đăng nhập bằng tài khoản GitHub.
3. Nhấn **"Create app"** và điền cấu hình:
   - **Repository:** `NTD666/HITC-Portal`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL:** Tùy chọn tên miền (ví dụ: `hitc-portal.streamlit.app`).
4. Nhấn **"Deploy!"**. Hệ thống sẽ tự động cài thư viện và tạo trang web trực tuyến hoạt động 24/7.

### Cách 2: Triển khai qua Render / Railway / Cloud VPS
Cấu hình lệnh khởi chạy (Start Command) với cổng động của server:
```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

---

## 🔒 8. Cam kết Quyền riêng tư & Bảo mật

- **Không lưu trữ cơ sở dữ liệu ngoài:** Toàn bộ dữ liệu điểm số và thông tin cá nhân của phiên làm việc chỉ tồn tại trong bộ nhớ đệm `st.session_state` của trình duyệt.
- **An toàn tuyệt đối:** Dữ liệu sẽ được làm mới khi kết thúc phiên hoặc đăng xuất, đảm bảo tính riêng tư và bảo mật thông tin cá nhân của sinh viên.

---

## 👨‍💻 9. Tác giả & Bản quyền

- **Tác giả:** Nguyễn Tấn Dũng
- **Đơn vị:** Khoa Công nghệ Thông tin - Trường Cao đẳng Công thương TP.HCM (HITC)
- **Cơ sở đào tạo:** 20 Tăng Nhơn Phú, Phường Phước Long B, TP. Thủ Đức, TP. Hồ Chí Minh
- **Giấy phép:** [MIT License](LICENSE)

<div align="center">
  <sub>© 2026 HITC Portal. Phát triển phục vụ cộng đồng sinh viên Cao đẳng Công thương TP.HCM.</sub>
</div>
