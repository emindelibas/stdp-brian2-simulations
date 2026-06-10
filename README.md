# STDP Brian2 Simülasyonları

Bu depo, **Öğrenmenin Biyokimyasal Süreçlerinin Modellenmesi** başlıklı bitirme projesi kapsamında kullanılan Python/Brian2 simülasyon kodlarını içermektedir.

Çalışmada, sinaptik plastisite, Hebbian öğrenme ve zamanlama temelli sinaptik plastisite (STDP) mekanizmaları hesaplamalı olarak incelenmiştir. Kodlar; LIF nöron modeli, simetrik ve asimetrik STDP öğrenme pencereleri, LTP/LTD baskın parametre analizleri ve tekil ağ dinamiği simülasyonlarını kapsamaktadır.

## Dosya Yapısı

```text
stdp-brian2-simulations/
│
├── src/
│   ├── 01_lif_neuron.py
│   ├── 02_symmetric_stdp_window.py
│   ├── 03_asymmetric_stdp_window.py
│   ├── 04_ltd_dominant_sweep.py
│   ├── 05_ltp_dominant_sweep.py
│   └── 06_single_network_dynamics.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Kodların Açıklaması

### 01_lif_neuron.py

Tek bir Leaky Integrate-and-Fire (LIF) nöronunun Brian2 ortamında gerçeklenmesini içerir. Zar potansiyelinin zamana bağlı değişimi ve eşik değere ulaşıldığında oluşan spike davranışı gözlemlenir.

### 02_symmetric_stdp_window.py

Simetrik STDP öğrenme penceresini üretir. Presinaptik ve postsinaptik spike zamanları arasındaki fark değiştirilerek sinaptik ağırlık değişimi incelenir.

### 03_asymmetric_stdp_window.py

Farklı zaman sabitleri ve öğrenme katsayıları kullanılarak asimetrik STDP öğrenme penceresi elde edilir.

### 04_ltd_dominant_sweep.py

Apre değeri sabit tutulurken farklı Apost değerleri denenir. Böylece LTD baskınlığının STDP öğrenme penceresi üzerindeki etkisi incelenir.

### 05_ltp_dominant_sweep.py

Apost değeri sabit tutulurken farklı Apre değerleri denenir. Böylece LTP baskınlığının STDP öğrenme penceresi üzerindeki etkisi incelenir.

### 06_single_network_dynamics.py

Poisson girişleriyle beslenen iletkenlik temelli bir LIF nöronu ve STDP sinapsları kullanılarak tekil ağ dinamiği incelenir. Kod içerisinde LTD baskın ve LTP baskın iki farklı senaryo çalıştırılır.

## Gereksinimler

Kodları çalıştırmak için Python ortamında aşağıdaki kütüphanelerin kurulu olması gerekir:

```bash
pip install -r requirements.txt
```

`requirements.txt` dosyasında kullanılan temel kütüphaneler şunlardır:

```text
brian2
numpy
matplotlib
```

## Kodların Çalıştırılması

Her dosya ayrı ayrı çalıştırılabilir:

```bash
python src/01_lif_neuron.py
python src/02_symmetric_stdp_window.py
python src/03_asymmetric_stdp_window.py
python src/04_ltd_dominant_sweep.py
python src/05_ltp_dominant_sweep.py
python src/06_single_network_dynamics.py
```

Kodlar çalıştırıldığında grafik çıktıları `outputs/` klasörü altında kaydedilir.

## Tez ile İlişkisi

Bu depodaki kodlar, bitirme projesinde sunulan Brian2 tabanlı simülasyonların tekrarlanabilirliğini desteklemek amacıyla paylaşılmıştır. Kodlar özellikle tezin ikinci ve dördüncü bölümlerinde yer alan LIF nöron modeli, STDP öğrenme pencereleri, LTP/LTD baskın parametre analizleri ve tekil ağ dinamiği sonuçlarıyla ilişkilidir.

## Not

Bu depo, bitirme projesinde elde edilen simülasyon çıktılarının düzenli ve tekrar çalıştırılabilir şekilde saklanması amacıyla hazırlanmıştır.
