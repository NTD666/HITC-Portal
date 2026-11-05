import streamlit as st
import pandas as pd
import datetime

# Khởi tạo trạng thái hệ thống nếu chưa có
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "student_info" not in st.session_state:
    st.session_state.student_info = {}

# Cấu hình trang Web mặc định
st.set_page_config(
    page_title="Cổng Thông Tin Sinh Viên - HITC TP.HCM Portal", 
    page_icon="🎓", 
    layout="centered"
)

# =========================================================================
# PHẦN 1: CẤU HÌNH THEME DARK MODE & COLOR ĐẶC TRƯNG HITC TP.HCM
# =========================================================================
# Cho người dùng lựa chọn chế độ màu sắc ở Sidebar bên trái
theme_choice = st.sidebar.selectbox("🎨 Chế độ hiển thị màn hình", ["Giao diện Sáng (Light)", "Giao diện Tối (Dark Mode)"])

# Thiết lập hệ màu dựa trên lựa chọn (Đỏ đô chủ đạo của Cao đẳng Công thương TP.HCM)
if theme_choice == "Giao diện Tối (Dark Mode)":
    bg_color = "#121212"      
    text_color = "#FFFFFF"    
    card_bg = "#1E1E1E"       
    border_color = "#333333"  
else:
    bg_color = "#FFFFFF"      
    text_color = "#333333"    
    card_bg = "#F8F9FA"       
    border_color = "#E0E0E0"  

