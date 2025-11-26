# 🚀 FrameFlow Deployment Guide

## ⚠️ Netlify Neden Çalışmıyor?

**Netlify** sadece statik dosyaları host eder (HTML, CSS, JS). FrameFlow ise:
- Python backend gerektirir (Gradio server)
- API çağrıları yapar (SambaNova, Hyperbolic, Nebius)
- Real-time WebSocket bağlantıları kullanır

→ **Çözüm**: Aşağıdaki platformlardan birini kullan:

---

## ✅ 1. HuggingFace Spaces (ÖNERİLEN - Ücretsiz!)

### Neden HuggingFace Spaces?
- ✅ **Tamamen ücretsiz**
- ✅ Dockerfile desteği (bizde hazır!)
- ✅ Python/Gradio için optimize edilmiş
- ✅ Otomatik HTTPS
- ✅ Kolay secrets yönetimi
- ✅ 16GB RAM, 8 vCPU (ücretsiz tier)

### Adım 1: HuggingFace Hesabı Oluştur

1. https://huggingface.co/join adresine git
2. Ücretsiz hesap oluştur
3. Email doğrulamasını tamamla

### Adım 2: Space Oluştur

1. https://huggingface.co/new-space adresine git
2. Space ayarlarını yap:
   ```
   Owner: [senin-kullanıcı-adın]
   Space name: frameflow
   License: MIT
   SDK: Docker
   ```
3. "Create Space" butonuna tıkla

### Adım 3: README_HF.md'yi README.md Yap

Space'in anasayfasında gözükecek README:

```bash
# Mevcut README'yi yedekle
mv README.md README_GITHUB.md

# HuggingFace README'sini kullan
cp README_HF.md README.md
```

### Adım 4: Repository'yi HuggingFace'e Push Et

#### Option A: Git ile (Önerilen)

```bash
# HuggingFace token al
# https://huggingface.co/settings/tokens
# "New token" → "Write" yetkisi ile

# HuggingFace remote ekle
git remote add hf https://huggingface.co/spaces/[KULLANICI-ADIN]/frameflow

# Push et
git push hf claude/start-frameflow-project-01U4FinfxJYU2wCM8sTGaVAT:main
```

Push ederken şifre isterse:
- **Username**: HuggingFace kullanıcı adın
- **Password**: Token (yukarıda aldığın)

#### Option B: Web UI ile (Kolay)

