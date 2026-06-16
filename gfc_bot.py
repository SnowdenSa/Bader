"""
نظام تداول: الجد – الابن – الحفيد  (GFC: Grand–Father–Child)

القاعدة الذهبية من المحاضرة:
  ❌  لا تشتري في سوق هابط حتى يكسر الجد
  ✅  عند كسر الجد → دخول قوي مع الابن والحفيد

المستويات:
  الجد    = الاتجاه الرئيسي (يومي / أسبوعي)
  الابن   = الاتجاه الثانوي (4 ساعات / يومي)
  الحفيد  = توقيت الدخول   (ساعة / 15 دقيقة)
"""

from __future__ import annotations

import pandas as pd
from dataclasses import dataclass, field
from typing import Literal


# ────────────────────────────────────────────
# 1. أنواع البيانات
# ────────────────────────────────────────────

TrendDir = Literal["UP", "DOWN", "RANGE", "UNKNOWN"]
Zone     = Literal["SUPPORT", "RESISTANCE", "MIDDLE"]
Signal   = Literal["BUY_GRAND_BREAK", "BUY", "SELL_GRAND_BREAK",
                   "SELL", "NO_TRADE", "WAIT"]


@dataclass
class TrendLevel:
    direction : TrendDir
    highs     : list[float]
    lows      : list[float]


@dataclass
class BreakStatus:
    """هل كسر مستوى معين؟ وما هو سعر الكسر؟"""
    broken   : bool
    direction: Literal["UP", "DOWN", "NONE"]
    level    : float   # مستوى الكسر
    price    : float   # السعر الحالي


@dataclass
class GFCResult:
    grand       : TrendLevel
    parent      : TrendLevel
    child       : TrendLevel
    grand_break : BreakStatus
    parent_break: BreakStatus
    price       : float
    support     : float
    resistance  : float
    zone        : Zone
    signal      : Signal
    reason      : str
    action      : str = field(default="")


# ────────────────────────────────────────────
# 2. تحليل الاتجاه
# ────────────────────────────────────────────

def classify_trend(highs: list[float], lows: list[float]) -> TrendDir:
    """
    صاعد  : آخر قمة > قمة قبلها  AND  آخر قاع > قاع قبله
    هابط  : آخر قمة < قمة قبلها  AND  آخر قاع < قاع قبله
    """
    if len(highs) < 2 or len(lows) < 2:
        return "UNKNOWN"
    if highs[-1] > highs[-2] and lows[-1] > lows[-2]:
        return "UP"
    if highs[-1] < highs[-2] and lows[-1] < lows[-2]:
        return "DOWN"
    return "RANGE"


def _swing_points(series: pd.Series, window: int = 3) -> tuple[list, list]:
    v = series.values
    highs, lows = [], []
    for i in range(window, len(v) - window):
        if all(v[i] >= v[i-j] for j in range(1, window+1)) and \
           all(v[i] >= v[i+j] for j in range(1, window+1)):
            highs.append(float(v[i]))
        if all(v[i] <= v[i-j] for j in range(1, window+1)) and \
           all(v[i] <= v[i+j] for j in range(1, window+1)):
            lows.append(float(v[i]))
    return highs[-6:], lows[-6:]


# ────────────────────────────────────────────
# 3. كسر الجد والابن — قلب النظام
# ────────────────────────────────────────────

def detect_break(trend: TrendLevel, price: float,
                 margin: float = 0.005) -> BreakStatus:
    """
    يكتشف كسر مستوى الاتجاه:

    جد/ابن هابط → الكسر = إغلاق فوق آخر قمة منخفضة (highs[-1])
                   هذه هي مقاومة الاتجاه الهابط
    جد/ابن صاعد → الكسر = إغلاق فوق أعلى قمة وصلها الاتجاه (max highs)
                   "كسر الابن" = تجاوز قمة الارتداد
    """
    if trend.direction == "DOWN":
        # آخر قمة منخفضة = سقف الاتجاه الهابط الذي يجب كسره
        level = trend.highs[-1]
        broken = price > level * (1 + margin)
        return BreakStatus(broken, "UP" if broken else "NONE", level, price)

    if trend.direction == "UP":
        # أعلى نقطة وصلها الاتجاه الصاعد = مقاومة ينتظر الجميع كسرها
        level = max(trend.highs)
        broken = price > level * (1 + margin)
        return BreakStatus(broken, "UP" if broken else "NONE", level, price)

    return BreakStatus(False, "NONE", 0.0, price)


