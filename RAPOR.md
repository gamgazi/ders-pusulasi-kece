# Ders Pusulası keçe üretim raporu

## Güncel durum

| Üretim listesi | Hedef | Denetimden geçen PNG ve WebP çifti | Kalan |
| --- | ---: | ---: | ---: |
| Nesne ve insansız sahne | 1971 | 1964 | 7 |
| İnsanlı kartlar | 888 | 888 | 0 |
| K serisi sözcük kartları | 724 | 724 | 0 |
| **Toplam** | **3583** | **3576** | **7** |

Nesne ve sahnelerde kalan yedi tarif, yazı veya rakam gerektiriyor. Bu hedeflere ek olarak, resimler.csv içinde 609 karakterli ve 55 yazılı satır okulun referanslarını veya yazı kararını bekliyor. K serisinde dosya adı, K kimliğini ve sözcüğün kaynakta geçen Türkçe yazımını koruyor.

## Son teslim

20 Kasım 2026 günü tamamlanan teslimde **3.576 ayrı kart** ve her kartın bir PNG ile bir WebP kopyası bulunuyor. Bunların 1.306’sı nesne, 658’i insansız sahne, 888’i insanlı kart ve 724’ü ek sözcük kartı. Stil örnekleri ve karşılaştırma sayfaları bu sayıya dahil edilmedi.

| İlk geçtiği yaş grubu | Müfredat resimleri (R) | Ek sözcük kartları (K) | Toplam |
| --- | ---: | ---: | ---: |
| 4–6 | 2.232 | 221 | 2.453 |
| 7–9 | 617 | 204 | 821 |
| 10–12 | 0 | 131 | 131 |
| 13–15 | 3 | 85 | 88 |
| 16–17 | 0 | 83 | 83 |
| **Toplam** | **2.852** | **724** | **3.576** |

Kelime grupları çalışma kitabı 35 seviyenin 616 ünitesindeki 5.040 dersi ve 17.535 sözcük ve kalıp geçişini kapsıyor. Ayrı resim kararı gereken 2.882 sözcüğün 724’ü görselleştirildi. Diğer 2.158 sözcüğün gerekçesi `kelime-kararlari.csv` içinde yer alıyor.

Son denetimde 2.852 R ve 724 K kartının tamamı geçti. Teslimdeki PNG’ler 912 × 944 piksel ve RGBA. Her kenarda en az 16 piksel saydam pay var. WebP kopyaları 570 × 590 piksel, alfa kanallı ve kalite 85 ile kaydedildi. Ana arşivdeki 7.152 üretim dosyası çalışma klasöründeki karşılıklarıyla bayt düzeyinde eşleşti. 3.576 PNG’nin SHA-256 özetleri birbirinden farklı. Ayrıca 50 parti arşivindeki görsel dosyalarının tamamı karşılaştırıldı ve her kartın bir parti arşivinde yer aldığı doğrulandı.

Görseller OpenAI ImageGen ile onaylı B örneklerine dayanarak üretildi. Araç modelin alt sürümünü bildirmedi. Üretimdeki malzeme ve ışık, el yapımı yün keçe oyuncağın üstten çekilmiş fotoğrafını canlandırıyor. İnsan figürlerinde renk uyumlu mat ip, koyu alanlarda kahverengi ip kullanıldı.

### Bekleyen 671 kaynak satırı

Okulun özgün karakter görsellerini bekleyen 609 satır ve okulun yazı kararını bekleyen 55 satır var. Ayrıca nesne veya sahne olarak sınıflandırılmış aşağıdaki yedi tarifin istenen anlamı yazı ya da rakam gerektiriyor. Bu yedi kart için üretim dosyası teslim edilmedi.

| Kimlik | Kaynak tarifi |
| --- | --- |
| R2237 | yedi rakamı |
| R2256 | adın ve imzan |
| R2417 | berabere yazan skor tabelası 2-2 |
| R2817 | içinde resimler ve yazılar olan süslü defter |
| R3396 | malzemeler ve adımlar yazılı kâğıt |
| R3410 | numaralı takım tişörtü |
| R3502 | gazetenin en üstünde büyük harfli başlık |

Aşağıdaki parti kayıtlarındaki sayılar, ilgili partinin tamamlandığı andaki durumu gösterir.

## Aşama 0 · Stil denemesi

| Yön | İlk üretim | Yeniden üretilen | Seçime sunulan | Teknik kontrolden geçen | Çözülemeyen |
| --- | ---: | ---: | ---: | ---: | ---: |
| A · Düz aplike | 4 | 0 | 4 | 4 | 0 |
| B · Dolgulu keçe oyuncak | 4 | 0 | 4 | 4 | 0 |
| C · Zengin el işi | 4 | 4 | 4 | 4 | 0 |

OpenAI ImageGen ile her yön için dört konuyu aynı levhada sıfırdan ürettim. Araç alt modelin sürümünü bildirmedi. C yönünün ilk levhasında özellikle elma ve evin nakışı düz aplikeye yakındı. İkinci levhada kabartmalı dikiş ve nakış motifleri daha belirgin. B yönünde dolgunluk hafif, özellikle ev ve elmada yönü ayırt ettiren özellik kenar dikişi.

Pillow ve SciPy ile her figürü saydam kanalı üzerinden ayırıp ortaladım. PNG dosyalarının 912 × 944 piksel ve RGBA olduğunu, her kenarda en az 16 piksel boşluk kaldığını doğruladım. WebP kopyalarını 570 × 590 piksel ve kalite 85 ile kaydettim, yeniden açıp boyutlarını ve alfa kanalını kontrol ettim. Görsel incelemede on iki konunun her biri tanınabiliyor, üç zürafa da sağa bakıyor ve figürlerde yazı görünmüyor. Keçe görünümünün okulun standardını karşılayıp karşılamadığı kurucunun değerlendirmesine açık.

Bu aşamada belirsiz çeviri yok. Stil seçimi bekleniyor. Müfredat listesindeki 609 karakterli ve 55 yazılı satır beklemede.

## B stilinin seçimi ve ilk üretim

Kurucu B yönünü seçti. Onaylanan kedi, zürafa, elma ve ev PNG dosyaları stil/ içinde. Üretimde bu dört fotoğrafı malzeme ve dikiş referansı olarak kullandım. Sade kedi ve elma derslerinde onaylanan iki özgün örneği doğrudan kullandım. Tekrar eden konuların ilk referanslarını tekrar-edenler.csv içinde kaydettim.

4–6 Kök partisinde ilk 24 için 19 nesne ve 5 sahne hazırlandı. İlk 24 sayfası sayfalar/ilk-24.png içinde. Sonraki 20 görselle birlikte 44 nesne ve sahne PNG’si ve 44 WebP kopyası hazır. Partideki 283 nesne ve sahnenin 44’ü teknik denetimden geçti, hatalı dosya 0, üretilmeyi bekleyen 239. Tüm partilerdeki 1.971 nesne ve sahneden kalan 1.927. Sayfalar 4-6-kok-01.png ve 4-6-kok-02.png bu 44 görseli kapsıyor.

Derslerin dinleme sorularında top oyuncak top olarak yorumlandı. Sabah, öğle ve akşam seçenekleri için güneşin yüksekliği, ufuk ve gökyüzü rengi kullanıldı. Görsel incelemede balon renkleri, kedinin pozları, sağa bakan taşıt ve köpek ile derslerdeki konuları karşılaştırdım. Bu 44 tarifte çözülmemiş anlam belirsizliği kaydedilmedi.

## İnsan denemesi · ip rengi düzeltmesi

Altı ilk deneme yeniden üretildi. Koyu saçta koyu kahverengi, tende ten tonuna yakın sıcak kahverengi veya ten rengi, giysilerde kumaşla uyumlu ip kullanıldı. El ele iki çocuk tek görselde bulunuyor. Onaya sunulan 6 PNG ve 6 WebP insan-denemesi/ ve insan-denemesi-web/ klasörlerinde. Altı dosya teknik kontrolden geçti. Deneme sayfası sayfalar/insan-deneme.png içinde. 888 insanlı ders görseli içinde bu 6 deneme kimliği bulunuyor. İnsan serisi stil onayını bekliyor. 609 karakterli ve 55 yazılı satır beklemede.

## Bütün seviyelerin kelime grupları

Ders Pusulası kelime grupları çalışma kitabında 5 yaş grubu, 35 seviye, 616 ünite, 5.040 ders bulunur. Yeni öğesi olan 3.205 ders ve yeni öğesi olmayan 1.835 ders kaynaktaki biçimiyle yer alır. Sözcük ve kalıp geçişlerinin 17.535'i de JSON dosyalarındaki yeni alanlarıyla ders ders, sıra korunarak karşılaştırıldı. Sınıflandırma ve kaynak kimlikleri kelimeler.csv dosyasından alındı.

Kelime-kararlari.csv resimler.csv içinde karşılığı bulunmayan 2.882 tekil sözcüğü kapsar. Yaş sütunu ilk geçişin yaş grubudur. Tek karede anlamı belirsiz kalan öğeler için olumsuz karar verildi. Örneğin aile bağı, hitap ve belgelerin salt metinle belirlenebilen türü ayrıca gerekçelendirildi. Bunlar pedagojik üretim kararlarıdır ve okulun incelemesine açıktır.

| İlk geçtiği yaş | Resmedilir | Resmedilemez |
| --- | ---: | ---: |
| 4–6 | 221 | 296 |
| 7–9 | 204 | 456 |
| 10–12 | 131 | 528 |
| 13–15 | 85 | 419 |
| 16–17 | 83 | 459 |
| Toplam | 724 | 2.158 |

