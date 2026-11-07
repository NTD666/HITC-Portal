"""Kiểm thử cấu trúc thư mục và các tệp cốt lõi của dự án HITC Portal."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_ROOT_FILES = {
    "README.md",
    "requirements.txt",
    "app.py",
    "grade_calculator.py",
    "ai_advisor.py",
    "test_app.py",
    "chay_ung_dung.bat",
    "day_code_len_github.bat",
    ".gitignore",
}

def test_required_root_files_exist():
    """Xác nhận tất cả các tệp cốt lõi bắt buộc đều tồn tại trong thư mục gốc."""
    actual_files = {p.name for p in ROOT.iterdir() if p.is_file()}
    missing = REQUIRED_ROOT_FILES - actual_files
    assert not missing, f"Thiếu các tệp cốt lõi trong dự án: {missing}"

def test_requirements_contains_core_dependencies():
    """Kiểm tra tệp requirements.txt có khai báo đầy đủ các thư viện quan trọng."""
    req_path = ROOT / "requirements.txt"
    assert req_path.exists(), "Không tìm thấy requirements.txt"
    content = req_path.read_text(encoding="utf-8").lower()
    for package in ["streamlit", "pandas", "altair"]:
        assert package in content, f"requirements.txt thiếu thư viện: {package}"

def test_batch_scripts_integrity():
    """Kiểm tra các tệp script .bat có nội dung thực thi hợp lệ."""
    run_bat = ROOT / "chay_ung_dung.bat"
    push_bat = ROOT / "day_code_len_github.bat"
    assert run_bat.exists() and run_bat.stat().st_size > 0
    assert push_bat.exists() and push_bat.stat().st_size > 0
