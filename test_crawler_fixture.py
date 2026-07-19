from unittest.mock import Mock, patch
from tymm_engine.crawler import discover_programs

HTML = '''
<html><body>
<h4>TYMM Temel Eğitim</h4>
<ul>
<li><a href="ProgramDetay.aspx?PID=10">[TYMM] FEN BİLİMLERİ DERSİ (3-8) (2024)</a></li>
<li><a href="ProgramDetay.aspx?PID=11">[TYMM] MATEMATİK DERSİ (5-8) (2026)</a></li>
</ul>
<h4>Eski Programlar</h4>
<a href="old.pdf">MATEMATİK (2018)</a>
</body></html>
'''

def test_discovery_from_fixture():
    response = Mock()
    response.text = HTML
    response.apparent_encoding = "utf-8"
    response.raise_for_status.return_value = None
    with patch("tymm_engine.crawler.requests.get", return_value=response):
        records = discover_programs()
    assert len(records) == 2
    assert records[0].year == 2024
    assert records[0].grade_text == "3-8"
    assert records[0].is_tymm is True
