"""
نظام تداول: الجد – الابن – الحفيد  (GFC: Grand–Father–Child)

يدعم وضعين:
  1. بيانات يدوية  — تُدخل القمم والقيعان مباشرة
  2. بيانات حقيقية — يسحب من yfinance (يحتاج إنترنت)
"""

from __future__ import annotations

import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Literal


# ────────────────────────────────────────────
# 1. أنواع البيانات
# ────────────────────────────────────────────

TrendDir  = Literal["UP", "DOWN", "RANGE", "UNKNOWN"]
Zone      = Literal["SUPPORT", "RESISTANCE", "MIDDLE"]
Signal    = Literal["BUY", "SELL", "NO_TRADE", "WAIT"]


@dataclass
class TrendLevel:
    direction : TrendDir
    highs     : list[float]
    lows      : list[float]
    last_price: float = 0.0


@dataclass
class GFCResult:
    grand    : TrendLevel
    parent   : TrendLevel
    child    : TrendLevel
    price    : float
    support  : float
    resistance: float
    zone     : Zone
    signal   : Signal
    reason   : str


# ────────────────────────────────────────────
# 2. تحليل الاتجاه من قمم وقيعان
# ────────────────────────────────────────────

def classify_trend(highs: list[float], lows: list[float]) -> TrendDir:
    """
    يحدد الاتجاه بقراءة آخر قمتين وآخر قاعين
    صاعد  : قمة أعلى + قاع أعلى
    هابط  : قمة أقل  + قاع أقل
    عرضي  : باقي الحالات
    """
    if len(highs) < 2 or len(lows) < 2:
        return "UNKNOWN"

    hh = highs[-1] > highs[-2]   # higher high
    hl = lows[-1]  > lows[-2]    # higher low
    lh = highs[-1] < highs[-2]   # lower high
    ll = lows[-1]  < lows[-2]    # lower low

    if hh and hl:
        return "UP"
    if lh and ll:
        return "DOWN"
    return "RANGE"


def _swing_points(series: pd.Series, window: int = 3) -> tuple[list, list]:
    """يستخرج القمم والقيعان من DataFrame باستخدام نافذة متحركة"""
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
# 3. الدعم والمقاومة
# ────────────────────────────────────────────

def find_sr(highs: list[float], lows: list[float],
            price: float) -> tuple[float, float]:
    """
    يجد أقرب دعم تحت السعر وأقرب مقاومة فوقه
    """
    below = [h for h in lows  if h <= price] or lows
    above = [h for h in highs if h >= price] or highs

    support    = max(below) if below else min(lows)
    resistance = min(above) if above else max(highs)

    # لا يكون الدعم = المقاومة
    if support >= resistance:
        support = resistance * 0.97

    return round(support, 4), round(resistance, 4)


def price_zone(price: float, support: float, resistance: float,
               margin: float = 0.02) -> Zone:
    """يصنّف موقع السعر الحالي"""
    if price <= support * (1 + margin):
        return "SUPPORT"
    if price >= resistance * (1 - margin):
        return "RESISTANCE"
    return "MIDDLE"


# ────────────────────────────────────────────
# 4. شجرة قرار الجد–الابن–الحفيد
# ────────────────────────────────────────────

def decide(grand: TrendDir, parent: TrendDir,
           child: TrendDir, zone: Zone) -> tuple[Signal, str]:
    """
    القرار الهرمي:
      1. الجد يحدد الاتجاه الكبير
      2. الابن يحدد التصحيح أو الاستمرار
      3. الحفيد يعطي توقيت الدخول
    """

    # ═══ جد صاعد ═══
    if grand == "UP":
        if parent == "UP":
            if child == "UP":
                if zone == "SUPPORT":
                    return "BUY", "جد↑ + ابن↑ + حفيد↑ عند دعم ← أقوى إشارة شراء"
                if zone == "RESISTANCE":
                    return "WAIT", "جد↑ + ابن↑ + حفيد↑ عند مقاومة ← انتظر الكسر"
                return "BUY", "جد↑ + ابن↑ + حفيد↑ ← استمرار صعود"
            if child == "DOWN":
                if zone == "SUPPORT":
                    return "BUY", "جد↑ + ابن↑، حفيد في تصحيح عند دعم ← فرصة دخول"
                return "WAIT", "جد↑ + ابن↑، حفيد هابط ← انتظر نهاية التصحيح"
            return "WAIT", "جد↑ + ابن↑، حفيد عرضي ← انتظر وضوح"

        if parent == "DOWN":
            if child == "UP" and zone == "SUPPORT":
                return "BUY", "جد↑، ابن في تصحيح، حفيد↑ من دعم ← دخول محتاط"
            if child == "DOWN":
                return "WAIT", "جد↑ لكن ابن وحفيد هابطان ← تصحيح عميق، انتظر"
            return "WAIT", "جد↑، ابن↓ ← انتظر انتهاء تصحيح الابن"

        return "NO_TRADE", f"جد↑ لكن الابن عرضي ← لا وضوح"

    # ═══ جد هابط ═══
    if grand == "DOWN":
        if parent == "DOWN":
            if child == "DOWN":
                if zone == "RESISTANCE":
                    return "SELL", "جد↓ + ابن↓ + حفيد↓ عند مقاومة ← أقوى إشارة بيع"
                if zone == "SUPPORT":
                    return "WAIT", "جد↓ + ابن↓ + حفيد↓ عند دعم ← انتظر كسر الدعم"
                return "SELL", "جد↓ + ابن↓ + حفيد↓ ← استمرار هبوط"
            if child == "UP":
                if zone == "RESISTANCE":
                    return "SELL", "جد↓ + ابن↓، حفيد ارتداد عند مقاومة ← بيع"
                return "WAIT", "جد↓ + ابن↓، حفيد↑ ← انتظر نهاية الارتداد"
            return "WAIT", "جد↓ + ابن↓، حفيد عرضي ← انتظر وضوح"

        if parent == "UP":
            if child == "DOWN" and zone == "RESISTANCE":
                return "SELL", "جد↓، ابن في تصحيح صاعد، حفيد↓ من مقاومة ← بيع محتاط"
            if child == "UP":
                return "NO_TRADE", "جد↓ لكن ابن وحفيد صاعدان ← تضارب، لا تداول"
            return "WAIT", "جد↓، ابن↑ ← تصحيح صاعد، انتظر تأكيد"

        return "NO_TRADE", "جد↓ لكن الابن عرضي ← لا وضوح"

    # ═══ جد عرضي ═══
    return "NO_TRADE", "الجد في نطاق عرضي ← لا تداول حتى يتحدد الاتجاه"


