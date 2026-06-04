import streamlit as st

st.set_page_config(
    page_title="سيناريو النجاح بالتجارة",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap');
html, body, [class*="css"], .stApp {
    font-family: 'Tajawal', sans-serif !important;
    direction: rtl;
}
.stMarkdown, .stText, p, h1, h2, h3, h4, label, .stRadio label,
.stSelectbox label, .stCheckbox label, .stNumberInput label {
    text-align: right !important;
    direction: rtl !important;
}
.block-container { padding-top: 1.5rem; }
.metric-box {
    background: #f8f9fa;
    border-radius: 12px;
    padding: 20px;
    border-right: 5px solid #1a73e8;
    margin-bottom: 14px;
}
.success-box {
    background: #e8f5e9;
    border-radius: 12px;
    padding: 16px;
    border-right: 5px solid #2e7d32;
    margin-bottom: 14px;
}
.warning-box {
    background: #fff8e1;
    border-radius: 12px;
    padding: 16px;
    border-right: 5px solid #f9a825;
    margin-bottom: 14px;
}
.danger-box {
    background: #fce4ec;
    border-radius: 12px;
    padding: 16px;
    border-right: 5px solid #c62828;
    margin-bottom: 14px;
}
.info-box {
    background: #e3f2fd;
    border-radius: 12px;
    padding: 16px;
    border-right: 5px solid #1565c0;
    margin-bottom: 14px;
}
div[data-testid="stMetricValue"] { font-family: 'Tajawal', sans-serif !important; }
</style>
""", unsafe_allow_html=True)

PAGES = {
    "🏠 الرئيسية: سنام المشروع": "home",
    "🔍 1. رادار التخصص والمحيط الأزرق": "niche",
    "📐 2. محاكي الرشاقة المساحية": "space",
    "🚗 3. فحص الموقع والجاهزية": "location",
    "🛵 4. حاسبة التوصيل العكسية": "delivery",
    "💰 5. موزع الميزانية ومصد الطوارئ": "budget",
    "🛠️ 6. فلتر التأسيس الرشيق": "lean",
    "🎯 7. حاسبة التسعير ورحلة البضاعة": "pricing",
    "🏛️ 8. التكاليف الحكومية والامتثال": "gov",
    "🛡️ 9. رادار المخالفات والـ Checklist": "violations",
    "🚀 10. قانون نعم أولاً واقتناص الفرص": "yes_first",
}

st.sidebar.markdown("## 📈 سيناريو النجاح بالتجارة")
st.sidebar.markdown("---")
menu = st.sidebar.radio("اختر الأداة:", list(PAGES.keys()), label_visibility="collapsed")
page = PAGES[menu]

if page == "home":
    from pages.home import render
    render()
elif page == "niche":
    from pages.niche import render
    render()
elif page == "space":
    from pages.space import render
    render()
elif page == "location":
    from pages.location import render
    render()
elif page == "delivery":
    from pages.delivery import render
    render()
elif page == "budget":
    from pages.budget import render
    render()
elif page == "lean":
    from pages.lean import render
    render()
elif page == "pricing":
    from pages.pricing import render
    render()
elif page == "gov":
    from pages.gov import render
    render()
elif page == "violations":
    from pages.violations import render
    render()
elif page == "yes_first":
    from pages.yes_first import render
    render()