# Bơm CSS động thay đổi giao diện theo thương hiệu HITC TP.HCM
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
    }}
    h1, h2, h3, h4, h5, h6, label, p, span {{
        color: {text_color} !important;
    }}
    
    /* Thiết kế phần HEADER rực rỡ mang bản sắc HITC TP.HCM (Đỏ đô sang trọng) */
    .hitc-header {{
        background: linear-gradient(135deg, #A31D1D 70%, #E8B86D 100%); /* Tông màu đỏ - vàng đặc trưng của trường */
        padding: 22px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin-bottom: 25px;
    }}
    .hitc-header h1 {{
        color: #FFFFFF !important;
        font-size: 24px !important;
        font-weight: bold !important;
        margin: 0 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
    }}
    .hitc-header p {{
        color: #F5E7B2 !important;
        font-size: 15px !important;
        margin: 5px 0 0 0 !important;
        font-style: italic;
    }}
    
    /* Các nút bấm theo tông đỏ đô thương hiệu */
    .stButton>button {{
        background-color: #A31D1D !important;
        color: white !important;
        border-radius: 5px !important;
        border: none !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
        transition: 0.3s !important;
    }}
    .stButton>button:hover {{
        background-color: #E8B86D !important;
        color: #A31D1D !important;
        box-shadow: 0 4px 10px rgba(232, 184, 109, 0.4) !important;
    }}
    
    /* Khối Form đăng nhập bo tròn */
    div[data-testid="stForm"] {{
        background-color: {card_bg} !important;
        border: 1px solid {border_color} !important;
        border-radius: 12px !important;
        padding: 25px !important;
        box-shadow: 0 6px 18px rgba(0,0,0,0.05) !important;
    }}
    
    /* Thiết kế phần FOOTER chuẩn HITC TP.HCM */
    .hitc-footer {{
        margin-top: 50px;
        padding: 15px;
        background-color: {card_bg};
        border-top: 3px solid #A31D1D;
        border-radius: 5px;
        text-align: center;
        font-size: 13px;
        color: {text_color};
    }}
    </style>
""", unsafe_allow_html=True)

# =========================================================================
# GIAO DIỆN CHÍNH HÀNH TRÌNH ĐĂNG NHẬP & PORTAL
# =========================================================================

# 1. HIỂN THỊ TRANG TRÍ HEADER CHUNG TRÊN ĐẦU TRANG
st.markdown("""
    <div class="hitc-header">
        <h1>🏫 TRƯỜNG CAO ĐẲNG CÔNG THƯƠNG THÀNH PHỐ HỒ CHÍ MINH</h1>
        <p>Hệ Thống Cổng Thông Tin & Quản Lý Tiến Độ Học Tập Sinh Viên (HITC Portal)</p>
    </div>
""", unsafe_allow_html=True)

# 2. KIỂM TRA ĐIỀU KIỆN HIỂN THỊ TRANG ĐĂNG NHẬP HOẶC TRANG TRONG
if not st.session_state.logged_in:
    st.subheader("🔑 Đăng nhập tài khoản sinh viên")
    
    with st.form(key="login_form"):
        ho_ten = st.text_input("Họ và tên sinh viên:", placeholder="Ví dụ: Nguyễn Tấn Dũng")
        mssv = st.text_input("Mã số sinh viên (MSSV):", placeholder="Ví dụ: 2125110061 (8 chữ số)")
        lop_hoc = st.text_input("Lớp học khóa học:", placeholder="Ví dụ: CCQ2511B")
        
        btn_login = st.form_submit_button("🔓 Đăng nhập vào hệ thống")
        
    if btn_login:
        if ho_ten.strip() == "" or mssv.strip() == "" or lop_hoc.strip() == "":
            st.error("❌ Vui lòng điền đầy đủ thông tin để hệ thống xác thực dữ liệu!")
        else:
            st.session_state.student_info = {"name": ho_ten.strip(), "id": mssv.strip(), "class": lop_hoc.strip()}
            st.session_state.logged_in = True
            st.success("Đăng nhập thành công vào HITC Portal!")
            st.rerun()

else:
    sv = st.session_state.student_info

    # THANH SIDEBAR HIỂN THỊ THÔNG TIN SINH VIÊN ĐỘNG
    st.sidebar.markdown("### 👤 THÔNG TIN SINH VIÊN")
    st.sidebar.info(f"""
    **Họ và tên:** {sv['name']}  
    **Mã số SV:** {sv['id']}  
    **Lớp học:** {sv['class']}  
    **Khóa học:** Khóa 49 / 50 (Chính Quy)  
    **Cơ sở:** 20 Tăng Nhơn Phú, Thủ Đức  
    **Trạng thái:** Đang học tích cực
    """)
    
    if st.sidebar.button("🔒 Đăng xuất khỏi hệ thống"):
        st.session_state.logged_in = False
        st.session_state.student_info = {}
        st.rerun()

    if "academic_records" not in st.session_state:
        st.session_state.academic_records = pd.DataFrame(columns=["Ngày nhập", "Học kỳ", "Môn học", "Điểm số", "Loại điểm"])

    # FORM NHẬP ĐIỂM
    st.header("📥 Cập nhật kết quả điểm số mới")
    with st.form(key="study_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Ngày đánh giá", datetime.date.today())
            semester = st.selectbox("Học kỳ đánh giá", [
                "Học kỳ I", "Học kỳ II", "Học kỳ III", "Học kỳ IV", "Học kỳ V", "Học kỳ VI", "Học kỳ Phụ / Cải thiện"
            ])
            subject = st.selectbox("Môn học (Chương trình đào tạo Khoa CNTT - HITC)", [
                # --- 1. Khối Kiến thức Đại cương & Kỹ năng ---
                "Triết học Mác - Lênin",
                "Tư tưởng Hồ Chí Minh",
                "Pháp luật đại cương",
                "Tin học đại cương",
                "Tiếng Anh cơ bản 1",
                "Tiếng Anh cơ bản 2",
                "Tiếng Anh chuyên ngành CNTT",
                "Kỹ năng mềm & Làm việc nhóm",
                "Giáo dục thể chất",
                "Giáo dục quốc phòng - An ninh",
                
                # --- 2. Khối Cơ sở ngành CNTT ---
                "Toán ứng dụng CNTT (Toán rời rạc)",
                "Nhập môn lập trình (C/C++)",
                "Kỹ thuật lập trình (C/C++)",
                "Kiến trúc máy tính & Vi xử lý",
                "Hệ điều hành (Windows & Linux)",
                "Lắp ráp, cài đặt & Bảo trì máy tính",
                "Mạng máy tính cơ bản",
                "Quản trị mạng máy tính (CCNA)",
                "Cơ sở dữ liệu (SQL Server)",
                "Hệ quản trị CSDL MySQL",
                "Cấu trúc dữ liệu và Giải thuật",
                "Thiết kế đồ họa đa phương tiện (Photoshop / AI)",
                
                # --- 3. Khối Chuyên ngành Lập trình & Kỹ thuật Phần mềm ---
                "Ngôn ngữ lập trình Python",
                "Lập trình hướng đối tượng (OOP Java / C#)",
                "Lập trình Windows Forms & .NET Core",
                "Phân tích & Thiết kế hệ thống thông tin",
                "Thiết kế Web căn bản (HTML5/CSS3/JavaScript)",
                "Lập trình Web Frontend (ReactJS / VueJS)",
                "Lập trình Web Backend (PHP & Laravel / NodeJS)",
                "Lập trình Web ASP.NET Core MVC / Web API",
                "Thiết kế trải nghiệm & Giao diện UI/UX (Figma)",
                "Lập trình ứng dụng Di động (Android / Kotlin)",
                "Lập trình ứng dụng Di động đa nền tảng (Flutter)",
                "Kiểm thử và Đảm bảo chất lượng phần mềm (QA/QC)",
                
                # --- 4. Khối Chuyên ngành Mạng & An toàn thông tin ---
                "An toàn & Bảo mật thông tin mạng",
                "Quản trị máy chủ Linux & Windows Server",
                "Điện toán đám mây & DevOps căn bản (Docker/AWS)",
                "Trí tuệ nhân tạo (AI) & Học máy (Machine Learning)",
                "Khai phá dữ liệu & Phân tích dữ liệu lớn",
                
                # --- 5. Khối Thực tập & Khóa luận Tốt nghiệp ---
                "Chuyên đề công nghệ mới",
                "Thực tập tốt nghiệp tại doanh nghiệp",
                "Đồ án chuyên ngành CNTT",
                "Đồ án / Khóa luận tốt nghiệp",
                
                # --- 6. Tùy chọn mở rộng ---
                "📌 [Môn học khác - Nhập tên bên dưới]"
            ])
            custom_subject = st.text_input("Hoặc nhập tên môn khác nếu chưa có trong danh sách:", placeholder="Ví dụ: Lập trình Game Unity, Lập trình iOS...")
        with col2:
            score = st.number_input("Điểm số thành phần", min_value=0.0, max_value=10.0, step=0.5, value=7.0)
            grade_type = st.selectbox("Loại điểm đánh giá", ["Điểm chuyên cần (10%)", "Điểm kiểm tra giữa kỳ (30%)", "Điểm thi kết thúc học phần (60%)"])
            
        submit_button = st.form_submit_button(label="🚀 Cập nhật kết quả")

    if submit_button:
        # Xác định tên môn học cuối cùng
        if custom_subject.strip() != "":
            final_subject = custom_subject.strip()
        elif subject == "📌 [Môn học khác - Nhập tên bên dưới]":
            st.error("❌ Vui lòng nhập tên môn học vào ô bên dưới khi chọn tùy chọn 'Môn học khác'!")
            final_subject = None
        else:
            final_subject = subject

        if final_subject:
            new_data = pd.DataFrame([{"Ngày nhập": date.strftime("%Y-%m-%d"), "Học kỳ": semester, "Môn học": final_subject, "Điểm số": float(score), "Loại điểm": grade_type}])
            st.session_state.academic_records = pd.concat([st.session_state.academic_records, new_data], ignore_index=True)
            st.success(f"Hệ thống HITC Portal đã đồng bộ điểm số môn '{final_subject}' thành công!")


    # HIỂN THỊ KẾT QUẢ TRA CỨU
    st.divider()
    st.header("📊 Tra Cứu Kết Quả Học Tập Tích Lũy")
    df = st.session_state.academic_records

    if df.empty:
        st.info("Hiện hệ thống trống dữ liệu. Vui lòng cập nhật điểm số để kích hoạt bảng tra cứu học phần!")
    else:
        average_score = df["Điểm số"].mean()
        if average_score >= 8.5: hoc_luc = "Xuất sắc 🏆"
        elif average_score >= 8.0: hoc_luc = "Giỏi 🥇"
        elif average_score >= 6.5: hoc_luc = "Khá 🥈"
        elif average_score >= 5.0: hoc_luc = "Trung bình 🥉"
        else: hoc_luc = "Yếu"

        c1, c2, c3 = st.columns(3)
        c1.metric(label="📈 Điểm trung bình (GPA)", value=f"{average_score:.2f} / 10")
        c2.metric(label="🎓 Học lực dự kiến", value=hoc_luc)
        c3.metric(label="📚 Số lượng đầu điểm", value=f"{len(df)} thành phần")
        
        st.subheader("📋 Chi tiết bảng điểm học phần")
        st.dataframe(df, use_container_width=True)
        
        st.subheader("📊 Đồ thị phân bổ năng lực môn học")
        summary = df.groupby("Môn học", as_index=False)["Điểm số"].mean()
        
        # Sử dụng thư viện Altair có sẵn để khóa cứng chữ nằm ngang (angle=0)
        import altair as alt
        
        chart = alt.Chart(summary).mark_bar(color="#A31D1D").encode(
            x=alt.X("Môn học:N", axis=alt.Axis(labelAngle=0, labelOverlap=False)),
            y=alt.Y("Điểm số:Q", scale=alt.Scale(domain=[0, 10])),
            tooltip=["Môn học", "Điểm số"]
        ).properties(
            width="container",
            height=350
        )
        
        st.altair_chart(chart, use_container_width=True)



# 3. TRANG TRÍ FOOTER CHUYÊN NGHIỆP Ở CUỐI TRANG
st.markdown("""
    <div class="hitc-footer">
        <p><b>© 2026 - Bản quyền thuộc về Trung tâm Đào tạo - Trường Cao đẳng Công thương TP.HCM (HITC)</b></p>
        <p>📍 Địa chỉ: Số 20 Tăng Nhơn Phú, P. Phước Long B, TP. Thủ Đức, TP. Hồ Chí Minh</p>
        <p><i>Hệ thống phát triển bởi Sinh viên khoa CNTT HITC - Nguyễn Tấn Dũng</i></p>
    </div>
""", unsafe_allow_html=True)
