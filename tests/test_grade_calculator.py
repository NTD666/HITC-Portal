"""Kiểm thử thuật toán tính điểm và xếp loại học lực của HITC Portal."""

import sys
from pathlib import Path
import pandas as pd

# Thêm thư mục gốc vào sys.path để import an toàn
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from grade_calculator import (
    calculate_subject_grades,
    get_academic_rank,
    GRADE_WEIGHTS,
)

def test_grade_weights_constants():
    """Kiểm tra tỷ lệ phần trăm các đầu điểm theo đúng quy chế đào tạo tín chỉ HITC."""
    assert GRADE_WEIGHTS["Điểm chuyên cần (10%)"] == 0.1
    assert GRADE_WEIGHTS["Điểm kiểm tra giữa kỳ (30%)"] == 0.3
    assert GRADE_WEIGHTS["Điểm thi kết thúc học phần (60%)"] == 0.6
    assert sum(GRADE_WEIGHTS.values()) == 1.0

def test_calculate_subject_grades_standard():
    """Kiểm tra môn học có đầy đủ 3 đầu điểm (10% - 30% - 60%)."""
    # 10*0.1 + 8*0.3 + 6*0.6 = 1.0 + 2.4 + 3.6 = 7.0
    mock_data = pd.DataFrame([
        {"Môn học": "Ngôn ngữ Python", "Điểm số": 10.0, "Loại điểm": "Điểm chuyên cần (10%)"},
        {"Môn học": "Ngôn ngữ Python", "Điểm số": 8.0, "Loại điểm": "Điểm kiểm tra giữa kỳ (30%)"},
        {"Môn học": "Ngôn ngữ Python", "Điểm số": 6.0, "Loại điểm": "Điểm thi kết thúc học phần (60%)"},
    ])
    result = calculate_subject_grades(mock_data)
    assert len(result) == 1
    python_score = result.loc[result["Môn học"] == "Ngôn ngữ Python", "Điểm tổng kết"].values[0]
    assert python_score == 7.0
    assert result.loc[result["Môn học"] == "Ngôn ngữ Python", "Số đầu điểm"].values[0] == 3

def test_calculate_subject_grades_partial():
    """Kiểm tra môn học mới có 1 hoặc 2 đầu điểm thì chuẩn hóa đúng trọng số hiện có."""
    mock_data = pd.DataFrame([
        # Chỉ có điểm thi cuối kỳ 60% -> Chuẩn hóa là 9.0
        {"Môn học": "Cơ sở dữ liệu", "Điểm số": 9.0, "Loại điểm": "Điểm thi kết thúc học phần (60%)"},
        # Có chuyên cần 10% (10đ) và giữa kỳ 30% (8đ) -> (10*0.1 + 8*0.3) / 0.4 = 3.4 / 0.4 = 8.5
        {"Môn học": "Mạng máy tính", "Điểm số": 10.0, "Loại điểm": "Điểm chuyên cần (10%)"},
        {"Môn học": "Mạng máy tính", "Điểm số": 8.0, "Loại điểm": "Điểm kiểm tra giữa kỳ (30%)"},
    ])
    result = calculate_subject_grades(mock_data)
    assert len(result) == 2
    db_score = result.loc[result["Môn học"] == "Cơ sở dữ liệu", "Điểm tổng kết"].values[0]
    net_score = result.loc[result["Môn học"] == "Mạng máy tính", "Điểm tổng kết"].values[0]
    assert db_score == 9.0
    assert net_score == 8.5

def test_calculate_subject_grades_empty():
    """Kiểm tra khi bảng điểm chưa có dữ liệu thì trả về DataFrame rỗng an toàn."""
    empty_df = pd.DataFrame(columns=["Ngày nhập", "Học kỳ", "Môn học", "Điểm số", "Loại điểm"])
    result = calculate_subject_grades(empty_df)
    assert result.empty
    assert list(result.columns) == ["Môn học", "Điểm tổng kết", "Số đầu điểm"]

def test_academic_rank_levels():
    """Kiểm tra toàn bộ các mốc phân loại học lực."""
    assert get_academic_rank(9.0) == "Xuất sắc 🏆"
    assert get_academic_rank(8.5) == "Xuất sắc 🏆"
    assert get_academic_rank(8.2) == "Giỏi 🥇"
    assert get_academic_rank(8.0) == "Giỏi 🥇"
    assert get_academic_rank(7.5) == "Khá 🥈"
    assert get_academic_rank(6.5) == "Khá 🥈"
    assert get_academic_rank(5.5) == "Trung bình 🥉"
    assert get_academic_rank(5.0) == "Trung bình 🥉"
    assert get_academic_rank(4.9) == "Yếu"
    assert get_academic_rank(2.0) == "Yếu"
