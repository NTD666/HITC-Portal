"""Kiểm thử module AI Advisor và Chế độ Cố vấn Tự động Chuẩn HITC."""

import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ai_advisor import (
    build_academic_analysis_prompt,
    generate_smart_academic_advice,
    run_crewai_advisor,
)

def test_build_academic_analysis_prompt():
    """Kiểm tra cấu trúc prompt tạo ra có đầy đủ thông tin sinh viên và môn học."""
    mock_df = pd.DataFrame([
        {"Ngày nhập": "2026-11-07", "Học kỳ": "Học kỳ I", "Môn học": "Ngôn ngữ Python", "Điểm số": 9.5, "Loại điểm": "Điểm thi kết thúc học phần (60%)"},
        {"Ngày nhập": "2026-11-07", "Học kỳ": "Học kỳ I", "Môn học": "Cơ sở dữ liệu", "Điểm số": 4.5, "Loại điểm": "Điểm thi kết thúc học phần (60%)"},
    ])
    prompt = build_academic_analysis_prompt(
        student_name="Nguyễn Tấn Dũng",
        student_id="2125110061",
        student_class="CCQ2511B",
        records_df=mock_df,
        gpa=7.0,
        academic_rank="Khá 🥈"
    )
    assert "Nguyễn Tấn Dũng" in prompt
    assert "2125110061" in prompt
    assert "CCQ2511B" in prompt
    assert "Ngôn ngữ Python" in prompt
    assert "Cơ sở dữ liệu" in prompt

def test_generate_smart_academic_advice_offline():
    """Kiểm tra chế độ cố vấn tự động nội bộ sinh báo cáo đầy đủ khi không có API Key."""
    mock_df = pd.DataFrame([
        {"Ngày nhập": "2026-11-07", "Học kỳ": "Học kỳ I", "Môn học": "Lập trình Web Frontend", "Điểm số": 9.0, "Loại điểm": "Điểm thi kết thúc học phần (60%)"},
        {"Ngày nhập": "2026-11-07", "Học kỳ": "Học kỳ I", "Môn học": "Toán ứng dụng CNTT (Toán rời rạc)", "Điểm số": 4.0, "Loại điểm": "Điểm thi kết thúc học phần (60%)"},
    ])
    advice = generate_smart_academic_advice(
        student_name="Nguyễn Tấn Dũng",
        student_id="2125110061",
        student_class="CCQ2511B",
        records_df=mock_df,
        gpa=6.5,
        academic_rank="Khá 🥈"
    )
    # Xác thực các đề mục quan trọng
    assert "BÁO CÁO CỐ VẤN HỌC TẬP" in advice
    assert "Lập trình Web Frontend" in advice
    assert "CẢNH BÁO NGUY CƠ HỌC VỤ" in advice
    assert "Kế Hoạch Hành Động Cá Nhân Hóa" in advice
    assert "Khoa CNTT - HITC" in advice

def test_run_crewai_advisor_fallback_when_no_api_key():
    """Khi không truyền API Key, run_crewai_advisor tự động trả về kết quả chế độ nội bộ thành công."""
    mock_df = pd.DataFrame([
        {"Ngày nhập": "2026-11-07", "Học kỳ": "Học kỳ I", "Môn học": "Ngôn ngữ Python", "Điểm số": 9.0, "Loại điểm": "Điểm thi kết thúc học phần (60%)"},
    ])
    result = run_crewai_advisor(
        student_name="Nguyễn Tấn Dũng",
        student_id="2125110061",
        student_class="CCQ2511B",
        records_df=mock_df,
        gpa=9.0,
        academic_rank="Xuất sắc 🏆",
        api_key=None
    )
    assert result["success"] is True
    assert "output" in result
    assert "Nguyễn Tấn Dũng" in result["output"]
