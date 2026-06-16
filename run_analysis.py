"""
أمثلة عملية على نظام GFC — الجد–الابن–الحفيد

يغطي الحالات التي ناقشناها:
  - جد هابط (11→4)، ابن صاعد (4→6.55)، حفيد هابط عند 6.16-6.33
  - أربع سيناريوهات إضافية للاختبار
"""

from gfc_bot import GFCBot

bot = GFCBot()

# ══════════════════════════════════════════════════════
#  الحالة الأساسية من المثال الحقيقي
# ══════════════════════════════════════════════════════

# الجد هابط: من قمة 11 إلى قاع 4
GRAND_HIGHS = [11.0, 9.0, 7.0, 5.5]
GRAND_LOWS  = [10.0, 8.0, 6.0, 4.0]

# الابن صاعد: من 4 نحو 6.55
PARENT_HIGHS = [4.5, 5.2, 6.0, 6.55]
PARENT_LOWS  = [4.0, 4.4, 5.0, 5.8]

# الحفيد — 4 سيناريوهات مختلفة

# 1. حفيد هابط عند دعم 6.16  (الوضع الحالي)
bot.report_manual(
    "سهم-وضع-حالي",
    grand_highs=GRAND_HIGHS, grand_lows=GRAND_LOWS,
    parent_highs=PARENT_HIGHS, parent_lows=PARENT_LOWS,
    child_highs=[6.55, 6.45, 6.33],
    child_lows =[6.40, 6.28, 6.16],
    current_price=6.18,
)

# 2. حفيد كسر الدعم 6.16 ونزل إلى 5.90  (سيناريو هبوط)
bot.report_manual(
    "سهم-كسر-دعم",
    grand_highs=GRAND_HIGHS, grand_lows=GRAND_LOWS,
    parent_highs=PARENT_HIGHS, parent_lows=PARENT_LOWS,
    child_highs=[6.33, 6.20, 6.10],
    child_lows =[6.18, 6.05, 5.90],
    current_price=5.95,
)

# 3. حفيد كسر المقاومة 6.55 وصعد إلى 6.90  (سيناريو صعود)
bot.report_manual(
    "سهم-كسر-مقاومة",
    grand_highs=GRAND_HIGHS, grand_lows=GRAND_LOWS,
    parent_highs=PARENT_HIGHS, parent_lows=PARENT_LOWS,
    child_highs=[6.55, 6.70, 6.90],
    child_lows =[6.40, 6.55, 6.65],
    current_price=6.88,
)

# 4. حفيد ارتد من الدعم وبدأ الصعود  (فرصة شراء داخل تصحيح)
bot.report_manual(
    "سهم-ارتداد-دعم",
    grand_highs=GRAND_HIGHS, grand_lows=GRAND_LOWS,
    parent_highs=PARENT_HIGHS, parent_lows=PARENT_LOWS,
    child_highs=[6.16, 6.22, 6.30],
    child_lows =[6.10, 6.14, 6.20],
    current_price=6.28,
)

# 5. جد صاعد — عكس الحالة (للمقارنة)
bot.report_manual(
    "BTC-سوق-صاعد",
    grand_highs=[40000, 55000, 70000, 95000],
    grand_lows =[38000, 48000, 62000, 85000],
    parent_highs=[95000, 92000, 90000],
    parent_lows =[90000, 88000, 86000],
    child_highs=[86000, 87500, 89000],
    child_lows =[85500, 86500, 88000],
    current_price=88200,
)
