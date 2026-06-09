"""
04_ltd_dominant_sweep.py

LTD baskın STDP parametre taraması.

Bu kodda Apre sabit tutulur ve farklı negatif Apost değerleri kullanılarak
uzun süreli depresyonun (LTD) STDP öğrenme penceresi üzerindeki etkisi incelenir.

Çıktı:
    outputs/fig_4_1_ltd_sweep.png
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# -------------------------------------------------------------------------
# Çıktı klasörü
# -------------------------------------------------------------------------

output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)


# -------------------------------------------------------------------------
# STDP parametreleri
# -------------------------------------------------------------------------

taupre = 20.0       # LTP zaman sabiti (ms)
taupost = 50.0      # LTD zaman sabiti (ms)

Apre = 0.05         # LTP katsayısı, sabit tutulur

Apost_degerleri = [-0.05, -0.10, -0.15, -0.20, -0.25]

renkler = ["#ffcccc", "#ff9999", "#ff4d4d", "#cc0000", "#800000"]


# -------------------------------------------------------------------------
# Zaman farkı aralığı
# -------------------------------------------------------------------------

delta_t = np.linspace(-100, 100, 1000)


# -------------------------------------------------------------------------
# LTD baskın STDP öğrenme pencerelerinin çizdirilmesi
# -------------------------------------------------------------------------

plt.figure(figsize=(9, 6))

for i, Apost in enumerate(Apost_degerleri):

    W_teorik = np.where(
        delta_t > 0,
        Apre * np.exp(-delta_t / taupre),       # LTP bölgesi
        Apost * np.exp(delta_t / taupost)       # LTD bölgesi
    )

    plt.plot(
        delta_t,
        W_teorik,
        color=renkler[i],
        linewidth=2.5,
        label=f"Apost = {Apost}"
    )


# -------------------------------------------------------------------------
# Grafik düzenlemeleri
# -------------------------------------------------------------------------

plt.axhline(0, color="black", linestyle="-", linewidth=1.2)
plt.axvline(0, color="black", linestyle="--", linewidth=1.2)

plt.xlabel(r"Spike zaman farkı $\Delta t = t_{post} - t_{pre}$ (ms)", fontsize=12)
plt.ylabel(r"Ağırlık değişimi ($\Delta w$)", fontsize=12)
plt.title(f"Sabit Apre = {Apre} Altında Farklı Apost Değerleri İçin STDP", fontsize=14)

plt.legend(loc="upper right", fontsize=11)
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(output_dir / "fig_4_1_ltd_sweep.png", dpi=300)
plt.show()
