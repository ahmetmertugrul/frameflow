# 🚀 FrameFlow - Hızlı Başlangıç Rehberi

## 5 Dakikada Çalıştır! ⚡

### 1️⃣ API Keylerini Hazırla (2 dakika)

Aşağıdaki servislere kaydol ve API keylerini al:

```bash
# Gerekli (Must-have):
✅ SambaNova Cloud  → https://cloud.sambanova.ai/
✅ Hyperbolic AI    → https://hyperbolic.xyz/

# Opsiyonel (Karakter tutarlılığı için):
⭕ Nebius AI        → https://nebius.com/
```

### 2️⃣ Environment Dosyasını Oluştur (30 saniye)

```bash
# .env.example'ı kopyala
cp .env.example .env

# .env dosyasını düzenle
nano .env  # veya vim, code, vb.
```

**Minimum gerekli konfigürasyon**:
```env
SAMBANOVA_API_KEY=your_sambanova_key_here
HYPERBOLIC_API_KEY=your_hyperbolic_key_here

# Opsiyonel (karakter consistency için):
# NEBIUS_API_KEY=your_nebius_key_here
# NEBIUS_PROJECT_ID=your_project_id_here
```

### 3️⃣ Bağımlılıkları Yükle (1 dakika)

```bash
# Python 3.11+ olduğundan emin ol
python --version

# Virtual environment oluştur (tavsiye edilir)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows

# Bağımlılıkları yükle
pip install -r requirements.txt
```

### 4️⃣ Uygulamayı Başlat (10 saniye)

```bash
python app.py
```

Tarayıcında otomatik olarak açılır: **http://localhost:7860**

---

## 🎬 İlk Senaryonu Oluştur (1 dakika)

### Adım 1: Hikaye Fikrini Gir
```
Örnek: "Bir dedektif, katili kendi gelecekteki benliği olduğunu keşfeder"
```

### Adım 2: Ayarları Seç
- **Tür**: Thriller, Drama, Action, vb.
- **Diyalog Stili**: Realistic, Stylized, Minimal
- **Yapı**: Three-Act, Five-Act, Hero's Journey

### Adım 3: Oluştur! 🚀
"🎬 Senaryo ve Storyboard Oluştur" butonuna tıkla

### Sonuç (30-60 saniye sonra):
- ✅ Profesyonel formatta senaryo
- ✅ 8 storyboard frame (görsel)
- ✅ İndirilebilir PDF'ler

---

## 📖 Örnek Kullanım

### Örnek 1: Sci-Fi Thriller
```
Prompt: "Bir yapay zeka, insanlığı kurtarmak için yaratıcısını öldürmek zorunda kalır"
Genre: Sci-Fi
Dialogue Style: Stylized
Act Structure: Three-Act

Beklenen Çıktı: ~5 sahne, 3 karakter, 8 storyboard frame
Süre: ~45 saniye
```

### Örnek 2: Romantik Drama
```
Prompt: "İki yıldız gözlemcisi, farklı zaman dilimlerinden birbirlerine mesaj bırakır"
Genre: Romance
Dialogue Style: Realistic
Act Structure: Five-Act

Beklenen Çıktı: ~7 sahne, 2 karakter, 8 storyboard frame
Süre: ~60 saniye
```

### Örnek 3: Aksiyon/Macera
```
Prompt: "Bir arkeolog, antik bir lanet yüzünden 24 saatte dünyayı kurtarmalı"
Genre: Action
Dialogue Style: Minimal
Act Structure: Hero's Journey

Beklenen Çıktı: ~12 sahne, 4 karakter, 8 storyboard frame
Süre: ~75 saniye
```

---

## 🧪 Testleri Çalıştır

```bash
# Tüm testleri çalıştır
pytest tests/ -v

# Coverage raporu ile
pytest tests/ -v --cov=core --cov=integrations --cov-report=html

# Sadece belirli bir test
pytest tests/test_schemas.py -v

# Async testler için
pytest tests/test_agent.py -v -s
```

**Beklenen Sonuç**: ✅ 110+ test passed

---

## 🐛 Sorun Giderme

### Problem: "API key bulunamadı" hatası
**Çözüm**: `.env` dosyasının proje root'unda olduğundan emin ol

```bash
# .env dosyasını kontrol et
cat .env

# Doğru konumda mı?
ls -la | grep .env
```

### Problem: "Module not found" hatası
**Çözüm**: Bağımlılıkları yeniden yükle

```bash
pip install --upgrade -r requirements.txt
```

### Problem: "Port 7860 already in use"
**Çözüm**: Başka bir port kullan

```bash
python app.py --server-port 7861
```

veya çalışan uygulamayı kapat:
```bash
# Linux/Mac
lsof -ti:7860 | xargs kill -9

# Windows
netstat -ano | findstr :7860
taskkill /PID <PID> /F
```

### Problem: Görsel üretilmiyor
**Çözüm**: Hyperbolic API key'ini kontrol et

```bash
# Test et
curl -H "Authorization: Bearer $HYPERBOLIC_API_KEY" \
  https://api.hyperbolic.xyz/v1/models
```

### Problem: Karakter tutarlılığı çalışmıyor
**Çözüm**: Bu normal! Nebius keyi opsiyonel.

```bash
# Nebius olmadan da çalışır
# Sadece karakter consistency disabled olur
# Log'da şu mesajı göreceksin:
# "Character consistency tracking not available (Nebius not configured)"
```