724 yeni sözcük için Türkçe tarif yazıldı. K serisi görseller için kelime kararlarının onayı bekleniyor. Görseller OpenAI ImageGen ile üretildi. Araç alt model sürümünü bildirmedi. Boyutlandırma ve saydam kanalla ayırma Pillow ve SciPy ile yapıldı.

## Seri üretim onayı

Kurucu altı insan örneğini ve üretimin kesintisiz sürdürülmesini onayladı. İnsan figürlerinde saç, ten ve giysiyle uyumlu mat ip kullanılıyor. Altı onaylı insan görseli kendi ders kimlikleriyle ana koleksiyona aktarıldı. Sözcük kararları üretim listesine alındı. Okul karakterleri ve yazılı satırlar için mevcut bekleme koşulları geçerli.

## Seri üretim · 4–6 Kök, Tohum ve Filiz

| Parti ve tür | Listedeki | PNG ve WebP hazır | Teknik kontrolden geçen | Teknik hatalı | Kalan |
| --- | ---: | ---: | ---: | ---: | ---: |
| 4–6 Kök · nesne ve sahne | 283 | 283 | 283 | 0 | 0 |
| 4–6 Tohum · nesne ve sahne | 116 | 116 | 116 | 0 | 0 |
| 4–6 Filiz · nesne ve sahne | 247 | 12 | 12 | 0 | 235 |

Onaylı altı insan görseliyle beraber bu teslimde 417 ayrı ders kimliği için PNG ve WebP hazır. Nesne ve sahnelerde 1.971 satırın 411’i, insanlılarda 888 satırın 6’sı hazır. K serisinde 724 satır üretim sırasında. Genel toplam 3.583 uygun kimlik, 417 hazır, 3.166 bekliyor. Buna ek olarak 609 karakterli ve 55 yazılı satır okul kararını veya referansını bekliyor.

Sayma kartları için üretilen gerçek keçe görselleri ayrıldı ve doğru sayıda dizildi. El pozları, elmalı tabaklar ve basamak sayıları gözle kontrol edildi. Tek basamak örneği iki basamak gibi göründüğü için yeniden üretildi. Kahvaltı masasında masa ayakları, yoldaki arabada yol, gökyüzündeki uçakta gökyüzü belirginleştirildi. Koyu saç ve ten dikişleri, kaş, kukla ve iki el örneğinde kumaşla uyumlu iplerle düzeltildi. Küçük ve büyük nesne çiftlerinde aynı keçe figürünün tuvalde kapladığı oran değiştirildi. Bunların anlamı özellikle kartlar aynı boyda yan yana gösterildiğinde okunuyor. Dört küçük figür ilk teknik kontrolde boyut eşiğinin altında kaldı. Yeniden ölçeklendikten sonra geçti.

**Bağlam ve öğretim notu.** R0271 “hortum” hava durumu ünitesinde dönen fırtına hunisi, R0305 “kürek” oyun ünitesinde kum küreği, R0432 “kart” doğum günü ünitesinde kutlama kartı olarak ele alındı. “Yavaş otobüs” için durağan bir keçe fotoğrafında hız kesin olarak okunamıyor. R0688, hız çizgileri olan hızlı taşıt kartlarıyla karşılaştırılarak kullanılabilir. Ayrıca ilk 24 görselin sabit sayfası sayfalar/ilk-24.png dosyasında korunuyor.

Devam sırası resimler.csv dosyasındaki partilere göre belirlenir. Sıradaki eksik nesne/sahne kimliği R0783. K serisinin sabit adları scratch/seri/kelime-sirasi.csv dosyasındadır. Yeni görseller için yürütme aracı OpenAI ImageGen. Malzeme denetiminde betiğin ince doku testi ve görsel inceleme birlikte kullanıldı.

## 4–6 Filiz tamamlandı, 4–6 Fidan ilk 40 kart

Bu çalışmada 235 Filiz ve 40 Fidan kartı eklendi. Her kimliğin 912 × 944 saydam PNG aslı ve 570 × 590 alfa kanallı WebP kopyası var. Sayma kartlarında aynı konunun önceden üretilen keçe figürleri kullanıldı. Diğer yeni motifler dört B referansı ve tekrar eden konuların görselleriyle OpenAI ImageGen üzerinden üretildi. Araç alt model sürümünü bildirmedi.

| Parti · nesne ve sahne | Bu çalışmada eklenen | Toplam hazır | Teknik kontrolden geçen | Teknik hatalı | Kalan |
| --- | ---: | ---: | ---: | ---: | ---: |
| 4–6 Filiz | 235 | 247 | 247 | 0 | 0 |
| 4–6 Fidan | 40 | 40 | 40 | 0 | 192 |

Filiz’de 164 nesne ve 83 sahne yedi sayfada, Fidan’da ilk 30 nesne ve 10 sahne iki sayfada görülebilir. Konum, çoğulluk, renk, meslek ve hareket kartları görsel olarak incelendi. Aynı levhadan yanlış ayrılan iki deniz hayvanı teknik denetimde boş göründü. Levha yeniden ayrıldı, ilgili dört kesit görsel olarak doğrulandı. Tava, gökyüzü, kumsal ve kum havuzu tariflerinde modelin eklediği nesneler yeniden üretimde giderildi. Fidan’da tavşan ve kaplumbağa tek sahnede birleştirildi. Boş bardak, süt dolu bardak ve fırın ayrı görseller olarak kontrol edildi. R1219 şaşkın yüzde son üretimde büyütülen gözler, açık ağız ve tene yakın kahverengi dikiş korundu.

**Anlam sınırları ve belirsiz tarifler.** R0872 “kuzen” için aile dersinin çocuk seçeneği kullanıldı. Akrabalık ilişkisini tek başına portreden çıkarmak mümkün olmadığından dersin sözlü bağlamı gerekir. R1137 “kemençe” için bölgesel tür belirtilmemiştir. Dar gövdeli, üç telli ve yaylı Karadeniz kemençesi yorumu kullanıldı. Bölgesel çalgı ayrıntıları için uzman doğrulaması yapılmadı. R1183’te piknik eylemi görünür, hafta sonu anlamı ders sorusundan gelir. R1201 ve R1202’de iki günlük takvimin sağ bölmesi yarının güneşini, sol bölmesi dünün yağmurunu gösterir. Boyut sıfatları aynı ölçekte gösterilen kartlar arasında karşılaştırılmalıdır.

**Güncel toplam.** 1.971 nesne ve sahnenin 686’sı, 888 insanlı kimliğin 6’sı hazır. K serisinde 724 kart sırada. Böylece onaylı 3.583 kimliğin 692’si tamamlandı ve 2.891’i kalan üretim listesinde. 609 karakterli ve 55 yazılı satır ayrıca beklemede. Sonraki eksik kimlik 4–6 Fidan R1241 “kütüphane”.

## 19 Kasım 2026 · 4–6 Fidan tamamlandı

192 yeni kart eklendi. Böylece partideki 154 nesne ve 78 sahnenin tamamı hazır. Verilen denetim betiği 232 PNG dosyasının 232’sini geçirdi. Hatalı 0, eksik 0. Yedi önizleme sayfası üretildi. Kartların 912 × 944 RGBA asılları ve 570 × 590 alfa WebP kopyaları (kalite 85) kaydedildi.

Görsel kontrolde R1267’de iki portakal, R1268’de iki armut sayıldı. R1255–R1258’de okların yönü, R1317–R1347’de nesnelerin konumu ve R1565–R1567’de ışık renkleri ve yaya simgesi karşılaştırıldı. R1259 çarşı ve R1418 çadır kartlarındaki fazladan bayrak, R1490 ay kartındaki yıldızlar ve R1542 elbisedeki amblem yeniden üretimde kaldırıldı. R1386 için poşet yerine açık karton kutu üretildi. R1337 ve R1339’da iki kişilik kanepe ve yanındaki kitabın yeri netleştirildi. R1438, R1446, R1449 ve R1457 levhasındaki düşük opaklıklı zemin temizlenerek dört kart yeniden ayrıldı. Üç yeniden denemeden sonra açık kalan Fidan sorunu yok.

Belirsiz tariflerde R1263 “kasa” alışveriş ünitesindeki ödeme kasası, R1353 “yuva” hayvan ünitesindeki kuş yuvası, R1425 “dil” ise ağız içindeki organ olarak işlendi. R1258 için kartın üst kenarına yönelen düz ok kullanıldı. R1434’te kütüphane görülebilir; sessizlik dersin sesli bağlamından anlaşılır. Üretim aracı OpenAI ImageGen, alt model sürümü araç tarafından belirtilmedi.

Bu parti sonunda uygun R ve K kartlarının 884/3.583’ü hazır. 878 nesne ve sahne, 6 insanlı kart üretildi. 1.093 nesne ve sahne, 882 insanlı kart ve 724 K kartı sırada (toplam 2.699). Ayrı bekleyen 609 karakterli ve 55 yazılı satır bu toplama dahil edilmedi.

## 19 Kasım 2026 · 4–6 Ağaç ilk 67 kart

45 nesne ve 22 sahne üretildi. Teknik kontrolden 67/67 kart geçti, hatalı 0. Bu partinin nesne ve sahne listesinde 139 kart kaldı. İlk iki önizleme sayfasında kutunun içinde, altında ve arkasındaki top ayrı ayrı görülebilir. Üç Küçük Domuz kartında üç figür sayıldı. R1613 kurt ve R1614 tavşanın ifadeleri yenilendi. Perde ve domuzcukların tasarımları tekrar eden sahnelerle eşleştirildi. R1641–R1645 çiçeklerinin merkezindeki yüzler kaldırıldı; solma ve sulanma gövde, yaprak ve toprakla gösterildi. R1595 “fener” için dersin mum ve lambayla karşılaştırdığı el feneri kullanıldı. R1662–R1664 için tercih edilen ortam kapının ardında gösterildi. Çözümsüz kalan üretim hatası 0. Üretim aracı OpenAI ImageGen.

