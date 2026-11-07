import sys
import pandas as pd
from grade_calculator import calculate_subject_grades, GRADE_WEIGHTS, get_academic_rank

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def test_calculate_average_score():
    """Kiểm tra tính điểm môn học theo đúng trọng số 10% - 30% - 60% và tính GPA tích lũy."""
    mock_data = pd.DataFrame([
        {"Môn học": "Ngôn ngữ Python", "Điểm số": 10.0, "Loại điểm": "Điểm chuyên cần (10%)"},
        {"Môn học": "Ngôn ngữ Python", "Điểm số": 8.0, "Loại điểm": "Điểm kiểm tra giữa kỳ (30%)"},
        {"Môn học": "Ngôn ngữ Python", "Điểm số": 6.0, "Loại điểm": "Điểm thi kết thúc học phần (60%)"},
        {"Môn học": "Cơ sở dữ liệu", "Điểm số": 9.0, "Loại điểm": "Điểm thi kết thúc học phần (60%)"}
    ])
    
    subject_summary = calculate_subject_grades(mock_data)
    python_score = subject_summary.loc[subject_summary["Môn học"] == "Ngôn ngữ Python", "Điểm tổng kết"].values[0]
    assert python_score == 7.0, f"Lỗi tính điểm môn Python: Tính ra {python_score} thay vì 7.0"
    
    db_score = subject_summary.loc[subject_summary["Môn học"] == "Cơ sở dữ liệu", "Điểm tổng kết"].values[0]
    assert db_score == 9.0, f"Lỗi tính điểm môn CSDL: Tính ra {db_score} thay vì 9.0"
    
    gpa = subject_summary["Điểm tổng kết"].mean()
    assert gpa == 8.0, f"Lỗi tính GPA: Tính ra GPA {gpa} thay vì 8.0"
    assert get_academic_rank(gpa) == "Giỏi 🥇"
    print(" Test tính điểm trọng số HITC: ĐẠT (PASS 10/10).")

def test_ai_advisor_prompt():
    from ai_advisor import build_academic_analysis_prompt
    mock_df = pd.DataFrame([
        {"Ngày nhập": "2026-11-07", "Học kỳ": "Học kỳ I", "Môn học": "Ngôn ngữ Python", "Điểm số": 9.0, "Loại điểm": "Điểm thi kết thúc học phần (60%)"},
        {"Ngày nhập": "2026-11-07", "Học kỳ": "Học kỳ I", "Môn học": "Toán rời rạc", "Điểm số": 5.0, "Loại điểm": "Điểm thi kết thúc học phần (60%)"}
    ])
    prompt = build_academic_analysis_prompt("Nguyễn Tấn Dũng", "2125110061", "CCQ2511B", mock_df, 7.0, "Khá 🥈")
    assert "Nguyễn Tấn Dũng" in prompt
    assert "Ngôn ngữ Python" in prompt
    assert "Toán rời rạc" in prompt
    print(" Test tích hợp Prompt CrewAI Advisor: ĐẠT (PASS).")

def test_smart_advisor_without_api_key():
    from ai_advisor import generate_smart_academic_advice
    mock_df = pd.DataFrame([
        {"Ngày nhập": "2026-11-07", "Học kỳ": "Học kỳ I", "Môn học": "Ngôn ngữ Python", "Điểm số": 9.0, "Loại điểm": "Điểm thi kết thúc học phần (60%)"},
        {"Ngày nhập": "2026-11-07", "Học kỳ": "Học kỳ I", "Môn học": "Toán rời rạc", "Điểm số": 5.0, "Loại điểm": "Điểm thi kết thúc học phần (60%)"}
    ])
    advice = generate_smart_academic_advice("Nguyễn Tấn Dũng", "2125110061", "CCQ2511B", mock_df, 7.0, "Khá 🥈")
    assert "BÁO CÁO CỐ VẤN HỌC TẬP" in advice
    assert "Nguyễn Tấn Dũng" in advice
    assert "Ngôn ngữ Python" in advice
    print(" Test Chế độ Cố vấn Tự động (Không cần API Key): ĐẠT (PASS).")

if __name__ == "__main__":
    print("\n" + "="*60)
    print(" KHỞI CHẠY BỘ KIỂM THỬ TỰ ĐỘNG HITC PORTAL (TEST SUITE)")
    print("="*60 + "\n")
    try:
        import pytest
        exit_code = pytest.main(["tests/", "-v"])
        sys.exit(exit_code)
    except ImportError:
        test_calculate_average_score()
        test_ai_advisor_prompt()
        test_smart_advisor_without_api_key()
        print("\n" + "="*60)
        print(" CHÚC MỪNG! TOÀN BỘ KIỂM THỬ ĐÃ CHẠY ĐẠT (PASS 100%).")
        print("="*60 + "\n")
