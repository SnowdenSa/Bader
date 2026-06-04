import streamlit as st


def render():
    st.title("💰 موزع الميزانية الذكي ومصد الطوارئ")
    st.caption("قانون الـ 40% + بايلوت الـ 20%. احمِ كاشك من الانتحار المالي في بداية المشروع.")
    st.markdown("---")

    st.markdown("""
    <div class="danger-box">
    <b>الحقيقة الميدانية:</b> الأرباح في البداية ليست حنفية ماء تفتحها فتصب كاش فوراً!
    في أول 3 أشهر ستواجه جفافاً في المبيعات. إذا وضعت كل كاشك في الديكور والتأسيس،
    ستضطر لحرق أسعارك لتغطية الرواتب والإيجار، فتقتل مشروعك بيدك.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📥 بيانات رأس المال والتشغيل")
    col1, col2 = st.columns(2)
    with col1:
        total_cash = st.number_input(
            "إجمالي رأس مالك المتوفر بالكامل (ريال):",
            min_value=10000, value=200000, step=10000,
        )
        target_cost = st.number_input(
            "التكلفة التأسيسية المقترحة — ديكور + بضاعة + تجهيز (ريال):",
            min_value=1000, value=200000, step=5000,
        )
    with col2:
        monthly_rent = st.number_input("الإيجار الشهري للمحل (ريال):", min_value=0, value=5000, step=500)
        monthly_salaries = st.number_input("مجموع الرواتب الشهرية (ريال):", min_value=0, value=6000, step=500)
        monthly_misc = st.number_input(
            "مصاريف التشغيل الشهرية الأخرى — كهرباء، فواتير (ريال):",
            min_value=0, value=2000, step=200,
        )

    rent_buffer = monthly_rent * 6
    salary_buffer = monthly_salaries * 3
    misc_buffer = monthly_misc * 3
    total_buffer = rent_buffer + salary_buffer + misc_buffer
    daily_expenses = (monthly_rent + monthly_salaries + monthly_misc) / 30
    runway_days = total_buffer / daily_expenses if daily_expenses > 0 else 0
    available_for_setup = total_cash - total_buffer

    st.markdown("---")
    st.subheader("🛡️ صناديق الحماية الإجبارية (مجمّدة ولا تُلمس)")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("إيجار 6 أشهر (مجمّد)", f"{rent_buffer:,} ﷼")
    c2.metric("رواتب 3 أشهر (مجمّد)", f"{salary_buffer:,} ﷼")
    c3.metric("مصاريف تشغيل 3 أشهر", f"{misc_buffer:,} ﷼")
    c4.metric("إجمالي الصندوق المحمي", f"{total_buffer:,} ﷼")

    st.markdown(f"**📅 مدة صمود المشروع بكاش الطوارئ (بدون أي مبيعات):** `{runway_days:.0f} يوماً ({runway_days/30:.1f} أشهر)`")

    st.markdown("---")
    st.subheader("⚖️ ميزان القرار التجاري")

    if target_cost > available_for_setup:
        st.markdown(f"""
        <div class="danger-box">
        🛑 <b>فخ الانكشاف المالي والغرور التشغيلي!</b><br>
        أنت تريد ضخ <b>{target_cost:,} ريال</b> في التأسيس، لكن الكاش المتاح للتأسيس
        بعد حجز صناديق الحماية هو <b>{available_for_setup:,} ريال</b> فقط.<br><br>
        <b>القرارات الحتمية الفورية:</b><br>
        1. اكسر غرور الديكور الكشخة — صغّر المساحة وبسّط التشطيب<br>
        2. ابدأ بعامل أو اثنين فقط، لا توظف المزيد إلا مع نمو الشغل<br>
        3. اشترِ أدوات مستعملة من حراج بدلاً من الجديدة<br>
        4. إذا ميزانيتك 200 ألف → ابحث عن مشروع تأسيسه 120 ألف فقط
        </div>
        """, unsafe_allow_html=True)
    elif runway_days < 90:
        st.markdown(f"""
        <div class="warning-box">
        ⚠️ <b>منطقة الخطر المالي:</b><br>
        كاش الطوارئ يكفيك {runway_days:.0f} يوماً فقط. هذا أقل من 3 أشهر —
        وهي فترة خطرة جداً لمرحلة الجفاف الأولى في المشاريع.
        </div>
        """, unsafe_allow_html=True)
    elif runway_days < 180:
        st.markdown(f"""
        <div class="warning-box">
        ⚠️ <b>منطقة الحذر (3 - 6 أشهر):</b><br>
        وضعك مقبول لكن أي عائق حكومي أو تراجع في السوق سيهددك.
        حاول ضغط مصاريف التأسيس أكثر لرفع كاش الطوارئ.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="success-box">
        🟢 <b>منطقة الأمان المالي الكامل!</b><br>
        كاش الطوارئ يغطي <b>{runway_days:.0f} يوماً ({runway_days/30:.1f} أشهر)</b>.
        أنت محمي من فخ حرق الأسعار في الأشهر الأولى.
        تقدم بثقة وركّز على جودة منتجك وتسويقك.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🧪 قانون بايلوت — حماية الميزانيات الكبيرة")
    st.markdown("""
    إذا كانت ميزانيتك كبيرة ولم تدخل هذا النشاط من قبل:
    """)

    pilot_pct = st.slider("نسبة ميزانية بايلوت للتعلم الميداني (%):", 10, 30, 20)
    pilot_budget = total_cash * (pilot_pct / 100)
    protected_capital = total_cash - pilot_budget

    col5, col6 = st.columns(2)
    col5.metric(f"ميزانية بايلوت التعلم ({pilot_pct}%)", f"{pilot_budget:,} ﷼")
    col6.metric("رأس المال المحمي في حسابك", f"{protected_capital:,} ﷼")

    st.markdown(f"""
    <div class="info-box">
    💡 <b>فلسفة البايلوت:</b><br>
    ادفع <b>{pilot_budget:,} ريال</b> لتتعلم: كيف تتعامل مع العمال، الموردين، والإيجارات.
    بعد سنة من التجربة، ستطلق مشروعك الكبير بربع الميزانية أو أقل.
    وفّرت <b>{protected_capital:,} ريال</b> من الضياع في غرور التأسيس!
    </div>
    """, unsafe_allow_html=True)
