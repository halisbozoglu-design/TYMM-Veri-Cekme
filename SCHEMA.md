# Veri Şeması

## Program kaydı

Her program için kaynak kimliği, başlık, kategori, yıl, sınıf aralığı, program URL'si, PDF URL'si, yerel PDF yolu, SHA-256 ve işlem durumu tutulur.

## Program JSON'u

```json
{
  "program": {},
  "content": {
    "page_count": 0,
    "headings": [],
    "learning_outcome_candidates": [],
    "pages": []
  }
}
```

`learning_outcome_candidates` otomatik yakalanan adaylardır; nihai pedagojik doğrulama katmanı daha sonra eklenmelidir.
