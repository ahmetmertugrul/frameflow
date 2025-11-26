# 🚀 Modal.com Deployment Rehberi - FrameFlow

## 💰 Krediler

Harika! Elindeki Modal.com $250 kredisi ile GPU-destekli, süper hızlı deployment yapacağız!

**Mevcut Krediler**:
- ✅ Modal.com: **$250** (GPU deployment için!)
- ✅ Blaxel.ai: $250
- ✅ Hyperbolic.ai: $25 (görsel üretimi için)
- ✅ Nebius.com: $50 (embeddings için)
- ✅ SambaNova.ai: $5 (LLM için)

---

## 🎯 Neden Modal.com?

| Özellik | HuggingFace Spaces | Modal.com |
|---------|-------------------|-----------|
| **Fiyat** | Ücretsiz | $250 kredin var! |
| **GPU** | ❌ Yok (CPU only) | ✅ T4, A10G, A100 |
| **Hız** | ~60 saniye | ~30 saniye (2x hızlı!) |
| **Cold Start** | Yok | ~5 saniye |
| **Scaling** | Sabit | Otomatik |
| **Deployment** | ~10 dk | ~2-3 dk |

→ **Modal.com ile 2x daha hızlı storyboard üretimi!** 🚀

---

## 📋 Deployment Adımları (10 Dakika)

### 1️⃣ Modal CLI Kurulumu (2 dakika)

```bash
# Modal CLI'yi yükle
pip install modal

# Versiyonu kontrol et
modal --version
```

Beklenen çıktı: `modal, version X.X.X`

---

### 2️⃣ Modal Token Al (1 dakika)

```bash
# Token authentication başlat
modal token new
```

Bu komut tarayıcıda Modal web sayfasını açacak:

1. Modal.com hesabınla giriş yap
2. "Authenticate" butonuna tıkla
3. Terminal'e dön - "✓ Initialized" göreceksin

**Not**: Eğer hesabın yoksa, önce https://modal.com adresinden GitHub ile giriş yap.

---

### 3️⃣ API Secrets Oluştur (2 dakika)

Tüm API keylerini tek bir secret'ta saklayacağız:

```bash
modal secret create frameflow-secrets \
  SAMBANOVA_API_KEY="your_sambanova_key_here" \
  HYPERBOLIC_API_KEY="your_hyperbolic_key_here" \
  NEBIUS_API_KEY="your_nebius_key_here" \
  NEBIUS_PROJECT_ID="your_nebius_project_id_here"
```

**Kendi keylerini koy!** Örnek:
```bash
modal secret create frameflow-secrets \
  SAMBANOVA_API_KEY="sk-sambanova-abc123..." \
  HYPERBOLIC_API_KEY="hf_abc123..." \
  NEBIUS_API_KEY="nb_abc123..." \
  NEBIUS_PROJECT_ID="project-123"
```

Secret başarıyla oluşturuldu mesajını göreceksin: ✅

**Nebius opsiyonel**: Eğer Nebius kullanmayacaksan:
```bash
modal secret create frameflow-secrets \
  SAMBANOVA_API_KEY="..." \
  HYPERBOLIC_API_KEY="..."
```

**Secrets'ı kontrol et**:
```bash
modal secret list
```

"frameflow-secrets" listede görünmeli.

---

### 4️⃣ Deploy Et! (3 dakika)

```bash
# Proje dizinine git
cd /home/user/frameflow

# Deploy komutu çalıştır
modal deploy modal_app.py
```

Deployment süreci:

```
⠙ Building image...
✓ Image built successfully
⠙ Deploying functions...
✓ Function deployed: generate_storyboard_frame
✓ Function deployed: gradio_app
✓ Deployment complete!

View your app at: https://your-username--frameflow-gradio-app.modal.run
```

**İlk deployment ~2-3 dakika sürer** (image build eder).
**Sonraki deploymentlar ~30 saniye** (cache kullanır).

---

### 5️⃣ Test Et! (1 dakika)

Deployment'tan aldığın URL'e git:
```
https://your-username--frameflow-gradio-app.modal.run
```

**Test Senaryosu**:
```
Story Prompt: "Bir astronot Mars'ta gizemli bir sinyal bulur"
Genre: Sci-Fi
Dialogue Style: Realistic
Act Structure: Three-Act
```

"🎬 Senaryo ve Storyboard Oluştur" butonuna tıkla!

