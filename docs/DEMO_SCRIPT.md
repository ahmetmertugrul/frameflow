# 🎬 FrameFlow Demo Video Script

**Duration**: 3-5 minutes
**Target**: MCP 1st Birthday Hackathon Judges

---

## Opening (0:00 - 0:30)

**Visual**: FrameFlow logo animation
**Narration**:
> "Merhaba! FrameFlow'a hoş geldiniz - hikaye fikirlerinizi dakikalar içinde profesyonel senaryo ve görsel storyboard'lara dönüştüren AI-powered agent.
>
> MCP 1st Birthday Hackathon için geliştirilmiş olan FrameFlow, Model Context Protocol kullanarak metin üretimi, görüntü sentezi ve doküman oluşturmayı tek bir akıcı workflow'da birleştirir."

---

## Problem Statement (0:30 - 1:00)

**Visual**: Split screen - confused writer vs. professional tools
**Narration**:
> "İçerik yaratıcıları, bağımsız film yapımcıları ve hikaye anlatıcıları pre-prodüksiyon aşamasında büyük zorluklarla karşılaşırlar:
>
> - Profesyonel senaryo yazımı format ve yapı uzmanlığı gerektirir
> - Storyboard oluşturma hem sanatsal beceri hem de görsel hikaye anlatımı bilgisi ister
> - Bu süreç genellikle günler, hatta haftalar alır
>
> FrameFlow bu engelleri ortadan kaldırır."

---

## Architecture Overview (1:00 - 1:30)

**Visual**: Architecture diagram animation
**Narration**:
> "FrameFlow, 4 özel MCP server kullanarak çalışır:
>
> 1. **screenplay-generator**: Hikaye analizi, karakter yaratma ve sahne yazımı
> 2. **storyboard-visualizer**: Görsel an tespiti ve prompt oluşturma
> 3. **character-consistency**: Karakter görsel tutarlılığı için embeddings
> 4. **document-exporter**: Profesyonel PDF ve ZIP export
>
> Tüm bunlar SambaNova, Hyperbolic ve Nebius AI ile güçlendirilmiş durumda."

---

## Live Demo - Screenplay (1:30 - 2:30)

**Visual**: Screen recording of Gradio interface
**Actions**:
1. Navigate to Screenplay tab
2. Enter story prompt:
   ```
   Noir bir şehirdeki dedektif, avladığı seri katilin
   aslında geleceği kendisi olduğunu keşfeder.
   ```
3. Select: Genre = Thriller, Style = Realistic, Structure = Three-Act
4. Click "Generate Screenplay"

**Narration**:
> "Bir hikaye fikri girelim. Bir gerilim hikayesi - dedektif, avladığı katilin kendi gelecek hali olduğunu keşfediyor.
>
> [Agent çalışırken]
> FrameFlow şimdi:
> - Hikaye yapısını analiz ediyor
> - Karakterleri oluşturuyor
> - Her sahneyi endüstri standardında yazıyor
>
> [Sonuç gösterme]
> Ve işte! Tam formatlı, 5 sahneli, karakter diyaloglarıyla eksiksiz bir senaryo."

---

## Live Demo - Storyboard (2:30 - 3:30)

**Visual**: Continue screen recording
**Actions**:
1. Navigate to Storyboard tab
2. Set: 8 frames, Noir style
3. Click "Generate Storyboard"
4. Show generated frames

**Narration**:
> "Şimdi bu senaryoyu görselleştirelim.
>
> [Agent çalışırken]
> Moment Detector en önemli sahneleri belirliyor
> Visual Prompt Generator her kare için detaylı prompt oluşturuyor
> Hyperbolic AI SDXL modeliyle görselleri üretiyor
>
> [Sonuçları gösterme]
> Ve voilà! 8 profesyonel storyboard karesi, Noir stilinde, kamera açılarıyla ve tam kompozisyonla.
>
> Karakter tutarlılığına dikkat edin - embeddings sayesinde karakterler tüm karelerde aynı görünüyor."

---

## Export Features (3:30 - 4:00)

**Visual**: Show export options and files
**Actions**:
1. Export screenplay as PDF
2. Export storyboard as ZIP
3. Show file downloads

**Narration**:
> "FrameFlow senaryonuzu PDF olarak, storyboard'unuzu ZIP paketi halinde, ya da her ikisini birleştirerek lookbook formatında export edebilir.
>
> Hepsi prodüksiyon-ready, hepsi dakikalar içinde."

---

## Technical Highlights (4:00 - 4:30)

**Visual**: Code snippets, architecture diagrams
**Narration**:
> "Teknik özellikler:
>
> - 4 tam fonksiyonel MCP server, 15 tool
> - 6,500+ satır production code
> - 110+ test case ile full coverage
> - GPU-accelerated görüntü üretimi
> - Modal ve HuggingFace Spaces ready
> - Async pipeline, fallback mekanizmaları
> - MIT License, tamamen açık kaynak"

---

## Closing (4:30 - 5:00)

**Visual**: FrameFlow in action montage
**Narration**:
> "FrameFlow, MCP'nin gücünü gösteriyor:
> - Multiple AI services tek bir coherent workflow'da
> - Text, images, documents - hepsi entegre
> - User-friendly interface, production-ready çıktılar
>
> Bir fikir girin, dakikalar içinde film için hazır materyaller alın.
>
> FrameFlow - From idea to storyboard in minutes. 🎬
>
> GitHub: github.com/ahmetmertugrul/frameflow
> Track: MCP in Action - Multimodal
>
> Teşekkürler!"

---

## Call to Action

**Visual**: Links and QR codes
**Text on screen**:
- 🌐 Try it: [HuggingFace Space URL]
- 💻 Code: github.com/ahmetmertugrul/frameflow
- 📺 MCP Hackathon: huggingface.co/MCP-1st-Birthday

---

## Recording Tips

1. **Clean Environment**: Hide desktop icons, close unnecessary apps
2. **Smooth Transitions**: Use screen recording with good frame rate
3. **Clear Audio**: Use quality microphone, no background noise
4. **Pacing**: Speak clearly and not too fast
5. **Show Real Features**: No mocked data, show actual generation
6. **Highlight MCP**: Emphasize MCP integration throughout
7. **Professional**: Good lighting if showing face, professional presentation

## Backup Slides (If Demo Fails)

Prepare slides with:
- Screenshots of successful runs
- Architecture diagrams
- Code samples showing MCP integration
- Test results and metrics
- Comparison before/after

## Video Export Settings

- **Resolution**: 1080p (1920x1080)
- **Frame Rate**: 30fps
- **Format**: MP4 (H.264)
- **Audio**: AAC, 128kbps
- **Length**: 3-5 minutes (strict)
