# 🐯 Macan Peramal
### *The Mystical Oracle of the Nusantara*

> A richly detailed desktop application blending **Javanese primbon wisdom**, **Pythagorean numerology**, and **Nusantara spiritual traditions** into a beautifully crafted, bilingual mystical experience.

---

## ✨ Overview

**Macan Peramal** (lit. *"The Prophetic Tiger"*) is a standalone Python desktop application built with **PySide6**. It brings together centuries of Javanese and broader Indonesian archipelago spiritual knowledge — weton calendars, dream interpretation, ancestral aura readings, and numerological profiling — into a modern, elegant dark-themed UI.

Whether you are curious about your birth weton, seeking interpretation of a vivid dream, or looking for the most auspicious date to begin a new venture, Macan Peramal serves as your personal digital primbon.



---

## 🖥️ Screenshots

> *Application runs in a frameless, translucent dark-purple window with ambient particle effects and a gold-accented sidebar.*
<img width="1148" height="767" alt="Screenshot 2026-06-15 135950" src="https://github.com/user-attachments/assets/d2f4ac91-ff28-478f-afef-c07478d80af5" />



---

## 🌟 Features

### 🔮 Dashboard — Cosmic Orb Oracle
- Animated glowing orb that generates dynamic daily cosmic messages
- Daily weton display with Neptu score, element, and day rating (⭐ to ⭐⭐⭐⭐⭐)
- Real-time energy bars for Aura, Prosperity, and Love resonance
- Special auto-message for **Friday Kliwon** — the most sacred night in the Javanese calendar

### 📜 Name & Destiny Analysis
- Full **Pythagorean Numerology** profile: Life Path, Destiny, Soul Urge, and Personality numbers
- Per-number archetype descriptions (1–9, plus Master Numbers 11, 22, 33)
- Lucky colors, lucky gemstones, best days of the week, and soul challenges for each number
- Integrated **Javanese Weton** birth reading with Neptu calculation
- Weton-specific career recommendations and element traits

### 📅 Birth Date Analysis (Weton Calculator)
- Calculates the precise Javanese **Weton** (day × pasaran combination) from any birthdate
- Displays Neptu score, spiritual element, character traits, and career alignment
- Includes **Chinese Zodiac (Shio)** derived from birth year
- Shows weton-specific **taboos (pantangan)** and **ritual/spiritual practice advice** per element
- Covers all 35 weton combinations

### 💞 Compatibility Calculator
- Compare two individuals across **Asmara (Romance)**, **Bisnis (Business)**, and **Persahabatan (Friendship)**
- Calculates compatibility score (%) based on weton Neptu harmony
- Displays Primbon category (e.g., *Pegat, Ratu, Jodoh, Topo, Tinari, Padu, Sujanan, Pesthi*)
- Bilingual relationship dynamic descriptions

### 🔢 Numerology Center
- Standalone numerology calculator for any name
- Produces a full **4-number Pythagorean profile** with rich archetypes
- Lucky number combination display

### 🌙 Dream Interpreter
- Searchable archive of **22+ dream categories** spanning:
  - Spiritual, Wealth (Rezeki), Warning (Peringatan), Luck, Love & Romance, Career & Knowledge, Ancestors & Death
- Keyword-based search and filtering
- Detailed interpretation panel with category icons, keyword tags, and spiritual advice per dream

### 📖 Primbon Encyclopedia
- Scrollable knowledge base of **30+ traditional Nusantara entries** organized into categories:
  - Natural Signs (Tanda Alam), Cosmic Seasons (Pranata Mangsa), Body Sensations (Firasat Tubuh)
  - Spiritual Aura, Special Weton, Traditional Taboos (Pantangan Adat)
  - Archipelago Rituals, Shio & Zodiac, Javanese Mysticism (Kejawen)
- Colored category badges, category icons, live search with entry count
- Full bilingual descriptions per entry

### 🗓️ Spiritual Calendar
- Monthly view of the entire **Javanese Pasaran calendar**
- Color-coded highlights:
  - 🔴 **Friday Kliwon** — most sacred date
  - 🟣 **Tuesday Kliwon** — warrior weton
  - 🟢 **High Neptu days** (≥ 14) — auspicious for major activities
  - 🟩 **Today** — always highlighted in green
