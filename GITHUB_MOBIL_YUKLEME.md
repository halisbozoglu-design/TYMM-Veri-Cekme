# GitHub'a Telefondan Doğru Yükleme

Bu ZIP'i telefonunda açtıktan sonra **tymm-data-engine klasörünün içindeki tüm dosya ve klasörleri** repo köküne yükle.

Repo ana sayfasında şu yapı görünmelidir:

```text
.github/
src/
tests/
data/
docs/
.gitignore
README.md
requirements.txt
pyproject.toml
```

Özellikle `.github/workflows/update-data.yml` dosyası bulunmalıdır. Bu dosya yoksa GitHub Actions çalışmaz.

Yükleme tamamlandıktan sonra:

1. GitHub reposunda **Actions** sekmesine gir.
2. **TYMM Verilerini Güncelle** iş akışını seç.
3. **Run workflow** düğmesine bas.
4. İlk denemede `catalog-only` ve `3` kullan.
