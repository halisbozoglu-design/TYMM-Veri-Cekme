from tymm_engine.utils import slugify

def test_slugify_turkish():
    assert slugify("Öğretim Programı") == "ogretim-programi"
