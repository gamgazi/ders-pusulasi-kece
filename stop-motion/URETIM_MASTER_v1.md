# Stop-motion seri üretim — MASTER v1.0

**Durum:** Üretim envanteri ve kalite standardı. Bu metin PNG varlıklarının GitHub'a yüklendiği anlamına gelmez.

## Dosya ağacı
- `arka-planlar/`: 16:9 sabit yüzeyler; kuru boya, yazısız, dekor nesnesiz.
- `yardimci-nesneler/`: ayrı şeffaf PNG, gerçek keçeli kalem mürekkebi ve elle kesilmiş kâğıt.
- `hedef-kece/`: dersin hedef kelimesi için ayrı yüksek çözünürlüklü keçe figür ve hareket pozları.
- `marka/`: sağ üstteki onaylı nakışlı etiket; aynı gövde ve farklı çift hasır ip pozları.
- `sahneler/`: ders eşleştirmeleri ve katman konumları.

## MASTER üretim kuralları
1. 16:9, hedef 3840×2160; önizleme 4K teslim değildir.
2. Arka planda yalnız sabit renk/yüzey ve gerekli mekân çizgileri. Güneş, yıldız, çiçek, ağaç, çim tutamı, bulut ve hareketli dekorlar ayrı dosyadır.
3. Kâğıt dekor keçeli kalemdir, kuru boya veya nakış değil. Bulut içi beyaz bırakılır.
4. Ana hedef keçe figür büyük, diğerleri küçük ve uzakta; nesneler temas gölgesiyle zemine oturur.
5. Etiket sağ üstte, küçük; iki lifli hasır ip yukarı uzanır. Onaylı tek gövdeyi her karede koru.
6. Kaynak ders kitaplarından doğrulanmamış yaş/ünite/ders/hedef kelime eşleştirmelerini onaylı sayma.
7. Her varlığın kaynak, çözünürlük, alfa, kalite ve onay durumu manifestte yer alır.

## Üretim sırası (aday, ders hedefi değil)
- Açık alan: gündüz çayır, park, orman yolu
- Mevsimler: ilkbahar, yaz, sonbahar, kış, gece
- Su: deniz, deniz dibi, sahil
- Şehir: sokak, okul yolu, pazar, mağaza
- İç mekân: sınıf, ev, mutfak
- Diğer: çöl, uzay

**Kontrol:** Yüksek çözünürlüklü ayrı PNG dosyaları, gerçek alfa kanalı ve tam müfredat eşleştirmesi doğrulanmadan seri üretim tamamlandı işareti verilmez.

## EK-01 — Gerçek fiziksel kâğıt / keçeli kalem kalite kapısı (2026-11-21)

Bu ek, kullanıcının son görsel geri bildirimine dayanır ve sonraki bütün **yardımcı kâğıt nesne** üretimlerinde zorunludur.

1. Kâğıt kesimi şablon gibi kusursuz ve simetrik görünmemelidir: sınır çizgisinde el makası kaynaklı küçük oynamalar, yer yer geniş/dar beyaz kenar ve doğal hafif el kaymaları olmalıdır.
2. En az bir veya iki kenarda fiziksel kâğıt kıvrılması/kalkması, eğim, çok hafif katlanma, kırışıklık veya bükülme hissi aranır; abartılı yırtık ve sahte eskimiş kâğıt zorunlu değildir.
3. Boyama mekanik ve kusursuz görünmemelidir: fiber uçlu **keçeli kalem**in aynı yöndeki boyama geçişleri, üst üste binen yerlerde koyu mürekkep bölgeleri ve yer yer ufak beyaz boşluklar görünür. Çizgi yoğunluğu ve elle kontrolü değişken olmalıdır.
4. **Mum boya, pastel, kuru boya, boya kalemi, keçeleşmiş kumaş, nakış veya dijital düz renk dolgusu yardımcı nesneye uygulanmaz.** Bu malzemeler kendi tanımlı farklı katmanlarında kullanılabilir.
5. Yardımcı bulut: yüzsüz, içi gerçek beyaz kâğıt, mavi keçeli kalemle çizilmiş çevre; bulutun gövdesine mavi pastel gölgelendirme doldurulmaz.
6. Her nesne **tek başına gerçek alfa kanallı şeffaf PNG** olmalı. Dama deseninin resme baskı olarak gömülmesi veya kâğıdı gölgede yüzdürmek başarısızlıktır.
7. Aynı modelden varyasyonlar görünür el farklılığı taşımalı; yalnız renk değişimi veya ölçekleme yeni farklı varlık sayılmaz.
8. Nesnenin üretimi tamamlandı denmeden önce **görsel malzeme kontrolü + RGBA alfa kontrolü + gerçekten ayrı dosya kontrolü** yapılır. Sanatsal onay alınmayan ürünler yalnızca prototiptir.

**Durum:** 2026-11-21 seri prototiplerdeki görsel kalite onayı henüz verilmemiştir.
