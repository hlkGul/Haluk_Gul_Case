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
```

### UI Testleri
Tüm UI testleri:
```bash
python -m pytest -q tests/ui -q
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

# API raporu
python -m pytest -q tests/api --html=api_report.html --self-contained-html

# UI raporu
python -m pytest -q tests/ui --html=ui_report.html --self-contained-html



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
pytest.ini          # pytest ayarları (plugin, yollar)
requirements.txt    # bağımlılıklar
```

## Notlar
- Webdriver indirme/kurulum `webdriver-manager` tarafından otomatik yapılır.
- UI testleri başlarken tarayıcı maksimize edilir; headless modda pencere boyutu sürücüye bağlıdır.
