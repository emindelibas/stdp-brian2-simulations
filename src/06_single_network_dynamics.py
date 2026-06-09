"""
06_single_network_dynamics.py

Tekil ağ dinamiği simülasyonu.

Bu kodda asimetrik STDP parametreleri kullanılarak iki farklı durum incelenir:

1. LTD baskın durum:
   Apre = 0.05, Apost = -0.25

2. LTP baskın durum:
   Apre = 0.25, Apost = -0.05

Çıktılar:
    outputs/fig_4_3_ltd_dominant_network.png
    outputs/fig_4_4_ltp_dominant_network.png
"""

from brian2 import *
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


# -------------------------------------------------------------------------
# Çıktı klasörü
# -------------------------------------------------------------------------

output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)


# -------------------------------------------------------------------------
# Tekil ağ simülasyon fonksiyonu
# -------------------------------------------------------------------------

def ag_dinamigi_calistir(Apre_degeri, Apost_degeri, baslik, cikti_adi, random_seed=1):
    """
    Verilen Apre ve Apost değerleri için iletkenlik temelli LIF nöronu ve
    STDP sinapsları kullanılarak tekil ağ dinamiği simüle edilir.
    """

    start_scope()

    seed(random_seed)
    np.random.seed(random_seed)

    defaultclock.dt = 0.1 * ms

    # ---------------------------------------------------------------------
    # 1. Parametreler
    # ---------------------------------------------------------------------

    N_pre = 90
    firing_rate = 40 * Hz

    tau_v = 10 * ms
    tau_g = 2 * ms

    E_leak = 0
    E_exc = 1

    taupre = 20 * ms
    taupost = 50 * ms

    Apre = Apre_degeri
    Apost = Apost_degeri

    wmax = 100.0

    # ---------------------------------------------------------------------
    # 2. Postsinaptik nöron modeli
    # ---------------------------------------------------------------------

    eqs_neuron = """
    dv/dt = (E_leak - v)/tau_v + g*(E_exc - v) : 1
    dg/dt = -g/tau_g : Hz
    """

    G = NeuronGroup(
        1,
        eqs_neuron,
        threshold="v > 0.8",
        reset="v = 0",
        method="euler"
    )

    G.v = 0
    G.g = 0 * Hz

    # ---------------------------------------------------------------------
    # 3. Presinaptik Poisson giriş grubu
    # ---------------------------------------------------------------------

    P = PoissonGroup(N_pre, rates=firing_rate)

    # ---------------------------------------------------------------------
    # 4. STDP sinaps modeli
    # ---------------------------------------------------------------------

    eqs_syn = """
    w : Hz
    dapre/dt = -apre/taupre : Hz (event-driven)
    dapost/dt = -apost/taupost : Hz (event-driven)
    """

    on_pre_eqs = """
    g_post += 0.8*w
    apre += Apre * Hz
    w = clip(w + apost, 0*Hz, wmax*Hz)
    """

    on_post_eqs = """
    apost += Apost * Hz
    w = clip(w + apre, 0*Hz, wmax*Hz)
    """

    S = Synapses(
        P,
        G,
        model=eqs_syn,
        on_pre=on_pre_eqs,
        on_post=on_post_eqs
    )

    S.connect()

    # Başlangıç ağırlıkları 0 ile wmax arasında rastgele seçilir.
    S.w = np.random.rand(len(S)) * wmax * Hz

    # ---------------------------------------------------------------------
    # 5. Monitörler
    # ---------------------------------------------------------------------

    M_v = StateMonitor(G, "v", record=True)
    M_g = StateMonitor(G, "g", record=True)
    M_w = StateMonitor(S, "w", record=True)
    spikemon = SpikeMonitor(G)

    # ---------------------------------------------------------------------
    # 6. Simülasyon
    # ---------------------------------------------------------------------

    run(
        2000 * ms,
        namespace={
            "E_leak": E_leak,
            "E_exc": E_exc,
            "tau_v": tau_v,
            "tau_g": tau_g,
            "taupre": taupre,
            "taupost": taupost,
            "Apre": Apre,
            "Apost": Apost,
            "wmax": wmax
        }
    )

    # ---------------------------------------------------------------------
    # 7. Ortalama sinaptik ağırlık hesabı
    # ---------------------------------------------------------------------

    mean_w = np.mean(M_w.w / Hz, axis=0)

    ilk_deger = mean_w[0]
    son_deger = mean_w[-1]
    net_degisim = son_deger - ilk_deger

    print("\n" + "=" * 50)
    print(baslik)
    print(f"Apre değeri            : {Apre}")
    print(f"Apost değeri           : {Apost}")
    print(f"İlk Ortalama Ağırlık   : {ilk_deger:.4f}")
    print(f"Son Ortalama Ağırlık   : {son_deger:.4f}")
    print(f"Net Değişim            : {net_degisim:.4f}")
    print("=" * 50 + "\n")

    # ---------------------------------------------------------------------
    # 8. Grafikler
    # ---------------------------------------------------------------------

    fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(
        5,
        1,
        figsize=(10, 10),
        sharex=True
    )

    # 1. Grafik: Membran potansiyeli
    ax1.plot(M_v.t / ms, M_v.v[0], color="steelblue")
    ax1.axhline(0.8, ls="--", c="crimson", label="Eşik")
    ax1.set_ylabel("Membran Pot. (v)")
    ax1.legend(loc="upper right")
    ax1.set_title(baslik)
    ax1.grid(alpha=0.3)

    # 2. Grafik: İletkenlik
    ax2.plot(M_g.t / ms, M_g.g[0] / Hz, color="darkorange")
    ax2.set_ylabel("İletkenlik (g)")
    ax2.grid(alpha=0.3)

    # 3. Grafik: Ortalama sinaptik ağırlık
    ax3.plot(M_w.t / ms, mean_w, color="forestgreen")
    ax3.set_ylabel("Ortalama Ağırlık (w)")
    ax3.grid(alpha=0.3)

    # 4. Grafik: Postsinaptik spike zamanları
    ax4.plot(spikemon.t / ms, spikemon.i, ".k")
    ax4.set_ylabel("Nöron İndeksi")
    ax4.grid(alpha=0.3)

    # 5. Grafik: İki örnek sinapsın ağırlık değişimi
    ax5.plot(
        M_w.t / ms,
        M_w.w[10] / Hz,
        color="#108b3c",
        linewidth=2.5,
        label="Sinaps #10"
    )

    ax5.plot(
        M_w.t / ms,
        M_w.w[80] / Hz,
        color="#7b7668",
        linewidth=2.5,
        label="Sinaps #80"
    )

    ax5.set_xlabel("Zaman (ms)")
    ax5.set_ylabel("Sinaptik Ağırlık (w)")
    ax5.legend(loc="center right")
    ax5.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / cikti_adi, dpi=300)
    plt.show()


# -------------------------------------------------------------------------
# Senaryo 1: LTD baskın durum
# -------------------------------------------------------------------------

ag_dinamigi_calistir(
    Apre_degeri=0.05,
    Apost_degeri=-0.25,
    baslik="LTD Baskın Durumda Tekil Ağ Dinamiği",
    cikti_adi="fig_4_3_ltd_dominant_network.png",
    random_seed=1
)


# -------------------------------------------------------------------------
# Senaryo 2: LTP baskın durum
# -------------------------------------------------------------------------

ag_dinamigi_calistir(
    Apre_degeri=0.25,
    Apost_degeri=-0.05,
    baslik="LTP Baskın Durumda Tekil Ağ Dinamiği",
    cikti_adi="fig_4_4_ltp_dominant_network.png",
    random_seed=1
)