1. Space'in "Files" sekmesine git
2. Tüm dosyaları sürükle-bırak ile yükle:
   - `app.py`
   - `Dockerfile`
   - `requirements.txt`
   - `core/` klasörü
   - `integrations/` klasörü
   - `mcp_servers/` klasörü
   - `templates/` klasörü
   - `README.md` (README_HF.md'yi yeniden adlandır)
   - `.env.example` (opsiyonel)

### Adım 5: Secrets Ekle

1. Space Settings → "Variables and secrets" bölümüne git
2. "New secret" butonuna tıkla
3. Şu secret'ları ekle:

```
Name: SAMBANOVA_API_KEY
Value: [senin-sambanova-key'in]

Name: HYPERBOLIC_API_KEY
Value: [senin-hyperbolic-key'in]

Name: NEBIUS_API_KEY (opsiyonel)
Value: [senin-nebius-key'in]

Name: NEBIUS_PROJECT_ID (opsiyonel)
Value: [senin-nebius-project-id'n]
```

### Adım 6: Build ve Deploy

1. Dosyaları push ettikten sonra otomatik build başlayacak
2. "Logs" sekmesinden build ilerlemesini takip et
3. Build süresi: ~5-10 dakika (ilk seferde)
4. Build başarılı olunca "App" sekmesi aktif olacak

### Adım 7: Test Et!

Space URL'i: `https://huggingface.co/spaces/[KULLANICI-ADIN]/frameflow`

Test senaryosu:
```
Prompt: "Bir dedektif, katili kendi gelecekteki benliği olduğunu keşfeder"
Genre: Thriller
Dialogue Style: Realistic
Act Structure: Three-Act
```

---

## 🎯 2. Modal.com (GPU Destekli - Hızlı!)

### Neden Modal.com?
- ✅ **GPU desteği** (T4, A10G, A100)
- ✅ Serverless (sadece kullanıldığında ödeme)
- ✅ Çok hızlı deployment (2-3 dakika)
- ✅ Otomatik scaling
- ⚠️ Ücretli (ama $30 free credit)

### Adım 1: Modal Hesabı

1. https://modal.com adresine git
2. GitHub ile giriş yap
3. $30 free credit al

### Adım 2: Modal CLI Kurulum

```bash
# Modal'ı yükle
pip install modal

# Token al
modal token new
```

Tarayıcıda açılan sayfadan authentication'ı tamamla.

### Adım 3: Secrets Oluştur

```bash
modal secret create frameflow-secrets \
  SAMBANOVA_API_KEY=your_key_here \
  HYPERBOLIC_API_KEY=your_key_here \
  NEBIUS_API_KEY=your_key_here \
  NEBIUS_PROJECT_ID=your_project_id_here
```

### Adım 4: Deploy

```bash
# Proje klasörüne git
cd /home/user/frameflow

# Deploy et!
modal deploy modal_app.py
```

Deployment başarılı olunca URL verecek:
```
✓ Created web function generate_storyboard_frame
✓ App deployed! View at: https://your-username--frameflow-gradio-app.modal.run
```

### Adım 5: Test Et

Modal URL'ine git ve aynı test senaryosunu dene.

**Performans Karşılaştırması**:
- HuggingFace Spaces (CPU): ~60 saniye
- Modal.com (GPU T4): ~30 saniye

---

## 🐳 3. Heroku / Railway / Render (Alternatifler)

### Render.com (Önerilen Alternatif)

**Avantajlar**:
- ✅ Ücretsiz tier (750 saat/ay)
- ✅ Dockerfile desteği
- ✅ Otomatik SSL
- ✅ Kolay secrets

**Adımlar**:

1. https://render.com adresine git ve hesap oluştur
2. "New" → "Web Service" seçeneğini tıkla
3. GitHub repo'nu bağla
4. Ayarlar:
   ```
   Name: frameflow
   Environment: Docker
   Plan: Free
   ```
5. Environment Variables ekle:
   - `SAMBANOVA_API_KEY`
   - `HYPERBOLIC_API_KEY`
   - `NEBIUS_API_KEY` (opsiyonel)
6. "Create Web Service" tıkla
7. ~10 dakika bekle

URL: `https://frameflow.onrender.com`

⚠️ **Render Free Tier Limitleri**:
- 750 saat/ay kullanım
- 15 dakika inaktivite sonrası uyku modu
- İlk istek 30-60 saniye bekletebilir (cold start)

---

## 📊 Platform Karşılaştırması

| Platform | Fiyat | GPU | Build Süresi | Performans | Cold Start |
|----------|-------|-----|--------------|------------|------------|
| **HuggingFace Spaces** | ✅ Ücretsiz | ❌ | ~10 dk | İyi (CPU) | Yok |
| **Modal.com** | 💰 $30 free | ✅ T4 | ~3 dk | Mükemmel | ~5 sn |
| **Render.com** | ✅ Free tier | ❌ | ~10 dk | İyi (CPU) | ~30-60 sn |
| **Railway.app** | 💰 $5/ay | ❌ | ~7 dk | İyi | ~10 sn |
| **Netlify** | ❌ Desteklemiyor | ❌ | - | - | - |
| **Vercel** | ❌ Desteklemiyor | ❌ | - | - | - |

---

## 🔧 Sorun Giderme

### Problem: "Application failed to start"

**Çözüm**: Logs'u kontrol et

```bash
# HuggingFace Spaces
# Space → Logs sekmesine git

# Modal.com
modal app logs frameflow

# Render.com
# Dashboard → Logs bölümüne git
```

### Problem: "Out of memory"

**Çözüm 1**: HuggingFace Spaces'te upgrade et (ücretli)

**Çözüm 2**: Modal.com kullan (daha fazla RAM)

**Çözüm 3**: `requirements.txt`'den gereksiz paketleri kaldır

### Problem: "Port already in use"

**Dockerfile'da port'u kontrol et**:

```dockerfile
# Dockerfile
EXPOSE 7860

# app.py'de
demo.launch(server_port=7860, server_name="0.0.0.0")
```

### Problem: Secrets çalışmıyor

**HuggingFace Spaces**:
1. Space Settings → Restart Space
2. Secrets'ın doğru yazıldığından emin ol (büyük/küçük harf)

**Modal.com**:
```bash
# Secrets'ı yeniden oluştur
modal secret delete frameflow-secrets
modal secret create frameflow-secrets SAMBANOVA_API_KEY=...
```

### Problem: Görseller üretilmiyor

**Hyperbolic API key'ini test et**:

```bash
curl -X POST "https://api.hyperbolic.xyz/v1/image/generation" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $HYPERBOLIC_API_KEY" \
  -d '{
    "model_name": "SDXL1.0-base",
    "prompt": "test image",
    "steps": 30
  }'
```

Hata alırsan:
- Key'in doğru olduğundan emin ol
- Hyperbolic account'unda credit olduğunu kontrol et

---

## ✅ Önerilen Deployment Akışı

**Başlangıç için**:
1. ✅ **HuggingFace Spaces** ile başla (ücretsiz)
2. Test et ve demo göster
3. Feedback topla

**Eğer performans önemliyse**:
1. ✅ **Modal.com** ile upgrade et
2. GPU ile 2x hızlı performans
3. Kullanım başına ödeme (cost-effective)

**Eğer sürekli uptime istiyorsan**:
1. ✅ **Render.com** veya **Railway** kullan
2. Custom domain bağla
3. Monitoring ve logging ekle

---

## 📝 Deployment Checklist

Deployment öncesi kontrol et:

- [ ] Platform seçildi (HuggingFace/Modal/Render)
- [ ] Hesap oluşturuldu
- [ ] API keyleri hazır
- [ ] Secrets eklendi
- [ ] Dockerfile test edildi (yerel Docker ile)
- [ ] `requirements.txt` güncel
- [ ] README.md hazır (HuggingFace için README_HF.md)
- [ ] .gitignore doğru yapılandırılmış

Deployment sonrası:

- [ ] Build logları kontrol edildi
- [ ] URL açılıyor
- [ ] Test senaryosu çalıştırıldı
- [ ] Senaryo üretimi çalışıyor
- [ ] Storyboard görselleri üretiliyor
- [ ] PDF export çalışıyor

---

## 🎯 HuggingFace Spaces - Hızlı Başlangıç (5 Dakika)

```bash
# 1. Token al
# https://huggingface.co/settings/tokens → "New token" (Write)

# 2. README'yi hazırla
mv README.md README_GITHUB.md
cp README_HF.md README.md

# 3. HuggingFace'e push et
git remote add hf https://huggingface.co/spaces/[KULLANICI-ADIN]/frameflow
git push hf claude/start-frameflow-project-01U4FinfxJYU2wCM8sTGaVAT:main

# Username: [HuggingFace kullanıcı adın]
# Password: [Token]

# 4. Secrets ekle (Web UI'dan)
# https://huggingface.co/spaces/[KULLANICI-ADIN]/frameflow/settings
# → Variables and secrets
# → SAMBANOVA_API_KEY, HYPERBOLIC_API_KEY

# 5. Build bekle (~10 dakika)
# Logs sekmesinden takip et

# 6. Hazır!
# https://huggingface.co/spaces/[KULLANICI-ADIN]/frameflow
```

---

## 📞 Yardım

Deployment sırasında sorun yaşarsan:

1. **Logs'u kontrol et** (en önemli adım!)
2. **DEPLOYMENT_GUIDE.md**'yi tekrar oku
3. **GitHub Issues** oluştur: https://github.com/ahmetmertugrul/frameflow/issues

---

**Son Güncelleme**: 2025-11-26
**Platform**: HuggingFace Spaces (önerilen)
**Durum**: Production Ready ✅

🚀 **İyi deploymentlar!**