- Neptu score displayed inside each date cell
- Color legend at the bottom of every month view

### 📆 Daily Fortune & Lucky Day Finder
- **Dynamic daily oracle** powered by today's real weton data — no two days are the same
- Element-specific prosperity, career, social, and health advice
- **Lucky Day Finder** searches up to 60 days ahead for auspicious dates
- Per-activity rules for Business Start, Travel, and Marriage Ceremony
- Sacred weton combinations flagged with a ✦ SAKRAL badge

### 🃏 Tarot Reading
- Daily Tarot
- Pick a Card

### ⚙️ Settings
- Full **bilingual support**: Bahasa Indonesia / English (switchable at runtime)
- Spiritual cache purge / history reset option

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.8+ |
| GUI Framework | PySide6 |
| Rendering | Qt HTML/CSS via `QTextBrowser` |
| Calendar Engine | Python `datetime` standard library |
| Numerology Engine | Custom `DestinyEngine` class (Pythagorean system) |
| Weton Engine | Algorithmically computed from epoch date offsets |
| Localization | Custom `LanguageManager` with runtime switching |
| Styling | Full custom Qt stylesheet (dark mystical theme) |

---

## ⚙️ Requirements

```
Python >= 3.8
PySide6 >= 6.9.0
```

Install dependencies:

```bash
pip install PySide6
```

---

## 🚀 Getting Started

1. **Clone or download** this repository.
2. Ensure Python 3.8+ and PySide6 are installed.
3. Run the application:

```bash
python macan_peramal_desktop_app.py
```

The application launches in a frameless window. Drag the title bar to move it. Use the sidebar to navigate between modules.

---

## 📁 Project Structure

```
macan_peramal_desktop_app.py   # Single-file application (self-contained)
README.md                      # This file
```

> All data, logic, UI, and assets are contained within a single Python file for maximum portability.

---

## 🌐 Bilingual Support

All features support both **Bahasa Indonesia** and **English** at runtime. Switch languages at any time via **Settings → Language Select** without restarting the application. All generated HTML reports, oracle messages, encyclopedia entries, dream interpretations, weton descriptions, and numerology profiles adapt instantly.

---

## 📚 Knowledge Sources

Macan Peramal draws from the following traditional knowledge systems:

- **Kitab Primbon Jawa** — Classical Javanese divination manuscripts
- **Pranata Mangsa** — Traditional Javanese agrarian and cosmic seasonal calendar
- **Kejawen** — Javanese mystical philosophy (Sedulur Papat, Memayu Hayuning Bawana, Sangkan Paraning Dumadi)
- **Pythagorean Numerology** — Western numerological system applied to Indonesian naming conventions
- **Shio / Chinese Zodiac** — 12-year animal cycle as integrated into Nusantara cultural practice
- **Weton / Neptu System** — 5-day Javanese Pasaran cycle combined with the 7-day week

> *All interpretations are presented for cultural appreciation and personal reflection. They do not constitute professional advice of any kind.*

---

## 🎨 Design Philosophy

Macan Peramal is designed around the concept of **"digital kejawen"** — making centuries-old Nusantara wisdom accessible and beautifully presented to modern users without losing its depth or cultural integrity.

The UI draws visual inspiration from:
- The deep indigo and violet hues of the Javanese night sky
- Gold accents representing spiritual prestige and ancestral blessing
- Ambient particle animations evoking the ethereal boundary between the seen and unseen worlds



---

## 🤝 Contributing

Contributions are welcome, especially from those with deep knowledge of Javanese, Sundanese, Balinese, or broader Nusantara spiritual traditions. Please open an issue first to discuss proposed additions to the data sets or feature modules.

---

## 📄 License

This project is released under the **MIT License**. See `LICENSE` for details.

---

## 🙏 Acknowledgements

Deep gratitude to the generations of Javanese scholars, primbon keepers, and Nusantara spiritual teachers whose accumulated wisdom forms the heart of this application.

---

<p align="center">
  <i>✦ Macan Peramal © 2026 — Macan Angkasa ✦</i><br/>
  <i>"Memayu Hayuning Bawana — Beautifying the Beauty of the World"</i>
</p>