# ────────────────────────────────────────────
# 4. الدعم والمقاومة
# ────────────────────────────────────────────

def find_sr(highs: list[float], lows: list[float],
            price: float) -> tuple[float, float]:
    below = [v for v in lows  if v <= price] or lows
    above = [v for v in highs if v >= price] or highs
    support    = max(below) if below else min(lows)
    resistance = min(above) if above else max(highs)
    if support >= resistance:
        support = resistance * 0.97
    return round(support, 4), round(resistance, 4)


def price_zone(price: float, support: float, resistance: float,
               margin: float = 0.02) -> Zone:
    if price <= support * (1 + margin):
        return "SUPPORT"
    if price >= resistance * (1 - margin):
        return "RESISTANCE"
    return "MIDDLE"


# ────────────────────────────────────────────
# 5. شجرة القرار الهرمي
# ────────────────────────────────────────────

def decide(grand: TrendDir, parent: TrendDir, child: TrendDir,
           zone: Zone,
           gb: BreakStatus,    # grand break
           pb: BreakStatus,    # parent break
           ) -> tuple[Signal, str, str]:
    """
    يعيد: (إشارة، سبب، إجراء موصى به)

    ترتيب الأولوية:
      1. كسر الجد  → إشارة دخول كبرى (الأقوى)
      2. كسر الابن → إشارة دخول جيدة (المحاضرة: حتى كسر الابن جيد)
      3. جد صاعد   → متابعة الاتجاه
      4. جد هابط   → انتظار أو بيع فقط
    """

    # ══════════════════════════════════════
    # 🔑 1. كسر الجد — الإشارة الكبرى
    # ══════════════════════════════════════

    if gb.broken:

        if gb.direction == "UP":
            if parent == "UP" and child == "UP":
                return (
                    "BUY_GRAND_BREAK",
                    f"🔑 كسر الجد فوق {gb.level:.4f} + ابن↑ + حفيد↑ ← دخول كبير",
                    f"ادخل شراءً الآن. الهدف: أعلى قمة سابقة. وقف: تحت {gb.level:.4f}",
                )
            if parent == "UP":
                return (
                    "BUY_GRAND_BREAK",
                    f"🔑 كسر الجد فوق {gb.level:.4f} + ابن↑ ← شراء",
                    f"ادخل شراءً. وقف: تحت {gb.level:.4f}",
                )
            return (
                "BUY_GRAND_BREAK",
                f"🔑 كسر الجد فوق {gb.level:.4f} ← شراء (انتظر تأكيد الابن)",
                f"دخول محتاط. وقف: إغلاق تحت {gb.level:.4f}",
            )

        if gb.direction == "DOWN":
            if parent == "DOWN" and child == "DOWN":
                return (
                    "SELL_GRAND_BREAK",
                    f"🔑 كسر الجد تحت {gb.level:.4f} + ابن↓ + حفيد↓ ← بيع كبير",
                    f"ادخل بيعاً الآن. الهدف: أدنى قاع سابق. وقف: فوق {gb.level:.4f}",
                )
            return (
                "SELL_GRAND_BREAK",
                f"🔑 كسر الجد تحت {gb.level:.4f} ← بيع",
                f"ادخل بيعاً. وقف: إغلاق فوق {gb.level:.4f}",
            )

    # ══════════════════════════════════════
    # 📌 2. كسر الابن — إشارة جيدة
    #    (حتى كسر الابن جيد كما ذكر المحاضر)
    # ══════════════════════════════════════

    if pb.broken and not gb.broken:

        if pb.direction == "UP":
            # الابن كسر للأعلى داخل جد هابط → إشارة جيدة لكن بحذر
            if grand == "DOWN":
                return (
                    "BUY",
                    f"📌 كسر الابن فوق {pb.level:.4f} ← إشارة جيدة (جد لا يزال هابطاً)",
                    f"يمكن الدخول بحجم محتاط. الهدف: كسر الجد فوق {gb.level:.4f}. وقف: تحت {pb.level:.4f}",
                )
            # جد صاعد + ابن يكسر → إشارة قوية
            return (
                "BUY",
                f"📌 كسر الابن فوق {pb.level:.4f} + جد↑ ← شراء جيد",
                f"ادخل شراءً. وقف: تحت {pb.level:.4f}",
            )

        if pb.direction == "DOWN":
            if grand == "UP":
                return (
                    "SELL",
                    f"📌 كسر الابن تحت {pb.level:.4f} ← إشارة بيع جيدة (جد لا يزال صاعداً)",
                    f"بيع محتاط. وقف: فوق {pb.level:.4f}",
                )
            return (
                "SELL",
                f"📌 كسر الابن تحت {pb.level:.4f} + جد↓ ← بيع جيد",
                f"ادخل بيعاً. وقف: فوق {pb.level:.4f}",
            )

    # ══════════════════════════════════════
    # 3. جد صاعد (لم ينكسر، ابن لم ينكسر)
    # ══════════════════════════════════════

    if grand == "UP":
        if parent == "UP":
            if child == "UP":
                if zone == "SUPPORT":
                    return "BUY", "جد↑ + ابن↑ + حفيد↑ عند دعم ← شراء", \
                           "ادخل شراءً. وقف: تحت الدعم"
                if zone == "RESISTANCE":
                    return "WAIT", "جد↑ + ابن↑ عند مقاومة ← انتظر الكسر", \
                           "انتظر إغلاق فوق المقاومة"
                return "BUY", "جد↑ + ابن↑ + حفيد↑ ← استمرار", "ادخل أو أضف"
            if child == "DOWN":
                if zone == "SUPPORT":
                    return "BUY", "جد↑ + ابن↑، حفيد عند دعم ← فرصة دخول", \
                           "ادخل شراءً من الدعم"
                return "WAIT", "جد↑ + ابن↑، حفيد هابط ← انتظر الحفيد", ""
            return "WAIT", "جد↑ + ابن↑، حفيد عرضي ← انتظر", ""

        if parent == "DOWN":
            if child == "UP" and zone == "SUPPORT":
                return "BUY", "جد↑، ابن في تصحيح، حفيد↑ من دعم ← محتاط", \
                       "دخول صغير. وقف: تحت الدعم"
            return "WAIT", "جد↑، ابن↓ ← انتظر انتهاء التصحيح", ""

        return "NO_TRADE", "جد↑ والابن عرضي ← لا وضوح", ""

    # ══════════════════════════════════════
    # 4. جد هابط — انتظر الكسر (القاعدة الذهبية)
    # ══════════════════════════════════════

    if grand == "DOWN":
        if parent == "DOWN":
            if child == "DOWN":
                if zone == "RESISTANCE":
                    return "SELL", "جد↓ + ابن↓ + حفيد↓ عند مقاومة ← بيع قوي", \
                           "ادخل بيعاً. وقف: فوق المقاومة"
                if zone == "SUPPORT":
                    return "WAIT", "جد↓ عند دعم ← انتظر كسر الدعم", \
                           "لا تشتري. انتظر إغلاق تحت الدعم"
                return "SELL", "جد↓ + ابن↓ + حفيد↓ ← استمرار هبوط", "بيع"
            if child == "UP":
                if zone == "RESISTANCE":
                    return "SELL", "جد↓ + ابن↓، حفيد ارتداد عند مقاومة ← بيع", \
                           "بيع من المقاومة"
                return "WAIT", "جد↓ + ابن↓، حفيد↑ ← ارتداد مؤقت", \
                       "لا تشتري. انتظر نهايته"
            return "WAIT", "جد↓ + ابن↓ ← انتظر", ""

        if parent == "UP":
            # تصحيح صاعد داخل جد هابط — المبتدئون يخطئون هنا
            if child == "DOWN" and zone == "RESISTANCE":
                return "SELL", \
                       "جد↓، ابن صاعد (تصحيح)، حفيد↓ من مقاومة ← بيع محتاط", \
                       "بيع من المقاومة"
            return "WAIT", \
                   f"⚠️ جد↓، ابن صاعد ← تصحيح. انتظر كسر الجد ({gb.level:.4f}) للشراء", \
                   f"أو كسر الابن ({pb.level:.4f}) للدخول المبكر"

        return "NO_TRADE", "جد↓ والابن عرضي ← انتظر", \
               f"انتظر كسر الجد فوق {gb.level:.4f}"

    # جد عرضي
    return "NO_TRADE", "الجد عرضي ← انتظر تحديد الاتجاه", ""