---

## 🚀 Deployment Seçenekleri

### Option 1: HuggingFace Spaces (Ücretsiz!)

1. HF hesabı oluştur: https://huggingface.co/join
2. Yeni Space oluştur: "New" → "Space"
3. Space Settings:
   - **SDK**: Docker
   - **Visibility**: Public veya Private
4. Repository'yi bağla:
   ```bash
   git remote add hf https://huggingface.co/spaces/USERNAME/frameflow
   git push hf claude/start-frameflow-project-01U4FinfxJYU2wCM8sTGaVAT:main
   ```
5. Space Settings → Variables → Add secrets:
   - `SAMBANOVA_API_KEY`
   - `HYPERBOLIC_API_KEY`
   - `NEBIUS_API_KEY` (opsiyonel)

**Deployment Süresi**: ~5-10 dakika
**URL**: `https://huggingface.co/spaces/USERNAME/frameflow`

### Option 2: Modal.com (GPU Destekli!)

1. Modal hesabı oluştur: https://modal.com
2. CLI kurulumu:
   ```bash
   pip install modal
   modal token new
   ```
3. Secrets ekle:
   ```bash
   modal secret create frameflow-secrets \
     SAMBANOVA_API_KEY=xxx \
     HYPERBOLIC_API_KEY=xxx \
     NEBIUS_API_KEY=xxx
   ```
4. Deploy:
   ```bash
   modal deploy modal_app.py
   ```

**Deployment Süresi**: ~2-3 dakika
**URL**: Modal tarafından otomatik oluşturulur

### Option 3: Docker (Kendi Sunucunda)

```bash
# Build
docker build -t frameflow:latest .

# Run
docker run -p 7860:7860 \
  -e SAMBANOVA_API_KEY=$SAMBANOVA_API_KEY \
  -e HYPERBOLIC_API_KEY=$HYPERBOLIC_API_KEY \
  frameflow:latest
```

---

## 📊 Performans Beklentileri

### Yerel Çalıştırma:
- **Senaryo Üretimi**: 15-25 saniye
- **Storyboard (8 frame)**: 30-45 saniye
- **Toplam Süre**: ~60 saniye
- **RAM Kullanımı**: ~500MB
- **GPU**: Gerekmiyor (API'lar remote)

### Modal.com (GPU):
- **Senaryo Üretimi**: 10-15 saniye
- **Storyboard (8 frame)**: 15-25 saniye (paralel üretim)
- **Toplam Süre**: ~30 saniye
- **GPU**: T4 (16GB VRAM)

### HuggingFace Spaces (CPU):
- **Senaryo Üretimi**: 15-25 saniye
- **Storyboard (8 frame)**: 35-50 saniye
- **Toplam Süre**: ~70 saniye
- **RAM**: 16GB limit

---

## 🎯 İleri Düzey Kullanım

### Custom Prompts

`core/prompts.py` dosyasını düzenleyerek kendi prompt'larını ekle:

```python
CUSTOM_GENRE_PROMPT = """
You are an expert in {genre} storytelling.
Create a compelling narrative that...
"""
```

### Visual Style Ekleme

`mcp_servers/storyboard_visualizer/prompt_generator.py`:

```python
def _load_style_modifiers(self):
    return {
        "Realistic": {...},
        "MyCustomStyle": {
            "prefix": "My custom visual prefix",
            "suffix": "with specific details",
            "lighting": "custom lighting",
            "color_palette": "vibrant colors"
        }
    }
```

### Karakter Limitlerini Değiştirme

`core/agent.py`:

```python
async def generate_screenplay_and_storyboard(...):
    # Karakter sayısını artır
    characters = await self.character_creator.create_characters(
        story_analysis,
        genre,
        num_characters=5  # Default: 3
    )

    # Frame sayısını artır
    key_moments = self.moment_detector.identify_key_moments(
        full_screenplay,
        num_frames=12  # Default: 8
    )
```

---

## 📞 Yardım & Destek

### Dokümantasyon
- 📄 **README.md** - Genel bakış ve kurulum
- 📄 **PROJECT_SUMMARY.md** - Detaylı proje özeti
- 📄 **DEMO_SCRIPT.md** - Demo video scripti
- 📄 **FrameFlow_Project_Plan.md** - Orijinal plan

### Örnek Dosyalar
- 📁 **examples/sample_screenplay.txt** - Örnek senaryo çıktısı
- 📁 **tests/** - Test örnekleri ve kullanım patterns

### Sorun Bildirimi
- 🐛 GitHub Issues: https://github.com/ahmetmertugrul/frameflow/issues

---

## ✅ Kontrol Listesi

Başlamadan önce kontrol et:

- [ ] Python 3.11+ kurulu
- [ ] SambaNova API key alındı
- [ ] Hyperbolic API key alındı
- [ ] `.env` dosyası oluşturuldu
- [ ] `requirements.txt` yüklendi
- [ ] Port 7860 boş

Hazırsan: `python app.py` 🚀

---

## 🎉 Başarılı Kurulum!

Eğer bu adımları tamamladıysan, artık FrameFlow'u kullanmaya hazırsın!

**İlk senaryonu oluştur** ve yapay zeka destekli hikaye anlatımının gücünü keşfet! 🎬✨

---

**Son Güncelleme**: 2025-11-26
**Versiyon**: 1.0.0
**Durum**: Production Ready ✅
