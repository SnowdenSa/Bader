import streamlit as st


def render():
    st.title("🛵 حاسبة التوصيل العكسية للتطبيقات")
    st.caption("احسبها بالعكس! اعرف السعر الصحيح في تطبيق التوصيل لحماية صافي ربح درجك.")
    st.markdown("---")

    st.markdown("""
    <div class="danger-box">
    <b>الخطأ الشائع:</b> تضع سعراً في التطبيق بناءً على تكلفتك، ثم تفاجأ أن التطبيق أخذ نسبته
    وبقي لك ربح أقل من المتوقع بكثير. الحل: احسب السعر بالعكس من الربح المستهدف.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📥 مدخلات الحساب العكسي")
    col1, col2 = st.columns(2)
    with col1:
        target_net = st.number_input(
            "الربح الصافي الذي تريده في درجك (ريال) — بعد كل التكاليف:",
            min_value=1.0, value=70.0, step=5.0,
        )
        app_commission = st.slider(
            "نسبة عمولة تطبيق التوصيل (%):",
            min_value=5, max_value=40, value=25,
        )
    with col2:
        st.markdown("#### معادلة الحساب العكسي:")
        st.latex(r"\text{السعر في التطبيق} = \frac{\text{الربح المستهدف}}{1 - \text{نسبة العمولة}}")
        st.markdown("**مثال:** إذا أردت 70 ريالاً وعمولة التطبيق 25%:")
        st.latex(r"\frac{70}{1 - 0.25} = \frac{70}{0.75} = 93.33 \text{ ريال}")

    commission_decimal = app_commission / 100
    if commission_decimal >= 1:
        st.error("نسبة العمولة لا يمكن أن تكون 100%")
        return

    recommended_price = target_net / (1 - commission_decimal)
    commission_amount = recommended_price * commission_decimal

    st.markdown("---")
    st.subheader("📊 الخطة السعرية الذكية للتطبيق")
    c1, c2, c3 = st.columns(3)
    c1.metric("السعر الإجباري في التطبيق", f"{recommended_price:.2f} ﷼")
    c2.metric("حصة التطبيق (ستُخصم تلقائياً)", f"{commission_amount:.2f} ﷼")
    c3.metric("صافي ما سيصلك في الدرج", f"{target_net:.2f} ﷼")

    st.markdown(f"""
    <div class="success-box">
    💡 <b>الخلاصة الاستراتيجية:</b><br>
    بوضع سعر <b>{recommended_price:.2f} ريال</b> في التطبيق، أنت لم تظلم العميل ولم تخسر ريالاً واحداً.
    أنت ترحّلت تكلفة راحة التوصيل إلى من يبحث عن الخدمة في بيته،
    وضمنت أن <b>{target_net:.2f} ريال</b> ستدخل درجك بالكامل في كل طلب.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📊 مقارنة السيناريوهات")

    scenarios = []
    for pct in [15, 20, 25, 30, 35]:
        dec = pct / 100
        price = target_net / (1 - dec)
        cut = price * dec
        scenarios.append({
            "تطبيق التوصيل": f"عمولة {pct}%",
            "السعر في التطبيق": f"{price:.2f} ﷼",
            "حصة التطبيق": f"{cut:.2f} ﷼",
            "يصلك في الدرج": f"{target_net:.2f} ﷼",
        })

    import pandas as pd
    df = pd.DataFrame(scenarios)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("""
    <div class="info-box">
    <b>تنبيه مهم:</b> عند المقارنة بين التطبيقات، لا تقارن نسبة العمولة فقط —
    قارن أيضاً حجم الطلبات الذي يجلبه كل تطبيق. أحياناً تطبيق بعمولة أعلى يجلب ضعف الطلبات.
    </div>
    """, unsafe_allow_html=True)
