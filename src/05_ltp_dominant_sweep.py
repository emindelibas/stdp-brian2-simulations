"""
05_ltp_dominant_sweep.py

LTP baskın STDP parametre taraması.

Bu kodda Apost sabit tutulur ve farklı Apre değerleri kullanılarak
uzun süreli potansiyasyonun (LTP) STDP öğrenme penceresi üzerindeki etkisi incelenir.

Çıktı:
    outputs/fig_4_2_ltp_sweep.png
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
# Sabit STDP parametreleri
# -------------------------------------------------------------------------

taupre = 20.0
taupost = 50.0
Apost = -0.05  # Sabit LTD değeri

# Karşılaştırılacak farklı Apre (LTP) değerleri
Apre_degerleri = [0.05, 0.10, 0.15, 0.20, 0.25]
renkler = ['#b3e6b3', '#66cc66', '#339933', '#006600', '#003300']

# Zaman farkı ekseni: -100 ms ile +100 ms arası
delta_t = np.linspace(-100, 100, 1000)


# -------------------------------------------------------------------------
# Grafik oluşturma
# -------------------------------------------------------------------------

plt.figure(figsize=(9, 6))

# Her bir Apre değeri için STDP eğrisini çizdir
for i, Apre in enumerate(Apre_degerleri):
    W_teorik = np.where(
        delta_t > 0,
        Apre * np.exp(-delta_t / taupre),      # dt > 0 ise LTP
        Apost * np.exp(delta_t / taupost)      # dt < 0 ise LTD
    )

    plt.plot(
        delta_t,
        W_teorik,
        color=renkler[i],
        linewidth=2.5,
        label=f'Apre = {Apre}'
    )

# Eksen çizgileri
plt.axhline(0, color='black', linestyle='-', linewidth=1.2)
plt.axvline(0, color='black', linestyle='--', linewidth=1.2)

# Grafik düzenlemeleri
plt.xlabel(r'Spike Zaman Farkı $\Delta t = t_{post} - t_{pre}$ (ms)', fontsize=12)
plt.ylabel(r'Ağırlık Değişimi ($\Delta w$)', fontsize=12)
plt.title(f'Sabit Apost ({Apost}) Altında Farklı Apre Değerleri İçin STDP', fontsize=14)
plt.legend(loc='upper right', fontsize=11)
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / "fig_4_2_ltp_sweep.png", dpi=300)
plt.show()
