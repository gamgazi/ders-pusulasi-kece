# Ders Pusulası keçe kartları

Ders Pusulası için üretilen 4.158 keçe kartı bu depoda yer alır. R serisinde 3.434 müfredat kartı, K serisinde 724 ek sözcük kartı bulunur. Her kartın saydam arka planlı WebP ve PNG sürümü vardır.

## Oyun için kart seçimi

- Oyun için gereken grubu bulmak üzere [kısa kataloğu aç](https://raw.githubusercontent.com/gamgazi/ders-pusulasi-kece/main/katalog.json). Her grupta kart sayısı, birkaç örnek ad ve o grubun bağlantısı bulunur.
- İlk müfredat grubunda *uyuyan kedi*, *top* ve *öğretmen* gibi kartlar yer alır. [R00 kartları](https://raw.githubusercontent.com/gamgazi/ders-pusulasi-kece/main/katalog/R00.json) · [Uyuyan kedi görseli](https://raw.githubusercontent.com/gamgazi/ders-pusulasi-kece/main/kartlar/R00/R0001.webp)
- Bir sözcüğü tüm koleksiyonda aramak için [tam kart listesini aç](https://raw.githubusercontent.com/gamgazi/ders-pusulasi-kece/main/kartlar.json). Her kayıtta kart kimliği (`id`), Türkçe adı (`ad`) ve iki doğrudan görsel bağlantısı (`webp`, `png`) vardır.

Oyunda kullanacağın kartların WebP dosyalarını indirip oyun projesinin görsel klasörüne ekle. Depo daha sonra gizli yapıldığında da oyun bu yerel kopyaları kullanabilir.

## Okul karakterleri ve müfredat

582 karakterli kart ana kataloğa eklendi. Karakterli tariflerin durumunu kimlikleriyle [üretim listesinde](pusula/uretim-durumu.csv) bulabilirsin.

35 seviyedeki 616 ünite ve 5.040 dersin içerikleri [ders dosyalarında](pusula/ders-pusulasi) yer alır. [15 keçe karakterin karşılaştırması](pusula/karakter-onizleme.png) ve [denetim raporu](pusula/RAPOR.md) aynı klasördedir.
