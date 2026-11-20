# Stop-motion varlık denetimi — 2026-11-21

## İncelenen gerçek kaynaklar
- `README.md`: 3.576 şeffaf PNG/WebP kart; R serisi 2.852, K serisi 724.
- `katalog.json`, `katalog/R14.json`, `katalog/R15.json`, `katalog/R17.json`, `katalog/R30.json`.
- `stop-motion/URETIM_MASTER_v1.md`, `stop-motion/PAKET_01_DURUM.md`, `stop-motion/arka-planlar/ENVANTER.md`.

## Yeniden üretme: varlığı doğrulanmış örnekler
| Kart | Kaynak adı | Karar |
|---|---|---|
| R1501 | sarı güneş | mevcut keçe PNG'sini kullan |
| R1736 | bir bulut | mevcut keçe PNG'sini kullan |
| R1768 | yağmur bulutu | mevcut keçe PNG'sini kullan |
| R1770 | gökyüzünde güneş | mevcut kartı koru |
| R1734 | saksı | mevcut keçe PNG'sini kullan |
| R1737 | sulama kabı | mevcut keçe PNG'sini kullan |
| R1701 | ağaçta kuş yuvası | birleşik kartı koru, katmanlara ayrılmış sayma |
| R3011 | kıyafet mağazası | mevcut kartı koru |
| R3012 | çiçek dükkânı | mevcut kartı koru |
| R3022 | oyun parkı | mevcut kartı koru |
| R3070 | dört kuş | birleşik kartı koru |
| R3084 | sık ağaçlar | birleşik kartı koru |

Kartların doğrudan PNG adresi: `https://raw.githubusercontent.com/gamgazi/ders-pusulasi-kece/main/kartlar/RXX/RXXXX.png` (ID'ye göre RXX grup adı).

## Ayrı üretim gerektiren türler
**Kesin ihtiyaç / format farkı:** Mevcut keçe kartı, keçeli kalemle çizilmiş kâğıt dekorla aynı varlık değildir. Yardımcı nesnelerin ayrı şeffaf PNG sürümleri gereklidir.

**Öncelikli üretim kuyruğu (ders hedefi onayı değil):**
1. `yardimci-nesneler/hava/`: güneş ×3, bulut ×5, yağmur damlası ×3, yıldız ×4.
2. `yardimci-nesneler/doga/`: çim tutamı ×6, yaprak ×6, ağaç ×3, çiçek ×4.
3. `yardimci-nesneler/mekan/`: kapı, pencere, sınıf tahtası, sandalye, masa, pazar tezgâhı (ayrı).
4. `hareket-pozlari/`: kuş kanat açık/orta/kapalı; kelebek kanat açık/kapalı; yaprak dönüş pozları.
5. `marka/`: onaylı tek nakışlı etiket gövdesi + yukarı uzanan çift hasır ip varyasyonları.

## Arka plan politikası
Mevcut onaylı düz arka planlar **yeniden üretilmeyecek**. `arka-planlar/ENVANTER.md` yalnız aday ve kaynak dayanaklarını içerir, PNG dosyalarının yüklendiğini kanıtlamaz. Yeni arka plan yalnızca gerçek eksik dosya doğrulandıktan sonra üretilir.

## Açık denetim / kabul kapıları
- [ ] 3.576 kartın tam `kartlar.json` dökümünden dosya bazında eşleştirilmesi
- [ ] GitHub'da onaylı düz arka plan PNG'lerinin yollarının doğrulanması
- [ ] Yardımcı nesnelerin PNG alfa kanalı ve yüksek çözünürlük kontrolü
- [ ] Keçeli kalem gerçekçiliği ve tekrar etmeyen kesim varyasyonlarının görsel onayı
- [ ] Ders kitabındaki yaş/ünite/ders/hedef sözcük eşleştirmelerinin doğrulanması
- [ ] Yeni ikili PNG dosyalarının GitHub'a yüklenmesi

**Durum:** Bu belge kaynak destekli kısmi denetimdir. Üretim tamamlandı, tüm katalog tarandı veya PNG yüklendi iddiası değildir.
