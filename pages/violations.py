import streamlit as st


def render():
    st.title("🛡️ رادار المخالفات والـ Self-Audit الأسبوعي")
    st.caption("المخالفة لا تُعلن قبل الزيارة. راجع نفسك أسبوعياً قبل أن يراجعك المفتش.")
    st.markdown("---")

    st.markdown("""
    <div class="warning-box">
    <b>القانون الذي يجهله 80% من التجار الجدد:</b><br>
    المفتش لا يُحذّرك. الغرامة تأتي فورية وقد تُغلق المحل. كل أسبوع خصص 15 دقيقة
    لمراجعة هذا الـ Checklist بنفسك قبل أن يأتي من يراجعك.
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "🏪 وزارة التجارة",
        "🧾 ZATCA الضريبة",
        "👷 العمالة والتأمينات",
        "🏙️ البلدية والصحة",
    ])

    with tab1:
        st.subheader("✅ Checklist وزارة التجارة")
        st.markdown("ضع علامة على كل بند تأكدت منه هذا الأسبوع:")

        cr_valid = st.checkbox("📄 السجل التجاري ساري وغير منتهي الصلاحية")
        prices_posted = st.checkbox("🏷️ أسعار جميع المنتجات معروضة بوضوح (تعليق السعر إلزامي)")
        no_misleading = st.checkbox("🚫 لا يوجد إعلان أو عرض مضلل على واجهة المحل أو السوشيال ميديا")
        warranty_clear = st.checkbox("🔄 شروط الاستبدال والاسترجاع مكتوبة وواضحة للعميل")
        cr_displayed = st.checkbox("📋 رقم السجل التجاري مُعلَّق داخل المحل في مكان ظاهر")
        origin_labeled = st.checkbox("🌍 منشأ البضاعة مذكور على المنتجات (Made in ...)")

        score1 = sum([cr_valid, prices_posted, no_misleading, warranty_clear, cr_displayed, origin_labeled])
        st.markdown(f"**النتيجة: {score1}/6**")

        if score1 == 6:
            st.success("🟢 ممتاز — أنت بعيد عن مخالفات وزارة التجارة هذا الأسبوع")
        elif score1 >= 4:
            st.warning(f"⚠️ يوجد {6 - score1} نقاط تحتاج معالجة فورية قبل أي زيارة تفتيشية")
        else:
            st.error(f"🛑 خطر عالٍ — {6 - score1} مخالفات محتملة. عالجها اليوم قبل الغد")

        with st.expander("💡 أكثر مخالفات وزارة التجارة شيوعاً والغرامات"):
            st.markdown("""
            | المخالفة | الغرامة التقديرية |
            |----------|------------------|
            | عدم عرض الأسعار | 1,000 - 5,000 ﷼ |
            | إعلان مضلل | 10,000 - 50,000 ﷼ |
            | عدم قبول الاسترجاع | 1,000 - 5,000 ﷼ |
            | السجل التجاري منتهٍ | إغلاق فوري |
            | عدم إظهار رقم السجل | 500 - 2,000 ﷼ |
            """)

    with tab2:
        st.subheader("✅ Checklist ZATCA والفوترة الإلكترونية")

        invoicing_system = st.checkbox("🧾 نظام الفوترة الإلكترونية (فاتورة) مُفعَّل ومعتمد من ZATCA")
        vat_filed = st.checkbox("📊 الإقرار الضريبي الأخير مُقدَّم في موعده")
        vat_registered = st.checkbox("✅ المنشأة مسجلة في ضريبة القيمة المضافة (إذا كانت الإيرادات > 375,000 ﷼)")
        prices_with_vat = st.checkbox("🔢 أسعار المنتجات تشمل الضريبة أو تُظهرها بوضوح")
        records_kept = st.checkbox("📁 فواتير الشراء والبيع محفوظة لمدة 5 سنوات")

        score2 = sum([invoicing_system, vat_filed, vat_registered, prices_with_vat, records_kept])
        st.markdown(f"**النتيجة: {score2}/5**")

        if score2 == 5:
            st.success("🟢 ممتاز — امتثال ضريبي كامل")
        elif score2 >= 3:
            st.warning(f"⚠️ يوجد {5 - score2} نقاط ضريبية تحتاج مراجعة")
        else:
            st.error(f"🛑 تعرضك لغرامات ZATCA مرتفع جداً — عالج هذا فوراً")

        with st.expander("💡 غرامات ZATCA الشائعة"):
            st.markdown("""
            | المخالفة | الغرامة |
            |----------|---------|
            | عدم التسجيل في VAT | 10,000 ﷼ |
            | التأخر في تقديم الإقرار | 5 - 25% من الضريبة |
            | عدم استخدام فاتورة إلكترونية | 1,000 ﷼ عن كل فاتورة |
            | عدم الاحتفاظ بالسجلات | 10,000 ﷼ |
            """)

    with tab3:
        st.subheader("✅ Checklist العمالة والتأمينات والرواتب")

        salaries_via_medad = st.checkbox("💳 رواتب هذا الشهر مُودَّعة عبر منصة مدد في موعدها")
        iqama_valid = st.checkbox("🪪 إقامات جميع العمال سارية وغير منتهية")
        gosi_registered = st.checkbox("🛡️ جميع العمال مسجلون في التأمينات الاجتماعية GOSI")
        nitaqat_ok = st.checkbox("📊 نسبة السعودة (نطاقات) في المنطقة الخضراء أو فوقها")
        contracts_signed = st.checkbox("📝 عقود العمل موقّعة مع جميع العمال وموثّقة في قوى")
        work_permits = st.checkbox("✅ تصاريح العمل (قوى) سارية لجميع العمال")

        score3 = sum([salaries_via_medad, iqama_valid, gosi_registered, nitaqat_ok, contracts_signed, work_permits])
        st.markdown(f"**النتيجة: {score3}/6**")

        if score3 == 6:
            st.success("🟢 ممتاز — ملف العمالة نظيف ومحمي")
        elif score3 >= 4:
            st.warning(f"⚠️ {6 - score3} مخالفات عمالية محتملة تستحق تدخلاً سريعاً")
        else:
            st.error(f"🛑 خطر عالٍ جداً — مشاكل في ملف العمالة قد تُجمّد نشاطك")

        with st.expander("💡 عواقب مخالفات العمالة"):
            st.markdown("""
            | المخالفة | العقوبة |
            |----------|---------|
            | التأخر في الراتب (مدد) | تجميد التأشيرات فوراً |
            | إقامة منتهية | 10,000 ﷼ + ترحيل العامل |
            | عدم التسجيل في GOSI | غرامة + فائدة تأخير |
            | نطاقات أحمر | إيقاف الخدمات الحكومية |
            | عامل بدون عقد في قوى | 10,000 ﷼ |
            """)

    with tab4:
        st.subheader("✅ Checklist البلدية والصحة والسلامة")

        balady_valid = st.checkbox("🏢 رخصة البلدية سارية وغير منتهية")
        fire_safety = st.checkbox("🔥 طفايات الحريق حاضرة وصالحة وضمن تاريخ الصيانة")
        health_cert_workers = st.checkbox("💉 شهادات صحية لجميع العاملين في الغذاء سارية (إن كان نشاطاً غذائياً)")
        expiry_dates = st.checkbox("📅 تواريخ انتهاء جميع المنتجات تحت المراقبة اليومية")
        clean_storage = st.checkbox("🧹 مخزن البضاعة نظيف ومنظم ومرفوع عن الأرض")
        no_unlicensed_workers = st.checkbox("🚫 لا يوجد عمال بدون هوية أو بدون تصريح في المحل")

        score4 = sum([balady_valid, fire_safety, health_cert_workers, expiry_dates, clean_storage, no_unlicensed_workers])
        st.markdown(f"**النتيجة: {score4}/6**")

        if score4 == 6:
            st.success("🟢 ممتاز — محلك جاهز لأي زيارة تفتيشية مفاجئة")
        elif score4 >= 4:
            st.warning(f"⚠️ {6 - score4} نقاط تحتاج إصلاحاً قبل الزيارة التالية")
        else:
            st.error(f"🛑 خطر إغلاق عالٍ — البلدية أو الصحة قد تُغلق المحل فوراً")

        with st.expander("💡 أسباب الإغلاق الفوري الشائعة"):
            st.markdown("""
            | السبب | الإجراء |
            |-------|---------|
            | رخصة بلدية منتهية | إغلاق + غرامة يومية |
            | منتجات منتهية الصلاحية | مصادرة + 50,000 ﷼ |
            | غياب طفايات الحريق | إغلاق حتى التصحيح |
            | عامل أجنبي بلا تصريح | 10,000 ﷼ + ترحيل |
            | مخالفة اشتراطات صحية | إغلاق فوري |
            """)

    st.markdown("---")
    st.subheader("📊 ملخص التدقيق الأسبوعي")

    total_score = score1 + score2 + score3 + score4
    max_score = 23

    col1, col2 = st.columns(2)
    col1.metric("نقاط الامتثال الكلية", f"{total_score} / {max_score}")
    compliance_pct = (total_score / max_score) * 100
    col2.metric("نسبة الامتثال", f"{compliance_pct:.0f}%")

    if compliance_pct == 100:
        st.markdown("""
        <div class="success-box">
        🟢 <b>امتثال كامل 100% — محلك محمي تماماً هذا الأسبوع!</b><br>
        استمر على هذا النهج. الالتزام الوقائي أرخص بكثير من الغرامات العلاجية.
        </div>
        """, unsafe_allow_html=True)
    elif compliance_pct >= 75:
        st.markdown(f"""
        <div class="warning-box">
        ⚠️ <b>امتثال جيد لكن يوجد ثغرات:</b><br>
        نسبة امتثالك {compliance_pct:.0f}%. راجع البنود الغير محددة وعالجها قبل نهاية هذا الأسبوع.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="danger-box">
        🛑 <b>مستوى مخاطرة عالٍ جداً!</b><br>
        نسبة امتثالك {compliance_pct:.0f}% فقط. أنت تشتغل على حافة الغرامات والإغلاق.
        أوقف كل شيء وعالج النقاط الحمراء اليوم — قبل أي زيارة تفتيشية.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("💰 حاسبة تقدير الغرامات المحتملة")
    st.markdown("قدّر الخسارة المالية إذا جاء المفتش اليوم:")

    potential_fine = (max_score - total_score) * 3000
    st.metric("تقدير الغرامات المحتملة (إذا جاء المفتش الآن)", f"{potential_fine:,} ﷼")
    st.caption("* التقدير تقريبي — الغرامات الفعلية تختلف حسب نوع المخالفة وتكرارها")