**Beklenen Performans**:
- Senaryo oluşturma: ~10-15 saniye
- Storyboard (8 frame): ~15-25 saniye
- **Toplam: ~30 saniye** (HuggingFace'in yarısı!)

---

## 🔧 Sorun Giderme

### Problem: "modal: command not found"

**Çözüm**: Modal CLI'yi global yükle

```bash
pip install --user modal

# veya
python -m pip install modal
```

### Problem: "Secret 'frameflow-secrets' not found"

**Çözüm**: Secret'ı yeniden oluştur

```bash
# Var olan secret'ı sil
modal secret delete frameflow-secrets

# Yeniden oluştur
modal secret create frameflow-secrets \
  SAMBANOVA_API_KEY="..." \
  HYPERBOLIC_API_KEY="..."
```

### Problem: "No module named 'app'"

**Çözüm**: `app.py` dosyasının proje root'unda olduğundan emin ol

```bash
# Kontrol et
ls -la app.py

# Eğer yoksa, deployment dizinini kontrol et
pwd
# /home/user/frameflow olmalı
```

### Problem: Deployment başarılı ama app açılmıyor

**Çözüm**: Logs'u kontrol et

```bash
modal app logs frameflow
```

Hataları bu komutla görebilirsin.

### Problem: "Out of GPU quota"

**Çözüm**: GPU tipini değiştir veya limitini artır

`modal_app.py`'de:
```python
# T4 yerine A10G kullan (daha güçlü ama daha pahalı)
@app.function(gpu="A10G", ...)

# veya CPU-only yap (yavaş ama daha ucuz)
@app.function(cpu=2, ...)
```

---

## 💰 Maliyet Tahmini ($250 Kredi ile)

Modal.com fiyatlandırması:

**GPU Kullanımı** (T4):
- T4 GPU: ~$0.60/saat
- Her storyboard: ~30 saniye = ~$0.005
- $250 ile: **~50,000 storyboard!** 🎉

**CPU Kullanımı** (Gradio UI):
- CPU: ~$0.04/saat
- Keep-warm (1 instance): ~$0.04/saat × 24 = ~$1/gün
- $250 ile: **~250 gün 24/7 uptime!**

**Toplam**: Kredinle aylarca rahatça kullanabilirsin! 💰

---

## 📊 GPU Seçenekleri

`modal_app.py`'de GPU tipini değiştirebilirsin:

```python
# Mevcut (hızlı ve ekonomik):
@app.function(gpu="T4", ...)

# Daha hızlı (2x hız, 2x fiyat):
@app.function(gpu="A10G", ...)

# En hızlı (4x hız, 4x fiyat):
@app.function(gpu="A100", ...)

# CPU only (en ucuz):
@app.function(cpu=4, memory=8192, ...)
```

**Önerim**: T4 ile başla, performans yeterliyse devam et. 👍

---

## 🎛️ İleri Düzey Ayarlar

### Paralel Image Generation

Daha hızlı storyboard için:

```python
# modal_app.py'de
@app.function(gpu="T4", concurrency_limit=4)  # 4 paralel request
async def generate_storyboard_frame(...):
    ...
```

Bu şekilde 8 frame'i paralel üretebilir, **toplam süreyi 15 saniyeye** indirebilirsin!

### Auto-scaling

Kullanıcı sayısı arttıkça otomatik scale:

```python
@app.function(
    gpu="T4",
    concurrency_limit=10,  # Aynı anda 10 request
    container_idle_timeout=300,  # 5 dakika sonra sleep
)
```

### Custom Domain

Modal'da custom domain:

1. Modal Dashboard → Settings → Domains
2. "Add domain" tıkla
3. DNS kayıtlarını ekle
4. `frameflow.yourdomain.com` hazır!

---

## 📈 Monitoring

### Real-time Logs

```bash
# Canlı logs izle
modal app logs frameflow --follow

# Sadece hataları göster
modal app logs frameflow --level ERROR
```

### Usage Dashboard

Modal Dashboard'da:
- GPU kullanımı
- Maliyet tracking
- Request counts
- Error rates

→ https://modal.com/dashboard

---

## 🔄 Güncelleme (Update Deployment)

Kod değiştirdiğinde yeniden deploy:

```bash
# Değişiklikleri yap
# Örnek: app.py'de UI değişikliği

# Yeniden deploy et
modal deploy modal_app.py
```

Deployment süresi: ~30 saniye (cache sayesinde)

---

## 🚀 Production Checklist

Deploy öncesi kontrol et:

- [ ] Modal token alındı (`modal token new`)
- [ ] Secrets oluşturuldu (`modal secret list`)
- [ ] API keyleri doğru (SambaNova, Hyperbolic)
- [ ] `modal_app.py` güncel
- [ ] `app.py` test edildi yerel olarak
- [ ] GPU tipi seçildi (T4 önerilen)

Deploy sonrası:

- [ ] URL açılıyor
- [ ] Test senaryosu çalışıyor
- [ ] Senaryo üretiyor
- [ ] Storyboard görselleri üretiliyor
- [ ] PDF download çalışıyor
- [ ] Logs'ta hata yok (`modal app logs frameflow`)

---

## 🎯 Hızlı Başlangıç Özet

```bash
# 1. Modal CLI kur
pip install modal

# 2. Token al
modal token new

# 3. Secrets oluştur (kendi keylerini koy!)
modal secret create frameflow-secrets \
  SAMBANOVA_API_KEY="sk-..." \
  HYPERBOLIC_API_KEY="hf_..."

# 4. Deploy et
cd /home/user/frameflow
modal deploy modal_app.py

# 5. URL'i aç ve test et!
# https://your-username--frameflow-gradio-app.modal.run
```

**Tüm süreç: 10 dakika!** ⚡

---

## 📞 Yardım

Sorun yaşarsan:

1. **Logs kontrol et**: `modal app logs frameflow`
2. **Secrets kontrol et**: `modal secret list`
3. **Modal docs oku**: https://modal.com/docs
4. **GitHub Issues**: https://github.com/ahmetmertugrul/frameflow/issues

---

## 🎉 Başarı!

Deployment başarılı olunca:

✅ GPU-destekli FrameFlow live!
✅ 2x daha hızlı storyboard üretimi
✅ $250 kredi ile binlerce üretim
✅ Otomatik scaling
✅ Production-ready!

**URL'ini paylaş** ve demo yap! 🚀

---

**Son Güncelleme**: 2025-11-26
**Platform**: Modal.com
**GPU**: NVIDIA T4
**Durum**: Production Ready ✅

🎬 **İyi deploymentlar!** ✨