# ────────────────────────────────────────────
# 5. البوت الرئيسي — وضع البيانات اليدوية
# ────────────────────────────────────────────

class GFCBot:
    """
    بوت GFC يعتمد على بيانات القمم والقيعان المُدخلة يدوياً

    المستويات:
      grand  = الجد  (يومي / أسبوعي)
      parent = الابن (4 ساعات / يومي)
      child  = الحفيد (ساعة / 15 دقيقة)
    """

    def analyze_manual(
        self,
        grand_highs : list[float],
        grand_lows  : list[float],
        parent_highs: list[float],
        parent_lows : list[float],
        child_highs : list[float],
        child_lows  : list[float],
        current_price: float,
    ) -> GFCResult:
        """تحليل GFC من بيانات يدوية"""

        grand  = TrendLevel(classify_trend(grand_highs,  grand_lows),
                            grand_highs,  grand_lows,  grand_lows[-1])
        parent = TrendLevel(classify_trend(parent_highs, parent_lows),
                            parent_highs, parent_lows, parent_lows[-1])
        child  = TrendLevel(classify_trend(child_highs,  child_lows),
                            child_highs,  child_lows,  current_price)

        # الدعم والمقاومة من الابن
        support, resistance = find_sr(
            parent_highs + child_highs,
            parent_lows  + child_lows,
            current_price
        )

        zone   = price_zone(current_price, support, resistance)
        signal, reason = decide(grand.direction, parent.direction,
                                child.direction, zone)

        return GFCResult(grand, parent, child,
                         current_price, support, resistance,
                         zone, signal, reason)

    def report_manual(self, ticker: str, **kwargs) -> GFCResult:
        """يطبع تقرير مرتّب ويعيد النتيجة"""
        r = self.analyze_manual(**kwargs)
        self._print(ticker, r)
        return r

    # ── اختياري: بيانات حقيقية (يحتاج إنترنت) ──
    def analyze_live(self, ticker: str, market: str = "crypto") -> GFCResult:
        """يسحب بيانات من yfinance ويحللها"""
        try:
            import yfinance as yf
        except ImportError:
            raise ImportError("نفّذ: pip install yfinance")

        TF = {
            "crypto": ("1d", "4h", "1h"),
            "stock":  ("1d", "4h", "1h"),
            "forex":  ("1wk","1d", "4h"),
        }
        grand_tf, parent_tf, child_tf = TF.get(market, TF["crypto"])

        def _fetch(period, interval):
            df = yf.download(ticker, period=period,
                             interval=interval, progress=False,
                             auto_adjust=True)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            return df

        gdf = _fetch("6mo", grand_tf)
        pdf = _fetch("60d", parent_tf)
        cdf = _fetch("14d", child_tf)

        gh, gl = _swing_points(gdf["High"], 4), _swing_points(gdf["Low"], 4)
        ph, pl = _swing_points(pdf["High"], 3), _swing_points(pdf["Low"], 3)
        ch, cl = _swing_points(cdf["High"], 2), _swing_points(cdf["Low"], 2)

        price = float(cdf["Close"].iloc[-1])
        return self.analyze_manual(
            gh[0] or [gdf["High"].max()], gl[1] or [gdf["Low"].min()],
            ph[0] or [pdf["High"].max()], pl[1] or [pdf["Low"].min()],
            ch[0] or [cdf["High"].max()], cl[1] or [cdf["Low"].min()],
            price,
        )

    # ── طباعة التقرير ──
    def _print(self, ticker: str, r: GFCResult) -> None:
        ARROWS = {
            "UP": "↑ صاعد", "DOWN": "↓ هابط",
            "RANGE": "↔ عرضي", "UNKNOWN": "؟ غير محدد"
        }
        ICONS = {
            "BUY": "🟢  شراء",
            "SELL": "🔴  بيع",
            "NO_TRADE": "⚪  لا تداول",
            "WAIT": "🟡  انتظار",
        }
        bar = "═" * 52
        print(f"\n{bar}")
        print(f"   تحليل GFC  ←  {ticker}")
        print(f"{bar}")
        print(f"  الجد    : {ARROWS[r.grand.direction]}")
        print(f"  الابن   : {ARROWS[r.parent.direction]}")
        print(f"  الحفيد  : {ARROWS[r.child.direction]}")
        print(f"  ─────────────────────────────────────")
        print(f"  السعر   : {r.price:.4f}")
        print(f"  الدعم   : {r.support:.4f}")
        print(f"  المقاومة: {r.resistance:.4f}")
        print(f"  المنطقة : {r.zone}")
        print(f"  ─────────────────────────────────────")
        print(f"  {ICONS[r.signal]}")
        print(f"  {r.reason}")
        print(f"{bar}\n")
