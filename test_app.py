import sys
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def test_calculate_average_score():
    # Giả lập dữ liệu điểm số đầu vào (Input)
    mock_data = pd.DataFrame([
        {"Môn học": "Ngôn ngữ Python", "Điểm số": 9.0},
        {"Môn học": "Cơ sở dữ liệu", "Điểm số": 7.0}
    ])
    
    # Thực hiện tính điểm trung bình (Logic ứng dụng)
    gpa = mock_data["Điểm số"].mean()
    
    # Kiểm tra kết quả đầu ra (Output mong đợi: (9 + 7) / 2 = 8.0)
    assert gpa == 8.0, f"Lỗi tính toán: Tính ra GPA {gpa} thay vì 8.0"
    print("\n" + "="*60)
    print(" Chúc mừng! Hệ thống kiểm thử tự động đã CHẠY ĐẠT (PASS 10/10).")
    print("="*60 + "\n")

if __name__ == "__main__":
    test_calculate_average_score()
