# 🧪 Bộ Kiểm Thử Tự Động của HITC Portal (Test Suite)

Thư mục `tests/` chứa toàn bộ các kịch bản kiểm thử tự động (Unit Tests & Integration Tests) được thiết kế theo chuẩn công nghiệp bằng framework **Pytest**, nhằm đảm bảo tính toàn vẹn, chính xác và không bị lỗi hồi quy (regression) cho hệ thống **Cổng Thông Tin Sinh Viên HITC Portal**.

---

## 📋 Danh Mục Các Nhóm Kiểm Thử

| Tệp kiểm thử | Đánh giá & Xác thực gì | Không đánh giá |
| :--- | :--- | :--- |
| `test_project_structure.py` | Kiểm tra sự tồn tại của các tệp cốt lõi, tài liệu hướng dẫn, file thực thi và phụ thuộc thư viện | Nội dung chi tiết giao diện web |
| `test_grade_calculator.py` | Thuật toán tính điểm trọng số học phần (10% - 30% - 60%), GPA tích lũy, các ngưỡng phân loại học lực và trường hợp biên (bảng trống, 1 đầu điểm) | Giao diện đồ họa Streamlit |
| `test_ai_advisor.py` | Kiểm thử sinh Prompt phân tích, Chế độ Cố vấn Tự động Chuẩn HITC (không cần API Key) và cơ chế Fallback an toàn | Tốc độ mạng internet bên ngoài |

---

## 🚀 Hướng Dẫn Chạy Kiểm Thử Tại Thư Mục Gốc Dự Án

### Cách 1: Sử dụng Pytest (Khuyến nghị chuẩn công nghiệp)
```bash
# Chạy toàn bộ test suite và hiển thị chi tiết:
python -m pytest tests/ -v

# Chạy tóm tắt ngắn gọn:
python -m pytest tests/ -q
```

### Cách 2: Chạy trực tiếp qua Python thuần
```bash
# Chạy script kiểm thử tổng hợp:
python test_app.py

# Hoặc chạy từng module test riêng lẻ:
python -m unittest discover tests/
```

---

## 📐 Nguyên Tắc & Quy Chuẩn Chất Lượng Kiểm Thử

1. **Tính chính xác về học vụ:** Thuật toán tính điểm phải tuân thủ nghiêm ngặt quy chế đào tạo theo hệ thống tín chỉ của Trường Cao đẳng Công thương TP.HCM (HITC).
2. **Khả năng tự phục hồi (Fault Tolerance):** Khi sinh viên không cấu hình API Key, hệ thống kiểm thử phải xác nhận rằng bộ máy Cố vấn Tự động nội bộ vẫn hoạt động hoàn hảo và trả về đầy đủ 4 phần tư vấn trọng tâm.
3. **Bảo toàn tính hồi quy:** Mọi tính năng mới được bổ sung phải vượt qua toàn bộ các test case có sẵn với tỷ lệ đạt chuẩn **100% (PASS)**.
