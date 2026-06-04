import streamlit as st


def render():
    st.title("📐 محاكي الرشاقة المساحية والتكلفة المتسلسلة")
    st.caption("الزيادة البسيطة في المساحة تجر خلفها تضاعفاً في الإيجار والتكييف والديكور. احسبها قبل التوقيع.")
    st.markdown("---")

    st.markdown("""
    <div class="warning-box">
    <b>القانون الذهبي:</b> المساحة الكبيرة ليست مجرد إيجار أعلى — هي كرة ثلج من التكاليف المتسلسلة.
    كل متر إضافي يتطلب: ديكوراً أكثر، تكييفاً أقوى، إضاءة أكبر، ونظافة أعمق.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📥 مدخلات الحساب")
    col1, col2 = st.columns(2)
    with col1:
        rent_per_meter = st.number_input(
            "سعر إيجار المتر المربع سنوياً (ريال):",
            min_value=100, value=1000, step=100,
        )
        chosen_space = st.slider(
            "اختر مساحة المحل (متر مربع):",
            min_value=10, max_value=300, value=100, step=5,
        )
    with col2:
        st.markdown("#### 🔢 معادلة الحساب:")
        st.markdown("""
        - **الإيجار السنوي** = المساحة × سعر المتر
        - **التكييف سنوياً** = يتضاعف بعد 50م²
        - **الديكور والتشطيب** = يتضاعف بعد 50م²
        """)

    annual_rent = rent_per_meter * chosen_space

    if chosen_space <= 50:
        est_ac_monthly = 50
        est_decor = 30000
    elif chosen_space <= 100:
        factor = chosen_space / 50
        est_ac_monthly = int(50 * factor * 8)
        est_decor = int(30000 * factor)
    else:
        factor = chosen_space / 50
        est_ac_monthly = int(50 * factor * 12)
        est_decor = int(30000 * factor * 1.3)

    est_ac_annual = est_ac_monthly * 12
    total_year1 = annual_rent + est_ac_annual + est_decor

    st.markdown("---")
    st.subheader("📊 التكلفة المتسلسلة لمساحتك المختارة")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("الإيجار السنوي", f"{annual_rent:,} ﷼")
    c2.metric("التكييف والكهرباء (سنوي)", f"{est_ac_annual:,} ﷼")
    c3.metric("الديكور والتشطيب", f"{est_decor:,} ﷼")
    c4.metric("إجمالي عبء السنة الأولى", f"{total_year1:,} ﷼")

    daily_burn = total_year1 / 365
    st.markdown(f"**⏱️ تكلفتك اليومية الثابتة (قبل أي مبيعات):** `{daily_burn:,.0f} ريال/يوم`")

    st.markdown("---")

    if chosen_space > 60:
        optimal_space = 50
        opt_rent = rent_per_meter * optimal_space
        opt_ac = 50 * 12
        opt_decor = 30000
        opt_total = opt_rent + opt_ac + opt_decor
        savings = total_year1 - opt_total

        st.markdown(f"""
        <div class="warning-box">
        ⚠️ <b>تنبيه هندسي صارم:</b><br>
        مساحتك الحالية ({chosen_space}م²) تسببت في تكلفة متسلسلة ضخمة!<br>
        لو قلصت المساحة إلى <b>50 متراً مربعاً</b>، ستوفر سنوياً: <b>{savings:,} ريال</b>
        هذا الكاش الموفر هو بالضبط ما يجب توجيهه لـ <b>البضاعة والتسويق الرقمي</b>.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="success-box">
        🟢 <b>خيار رشيق ممتاز!</b><br>
        مساحتك في النطاق الآمن. أنت تحمي مشروعك من تضخم تكاليف التكييف والديكور.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📊 مقارنة بصرية: 50م² مقابل اختيارك")
    compare_data = {
        "البند": ["الإيجار السنوي", "التكييف (سنوي)", "الديكور"],
        f"50م² (الرشيق)": [f"{rent_per_meter * 50:,}", "600", "30,000"],
        f"{chosen_space}م² (اختيارك)": [
            f"{annual_rent:,}", f"{est_ac_annual:,}", f"{est_decor:,}"
        ],
    }
    import pandas as pd
    st.dataframe(pd.DataFrame(compare_data), use_container_width=True, hide_index=True)
