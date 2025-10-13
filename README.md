# 🌿 TerraNova — Miniature Ecosystems in a Digital World

**TerraNova** is a modern, responsive **full-stack e-commerce platform** built with **Flask** and **Python**, blending technology and nature into a single experience.  
It demonstrates a complete technical workflow — from **ethical data acquisition and preprocessing** to a **seamless, AJAX-driven shopping experience**.

> 🌱 *"A digital store where nature meets technology — bringing serenity, creativity, and sustainability into every jar."*

---

## 🎥 Live Demo
Coming soon on **YouTube!**  
*(A complete walkthrough video showcasing how TerraNova works will be added here.)*

---

## ⚙️ Tech Stack

**Backend:**  
- Python (Flask)

**Data Science / Engineering:**  
- pandas, requests, BeautifulSoup4, selenium, csv

**Storage & State Management:**  
- Flask Session (for Cart)

**Frontend:**  
- HTML5, Jinja2  
- Tailwind CSS (via CDN)  
- Custom CSS (style.css)  
- JavaScript (AJAX for asynchronous cart updates)

---

## 🧩 Project Overview

TerraNova offers users a smooth and visually engaging experience where they can:
- Explore pre-made terrarium designs from real data sources.
- Build their **own custom terrarium** using a multi-category builder.
- Enjoy instant, interactive feedback with **AJAX-powered** UI updates.
- Experience a polished, minimalist, and artistic interface.

The project serves as a showcase of **data-driven web development** — transforming raw scraped data into a living, dynamic e-commerce platform.

---

## 💻 Technical Workflow & Architecture

### 1. Data Acquisition & Preprocessing
- **Ethical Scraping:** Verified and followed all legal and ethical data sourcing guidelines.  
- **Data Pipeline:** Used Python libraries (`requests`, `BeautifulSoup4`, `selenium`) to scrape terrarium product listings from external websites (e.g., **FNP**, **Etsy**).  
- **Preprocessing:** Cleaned raw data using `pandas` — handling missing fields, normalizing text, and formatting prices.  
- **Final Dataset:** Created a clean, structured `terra.csv` file used directly by the application.  
- **Integration:** Loaded dynamically via a helper function in `data.py` at app startup.

---

### 2. Core Application Logic (`app.py`)
- **Dynamic Routing:** Renders product, customization, and cart pages (`/shop`, `/customize`, `/cart`) with real-time data.  
- **Custom Terrarium Builder:**  
  - Six-category dynamic form (plants, jars, decor, soil, stones, accessories).  
  - Multi-select handling and dynamic Rupee (₹) pricing.  
- **Session-Based Cart:** Managed using Flask sessions, ensuring fast and lightweight performance.  
- **Code Optimization:** Refactored repetitive cart functions into reusable helpers for maintainability.

---

## ✨ Key Features

| Feature | Implementation | Impact |
|----------|----------------|---------|
| **AJAX Cart System** | Asynchronous Flask endpoint (`/add-premade-to-cart-ajax`) + `fetch()` | Smooth cart updates without reloads. |
| **Price Standardization** | Unified Rupee (₹) display and formatted discounts | Builds pricing clarity and user trust. |
| **Visual Confirmation** | “+1” popup and “Added!” animation when adding products | Enhances micro-interactions and satisfaction. |
| **UI Design & Theme** | Dark, high-contrast layout with white main content and custom “brush stroke” CSS | Professional, aesthetic, and accessible look. |

---

## 🧠 Project Highlights

- 🧩 **Data + Web Fusion:** Real-world combination of data preprocessing and web integration.  
- 🧠 **Scalable Architecture:** Clear separation of routes, logic, and data handling.  
- 🌿 **Nature-Inspired Design:** A UI that visually captures the essence of terrariums.  
- ⚡ **Performance-Oriented UX:** AJAX ensures responsiveness and zero reload frustration.  
- 💡 **Academic & Practical Value:** Demonstrates full-stack capability using Python and Flask.

---

## 🧰 Installation & Setup

Run TerraNova locally with just a few steps:

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/terranova.git
cd terranova