Bu çalışmanın toplamı 259 yeni PNG ve 259 WebP (192 Fidan, 67 Ağaç). Onaylı 3.583 karttan 951’i hazır, 2.632’si sırada. Hazır kartlar 945 nesne ve sahne ile 6 insanlı karttan oluşuyor. Sırada 1.026 nesne ve sahne, 882 insanlı kart ve 724 K kartı var. 609 karakterli ve 55 yazılı kart ayrıca bekliyor. Sıradaki kimlik 4–6 Ağaç R1669 “sağa dönen ok”.

## 19 Kasım 2026 · 4–6 Ağaç tamamlandı

Bu çalışmada 139 yeni nesne ve sahne kartı eklendi. Ağaç partisindeki 137 nesne ve 69 sahnenin tamamı hazır. Teknik denetim 206/206 PNG dosyasını geçirdi, hata 0. Altı karşılaştırma sayfası oluşturuldu. Saydam PNG asılları 912 × 944, alfa WebP kopyaları 570 × 590 piksel ve kalite 85. Üretimde onaylı B referanslarıyla OpenAI ImageGen kullanıldı. Alt model sürümü araç tarafından bildirilmedi.

R1669 ve R1670’te sağa ve sola dönen oklar, R1671–R1673’te robotun yürüdüğü, durduğu ve döndüğü görseller karşılaştırıldı. İlk R1683 görselinde dört iz vardı. Tek iz görselinden iki ve beş iz kartları kuruldu ve sayıldı. R1687’de fırın ve okulun arasından yol geçiyor. R1728, R1732 ve R1733 için toprak, fide ve kök ayrı üretildi. R1858–R1860’ta resim ile nesneyi ayırt etmek için kâğıdın kenarları görünür bırakıldı. R1880 sakin karda kar taneleri, R1881 doluda taneli buz görülebilir. Ayrıştırma hatası görülen hava kartları yeniden gösterilip kontrol edildi.

“Türkiye’de” ünitesinin R1824 sorusu Rize’de bahçelerde yetişen çayı soruyor. Tomurcuk ve yeşil yapraklı çay sürgünü kullanıldı. Belirsiz R1822 “çay bahçesi” aynı ünitenin Rize bağlamında yamaçtaki çay tarımı olarak işlendi. R1818 “gökte balonlar” Kapadokya sorusuna göre sıcak hava balonlarıdır. R1861 “hamurdan kedi” küçük yuvarlak parçalardan kurulmuş bir figürdür; hamur malzemesini yalnızca keçe görüntüsünden ayırt etmek güçtür. Bu kart öğretmenin sözlü tarifiyle birlikte değerlendirilmelidir.

Parti sonunda toplam 1.090/3.583 kart hazır. 1.084 nesne ve sahne ile 6 insanlı kart üretildi. Sırada 887 nesne ve sahne, 882 insanlı, 724 K kartı var (toplam 2.493). Ayrıca 609 karakterli ve 55 yazılı satır bekliyor.

## 19 Kasım 2026 · 4–6 Çınar ilk 163 kart

98 nesne ve 65 sahne görsel olarak incelendi. Teknik denetim 163/163 kartı geçirdi, hata 0. Beş önizleme sayfası oluşturuldu. Aynı keçeden kesilmiş kırmızı toplar R1981’de iki, oyuncaklar R1982’de üç adet. R1983’te tek top ve tek araba, R1984’te yeşil elma ve R1985’te çizgili karpuz doğrulandı. Piyon kartlarında mavi taş başlangıç konumunu, kırmızı taş hedef konumunu gösterir. R2091 ve R2093’te kareler sayıldı; R2092’de kırmızı piyon tahtanın dışında. R1987’de kalem defterin altında, R2021’de ataş ve R2128’de elma masanın üzerinde. R2115’te kedi ve köpek mamaları birlikte gösterildi. R2034–R2035’te kuklanın ipleri görünür. R2001’de örümcek başına sekiz, R2141’de karıncada altı bacak sayıldı. Çınar’ın bu bölümünde açık kalan deneme yok.

Ağaç ile birlikte bu noktaya kadar 302 yeni PNG ve 302 WebP eklendi. 1.253/3.583 kart hazır. Kalan 2.330 kartın 724’ü nesne ve sahne, 882’si insanlı, 724’ü ek sözcüktür. Ayrı bekletilen 609 karakterli ve 55 yazılı satır bu sayılara dahil edilmedi. Çınar’da sonraki kart R2189 “el ele takım”.

## 19 Kasım 2026 · 4–6 Çınar, 261 kart teslimde

98 kart daha eklendi. Partide 162 nesne ve 99 sahne hazır. Teknik kontrolde 261/261 geçti, hatalı dosya 0. Sekiz önizleme sayfası var. R2218 “kabuk” için dersin kaplumbağanın sırtını sorması nedeniyle kaplumbağa kabuğu seçildi. R2194’te takım oyunu ünitesine uygun sade bir oyun bayrağı kullanıldı. R2311’de uyuyan kukla üretimine eklenen harfler kaldırıldı. R2343’te tam üç taş sayıldı. R2320 ve R2327’de nesnenin kayıp olduğu bilgisi sözlü öyküyle tamamlanır.

263 nesne ve sahne satırından iki tanesi yayınlanmadı. R2237 “yedi rakamı” sorusu yediyi rakam olarak göstermeyi, R2256 “adın ve imzan” seçeneği isim ve imza göstermeyi gerektiriyor. Saat ve takvim dışındaki kartlarda rakam ve harf kullanımına izin verilmediği için ikisi açık bırakıldı. Yedi nesne resmi veya boş bir mektup, bu iki seçeneğin anlamını karşılamıyor. Bu iki kimlik çelişkisi çözülmemiş kart olarak sıradaki toplamda sayılıyor. 609 karakterli ve 55 yazılı satırdan ayrıdır.

Çınar sonunda 1.351/3.583 kart hazır, kalan 2.232. Hazır kartların 1.345’i nesne ve sahne, 6’sı insanlı. Kalanlar 626 nesne ve sahne (Çınar’daki iki kart dahil), 882 insanlı ve 724 K serisi. Sıradaki parti 4–6 Orman.

## 19 Kasım 2026 · 4–6 Orman

145 nesne ve 90 sahne üretildi. 235/235 kart teknik kontrolden geçti, hatalı dosya 0. Yedi önizleme sayfası oluşturuldu. R2561’de üç ve R2562’de bir salıncak sayıldı. R2799 ve R2800’de aynı ayakkabı 824 ve 660 piksel genişlikle gösterilerek fark karşılaştırılabilir hale getirildi. R2502 uyuyan robottaki harfler, R2457 muhabirdeki soru balonu ve R2773 penguendeki fazladan aksesuarlar kaldırıldı. R2450 kumdan kale sadeleştirildi. R2681 dalgıcın denizde olduğu açıkça gösterildi.

