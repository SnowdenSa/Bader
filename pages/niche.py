import streamlit as st


def render():
    st.title("🔍 رادار التخصص والمحيط الأزرق")
    st.caption("لا تغرق في المحيطات الحمراء المطحونة. ابحث عن السوق المنسي الذي يتعطش لحلك.")
    st.markdown("---")

    st.markdown("""
    <div class="info-box">
    <b>القانون الأساسي:</b> بدل ما تبيع منتجاً عاماً للجميع في سوق مطحون بالأسعار،
    اذهب لشريحة منسية ومحددة. قد يكون عدد زبائنها أقل، لكنهم متعطشون للحل
    ولديهم استعداد عالٍ للدفع لأنهم لا يجدون بديلاً يخدمهم بجودة.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📊 اختبار تصنيف السوق")
    col1, col2 = st.columns(2)
    with col1:
        competitor_count = st.selectbox(
            "كم عدد المنافسين المباشرين في منطقتك؟",
            ["1 - 3 منافسين (قليل)", "4 - 10 منافسين (متوسط)", "أكثر من 10 (كثير جداً)"],
        )
        profit_margin = st.selectbox(
            "هامش الربح السائد في هذا النشاط؟",
            ["أعلى من 30% (مريح)", "10% - 30% (متوسط)", "أقل من 10% (ضئيل)"],
        )
    with col2:
        competitor_tech = st.selectbox(
            "هل المنافسون يستخدمون التكنولوجيا والتسويق الحديث؟",
            ["لا — تقليديون جداً", "بعضهم فقط", "نعم — معظمهم متطور"],
        )
        demand_growth = st.selectbox(
            "هل الطلب على هذا النشاط ينمو أم ثابت؟",
            ["ينمو بشكل واضح", "ثابت نسبياً", "في تراجع"],
        )

    st.markdown("---")
    st.subheader("🗺️ نتيجة تصنيف سوقك")

    red_score = 0
    if "كثير" in competitor_count:
        red_score += 2
    elif "متوسط" in competitor_count:
        red_score += 1
    if "ضئيل" in profit_margin:
        red_score += 2
    elif "متوسط" in profit_margin:
        red_score += 1
    if "متطور" in competitor_tech:
        red_score += 1
    if "تراجع" in demand_growth:
        red_score += 2

    if red_score >= 4:
        st.markdown("""
        <div class="danger-box">
        🔴 <b>محيط أحمر شرس — ابتعد!</b><br>
        هذا السوق مكتظ بالمنافسة وهوامش الربح ضئيلة.
        دخوله بدون ميزة تنافسية قوية جداً هو انتحار تجاري.
        <b>التوصية:</b> ابحث عن نيتش متخصص داخل هذا القطاع أو انتقل لنشاط مختلف.
        </div>
        """, unsafe_allow_html=True)
    elif red_score >= 2:
        st.markdown("""
        <div class="warning-box">
        🟡 <b>سوق متوسط — ادخل بحذر وتميز</b><br>
        يمكن الدخول بشرط امتلاك ميزة تنافسية واضحة.
        ركز على تميز الخدمة أو التخصص في شريحة معينة.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="success-box">
        🔵 <b>محيط أزرق واعد — تقدم!</b><br>
        هذا السوق فيه فرصة حقيقية. المنافسة منخفضة والطلب جيد.
        ادخل بسرعة قبل أن يكتشفه الآخرون وابنِ موقعك.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🎯 أداة بناء التخصص الذكي (Niche Builder)")
    st.markdown("حدد تخصصك الدقيق بالإجابة على الأسئلة التالية:")

    col3, col4 = st.columns(2)
    with col3:
        target_segment = st.text_input("من هي شريحتك المحددة جداً؟",
                                        placeholder="مثال: أصحاب الأوزان الزائدة، المطاعم الصغيرة، المزارع العائلية")
        real_pain = st.text_area("ما هو ألمهم الحقيقي الذي يعانون منه في السوق الحالي؟",
                                  placeholder="مثال: لا يجدون ملابس بمقاسات مريحة وتصاميم عصرية")
    with col4:
        why_you = st.text_area("لماذا سيتجاهلون المنافس الكبير ويأتون إليك؟",
                                placeholder="مثال: لأن المنافس يبيع للجميع ولا يهتم بتفاصيلهم الخاصة")
        your_edge = st.text_input("ما ميزتك التي لا يمكن للمنافس نسخها خلال 24 ساعة؟",
                                   placeholder="مثال: خبرة 5 سنوات، خلطة سرية، علاقات مع الموردين")

    if st.button("🔍 تحليل تخصصي"):
        if target_segment and real_pain and why_you and your_edge:
            st.markdown(f"""
            <div class="success-box">
            <b>✅ ملخص استراتيجية التخصص:</b><br>
            • <b>شريحتك:</b> {target_segment}<br>
            • <b>مشكلتهم:</b> {real_pain}<br>
            • <b>سبب اختيارهم لك:</b> {why_you}<br>
            • <b>ميزتك التنافسية:</b> {your_edge}
            </div>
            """, unsafe_allow_html=True)
            st.success("🏆 ممتاز! تخصصك واضح وقابل للتطبيق. انتقل الآن للشاشة التالية.")
        else:
            st.warning("⚠️ أكمل جميع الحقول للحصول على التحليل الكامل.")

    st.markdown("---")
    st.markdown("""
    <div class="info-box">
    <b>أمثلة على التخصص الذكي:</b><br>
    • بدلاً من "ملابس عامة" → ملابس الأحجام الكبيرة للرجال<br>
    • بدلاً من "مطعم عام" → مطعم متخصص بالمأكولات الصحية للرياضيين<br>
    • بدلاً من "ورشة سيارات" → متخصص فقط في صيانة سيارات Toyota و Lexus<br>
    • بدلاً من "خياط" → تفصيل الثياب الرسمية للأعراس فقط
    </div>
    """, unsafe_allow_html=True)
