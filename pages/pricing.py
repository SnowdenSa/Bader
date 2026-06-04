import streamlit as st


def render():
    st.title("🎯 حاسبة التسعير الحقيقي ورحلة البضاعة بالهللات")
    st.caption("السعر الحقيقي للمنتج لا يُحسب من الجملة فقط — هناك رحلة كاملة من التكاليف الخفية.")
    st.markdown("---")

    st.markdown("""
    <div class="danger-box">
    <b>الحقيقة الصادمة:</b> التاجر الذي يشتري البضاعة بـ 3 ريال ويبيعها بـ 5 ريال لا يربح ريالين!
    هناك رحلة كاملة من الهللات الخفية قبل أن تصل البضاعة لكفّك:
    شحن + جمارك + وسطاء + خسارة البضاعة التالفة + أجرك أنت.
    من لم يحسب هذه الرحلة، حسب خسارته بعد فوات الأوان.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📥 بيانات المنتج والسوق")
    col1, col2 = st.columns(2)
    with col1:
        market_price = st.number_input(
            "سعر السوق الحالي (ما يبيعه المنافس بالريال):",
            min_value=0.5, value=5.0, step=0.5,
        )
        wholesale_price = st.number_input(
            "سعر الجملة للقطعة الواحدة (ريال):",
            min_value=0.1, value=2.5, step=0.1,
        )
        monthly_volume = st.number_input(
            "الكمية المتوقعة للبيع شهرياً (قطعة):",
            min_value=1, value=500, step=50,
        )
    with col2:
        dead_stock_pct = st.slider(
            "نسبة البضاعة التي لن تُباع (تالفة / راكدة %):",
            min_value=0, max_value=50, value=15,
        )
        st.markdown("#### 🔢 التكاليف الشهرية الثابتة:")
        monthly_rent = st.number_input("الإيجار الشهري (ريال):", min_value=0, value=3000, step=500)
        monthly_salaries = st.number_input("الرواتب الشهرية (ريال):", min_value=0, value=4000, step=500)
        monthly_gov = st.number_input("الرسوم الحكومية الشهرية (ريال):", min_value=0, value=500, step=100)
        owner_wage = st.number_input("أجرك أنت كصاحب (ريال):", min_value=0, value=3000, step=500)

    st.markdown("---")
    st.subheader("📦 رحلة البضاعة بالهللات")

    col3, col4 = st.columns(2)
    with col3:
        logistics_pct = st.slider("تكلفة الشحن والنقل (% من سعر الجملة):", 0, 30, 8)
        customs_pct = st.slider("الجمارك والتخليص (% من سعر الجملة):", 0, 20, 5)
        gateway_pct = st.slider("عمولة البوابة / الوسيط (% من سعر البيع):", 0, 15, 3)

    logistics_cost = wholesale_price * (logistics_pct / 100)
    customs_cost = wholesale_price * (customs_pct / 100)
    full_unit_cost = wholesale_price + logistics_cost + customs_cost

    actual_selling_units = monthly_volume * (1 - dead_stock_pct / 100)
    total_monthly_purchase = full_unit_cost * monthly_volume
    total_fixed_monthly = monthly_rent + monthly_salaries + monthly_gov + owner_wage
    fixed_per_unit = total_fixed_monthly / actual_selling_units if actual_selling_units > 0 else 0
    dead_stock_cost_per_unit = (full_unit_cost * monthly_volume * (dead_stock_pct / 100)) / actual_selling_units if actual_selling_units > 0 else 0

    real_cost_before_gateway = full_unit_cost + fixed_per_unit + dead_stock_cost_per_unit
    gateway_amount = market_price * (gateway_pct / 100)
    real_total_cost = real_cost_before_gateway + gateway_amount
    real_margin = market_price - real_total_cost
    margin_pct = (real_margin / market_price * 100) if market_price > 0 else 0

    with col4:
        st.markdown("#### 📊 تفصيل التكلفة الحقيقية للقطعة:")
        st.markdown(f"""
        | البند | التكلفة |
        |-------|---------|
        | سعر الجملة | {wholesale_price:.2f} ﷼ |
        | الشحن والنقل | {logistics_cost:.2f} ﷼ |
        | الجمارك | {customs_cost:.2f} ﷼ |
        | حصة التكاليف الثابتة | {fixed_per_unit:.2f} ﷼ |
        | تكلفة البضاعة الراكدة | {dead_stock_cost_per_unit:.2f} ﷼ |
        | عمولة البوابة | {gateway_amount:.2f} ﷼ |
        | **التكلفة الحقيقية الإجمالية** | **{real_total_cost:.2f} ﷼** |
        """)

    st.markdown("---")
    st.subheader("⚖️ ميزان السوق والربحية")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("سعر السوق", f"{market_price:.2f} ﷼")
    c2.metric("تكلفتك الحقيقية", f"{real_total_cost:.2f} ﷼")
    c3.metric("هامش الربح الفعلي", f"{real_margin:.2f} ﷼")
    c4.metric("نسبة الربح", f"{margin_pct:.1f}%")

    st.markdown("---")

    if real_total_cost >= market_price:
        st.markdown(f"""
        <div class="danger-box">
        🛑 <b>ضع X على هذا المشروع — لا تدخله!</b><br>
        تكلفتك الحقيقية للقطعة (<b>{real_total_cost:.2f} ريال</b>) أعلى من أو تساوي
        سعر السوق (<b>{market_price:.2f} ريال</b>).<br><br>
        <b>هذا يعني:</b> أنت ستبيع بخسارة أو بلا ربح في أفضل الأحوال.
        المنافس إما يبيع بخسارة ليفنيك (مستحيل الصمود)، أو لديه ميزة تكلفة لا تملكها أنت.
        <br><br>
        <b>بدائل الهروب:</b><br>
        1. ابحث عن مورد أرخص بنفس الجودة<br>
        2. غير الشريحة المستهدفة: بيع لعميل يدفع أكثر (Premium)<br>
        3. ابحث عن منتج مكمّل بهامش أعلى تبيعه بجانبه<br>
        4. انظر في التخصص الضيق: نفس المنتج لشريحة خاصة بسعر أعلى
        </div>
        """, unsafe_allow_html=True)
    elif margin_pct < 10:
        st.markdown(f"""
        <div class="warning-box">
        ⚠️ <b>هامش خطر — منطقة البقاء لا الربح!</b><br>
        ربحك {margin_pct:.1f}% فقط. هذا هامش بقاء، أي زيادة في تكلفة واحدة تأكله.<br>
        <b>المنافس الذي يبيع بنفس السعر:</b> إما يخسر، أو عنده حجم ضخم يضغط تكاليفه.
        أنت تحتاج حجماً أو ميزة مختلفة.
        </div>
        """, unsafe_allow_html=True)
    elif margin_pct < 25:
        st.markdown(f"""
        <div class="warning-box">
        ⚠️ <b>هامش معقول لكن هش:</b><br>
        ربحك {margin_pct:.1f}%. مقبول، لكن لا يتحمل صدمات التكلفة أو انخفاض الطلب.
        ركز على رفع الحجم أو خفض تكلفة الشحن والوسيط.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="success-box">
        🟢 <b>هامش صحي — مشروع يستحق المتابعة!</b><br>
        ربحك {margin_pct:.1f}%. هذا هامش يتحمل المفاجآت ويسمح بالنمو.
        ركز الآن على حجم المبيعات والتسويق، لا على تخفيض التكاليف فقط.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🔬 تحليل نوع المنافس")
    st.markdown("""
    <div class="info-box">
    <b>عندما تجد منافساً يبيع بسعر يبدو مستحيلاً، اسأل نفسك:</b><br>
    هل هو <b>منافس البقاء</b> (يبيع بلا ربح ليغطي إيجاره ولن يصمد) ؟
    أم هو <b>منافس الحجم</b> (يشتري بأسعار الجملة الكبيرة ويضغط التكاليف) ؟
    أم هو <b>منافس التميز</b> (يضيف قيمة فعلية تبرر السعر الأعلى) ؟
    <br><br>
    <b>قرارك:</b> لا تنافس منافس البقاء في الحرب السعرية — دعه يخرج من السوق بنفسه.
    نافس بالتميز والتخصص والخدمة التي لا يقدمها.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📊 جدول سيناريوهات الحجم")

    import pandas as pd
    scenarios = []
    for vol in [200, 300, 500, 750, 1000]:
        act_units = vol * (1 - dead_stock_pct / 100)
        fixed_pu = total_fixed_monthly / act_units if act_units > 0 else 0
        dead_pu = (full_unit_cost * vol * (dead_stock_pct / 100)) / act_units if act_units > 0 else 0
        cost = full_unit_cost + fixed_pu + dead_pu + gateway_amount
        margin = market_price - cost
        scenarios.append({
            "الحجم الشهري": f"{vol} قطعة",
            "التكلفة الحقيقية": f"{cost:.2f} ﷼",
            "هامش الربح": f"{margin:.2f} ﷼",
            "نسبة الربح": f"{(margin/market_price*100):.1f}%" if market_price > 0 else "—",
        })

    st.dataframe(pd.DataFrame(scenarios), use_container_width=True, hide_index=True)