# ────────────────────────────────────────────
# 6. البوت الرئيسي
# ────────────────────────────────────────────

class GFCBot:
    """
    بوت GFC — نظام الجد–الابن–الحفيد

    الاستخدام:
        bot = GFCBot()
        bot.report_manual("BTC", grand_highs=[...], grand_lows=[...], ...)
    """

    def analyze_manual(
        self,
        grand_highs  : list[float],
        grand_lows   : list[float],
        parent_highs : list[float],
        parent_lows  : list[float],
        child_highs  : list[float],
        child_lows   : list[float],
        current_price: float,
    ) -> GFCResult:

        grand  = TrendLevel(classify_trend(grand_highs,  grand_lows),
                            grand_highs, grand_lows)
        parent = TrendLevel(classify_trend(parent_highs, parent_lows),
                            parent_highs, parent_lows)
        child  = TrendLevel(classify_trend(child_highs,  child_lows),
                            child_highs, child_lows)

        gb = detect_break(grand,  current_price)   # كسر الجد
        pb = detect_break(parent, current_price)   # كسر الابن

        support, resistance = find_sr(
            parent_highs + child_highs,
            parent_lows  + child_lows,
            current_price,
        )
        zone = price_zone(current_price, support, resistance)

        signal, reason, action = decide(
            grand.direction, parent.direction, child.direction, zone, gb, pb
        )

        return GFCResult(grand, parent, child, gb, pb,
                         current_price, support, resistance,
                         zone, signal, reason, action)

    def report_manual(self, ticker: str, **kwargs) -> GFCResult:
        r = self.analyze_manual(**kwargs)
        self._print(ticker, r)
        return r

    def _print(self, ticker: str, r: GFCResult) -> None:
        ARROWS = {
            "UP": "↑ صاعد", "DOWN": "↓ هابط",
            "RANGE": "↔ عرضي", "UNKNOWN": "؟ غير محدد",
        }
        ICONS = {
            "BUY_GRAND_BREAK" : "🚀  شراء — كسر الجد",
            "BUY"             : "🟢  شراء",
            "SELL_GRAND_BREAK": "💣  بيع — كسر الجد",
            "SELL"            : "🔴  بيع",
            "NO_TRADE"        : "⚪  لا تداول",
            "WAIT"            : "🟡  انتظار",
        }
        bar = "═" * 54

        def break_str(b, label: str) -> str:
            if b.level == 0.0:
                return f"  {label}: ─ (عرضي)"
            if b.broken:
                return f"  {label}: ✅ مكسور ({b.direction}) | مستوى: {b.level:.4f}"
            return f"  {label}: ❌ لم يُكسر | مستوى الكسر: {b.level:.4f}"

        print(f"\n{bar}")
        print(f"   تحليل GFC  ←  {ticker}")
        print(f"{bar}")
        print(f"  الجد    ({r.grand.direction:>7}): {ARROWS[r.grand.direction]}")
        print(f"  الابن   ({r.parent.direction:>7}): {ARROWS[r.parent.direction]}")
        print(f"  الحفيد  ({r.child.direction:>7}): {ARROWS[r.child.direction]}")
        print(f"  {'─'*50}")
        print(break_str(r.grand_break,  "🔑 كسر الجد  "))
        print(break_str(r.parent_break, "📌 كسر الابن "))
        print(f"  {'─'*50}")
        print(f"  السعر    : {r.price:.4f}")
        print(f"  الدعم    : {r.support:.4f}")
        print(f"  المقاومة : {r.resistance:.4f}")
        print(f"  المنطقة  : {r.zone}")
        print(f"  {'─'*50}")
        print(f"  {ICONS[r.signal]}")
        print(f"  {r.reason}")
        if r.action:
            print(f"  ➜  {r.action}")
        print(f"{bar}\n")

    # ── اختياري: بيانات حقيقية ──
    def analyze_live(self, ticker: str, market: str = "crypto") -> GFCResult:
        """يسحب بيانات من yfinance (يحتاج إنترنت)"""
        try:
            import yfinance as yf
        except ImportError:
            raise ImportError("نفّذ: pip install yfinance")

        TF = {
            "crypto": ("1d", "4h", "1h"),
            "stock" : ("1d", "4h", "1h"),
            "forex" : ("1wk","1d", "4h"),
        }
        gtf, ptf, ctf = TF.get(market, TF["crypto"])

        def _fetch(period, interval):
            df = yf.download(ticker, period=period, interval=interval,
                             progress=False, auto_adjust=True)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            return df

        gdf, pdf, cdf = _fetch("6mo", gtf), _fetch("60d", ptf), _fetch("14d", ctf)

        def _sp(df, w):
            h, l = _swing_points(df["High"], w), _swing_points(df["Low"], w)
            return (h[0] or [float(df["High"].max())],
                    l[1] or [float(df["Low"].min())])

        gh, gl = _sp(gdf, 4)
        ph, pl = _sp(pdf, 3)
        ch, cl = _sp(cdf, 2)
        return self.analyze_manual(gh, gl, ph, pl, ch, cl,
                                   float(cdf["Close"].iloc[-1]))