R2716 Türk bayrağı, Türk Bayrağı Tüzüğü’nün 4. maddesindeki ölçülerden oluşturulan kalıpla karşılaştırıldı. Bayrak 3:2 en-boy görünümünde yataydır. Kırmızı keçe ve beyaz dikişli ay-yıldız fotoğrafındaki biçimler kalıba hizalandı. Lifler ve dikiş nedeniyle beyaz alanların kalıpla piksel örtüşmesi tam değildir. Kesişim/birleşim oranı ayda %95,7 ve yıldızda %94,7 olarak ölçüldü. [Türk Bayrağı Tüzüğü, madde 4 ve Ek 1](https://fidi.meb.k12.tr/meb_iys_dosyalar/60/04/606961/dosyalar/2019_10/26092232_bayrak_tuzuYu.pdf)

R2514 “kupa” çay bardağı ve şişe seçenekleriyle birlikte sorulduğundan kulplu içecek kupasıdır. R2583 atasözü kitabının kapağında, derste geçen “Damlaya damlaya göl olur” sözüne gönderme yapan damlalar ve göl vardır. R2693–R2695’te ucuzluk ve pahalılık ders içi karşılaştırmaya dayanır. R2415 (3–0) ve R2416 (1–0) skorları, tarafları renklerle ayırt edilen aynı tabelanın bölmelerinde üç veya bir kırmızı pul ile boş mavi bölme kullanılarak gösterildi.

İki satır yazı kuralıyla çeliştiğinden açık bırakıldı. R2417 açıkça “berabere” yazan 2–2 skor tabelası, R2817 ise içinde hem resimler hem yazılar olan süslü defter istiyor. İkisi de bu partideki 237 hedefin içinde ve kalan sayısına dahil. Çınar ile birlikte bu sebeple açık kalan nesne/sahne kimlikleri R2237, R2256, R2417 ve R2817. 609 karakterli ve 55 yazılı satır bunlara ek olarak bekliyor. Araç OpenAI ImageGen. Alt model sürümü belirtilmedi.

## 19 Kasım 2026 · 7–9 Tohum ilk 55 nesne ve sahne

42 nesne ve 13 sahnenin 55/55’i teknik kontrolden geçti. Hatalı dosya 0, bu partide sırada 56 nesne ve sahne var. İki önizleme sayfasında daha önce onaylanan bir insan kartı da yer alıyor. R2822–R2824 için “Günaydın!”, “Merhaba!” ve “Hoşça kal!” sözleri, yazısız olarak sabah uyanma, karşılıklı selamlaşma ve el sallayarak ayrılma sahneleriyle gösterildi.

R2859’da beş ve iki açık parmak sayıldı. 2, 4, 5, 6, 7, 8 ve 9 mumlu pasta kartları aynı pembe pasta ve aynı ayrı keçe mum kullanılarak kuruldu. R2863–R2872’de yıldız, kalem ve elma sayıları görsel olarak kontrol edildi; çoğaltılan parçalar teknik olarak da sayıldı. R3039 ve R3040 aynı serinin daha ilerideki beş ve sekiz mumlu pasta kartlarıdır, bu 55’e dahildir. Ders sırasındaki sonraki eksik R2932 “ocak ve tencere”.

Son güncellemede onaylı 3.583 hedeften 1.641 PNG ve bunların 1.641 alfa WebP kopyası hazır. Bunların 1.635’i nesne ve sahne, 6’sı insanlı kart. Kalan 1.942 hedefin 336’sı nesne ve sahne (yazı/rakam kuralıyla çelişen dört satır dahil), 882’si insanlı ve 724’ü K kartı. 609 karakterli ve 55 yazılı satır ayrıca bekliyor. Bir önceki 951 kartlık teslimden bu güncellemeye toplam 690 kart eklendi (139 Ağaç, 261 Çınar, 235 Orman, 55 adet 7–9 Tohum).

## 19 Kasım 2026 · 7–9 Tohum tamamlandı

56 yeni kart eklendi. 111 nesne ve sahne kartının tamamı teknik kontrolden geçti. Hatalı 0, eksik 0. Dört önizleme sayfasında daha önce onaylanan bir insan kartıyla birlikte toplam 112 görsel var. R2859–R2876 sayma serisinin dosyaları üretim başında yeniden sayıldı ve eksik dosya bulunmadı.

R2980–R2986’da yedi işaretli hafta şeridinin ilk günü pazartesi, seçili gün kırmızı. Sözcüğün öğrenilmesinde haftanın bu sırasının derste tanıtılması gerekir. R2987–R2989 açıkça takvim istediğinden seçili günün Türkçe adı da gösterildi. R2944’te fırtına bulutundaki yüz kaldırıldı. R2995’te gökyüzü, R2998’de su ve R2999’da yol eklenerek taşıtın bulunduğu yer görünür hale getirildi. R3000 için taşıtlar ünitesinin bağlamına göre sıcak hava balonu kullanıldı. Üretim aracı OpenAI ImageGen; alt model sürümü bildirilmedi.

## 19 Kasım 2026 · 7–9 Kök tamamlandı

88 nesne ve sahne üretildi. Sayma kartlarında iki kalem, dört kuş, üç/yedi/beş köpek ve üç mumlu pasta kontrol edildi. Altı analog saatte uzun yelkovan 12’ye bakar. Kısa akrep sırasıyla 9, 3, 7, 5, 8 ve 10’u gösterir. Kök’teki üç takvimde seçilen günün adı ve yedi gün arasındaki konumu karşılaştırıldı. R3115 matematik dersini bir kırmızı pul, bir artı ve iki mavi pulla temsil ediyor. R3079 içecek seçeneklerinin bağlamından bir bardak su olarak yorumlandı. R3091, R3093 ve R3094’te model ilk denemede zürafa kullandı. Üç kart yeniden üretildi; çöl, kar ve ormanda aynı tek hörgüçlü kahverengi deve görülüyor. R3102’de yalnızca kaşları çatık yüz bırakıldı. Teknik kontrolde 88/88 geçti. Üç önizleme sayfası var.

## 19 Kasım 2026 · 7–9 Filiz ve Fidan

Filiz’de 83 nesne ve sahnenin 83’ü teknik denetimden geçti. Hatalı 0. Üç önizleme sayfası hazır. R3300–R3302 kartlarında on, altı ve iki domates sayıldı. R3223, R3298 ve R3299’da raflar dükkân cephesinden ayrıldı. R3226 havuzunda sıvı su ve merdiven, R3262’de uçan kartalın altında bulut var. R3297 meyve tezgâhında elma, armut ve muz yer alıyor. Hastalık ünitesindeki R3239 ilaç şişesi ve kaşık, R3240 ise beyaz ilaç tableti olarak yorumlandı. R3328 uzun saplı bağlama, R3329 kanun olarak kontrol edildi.

Fidan’da 39 hedeften 37 PNG ve WebP çifti üretildi. 37/37 teknik kontrolden geçti, iki önizleme sayfası hazır. R3395 ve R3398’de yoğurtlu mantı, R3394 ve R3397’de tepsi ve tek dilim baklava ayrımı kontrol edildi. R3396 malzeme ve adımları yazılı kâğıt, R3410 ise numaralı forma gerektiriyor. Yazı ve rakam kuralıyla çelişen bu iki satır açık bırakıldı. Bu bölümde kullanılan görsel araç OpenAI ImageGen. Alt model sürümü araç tarafından bildirilmedi.

## 19 Kasım 2026 · Son nesne ve sahne partileri

7–9 Ağaç’ta 28/28, 7–9 Çınar’da 18/18 ve 13–15 Kök’te 3/3 kart üretildi. Ağaç’ta R3444 aynı boy iki kırmızı top, R3445 aynı desende büyük ve küçük top içeriyor. R3465’te yumurta, tırtıl, koza ve kelebek saat yönünde sıralandı. Çınar’da R3484’te iki özdeş araç var. R3485’te “Cuma” takvimde kırmızı ip halkasının içinde. R3489’da balık sağa sıçrıyor ve sudaki akıntı okları sola gidiyor. 13–15 Kök’te aynı kalem kutusunun çantanın içinde, masanın üstünde ve masanın altında olduğu kontrol edildi. Her parti için bir önizleme sayfası oluşturuldu.

7–9 Orman’da 17 hedeften 16’sı üretildi ve teknik kontrolden geçti. R3502 gazete başlığını büyük harflerle göstermeyi gerektirdiği için açık bırakıldı. R3508’de nazar boncuğu, R3509’da kına gösterildi. R3513 “bir tahmin” için çevre ünitesinde çocuğun yağmur yağacağını düşünmesi seçildi. Görsel bu somut örneği gösteriyor. R3515 denizdeki plastiklerin fotoğrafını keçe dalga, keçe şişeler ve beyaz dikişli fotoğraf kenarıyla temsil ediyor.

Nesne ve sahnelerde toplam 1.971 satırın 1.964’ü teslim edilebilir durumda. Açık yedi satır R2237, R2256, R2417, R2817, R3396, R3410 ve R3502. Bunlar CSV’de nesne ya da sahne olarak sınıflandırılmış, ancak tarif yazı veya rakam gerektiriyor. 609 karakterli ve 55 yazılı satır bu yedi satırdan ayrı tutuldu.

## 19 Kasım 2026 · 4–6 Kök insanlı kartları

106 yeni kart, onaylı beş eski Kök örneğiyle birlikte 111 insanlı kartı tamamladı. İnsan kartlarında malzeme için dört B görseli, figür ve dikiş için altı onaylı insan denemesi ve sahneye göre yinelenen nesneler kullanıldı. R0128’de annenin açık ellerinde beşer parmak sayıldı. R0037 ve R0488 asıl öğretmenin koyu saç topuzu, sarı üstü ve mavi eteğiyle yeniden üretildi. R0132, R0154 ve R0447’de genç baba ile gri saçlı dede ayrımı düzeltildi. R0024 ve R0332’de uyuyan figür okul çağında bir çocuktur. R0360 kaldırımda bekleyen kız olarak düzeltildi. R0137 ve R0150’de abla aynı mor kapüşonlu giysiyi giyiyor. Koyu saçta ve koyu ten kenarında renk uyumlu koyu ip kullanıldı. CSV’nin insanlı sınıfında geçen R0209 patates kızartması, R0282 kardan adam ve R0407 polis arabası tariflerine göre insan eklenmeden üretildi. 4–6 Kök için dört insan önizleme sayfası hazır.

Bu teslim noktasında 1.964 nesne ve sahne ile 112 insanlı kart olmak üzere 2.076 PNG ve 2.076 WebP çifti hazır. 3.583 hedefin 1.507’si henüz teslim kapsamında değil. Bunların 7’si yazı veya rakam gerektiren nesne/sahne, 776’sı insanlı kart ve 724’ü K serisi sözcük. 609 karakterli ve 55 yazılı kaynak satırı ayrıca bekliyor.

## 19 Kasım 2026 · 4–6 Tohum insanlı kartları

46 yeni PNG ve WebP çifti üretildi, 46/46 teknik denetimden geçti. İnsan kartları iki önizleme sayfasında. R0522 ve R0554’te genç babanın kısa koyu saçları ve mavi gömleği, R0531’de öğretmenin saç topuzu, sarı üstü ve mavi eteği düzeltildi. R0525’te yerde uzanan çocuk uyanık. R0727’de dönme hareketi tek çocuk ve ayaklarının çevresindeki kavisli işaretle gösterildi. R0611 babaanne ve R0140 anneanne kartlarında ailedeki iki büyüğe ayrı görünüş verildi. Akrabalığın hangi ebeveyn üzerinden kurulduğu tek başına bir yetişkin portresinden anlaşılamaz, bu kartların anlamını ders belirler.

Teslimde 2.122 kart var. 1.964 nesne ve sahne, 158 insanlı kart. 1.461 kalan hedefin 7’si yazı/rakam çelişkisi, 730’u insanlı kart ve 724’ü K sözcüğü.

## 19 Kasım 2026 · 4–6 Filiz insanlı kartları

96 kart üretildi ve üç önizleme sayfasına yerleştirildi. 96/96 insanlı kart teknik denetimden geçti. R0881’de anne, baba ve iki çocuk sayıldı. R0990’daki öğlen parkı tek çocukla yeniden yapıldı. R1004 aynı doktorla, R1018 aynı hemşireyle ve R1022 aynı ressamla eşleştirildi. R1059’da bankta oturan iki kişi çocuk. R1102’de tek başına uyuyan çocuk ile R1097’de ağlayan bebek kendi yaş özellikleriyle ayrıldı. R1127’de darbukanın kadeh biçimli gövdesi ve çıplak elle çalınması kontrol edildi. R0873 dayı ve R0874 hala için standart yetişkin portresi kullanıldı. Akrabalık bağı ders bağlamında öğreniliyor.

Teslimde 2.218 kart var. 1.964 nesne ve sahne, 254 insanlı kart. Kalan 1.365 hedefin 7’si yazı/rakam çelişkisi, 634’ü insanlı kart ve 724’ü K sözcüğü.

## 4-6 Fidan · insanlı seri denetimi

111 PNG ve 111 alfa WebP üretildi. Teknik denetimden 111/111 kart geçti. 4 önizleme sayfası var. R1187’de ilk takvim hücresi bugünü, kırmızı işaretli üçüncü hücre iki gün sonrasını gösteriyor. R1297’de çocuk yatağın yanında ayakta su içiyor. R1322–R1324’te aynı bebeğin yatakta, masanın altında ve kutunun içinde olması karşılaştırıldı. R1398, R1409 ve R1410’da prensesin tacı, bukleleri ve mor elbisesi eşleştirildi. R1452’de ikişer çocuklu iki takım var. R1455’te çocuk kaldırımda kırmızı ışıkta bekliyor. R1533’te uyuyan dedenin üzerindeki harfler kaldırıldı. R1538 ve R1544’te çocuğun konukla etkileşimi, R1575’te çocukların sinema perdesine bakış yönü kontrol edildi. R1579’da kamera file dönük. R1581’de aile zürafanın önünde, fotoğraf makinesi babanın elinde.

Teslimde 2.329 kart var. Nesne ve sahne 1964, insanlı 365, K serisi 0. Kalan 1254 hedefin 7 tanesi nesne/sahne, 523 tanesi insanlı ve 724 tanesi K serisi. 609 karakterli ve 55 yazılı satır ayrıca bekliyor.

## 4-6 Ağaç · insanlı seri denetimi

62 PNG ve 62 alfa WebP üretildi. Teknik denetimden 62/62 kart geçti. 2 önizleme sayfası var. R1626–R1628’de ormanda yürüyen, yüzen ve evde uyuyan masal kızının saç ve yüzü aynı örnekle eşleştirildi. R1706’da tek uçurtmayı iki çocuk birlikte uçuruyor. R1827, R1828, R1835 ve R1838 aynı kaynak sayfasından ayrı saydam dosyalara alındı. R1841–R1843’te iki yarım elma ve iki çocuk, bir bütün elma ve bir çocuk, üç elma ve üç çocuk ayrı ayrı sayıldı. R1854’te hamur yoğuran çocuk, R1779’da doktor önlüğü giymiş çocuk var. R1899’da önkolu tutma ile R1906’da omza dokunma ayrımı görselde kontrol edildi.

Teslimde 2.391 kart var. Nesne ve sahne 1964, insanlı 427, K serisi 0. Kalan 1192 hedefin 7 tanesi nesne/sahne, 461 tanesi insanlı ve 724 tanesi K serisi. 609 karakterli ve 55 yazılı satır ayrıca bekliyor.

## 4-6 Çınar · insanlı seri denetimi

61 PNG ve 61 alfa WebP üretildi. Teknik denetimden 61/61 kart geçti. 2 önizleme sayfası var. R2138’de çocuk dürbünle kuşa, R2140’ta büyüteçle karıncaya bakıyor. R2197 “uzakta oturan çocuk” için önde bank, geride daha küçük ölçekte oturan çocuk kullanıldı. R2165’te atık yere düşüyor, R2250’de çocuk kâğıdı kutuya atıyor. R2231’de koşan çocuğun yanına komşu yüzme kartından taşan mavi damlalar kaldırıldı. R2260–R2262’de uyuyan, koşan ve öğrenciye yardım eden öğretmenin saç topuzu, sarı üstü ve mavi eteği eşleştirildi. R2267 bir bebek çıngırağı olduğu için karta figür eklenmedi.

Teslimde 2.452 kart var. Nesne ve sahne 1964, insanlı 488, K serisi 0. Kalan 1131 hedefin 7 tanesi nesne/sahne, 400 tanesi insanlı ve 724 tanesi K serisi. 609 karakterli ve 55 yazılı satır ayrıca bekliyor.

## 4-6 Orman · insanlı seri denetimi

165 PNG ve 165 alfa WebP üretildi. Teknik denetimden 165/165 kart geçti. 5 önizleme sayfası var. R2432’de aynı iki çocuk önce denizde, sonra parkta görülüyor. R2496’daki fazladan su damlaları temizlendi. R2498’de aşçı şapkası takan figürün çocuk olması, R2520’de çocuğun elbiseyi üzerine geçirmesi düzeltildi. R2534’te iki çocuk aynı salıncakta, R2542’de biri salıncakta, diğeri sıra bekliyor. R2651’e çocuğun uzaklaştığı kaydırak eklendi. R2708’de yerdeki dört araba ve teslim edilen beşinci araba sayıldı. R2728’de uçağa binen aile ile Türk bayrağı görülebiliyor. R2746’da dizde küçük bir yara bandı var. R2782’de uyku harfleri temizlendi. R2783 ve R2787’de satıcının saç topuzu, giysisi ve dükkânı diğer satıcı kartlarıyla eşleştirildi.

Teslimde 2.617 kart var. Nesne ve sahne 1964, insanlı 653, K serisi 0. Kalan 966 hedefin 7 tanesi nesne/sahne, 235 tanesi insanlı ve 724 tanesi K serisi. 609 karakterli ve 55 yazılı satır ayrıca bekliyor.

## 7-9 Tohum · insanlı seri denetimi

45 PNG ve 45 alfa WebP üretildi. Teknik denetimden 45/45 kart geçti. 2 önizleme sayfası var. R2836’da kapıyı açan ve ziyarete gelen iki çocuk aynı yaşta görünüyor. R2886 biri küçük iki kardeşi, R2887 bir çocuk ve üç kardeşini gösteriyor. R2903’te parmak burunda, R2904’te kulakta. R2914 ve R2924’te çocuğun havucu ve yumurta tabağını ileri itmesi için elin nesneyle teması düzeltildi. R2968’de çocuk sandalyeye oturuyor. R3004’te okula giden çocuk arka koltukta, sürücü önde. R3016’da mumları bir çocuk üflüyor ve R3019’da pastayı bir çocuk kesiyor. Bu partinin 45 kartından R3044 daha önce onaylanan insan denemesinden geliyor.

Teslimde 2.661 kart var. Nesne ve sahne 1964, insanlı 697, K serisi 0. Kalan 922 hedefin 7 tanesi nesne/sahne, 191 tanesi insanlı ve 724 tanesi K serisi. 609 karakterli ve 55 yazılı satır ayrıca bekliyor.

## 7-9 Kök · insanlı seri denetimi

64 PNG ve 64 alfa WebP üretildi. Teknik denetimden 64/64 kart geçti. 2 önizleme sayfası var. R3059–R3061 aynı anneyi banyoda, bahçede ve mutfakta gösteriyor. R3099’da çocuğun eli kendi önkolunu tutuyor. R3110’da montu giyen, R3131’de çamaşır asan figür çocuk olarak düzeltildi. R3151’de tarlada sağa giden traktörü yetişkin bir çiftçi sürüyor. R3191’de çocuk kendi sırt çantasıyla arkadaşının çantasını taşıyor. R3195’te gündelik bir şapka kullanıldı. R3198, R3199 ve R3200’de sırasıyla üç, bir ve iki çocuk sayıldı. R3199’un özgün üretiminden tek çocuk ayrıldı.

Teslimde 2.725 kart var. Nesne ve sahne 1964, insanlı 761, K serisi 0. Kalan 858 hedefin 7 tanesi nesne/sahne, 127 tanesi insanlı ve 724 tanesi K serisi. 609 karakterli ve 55 yazılı satır ayrıca bekliyor.

## 7-9 Filiz · insanlı seri denetimi

65 PNG ve 65 alfa WebP üretildi. Teknik denetimden 65/65 kart geçti. 2 önizleme sayfası var. R3206’da yüzen çocuk ve R3284’te çöp poşetini kutuya bırakan çocuk okul çağı figürleriyle yeniden üretildi. R3212’de aile pastayı mutfakta hazırlıyor. R3217 ve R3219’da üçer çocuğun en kısası ve en uzunu ayırt edilebiliyor. R3254’te çocuğun yolunu bilmediği, yüz ifadesi ve çatallanan patikayla gösterildi. R3267’de kızıl kuyruklu tilki sağa bakıyor, kartta insan yok. R3277 boş hasta yatağı. R3282’de bilgisayar ekranındaki fotoğraf ve dışarı yönelen ok, gönderme eylemini gösteriyor. R3310’da çocuk kolonya şişesini misafire uzatıyor.

Teslimde 2.790 kart var. Nesne ve sahne 1964, insanlı 826, K serisi 0. Kalan 793 hedefin 7 tanesi nesne/sahne, 62 tanesi insanlı ve 724 tanesi K serisi. 609 karakterli ve 55 yazılı satır ayrıca bekliyor.

## 7-9 Fidan · insanlı seri denetimi

23 PNG ve 23 alfa WebP üretildi. Teknik denetimden 23/23 kart geçti. 1 önizleme sayfası var. R3357’deki uyku harfleri temizlendi. R3377’de çocuk dedesini ekranda görüyor. R3386’da baretli kişi köprü çiziyor. R3387 boş hasta yatağı. R3403’te tahtanın önündeki öğretmen masasının üzerinde yalnız kitaplar var. R3409’da aynı çocuk önce topu atıyor, ardından uzaklaşıyor. R3411’de çocuk kitapları okula taşıyor, R3412’de kitap evde masanın üzerinde kalıyor.

Teslimde 2.813 kart var. Nesne ve sahne 1964, insanlı 849, K serisi 0. Kalan 770 hedefin 7 tanesi nesne/sahne, 39 tanesi insanlı ve 724 tanesi K serisi. 609 karakterli ve 55 yazılı satır ayrıca bekliyor.

## 7-9 Ağaç · insanlı seri denetimi

27 PNG ve 27 alfa WebP üretildi. Teknik denetimden 27/27 kart geçti. 1 önizleme sayfası var. R3421’de taş figür gri keçeyle işlendi. R3428’de çocuk, ince belli bardakta çayı ve tek kurabiyeyi tepsiyle misafire uzatıyor. R3430’daki bütün pastayı alan çocuğun yanına taşan figür, ait olduğu sıra kartına alındı. R3449’da çocuklar kutuyu taşırken uzatılan parayı geri çeviriyor. R3458’de oyuncağın kırılması, oyuncak arabadan ayrılan tekerlekle gösterildi. R3463’te masal devi ağaçlardan uzun. R3471’de çocuk sahne perdesinin arkasında, elini göğsünde tutuyor.

Teslimde 2.840 kart var. Nesne ve sahne 1964, insanlı 876, K serisi 0. Kalan 743 hedefin 7 tanesi nesne/sahne, 12 tanesi insanlı ve 724 tanesi K serisi. 609 karakterli ve 55 yazılı satır ayrıca bekliyor.

## 7-9 Çınar · insanlı seri denetimi

4 PNG ve 4 alfa WebP üretildi. Teknik denetimden 4/4 kart geçti. 1 önizleme sayfası var. R3487’de çocuk sınav kâğıdının başında tırnağını yiyor. R3493’te yatağa çıkan çocuğun ayakkabıları görünür durumda. Şiir ve Duygu ünitesinde R3494 iki çocuğun birlikte gülüp dans etmesini, R3495 bir çocuğun yağmurda tek başına durmasını gösteriyor. R3495’teki şemsiye kaldırıldı.

Teslimde 2.844 kart var. Nesne ve sahne 1964, insanlı 880, K serisi 0. Kalan 739 hedefin 7 tanesi nesne/sahne, 8 tanesi insanlı ve 724 tanesi K serisi. 609 karakterli ve 55 yazılı satır ayrıca bekliyor.

## 7-9 Orman · insanlı seri denetimi

8 PNG ve 8 alfa WebP üretildi. Teknik denetimden 8/8 kart geçti. 1 önizleme sayfası var. R3496’da torun ve dede sarılıyor, ikisinin de yanağında sevinç gözyaşı var. R3497’de palyaçonun düşüşü yumuşak ve komik. R3500’de çocuklar iki ayrı kitap tutuyor. R3511’de kürsü ve tokmak, R3519’da tren peronunda birbirine el sallayan iki arkadaş, R3520’de sınav kâğıdına yazan çocuk görülüyor.

Teslimde 2.852 kart var. Nesne ve sahne 1964, insanlı 888, K serisi 0. Kalan 731 hedefin 7 tanesi nesne/sahne, 0 tanesi insanlı ve 724 tanesi K serisi. 609 karakterli ve 55 yazılı satır ayrıca bekliyor.

## R serisi toplu denetimi

Tüm partiler birlikte denetlendi. Nesne, sahne ve insanlı türlerindeki 2.859 satırın 2.852’sinde dosya var. Teknik denetimden 2.852 kart geçti, hatalı dosya ve birebir kopya sayısı sıfır. Kalan yedi tarif yazı veya rakam gerektiriyor. Karakterli ve yazılı türler bu sayılara dahil değil.

## K0001–K0036 · sözcük görselleri

36 kart üretildi. PNG ölçüsü ve ortalaması, saydam zemin, malzeme dokusu, kenar payı ve WebP alfa kanalı denetlendi. K0005’te çocuk ellerini oturağa dayayarak ayağa kalkıyor. K0014 ve K0020’de aynı tipte çocuk yastık olmadan yan yatıyor. K0021’de çocuk yalnızca ekmeği tutuyor. K0034’te iki tavşan özgün üretimden ayrılıp sağa bakacak şekilde yan yana yerleştirildi. K0035’te iki tavuk sayıldı.

Teslimde 2888 görsel ve bunların WebP kopyaları var. R serisinde 2852, K serisinde 36 kart hazır. K serisinde 688 sözcük kaldı. Yedi nesne/sahne tarifindeki yazı veya rakam çelişkisi, 609 karakterli ve 55 yazılı kaynak satırı ayrıca kayıtlıdır.

## K0037–K0072 · sözcük görselleri

36 kart üretildi. PNG ölçüsü ve ortalaması, saydam zemin, malzeme dokusu, kenar payı ve WebP alfa kanalı denetlendi. K0038’de çocuk dirseğine öksürüyor, K0039’da mendille hapşırıyor ve K0040’ta burnunu siliyor. K0041–K0044’te elin değdiği diş, karın, şakak ve boğaz ayrı ayrı karşılaştırıldı. K0061’de kaşıklar yan yana diziliyor. K0070’te çocuk iki elmasından birini arkadaşına uzatıyor.

Teslimde 2924 görsel ve bunların WebP kopyaları var. R serisinde 2852, K serisinde 72 kart hazır. K serisinde 652 sözcük kaldı. Yedi nesne/sahne tarifindeki yazı veya rakam çelişkisi, 609 karakterli ve 55 yazılı kaynak satırı ayrıca kayıtlıdır.

## K0073–K0108 · sözcük görselleri

36 kart üretildi. PNG ölçüsü ve ortalaması, saydam zemin, malzeme dokusu, kenar payı ve WebP alfa kanalı denetlendi. K0081’de üç top sayıldı. K0089’un terazisinde taş aşağıda, tüy yukarıda. K0096’da yetişkin bir erkek yakalı gömlek ütülüyor. K0097 “yerleri silmek” için ilk süpürge görseli değiştirildi, sözcük nemli bezli paspasla gösterildi. K0099’da ipe mandallanan tek ıslak gömleğin yakası ve düğmeleri görünür.

Teslimde 2960 görsel ve bunların WebP kopyaları var. R serisinde 2852, K serisinde 108 kart hazır. K serisinde 616 sözcük kaldı. Yedi nesne/sahne tarifindeki yazı veya rakam çelişkisi, 609 karakterli ve 55 yazılı kaynak satırı ayrıca kayıtlıdır.

## K0109–K0144 · sözcük görselleri

36 kart üretildi. PNG ölçüsü ve ortalaması, saydam zemin, malzeme dokusu, kenar payı ve WebP alfa kanalı denetlendi. K0109–K0113’te rendeleme, karıştırma, kaynatma, dilimleme ve yoğurma ayrı hareketler olarak kontrol edildi. K0114’te kanepe ve K0129’da teleskop tek başına görünüyor. K0130’da çocuk büyüğünün elini öpüyor. K0144’te çocuk ekranın dışından, görüntülü aramadaki büyüğüne el sallıyor.

Teslimde 2996 görsel ve bunların WebP kopyaları var. R serisinde 2852, K serisinde 144 kart hazır. K serisinde 580 sözcük kaldı. Yedi nesne/sahne tarifindeki yazı veya rakam çelişkisi, 609 karakterli ve 55 yazılı kaynak satırı ayrıca kayıtlıdır.

## K0145–K0180 · sözcük görselleri

36 kart üretildi. PNG ölçüsü ve ortalaması, saydam zemin, malzeme dokusu, kenar payı ve WebP alfa kanalı denetlendi. K0152’de İstanbul, Boğaz’daki Kız Kulesi ve arka kıyıyla gösterildi. K0153’te tek bir doğal peri bacası var. K0162’de seksek alanının tekli ve ikili kareleri, K0166 ve K0168’de aynı mavi kuşun uçarken ve dala konarken ayaklarının konumu kontrol edildi. K0177’de yalnız el, bez ve pencere yer alıyor. K0180’de ağaçtan düşen iki yaprak sayıldı.

Teslimde 3032 görsel ve bunların WebP kopyaları var. R serisinde 2852, K serisinde 180 kart hazır. K serisinde 544 sözcük kaldı. Yedi nesne/sahne tarifindeki yazı veya rakam çelişkisi, 609 karakterli ve 55 yazılı kaynak satırı ayrıca kayıtlıdır.

## K0181–K0216 · sözcük görselleri

36 kart üretildi. PNG ölçüsü ve ortalaması, saydam zemin, malzeme dokusu, kenar payı ve WebP alfa kanalı denetlendi. K0184’te köpek kulübenin dışında, yanında oturuyor. K0194 ve K0196’da taşların düz ve pürüzlü yüzeyleri karşılaştırıldı. K0206’da bayram şekeri tek, iki ucundan bükülmüş ambalajlı şeker olarak düzeltildi. K0207’de sırada üç kişi var. K0208’in mezurasında yalnız ölçü çizgileri bulunuyor.

Teslimde 3068 görsel ve bunların WebP kopyaları var. R serisinde 2852, K serisinde 216 kart hazır. K serisinde 508 sözcük kaldı. Yedi nesne/sahne tarifindeki yazı veya rakam çelişkisi, 609 karakterli ve 55 yazılı kaynak satırı ayrıca kayıtlıdır.

## K0217–K0252 · sözcük görselleri

36 kart üretildi. PNG ölçüsü ve ortalaması, saydam zemin, malzeme dokusu, kenar payı ve WebP alfa kanalı denetlendi. K0219 ve K0220’de küçük ve büyük giysiler kol boyuyla ayırt ediliyor. K0226’da sade altın renkli madalyon, K0230’da kangal sucuk ve K0231’de açık sarı kaşar dilimi var. K0240’ta iki vagonlu metro sağa bakıyor. K0243’te K0114’ün mavi kanepesi sehpanın arkasında. K0245’te iki elma sayıldı. İlk geçtiği yaşa göre 4–6 grubundaki 221 sözcük kartının tamamı bu partiyle hazır.

Teslimde 3104 görsel ve bunların WebP kopyaları var. R serisinde 2852, K serisinde 252 kart hazır. K serisinde 472 sözcük kaldı. Yedi nesne/sahne tarifindeki yazı veya rakam çelişkisi, 609 karakterli ve 55 yazılı kaynak satırı ayrıca kayıtlıdır.

## K0253–K0288 · sözcük görselleri

36 kart üretildi. PNG ölçüsü ve ortalaması, saydam zemin, malzeme dokusu, kenar payı ve WebP alfa kanalı denetlendi. K0256’da diş hekimi koltuktaki çocuğun dişini küçük aynayla muayene ediyor. K0264–K0266’da aynı renkli top sırasıyla kutunun önünde, kutunun arkasında ve iki kutunun ortasında. K0269’da çocuk arkadan sağa, K0270’te sola dönüyor. K0288’de bağlamanın teknesi, uzun sapı ve telleri görünüyor.

Teslimde 3140 görsel ve bunların WebP kopyaları var. R serisinde 2852, K serisinde 288 kart hazır. K serisinde 436 sözcük kaldı. Yedi nesne/sahne tarifindeki yazı veya rakam çelişkisi, 609 karakterli ve 55 yazılı kaynak satırı ayrıca kayıtlıdır.

## K0289–K0324 · sözcük görselleri

36 kart üretildi. PNG ölçüsü ve ortalaması, saydam zemin, malzeme dokusu, kenar payı ve WebP alfa kanalı denetlendi. Un kartı yeniden üretildi ve tuzla yan yana kontrol edildi. Unda yumuşak toz kıvrımları, tuzda ayrı kristaller görünüyor. Kırağı, kuraklık, buz tutmak ve meslek kartları kendi tarifleriyle karşılaştırıldı.

Teslimde 3176 görsel ve bunların WebP kopyaları var. R serisinde 2852, K serisinde 324 kart hazır. K serisinde 400 sözcük kaldı. Yedi nesne/sahne tarifindeki yazı veya rakam çelişkisi, 609 karakterli ve 55 yazılı kaynak satırı ayrıca kayıtlıdır.

## K0325–K0360 · sözcük görselleri

36 kart üretildi. PNG ölçüsü ve ortalaması, saydam zemin, malzeme dokusu, kenar payı ve WebP alfa kanalı denetlendi. Buharlaşmak kartında kapak kaldırılarak su ve üzerinden yükselen buhar görünür hâle getirildi. Kaynamak kartındaki kabarcıklar, damlamak kartındaki tek damla ve okul servisinin açık kapısı görsellerde kontrol edildi.

Teslimde 3212 görsel ve bunların WebP kopyaları var. R serisinde 2852, K serisinde 360 kart hazır. K serisinde 364 sözcük kaldı. Yedi nesne/sahne tarifindeki yazı veya rakam çelişkisi, 609 karakterli ve 55 yazılı kaynak satırı ayrıca kayıtlıdır.

## K0361–K0396 · sözcük görselleri

36 kart üretildi. PNG ölçüsü ve ortalaması, saydam zemin, malzeme dokusu, kenar payı ve WebP alfa kanalı denetlendi. Tasmanın mavi rengi ve tokası önceki köpek tasmasıyla eşleştirildi. Sesli okuyan çocuğun ağzı ve hüzünlü çocuğun tek gözyaşı yeniden üretimden sonra kontrol edildi. Çikolatalı kek diliminden tarifte bulunmayan meyve ve süsler kaldırıldı. Pamukkale kartındaki beyaz teraslar ve turkuaz havuzlar kontrol edildi.

Teslimde 3248 görsel ve bunların WebP kopyaları var. R serisinde 2852, K serisinde 396 kart hazır. K serisinde 328 sözcük kaldı. Yedi nesne/sahne tarifindeki yazı veya rakam çelişkisi, 609 karakterli ve 55 yazılı kaynak satırı ayrıca kayıtlıdır.

## K0397–K0432 · sözcük görselleri

36 kart üretildi. PNG ölçüsü ve ortalaması, saydam zemin, malzeme dokusu, kenar payı ve WebP alfa kanalı denetlendi. Yargıç kartı tokmak kaldırılarak cübbeli ve kürsüde oturan figürle yeniden üretildi. Çeyrek kartında tek elma diliminin iki düz kesitinin dik açıyla birleştiği kontrol edildi. Mezuniyet, takas, hakem, Türk kahvesi ve çöp ayırmak kartları tarifleriyle karşılaştırıldı.

Teslimde 3284 görsel ve bunların WebP kopyaları var. R serisinde 2852, K serisinde 432 kart hazır. K serisinde 292 sözcük kaldı. Yedi nesne/sahne tarifindeki yazı veya rakam çelişkisi, 609 karakterli ve 55 yazılı kaynak satırı ayrıca kayıtlıdır.

## K0433–K0468 · sözcük görselleri

36 kart üretildi. PNG ölçüsü ve ortalaması, saydam zemin, malzeme dokusu, kenar payı ve WebP alfa kanalı denetlendi. Satranç tahtası yeniden üretildi, sekiz satır ve sekiz sütun sayıldı. Islık çalan çocuğun dudakları büzülmüş, elleri aşağıda. Masa tenisinde iki raket, bir top ve file görünür. Yarımadanın karayla bağlantısı kontrol edildi.

Teslimde 3320 görsel ve bunların WebP kopyaları var. R serisinde 2852, K serisinde 468 kart hazır. K serisinde 256 sözcük kaldı. Yedi nesne/sahne tarifindeki yazı veya rakam çelişkisi, 609 karakterli ve 55 yazılı kaynak satırı ayrıca kayıtlıdır.

## K0469–K0504 · sözcük görselleri

36 kart üretildi. PNG ölçüsü ve ortalaması, saydam zemin, malzeme dokusu, kenar payı ve WebP alfa kanalı denetlendi. Sıraya girmek kartında tek sıradaki üç kişi sayıldı. Not kartı sade çizgili kart olarak, teneffüs zili duvara takılan tokmaklı okul zili olarak yeniden üretildi. Ölçüm kartında mezuranın kutunun kenarına temas ettiği kontrol edildi.

Teslimde 3356 görsel ve bunların WebP kopyaları var. R serisinde 2852, K serisinde 504 kart hazır. K serisinde 220 sözcük kaldı. Yedi nesne/sahne tarifindeki yazı veya rakam çelişkisi, 609 karakterli ve 55 yazılı kaynak satırı ayrıca kayıtlıdır.

## K0505–K0540 · sözcük görselleri

36 kart üretildi. PNG ölçüsü ve ortalaması, saydam zemin, malzeme dokusu, kenar payı ve WebP alfa kanalı denetlendi. Halay kartında el ele üç kişi aynı ayağı kaldırıyor. Grafiklerde sütunlar ve dilimler sayıldı. Kız Kulesi kartından arka plandaki şehir kaldırıldı. Efes kartında Celsus Kütüphanesi’nin alt katındaki üç giriş yeniden üretildi. Yerlerin ayırt edici mimari özellikleri için başvurulan kaynaklar [Topkapı Sarayı](https://islamansiklopedisi.org.tr/topkapi-sarayi), [Celsus Kütüphanesi](https://libdigitalcollections.ku.edu.tr/digital/collection/GHC/id/15719/) ve [Kız Kulesi restorasyon güncesi](https://kizkulesi.gov.tr/restorasyon-guncesi).

Teslimde 3392 görsel ve bunların WebP kopyaları var. R serisinde 2852, K serisinde 540 kart hazır. K serisinde 184 sözcük kaldı. Yedi nesne/sahne tarifindeki yazı veya rakam çelişkisi, 609 karakterli ve 55 yazılı kaynak satırı ayrıca kayıtlıdır.

## K0541–K0576 · sözcük görselleri

36 kart üretildi. PNG ölçüsü ve ortalaması, saydam zemin, malzeme dokusu, kenar payı ve WebP alfa kanalı denetlendi. Kek kalıbı, fırın tepsisinden ayırt edilecek biçimde ortası borulu ve oluklu olarak yeniden üretildi. Göktaşı kartında yerde bulunan, koyu kabuklu taş anlamı kullanıldı ve alev izi kaldırıldı. Okul korosunda üç öğrenci sayıldı. Kabartma yazı ve tekerlekli sandalye tarifleri kontrol edildi.

Teslimde 3428 görsel ve bunların WebP kopyaları var. R serisinde 2852, K serisinde 576 kart hazır. K serisinde 148 sözcük kaldı. Yedi nesne/sahne tarifindeki yazı veya rakam çelişkisi, 609 karakterli ve 55 yazılı kaynak satırı ayrıca kayıtlıdır.

## K0577–K0612 · sözcük görselleri

36 kart üretildi. PNG ölçüsü ve ortalaması, saydam zemin, malzeme dokusu, kenar payı ve WebP alfa kanalı denetlendi. Komodinin üzerindeki lamba kaldırıldı. Peribacası tek kaya oluşumuna indirildi. Işıkları kapatmak kartında düğmeye basan el ve sönmüş lamba görünüyor. İlkokul, lise ve üniversite görselleri yan yana karşılaştırıldı. İlkokul girişinden otele özgü yıldızlar çıkarıldı.

Teslimde 3464 görsel ve bunların WebP kopyaları var. R serisinde 2852, K serisinde 612 kart hazır. K serisinde 112 sözcük kaldı. Yedi nesne/sahne tarifindeki yazı veya rakam çelişkisi, 609 karakterli ve 55 yazılı kaynak satırı ayrıca kayıtlıdır.

## K0613–K0648 · sözcük görselleri

36 kart üretildi. PNG ölçüsü ve ortalaması, saydam zemin, malzeme dokusu, kenar payı ve WebP alfa kanalı denetlendi. Ay evreleri kartında aynı ölçekte hilal, yarım ay ve dolunay bulunuyor. Dolunay için aynı keçe diski kullanıldı. Takımyıldız kartında dört yıldızlı çanak ve sapta üç ek yıldız sayıldı. Patlak lastik kartından otomobil gövdesi, çizelge kartından takvim halkaları kaldırıldı. Kampüste iki bina ve ortak yol görünüyor.

Teslimde 3500 görsel ve bunların WebP kopyaları var. R serisinde 2852, K serisinde 648 kart hazır. K serisinde 76 sözcük kaldı. Yedi nesne/sahne tarifindeki yazı veya rakam çelişkisi, 609 karakterli ve 55 yazılı kaynak satırı ayrıca kayıtlıdır.

## K0649–K0684 · sözcük görselleri

36 kart üretildi. PNG ölçüsü ve ortalaması, saydam zemin, malzeme dokusu, kenar payı ve WebP alfa kanalı denetlendi. Çevrim içi toplantı kartında el sallayan katılımcı ile ekranın içindeki konuşmacı ayrı ayrı görünüyor. Öğrenci yurdu kartı ranza ve çantasıyla gelen öğrenciyle yeniden üretildi. Bayram kahvaltısında çay, peynir ve ekmek bırakıldı. Şehirlerarası otobüs, gece treni ve kampüs servisi sağa dönük.

Teslimde 3536 görsel ve bunların WebP kopyaları var. R serisinde 2852, K serisinde 684 kart hazır. K serisinde 40 sözcük kaldı. Yedi nesne/sahne tarifindeki yazı veya rakam çelişkisi, 609 karakterli ve 55 yazılı kaynak satırı ayrıca kayıtlıdır.

## K0685–K0720 · sözcük görselleri

36 kart üretildi. PNG ölçüsü ve ortalaması, saydam zemin, malzeme dokusu, kenar payı ve WebP alfa kanalı denetlendi. Kulak tıkacı tek nesne olarak yeniden üretildi. Elektrikli araçta şarj girişi gövde üzerinde kaldı. Kampüs haritası bina izleri ve yolları gösteren bir plan olarak yeniden üretildi. Gar kartında perondaki tren ve bağlı vagonu görünüyor. Cezvenin uzun sapı ile dar ağzı ve temassız ödeme kartının cihaz üzerindeki konumu kontrol edildi.

Teslimde 3572 görsel ve bunların WebP kopyaları var. R serisinde 2852, K serisinde 720 kart hazır. K serisinde 4 sözcük kaldı. Yedi nesne/sahne tarifindeki yazı veya rakam çelişkisi, 609 karakterli ve 55 yazılı kaynak satırı ayrıca kayıtlıdır.

## K0721–K0724 · sözcük görselleri

4 kart üretildi. PNG ölçüsü ve ortalaması, saydam zemin, malzeme dokusu, kenar payı ve WebP alfa kanalı denetlendi. Hüzün kartında tek gözyaşı, işçi kartında yerleştirilen tuğla, diploma kartında bağlı belge kontrol edildi. Mahkeme kartı, yükseltilmiş kürsü ile dinleyici sıralarını gösteren boş duruşma salonu olarak yeniden üretildi.

Teslimde 3576 görsel ve bunların WebP kopyaları var. R serisinde 2852, K serisinde 724 kart hazır. K serisinde 0 sözcük kaldı. Yedi nesne/sahne tarifindeki yazı veya rakam çelişkisi, 609 karakterli ve 55 yazılı kaynak satırı ayrıca kayıtlıdır.

## Okul karakterleri ve boy düzeltmesi

Okulun verdiği 15 isim ve resmi karakter sayfasındaki çizimler esas alındı. Ela listede ve resmi sayfada yer alıyor. Giray verilen listede olmadığı için kadroya alınmadı. ImageGen ile üretilen 15 keçe modelinin 912 × 944 PNG ve 570 × 590 WebP kopyaları kontrol edildi. Her modelin etrafında en az 16 piksel saydam alan var.

Ela, Pingucan ve Dino yeni baş ve gövde oranlarıyla tekrar üretildi. Karşılaştırma sayfasında tüm karakterler satırlarında ortak bir taban çizgisine basar. Dünya’nın 770 piksellik boyuna karşılık Ela 454, Pingucan 323 ve Dino 508 pikseldir. Bu çalışma ölçüleri resmi kadro görselinden yaklaşık olarak alındı.

Pusula’nın 35 seviye, 616 ünite ve 5.040 ders içeren sürümü güncellendi. 829 derste içerik değişti. 10.050 testin seçenek ve cevap ilişkileri denetlendi. Karakter olarak kullanılan Can, Deniz ve Ece yerleri sırasıyla Ahmet, Gazi ve Eylül olarak güncellendi. Deniz canlıları, can sıkıntısı gibi sözcükler ve gerçek tarihî kişiler korundu. Öğretim metinlerinde çeşitli yaşları canlandıran roller bulunur. Karakter görsellerinin kaynağı okulun resmi karakter sayfasıdır.

609 karakterli kart tarifinden 27’si belirli sözlerin aktarılmasını gerektiriyor. Görsel üretim listesinde 582 tarif var. Önceki teslimdeki 55 yazılı kart ve yazı veya rakam isteyen 7 nesne ve sahne kartı ayrıca bekliyor. Karakterli kartların sonuçları aşağıdaki tabloda yer alıyor.

İlk 130 karakterli kartın görsel ve teknik denetimi tamamlandı. Denetlenen kartların PNG ve WebP kopyaları ana teslim klasörlerinde yer alıyor.

4–6 Kök partisinin resmedilebilir 92 karakterli kartı tamamlandı. Teknik denetim 92 kartın tümünü geçirdi. Bu partinin 14 sözlü tarifi yazı kararını bekliyor. Üç önizleme sayfası ile 92 PNG ve 92 WebP dosyası parti arşivinde doğrulandı.

## Karakterli kartların güncel durumu

| Parti | Denetimden geçti | Görsel denetim bekliyor | Üretim bekliyor | Yazı kararı bekliyor |
|---|---:|---:|---:|---:|
| 4-6 Kök | 92 | 0 | 0 | 14 |
| 4-6 Tohum | 88 | 0 | 0 | 7 |
| 4-6 Filiz | 52 | 0 | 0 | 0 |
| 4-6 Fidan | 82 | 0 | 0 | 0 |
| 4-6 Ağaç | 82 | 0 | 0 | 0 |
| 4-6 Çınar | 78 | 0 | 0 | 1 |
| 4-6 Orman | 74 | 0 | 0 | 1 |
| 7-9 Tohum | 33 | 0 | 0 | 4 |
| 7-9 Kök | 1 | 0 | 0 | 0 |

Karakterli kartlardan 582 tanesi görsel ve teknik denetimden geçti. Ana teslimde daha önce tamamlanan 3.576 kartla birlikte 4.158 PNG ve WebP çifti bulunuyor.

582 uygun karakterli kartın tamamı geçti. Son denetimde tutmayan uygun kart sayısı sıfırdır. Üretim dışında kalan 89 tarifin 27’si karakterli kartta belirli sözler, 55’i yazılı kart, 7’si yazı veya rakam gerektiren nesne ve sahne tarifidir. Karakterli tariflerin satır bazında açıklaması uretim-durumu.csv dosyasındadır.

Görseller ImageGen ile resmi karakter çizimleri ve B stili referans alınarak üretildi. Araç bu oturumda ayrıca bir model sürüm numarası sunmadı. PNG ve WebP çıktıları Pillow ile işlendi. Ana teslimde 3.434 R ve 724 K kartı vardır. 15 keçe karakter modeli ayrıca teslim edilir.

Ders bağlamında “anneannesini arayan Pingucan” iletişim ünitesinde telefonla konuşurken gösterildi. “Denizde balık gibi yüzen Ela” kartında benzetme Ela’nın hareketiyle anlatıldı. Aynı testteki dev ve minicik Pingucan kartlarında boy farkı görünür kılındı.
