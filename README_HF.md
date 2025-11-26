---
title: FrameFlow
emoji: 🎬
colorFrom: purple
colorTo: blue
sdk: gradio
sdk_version: "6.0.0"
app_file: app.py
pinned: false
tags:
  - screenplay
  - storyboard
  - mcp
  - ai-agent
  - multimodal
  - creative-writing
  - film-production
license: mit
---

# 🎬 FrameFlow

**From idea to storyboard in minutes**

FrameFlow, hikaye fikirlerinizi profesyonel senaryo ve görsel storyboard'lara dönüştüren akıllı bir AI agent'tır. MCP 1st Birthday Hackathon için geliştirilmiştir.

## ✨ Özellikler

### 📝 Senaryo Oluşturma
- Endüstri standardı formatlama (INT/EXT, karakter cues, aksiyon satırları)
- Çoklu tür şablonları (Drama, Komedi, Gerilim, Bilim-Kurgu, Korku)
- Hikaye yapısı analizi (Three-Act, Five-Act, Hero's Journey)
- Otomatik karakter geliştirme
- 5 farklı diyalog stili

### 🎨 Storyboard Oluşturma
- Otomatik anahtar an tespiti
- Kamera açısı önerileri
- Karakter görsel tutarlılığı (embeddings)
- 5 farklı görsel stil (Realistic, Noir, Anime, Illustrated, Sketch)
- Profesyonel kompozisyon ve ışıklandırma

### 📦 Export Özellikleri
- PDF senaryo çıktısı
- Storyboard görüntü paketi (ZIP)
- Kombine lookbook dokümanı
- Prodüksiyon shot list

## 🚀 Kullanım

1. **Hikaye Fikrinizi Girin**: Kısa bir açıklama yazın
2. **Tercihleri Seçin**: Tür, diyalog stili, yapı
3. **Senaryo Oluşturun**: AI senaryonuzu yazacak
4. **Storyboard Oluşturun**: Görsel kareler oluşturun
5. **Export Edin**: PDF/ZIP formatında indirin

## 🏗️ Mimari

FrameFlow, Model Context Protocol (MCP) kullanan multi-agent mimariye sahiptir:

- **screenplay-generator**: Hikaye analizi, karakter oluşturma, sahne yazımı
- **storyboard-visualizer**: Görsel prompt oluşturma, kamera açıları
- **character-consistency**: Karakter tutarlılığı (embeddings)
- **document-exporter**: PDF/ZIP export

## 🎯 Teknoloji

- **Frontend**: Gradio 6
- **Backend**: Python 3.11, FastAPI
- **MCP Framework**: mcp-server-python
- **LLM**: SambaNova AI
- **Image Gen**: Hyperbolic.ai (SDXL/Flux)
- **Embeddings**: Nebius AI
- **Deployment**: Modal.com, HuggingFace Spaces

## 📝 Örnek Promptlar

**Drama**
```
İki işte çalışan bekar bir anne, liseli oğlunun evsizlere
gizlice garajlarında yardım ettiğini keşfeder.
```

**Gerilim**
```
Noir bir şehirdeki dedektif, avladığı seri katilin
aslında geleceği kendisi olduğunu keşfeder.
```

**Bilim-Kurgu**
```
2157'de bir zaman-yolculuğu tamircisi, geçmiş benliğinin
zaman yolculuğunu icat etmesini engellemek zorunda kalır.
```

## 🏆 MCP 1st Birthday Hackathon

**Track**: MCP in Action - Multimodal
**Tag**: `mcp-in-action-track-multimodal`

FrameFlow, MCP protokolünü kullanarak metin üretimi, görüntü sentezi ve doküman oluşturmayı tek bir akıcı workflow'da birleştirir.

## 📄 License

MIT License

## 🔗 Links

- [GitHub Repository](https://github.com/ahmetmertugrul/frameflow)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [Demo Video](#) (coming soon)

---

**Not**: API anahtarları gereklidir. Detaylar için [README](https://github.com/ahmetmertugrul/frameflow) dosyasına bakın.
