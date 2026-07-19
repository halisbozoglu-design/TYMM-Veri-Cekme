# TYMM Data Engine

MEB'in **Öğretim Programları** sayfasındaki Türkiye Yüzyılı Maarif Modeli programlarını keşfeder; program bağlantılarını kataloglar, PDF dosyalarını indirir, metin ve öğrenme çıktısı adaylarını ayrıştırır, JSON dosyaları ve SQLite veritabanı üretir.

Kaynak: `https://mufredat.meb.gov.tr/Programlar.aspx`

## Telefonda kullanım

1. GitHub uygulamasında repoyu açın.
2. **Actions** sekmesine girin.
3. **TYMM Verilerini Güncelle** iş akışını seçin.
4. **Run workflow** düğmesine basın.
5. `full` seçeneği PDF + JSON + SQLite üretir. `catalog-only` yalnızca program listesini günceller.
6. İşlem bitince oluşan veriler repodaki `data/` klasörüne otomatik commit edilir. Ayrıca Actions çalışmasının altında ZIP artifact oluşur.

## Üretilen çıktılar

- `data/json/catalog.json`: Tüm programların kataloğu
- `data/json/programs/*.json`: Program bazında sayfalar, başlıklar ve öğrenme çıktısı adayları
- `data/json/run-summary.json`: Çalışma özeti ve hatalar
- `data/db/tymm.sqlite3`: Sorgulanabilir SQLite veritabanı
- `data/pdfs/*.pdf`: Kaynak program PDF'leri

## Veritabanı tabloları

- `programs`
- `pages`
- `learning_outcomes`

## Yerel kullanım

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
tymm --limit 3
```

## Tasarım ilkeleri

- Aynı dersin farklı yılları ayrı sürüm olarak saklanır.
- Kaynak URL ve SHA-256 özeti korunur.
- Bir programdaki hata tüm çalışmayı durdurmaz.
- İş akışı elle telefondan veya haftalık zamanlamayla çalışabilir.
- Ham kaynak metni korunur; AI tarafından üretilecek zenginleştirmeler daha sonra ayrı alanlarda tutulur.

## Sonraki geliştirme katmanları

Bu temel veri deposu; yıllık plan, ders planı, soru üretimi, rubrik, çalışma kâğıdı ve içerik üretim servislerinin ortak veri kaynağı olarak kullanılabilir.
