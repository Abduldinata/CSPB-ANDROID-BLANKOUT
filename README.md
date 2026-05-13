<p align="center">
  <img src="icon/icon.png" width="120" />
</p>

<h1 align="center">CSPB ANDROID BLANKOUT</h1>

<p align="center">
  Experimental CSPB Port on Xash3D FWGS (ARM64)
</p>

> ⚠️ This project is not affiliated with Valve or official Counter-Strike.

CSPB Android Blankout adalah project porting dan eksperimen dari Counter Strike Portable berbasis **Xash3D FWGS Engine**, dengan target arsitektur **ARM64**.

Project ini bertujuan untuk:
- Porting dari base lama (CSPB V16) ke engine terbaru (Xash FWGS)
- Eksperimen sistem inventory, touch UI, dan lobby (**NEDA System**)
- Optimasi performa untuk perangkat Android modern

---

## 🔧 Base & Source

- CSPB V16 Open Source — BILLFLX  
- Engine: :contentReference[oaicite:0]{index=0}  
- Partial reference: CSPB V20 assets & system  

Xash3D FWGS adalah engine kompatibel Half-Life/GoldSrc yang dikembangkan untuk cross-platform dan modding modern :contentReference[oaicite:1]{index=1}

---

## ✨ Features (Work in Progress)

- ARM64 build support (Native NDK & Gradle)
- Custom Touch UI (**NEDA System**)  
- Custom Inventory System  
- Weapon porting (CSPB → Xash FWGS)  
- **ARM64 Engine Stabilization** (Tahap uji coba mitigasi FORTIFY vsnprintf & memory pointers)
- **Automated Build Scripts** (Single-click compilation & signed APK generation via `.bat`)

---

## ⚠️ Known Issues

- Map loading initialization (WAD & Precache) sedang dalam tahap stabilisasi akhir
- Inventory belum sepenuhnya sinkron (v16 vs v20 mismatch)  
- Touch UI masih dalam tahap pengembangan  

---

## 📂 Project Structure

- CSPB-ANDROID-OPEN-SOURCE/ → Game source (DLL / logic)
- xash3d-fwgs/ → Engine source
- files/ → Game assets & configuration
- tools/ → Tools & scripts (Python, dll)


---

## 👤 Author

- Abdul Dinata  
  *(Porting, NEDA System, Development)*  

---

## 🙏 Credits

### Core Source
- BILLFLX — CSPB V16 Open Source  
- Tempo Channel  

### Engine
- FWGS Team — Xash3D FWGS Engine  
- https://github.com/fwgs/xash3d-fwgs  

### Additional Contributors
Moemod Hymei / MOE Team  
Counter Strike Federation  
David Vincent B  
Ryuzuu  
Kurobox  
Rikanami Inc  
Abd Rahman  
Imandoe  
Shinmai  
Dzery27  
Jahshz  
Beteman  
Dewa Project  
Ryn  
Az_3  
Lorayna  
Seven Foresight  
Ballistic  
Joe Krisna  
Muhammad Fadla Wajiha Soleh  
Pegasus  
RE-29 Project  
Fiko R  
Yasao  
Roy  

And all contributors & CSPB community.

---

## 📜 License

This project is licensed under the **GNU General Public License (GPL)**.

- Xash3D FWGS Engine is licensed under GPL :contentReference[oaicite:2]{index=2}  
- This project follows GPL requirements as it is based on HLSDK/Xash ecosystem  

---

## ⚠️ Disclaimer

This project is intended for **educational and research purposes only**.

All assets, trademarks, and content belong to their respective owners.  
This repository does **not claim ownership of any original CSPB or Valve assets**.

---

## ❤️ Respect

Respect all developers, contributors, and communities behind:
- CSPB Project  
- Xash3D FWGS Engine  
- GoldSrc / Half-Life modding ecosystem  
