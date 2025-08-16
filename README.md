# Test Insider

Python + pytest API ve UI testleri.

## Gereksinimler
- Python 3.11+ (önerilen)
- macOS/Linux/Windows
- Google Chrome ve/veya Firefox (UI testleri için)

## Kurulum
```bash
# Sanal ortam
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Bağımlılıklar
pip install -r requirements.txt
```

## Testleri Çalıştırma
### API Testleri
```bash
python -m pytest -q tests/api -q
or
python -m pytest -q -m api
```

### UI Testleri
Tüm UI testleri:
```bash
python -m pytest -q tests/ui -q
or 
python -m pytest -q -m ui
```
Tek bir dosya/tek bir test:
```bash
python -m pytest -q tests/ui/test_qa_view_role_redirect_5.py -q
python -m pytest -q tests/ui/test_qa_view_role_redirect_5.py::test_view_role_opens_lever -q
```
Tarayıcı seçimi (chrome varsayılan):
```bash
python -m pytest -q tests/ui -q --browser chrome
python -m pytest -q tests/ui -q --browser firefox
```
Headless mod:
```bash
export HEADLESS=true  # Windows PowerShell: $env:HEADLESS='true'
python -m pytest -q tests/ui -q
```

### Raporlama (pytest-html)
- HTML rapor, pytest.ini içindeki addopts sayesinde otomatik üretilir.
- Çalıştırma sonrası proje kökünde `report.html` oluşur.
- Farklı isim/konum için `pytest.ini` dosyasındaki `--html=...` kısmını değiştirebilirsiniz.
- Manuel çalıştırma örneği:
```bash
python -m pytest -q --html=report.html --self-contained-html
```

## Performans Testleri (Locust)
- Senaryo konumu: `tests/performance_tests/n11_basic_search_performance.py`
- Amaç: n11 ana sayfayı açmak ve basit bir arama (`/arama?q=telefon`) sonucunu listelemek; yalnızca 200 döndüğünü ve içerikte temel işaretlerin bulunduğunu kontrol etmek.
- Tek kullanıcı yeterlidir (case gereği).

Çalıştırma (web arayüzü ile):
```bash
locust -f tests/performance_tests/n11_basic_search_performance.py --host https://www.n11.com
# Tarayıcıda http://localhost:8089 açılır; Users: 1, Spawn rate: 1 girip Start'a basın.
```
CLI üzerinden başlatmak (headless, CSV çıktı):
```bash
locust -f tests/performance_tests/n11_basic_search_performance.py --host https://www.n11.com -u 1 -r 1 --run-time 15s --headless --csv=performance_test_results/perf
```
CLI üzerinden başlatmak (headless, HTML rapor):
```bash
locust -f tests/performance_tests/n11_basic_search_performance.py --host https://www.n11.com -u 1 -r 1 --run-time 15s --headless --html performance_test_results/report.html
```
Notlar:
- CSV dosyaları `performance_test_results/` klasöründe `perf_*.csv` adıyla oluşur.
- HTML rapor `performance_test_results/report.html` olarak üretilir.
- Süreyi değiştirmek için `--run-time 10s`, `30s` veya `1m` gibi değerler verebilirsiniz.

## Ortam Değişkenleri
- `HEADLESS`: `true` ise tarayıcı headless açılır.
- `BROWSER`: `chrome` veya `firefox` (CLI `--browser` ile de verilebilir).


## Ekran Görüntüleri
Hatalı UI testlerinde ekran görüntüleri `tests/ui/screenshots/` klasörüne kaydedilir.

## Proje Yapısı (özet)
```
src/
  ui/pages/         # POM sayfa nesneleri (BasePage, HomePage, CareersPage, QAPage, OpenPositionsPage)
  api/              # API istemcileri/yardımcıları
tests/
  api/              # API testleri (GET/POST/PUT/DELETE)
  ui/               # UI testleri ve pytest fixture’ları
  performance_tests/ # Locust performans senaryosu
pytest.ini          # pytest ayarları (plugin, yollar)
requirements.txt    # bağımlılıklar
```

## Notlar
- Webdriver indirme/kurulum `webdriver-manager` tarafından otomatik yapılır.
- UI testleri başlarken tarayıcı maksimize edilir; headless modda pencere boyutu sürücüye bağlıdır.
