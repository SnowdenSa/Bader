import streamlit as st


def render():
    st.title("🛠️ فلتر التأسيس الرشيق وهندسة البدائل الأرخص")
    st.caption("أنت لست ماركة عالمية. أنت تبحث عن تقليل التكاليف وزيادة الربح. وفّر في التجهيز!")
    st.markdown("---")

    st.markdown("""
    <div class="info-box">
    <b>مبدأ التاجر الشاطر:</b> ليش تشتري أثاث وأدوات تعيش 1000 سنة لمشروع في بدايته؟
    ابحث عن المستعمل في موقع <b>حراج</b>، وعن البدائل الصينية الاقتصادية التي توفر عليك
    5 و 10 ريالات في كل قطعة وتؤدي نفس الغرض تماماً.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📥 تكاليف التجهيز المقترحة (بالأسعار الجديدة)")
    col1, col2 = st.columns(2)
    with col1:
        decor_cost = st.number_input("الديكور والواجهة واللوحة الخارجية (ريال):", min_value=0, value=40000, step=5000)
        shelves_cost = st.number_input("الرفوف والاستاندات وطاولات العرض — جديد (ريال):", min_value=0, value=25000, step=2000)
    with col2:
        appliances_cost = st.number_input("الأجهزة والمعدات الأساسية — جديد (ريال):", min_value=0, value=35000, step=5000)
        small_items = st.number_input("الأدوات الصغيرة والقطع الداخلية (ريال):", min_value=0, value=10000, step=1000)

    total_original = decor_cost + shelves_cost + appliances_cost + small_items

    lean_decor = decor_cost * 0.50
    lean_shelves = shelves_cost * 0.40
    lean_appliances = appliances_cost * 0.60
    lean_small = small_items * 0.50
    total_lean = lean_decor + lean_shelves + lean_appliances + lean_small
    saved = total_original - total_lean

    st.markdown("---")
    st.subheader("📊 خطة التجهيز الرشيق المقترحة")
    c1, c2, c3 = st.columns(3)
    c1.metric("تكلفة الجديد (قبل التحسين)", f"{total_original:,} ﷼")
    c2.metric("تكلفة الرشيق (بعد التحسين)", f"{int(total_lean):,} ﷼")
    c3.metric("الكاش الموفر لصندوق الطوارئ", f"{int(saved):,} ﷼")

    st.markdown("---")
    st.subheader("💡 كيف تطبق هندسة البدائل؟")

    with st.expander("🎨 الديكور والواجهة"):
        st.markdown(f"""
        **التوفير المحقق: {int(decor_cost - lean_decor):,} ريال**
        - بدّل الجبس المعقد بصبغ نظيف عالي الجودة
        - إضاءة LED بسيطة وعملية بدلاً من الإضاءة المسرحية
        - واجهة نظيفة بسيطة تعكس هويتك بدلاً من الزخارف الباهظة
        - كاش الديكور الموفر يذهب للبضاعة والتسويق
        """)

    with st.expander("🗄️ الرفوف والاستاندات"):
        st.markdown(f"""
        **التوفير المحقق: {int(shelves_cost - lean_shelves):,} ريال**
        - افتح **موقع حراج** وابحث عن تصفية محلات مشابهة
        - الأثاث الحديدي المستعمل النظيف يُغسل ويبدو كالجديد
        - محلات أغلقت تبيع معداتها بنصف السعر
        - العميل لن يسألك: "هل هذا الرف جديد؟"
        """)

    with st.expander("⚙️ الأجهزة والمعدات"):
        st.markdown(f"""
        **التوفير المحقق: {int(appliances_cost - lean_appliances):,} ريال**
        - ابحث عن ماركات اقتصادية كورية أو صينية بضمان ساري
        - استعمل بضمان من محلات الضمان الموثوقة
        - لا تشترِ أجهزة "خارقة لـ 10 سنوات" — اشترِ ما يمشّك 3 سنوات
        """)

    with st.expander("🔧 الأدوات الصغيرة والقطع"):
        st.markdown(f"""
        **التوفير المحقق: {int(small_items - lean_small):,} ريال**
        - انزل لأسواق الجملة (الفيصلية، الباطحاء، الديرة)
        - لكل قطعة تحتاجها هناك بديل صيني بـ 5 - 10 ريالات أقل
        - الفروقات الصغيرة تتراكم لتصبح عشرات الآلاف
        - لا تشتري الكميات الكبيرة من أول يوم — ابدأ بما تحتاجه فعلاً
        """)

    st.markdown("---")
    st.markdown(f"""
    <div class="success-box">
    🟢 <b>الكاش الموفر ({int(saved):,} ريال) هو وقود مشروعك الحقيقي:</b><br>
    هذا المبلغ يُرحَّل فوراً إلى صندوق الطوارئ لتمويل الرواتب والإيجار في أشهر الجفاف الأولى،
    أو لشراء بضاعة إضافية، أو لحملات التسويق الرقمي بجوالك.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🛡️ قاعدة السيادة التشغيلية")
    st.markdown("""
    قبل اختيار أي عمال، أجب على هذا السؤال الحاسم:
    """)

    knows_trade = st.radio(
        "هل تعرف أسرار الصنعة وتقدر تقف مكان العامل لو غاب؟",
        [
            "✅ نعم — أنا فاهم الصنعة وأقدر أغطي مكانه فوراً",
            "❌ لا — أنا معتمد عليه بالكامل وهو يعرف الخلطة",
            "🔄 لا، لكن عندي بديل جاهز ومدرب تحت الطلب",
        ],
    )

    if "❌" in knows_trade:
        st.markdown("""
        <div class="danger-box">
        🛑 <b>مشروعك رهينة — خطر الشخص الواحد!</b><br>
        إذا ترك العامل أو غضب، ينهار محلك فوراً. الحل:<br>
        1. تعلم الصنعة بنفسك في المشروع المصغر (بايلوت)<br>
        2. وثّق الوصفات والأنظمة كتابياً بتفصيل دقيق<br>
        3. درّب عاملاً احتياطياً على نفس الأسلوب
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="success-box">
        🟢 <b>سيادة تشغيلية كاملة!</b><br>
        أنت في وضع أمان. العمال يعلمون أن صاحب الحلال معلم ولا يمكن ابتزازه.
        </div>
        """, unsafe_allow_html=True)
