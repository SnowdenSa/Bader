import streamlit as st


def render():
    st.title("🚗 فحص الموقع والجاهزية الإنشائية")
    st.caption("وفّر 50,000 ريال بمجرد النظر الصحيح. الفحص البصري السباعي قبل توقيع عقد الإيجار.")
    st.markdown("---")

    st.markdown("""
    <div class="info-box">
    <b>القاعدة الميدانية:</b> هناك محل تجهيزه لا يتعدى 3,000 - 4,000 ريال (رشة بوية ونظافة)،
    ومحل بجانبه بنفس النشاط يكلف 50,000 ريال! الفرق في الحالة الإنشائية والتشطيبات.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🔍 الفحص البصري السباعي للمحل")
    st.markdown("قف داخل المحل المعروض وضع علامة ✓ أمام كل عنصر جاهز وسليم:")

    col1, col2 = st.columns(2)
    with col1:
        roof_ok = st.checkbox("🏗️ **السقف:** سليم ومغطى ولا يحتاج جبس أو ترميم")
        floor_ok = st.checkbox("🧱 **الأرضية:** بلاط/سيراميك نظيف مناسب للنشاط")
        electricity_ok = st.checkbox("⚡ **الكهرباء:** طبلون جاهز يتحمل المكيفات والآلات")
        water_ok = st.checkbox("💧 **المياه والسباكة:** تمديدات سليمة بدون تهريبات")
    with col2:
        ac_ok = st.checkbox("❄️ **مكان التكييف:** فتحات جاهزة لا تحتاج تكسير جدران")
        glass_ok = st.checkbox("🪟 **القزاز والأبواب:** الواجهة الزجاجية والباب سليمان")
        sign_ok = st.checkbox("📋 **مكان اللوحة:** مناسب لواجهة العمارة وشروط البلدية")

    ready_points = sum([roof_ok, floor_ok, electricity_ok, water_ok, ac_ok, glass_ok, sign_ok])
    estimated_repair = (7 - ready_points) * 8000

    st.markdown("---")
    st.subheader("📊 تقييم الجاهزية الإنشائية")
    col3, col4 = st.columns(2)
    col3.metric("عناصر جاهزة", f"{ready_points} / 7")
    col4.metric("تكلفة إصلاح العيوب (تقديري)", f"{estimated_repair:,} ﷼")

    if ready_points == 7:
        st.markdown("""
        <div class="success-box">
        🟢 <b>محل لُقطة جاهز تماماً (Turnkey)!</b><br>
        نجح في الفحص 100%. تجهيزه لن يكلفك أكثر من <b>3,000 - 4,000 ريال</b> فقط.
        توكل على الله إذا كان السعر والإيجار مناسبين.
        </div>
        """, unsafe_allow_html=True)
    elif ready_points >= 4:
        st.markdown(f"""
        <div class="warning-box">
        ⚠️ <b>محل يحتاج ترميم متوسط:</b><br>
        لديك {7 - ready_points} عناصر غير جاهزة. التكلفة التقديرية للإصلاح: <b>{estimated_repair:,} ريال</b>.<br>
        <b>نصيحة:</b> تفاوض مع المالك لخصم هذا المبلغ من الإيجار السنوي
        أو اطلب شهرين سماح بدون إيجار للتشطيب.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="danger-box">
        🛑 <b>فخ مالي — المحل عبارة عن عظم وركام!</b><br>
        أغلب العناصر تالفة. التكلفة التقديرية: <b>{estimated_repair:,} ريال</b> كحد أدنى
        قبل أن تضع رفاً واحداً للبضاعة!<br>
        <b>القرار:</b> لا تستأجر هنا إلا إذا كان الإيجار رخيصاً جداً ليعوض هذا الهدر.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🅿️ فحص الرؤية والوصول")
    col5, col6 = st.columns(2)
    with col5:
        has_parking = st.checkbox("✅ تتوفر مواقف سيارات كافية أمام المحل")
        is_visible = st.checkbox("✅ المحل مشاهَد وباين وواضح للمشاة والسيارات")
        is_corner = st.checkbox("✅ يقع على زاوية أو في شارع رئيسي")

    visibility_score = sum([has_parking, is_visible, is_corner])
    with col6:
        if visibility_score == 3:
            st.markdown("""
            <div class="success-box">
            🟢 <b>موقع مثالي — تدفق الزبائن العفوي مضمون!</b><br>
            المحل مكشوف ومريح للوصول. الزبون سيجدك بسهولة.
            </div>
            """, unsafe_allow_html=True)
        elif visibility_score >= 1:
            st.markdown("""
            <div class="warning-box">
            ⚠️ <b>موقع متوسط الوضوح:</b><br>
            يحتاج دعم تسويق رقمي قوي (Google Maps، سناب، تيك توك)
            لجلب الزبائن الذين لن يجدوك عفوياً.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="danger-box">
            🛑 <b>موقع أعمى — خطر تشغيلي عالٍ!</b><br>
            بدون مواقف وبدون رؤية، الزبون لن يأتيك. أنت مجبر على
            <b>التسويق الرقمي الثقيل</b> أو اختيار موقع آخر.
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div class="info-box">
    <b>تذكر:</b> اذا كان الموقع بعيد وغير واضح،
    إيجاره يجب أن يكون رخيصاً جداً لتوفير كاش لحملات التسويق الرقمي
    التي ستسحب الزبائن إليك بالاسم.
    </div>
    """, unsafe_allow_html=True)
