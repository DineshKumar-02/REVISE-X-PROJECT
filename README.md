# Revise-X ⚡ — Developer Revision & Technical Study Hub

<div align="center">

![Revise-X Banner](https://img.shields.io/badge/Revise--X-Developer%20Study%20Guides-ea580c?style=for-the-badge&logo=code&logoColor=white)
![Pricing](https://img.shields.io/badge/All%20Notes-Flat%20₹50%20Only-f59e0b?style=for-the-badge)
![React 19](https://img.shields.io/badge/React-19.2-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-8.2-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![Python PDF Engine](https://img.shields.io/badge/Engine-ReportLab%20%26%20PyPDF-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

<br />

**Revise Fast. Crack Interviews. High-yield, visual developer study guides & cheatsheets at just ₹50.**

[Explore Catalog](#-curated-study-notes-catalog) • [Key Features](#-key-features) • [PDF Generation Engine](#-automated-pdf--watermarking-pipeline) • [Design System](#-brand-identity--design-system) • [Project Architecture](#-project-architecture)

</div>

---

## 📖 Overview

**Revise-X** is an ultra-fast, modern e-learning and revision platform tailored for software engineering students, bootcamp grads, and technical interview candidates. 

Preparing for interviews or technical exams usually means sifting through 600-page textbooks or 40-hour video playlists. **Revise-X** solves this problem by delivering distilled, visually structured, high-resolution vector PDF notes and cheatsheets—covering **Frontend (HTML5, CSS3, React 19)**, **Databases (MongoDB Aggregation)**, and **Cloud Infrastructure (AWS IAM, S3, EC2)**—all micro-priced at an accessible **₹50 per guide**.

---

## ✨ Key Features

### 🔍 Interactive 2-Page Sample Preview Modal
- **Live In-Browser Reader**: Inspect a real 2-page sample before purchasing any study guide.
- **Syllabus & Topic Breakdown**: Direct view of all key concepts, page counts, and formats.
- **Teaser & Lock Notice**: Transparent previews showing remaining pages and premium content breakdown.
- **Direct Cart Conversion**: Add to cart directly from within the modal viewer.

### ⚡ Live Instant Search & Multi-Category Filtering
- **Fuzzy Search**: Filter notes instantaneously by keyword, language, or specific subtopics (e.g., *Flexbox*, *S3*, *Aggregation*, *Hooks*).
- **Category Tabs**: Seamless switching across *All*, *Frontend*, *Database*, and *Cloud*.
- **Dynamic Sorting**: Sort notes by *Featured*, *Price: Low to High*, *Price: High to Low*, or *Page Count*.
- **Live Counter Badges**: Instant visibility into the number of available notes per category.

### 🛒 Slide-over Revision Cart & Discount Engine
- **Persistent Local Storage**: Cart state automatically syncs to local storage across browser refreshes.
- **Slide-Out Drawer UX**: Smooth drawer layout with item removal, category indicators, and price comparisons.
- **Discount Engine**: Built-in promotional coupon redemption (e.g., `REVISE20` for 20% off, `FREEFIRST`).
- **Real-Time Savings Tracker**: Visual breakdown of original price, store savings, promo discounts, and final payable amount.

### 💳 Realistic Multi-Method Checkout Flow
- **256-Bit SSL Encrypted Interface**: Authentic checkout simulation designed for modern student payment expectations.
- **Supported Payment Channels**:
  - 📱 **UPI Apps**: Instant mock handling for Google Pay, PhonePe, Paytm, and CRED.
  - 📷 **Dynamic QR Code**: Interactive scanner box simulation for mobile UPI payments.
  - 💳 **Debit & Credit Cards**: Card number validation and CVV inputs.
  - 🏛️ **NetBanking**: Direct bank selector (SBI, HDFC, ICICI, Axis, Kotak).
- **Celebratory Confetti**: Triggered via `canvas-confetti` upon successful verification.
- **Immediate PDF Download Link**: Direct, instantaneous client-side download links delivered right on the success screen with generated Order IDs.

### 🎁 Free Community Sample Cheatsheet Giveaway
- 15-page sample developer cheatsheet covering essential interview questions (Event Loop, React Hook rules, Flexbox vs. Grid matrix, REST conventions).
- Free email-based instant download to help students test quality with zero initial financial commitment.

---

## 📚 Curated Study Notes Catalog

Each study guide is crafted for high retention, combining visual architecture diagrams, typed code samples, syntax quick-references, and common interview questions.

| Guide Name | Category | Format | Pages | Topics Included | Regular Price | Revise-X Price |
| :--- | :---: | :---: | :---: | :--- | :---: | :---: |
| **HTML5 Complete Notes** *(Typed Edition)* | Frontend | Vector PDF | 10 | Skeleton & `<!DOCTYPE>`, Semantic Tags (`<nav>`, `<main>`, `<article>`), Forms & Validation, Tables, Block vs Inline, Audio/Video | ~₹199~ | **₹50** |
| **CSS3 Complete Notes** *(Typed Edition)* | Frontend | Vector PDF | 7 | Selectors & Combinators (`>`, `+`, `~`), Box Model reset, Positioning, 1D Flexbox, 2D Grid, Media Queries & Animations | ~₹199~ | **₹50** |
| **React Architecture & State Management** | Frontend | Digital PDF | 62 | Component Lifecycle, Hooks (`useState`, `useEffect`, `useMemo`, `useCallback`), Custom Hooks, Context API, React 19 Actions | ~₹199~ | **₹50** |
| **MongoDB & Aggregation Pipeline Guide** | Database | Digital PDF | 27 | Embedding vs Referencing, Compound & Text Indexes, Pipeline Stages (`$match`, `$group`, `$lookup`, `$project`), Facets & Cursors | ~₹199~ | **₹50** |
| **AWS Cloud Core (IAM, S3 & EC2)** | Cloud | Digital PDF | 14 | IAM Policies & Least Privilege, S3 Bucket Security & Pre-signed URLs, EC2 Security Groups, VPC Basics, AWS SDK v3 snippets | ~₹249~ | **₹50** |

---

## 🛠️ Automated PDF & Watermarking Pipeline

Revise-X includes a suite of Python scripts in `scripts/` that build, format, and brand study materials:

```
scripts/
├── build_typed_notes_suite.py     # Automated ReportLab generator for clean digital PDFs
├── watermark_uploaded_notes.py    # Non-intrusive vector watermark & running header overlay engine
├── generate_digital_notes.py      # Digital notes compiler with custom syntax styling
├── generate_js_notes.py           # Specialized JavaScript cheatsheet generator
└── build_all_digital_and_bundles.py # Batch processing script for complete catalog builds
```

### Key Capabilities:
- **Non-Intrusive Vector Watermarking**: Applies a subtle, 4.2% alpha diagonal `REVISE-X` brand mark across document bodies without affecting legibility.
- **Running Headers & Footers**: Overlays precise hairline separator rules, dynamic page numbering (`Page X of Y`), copyright notices, and document titles.
- **Adaptive Canvas Modes**: Handles both typed digital vector PDFs and scanned handwritten study guides with dedicated coordinate offsets.

---

## 🎨 Brand Identity & Design System

### Custom Architectural Vector Logo
Revise-X features a custom-engineered SVG logo mark (`Logo.jsx`):
- **Dynamic Monogram "X"**: Layered diagonally to represent rapid study progression and knowledge multiplication.
- **Cheatsheet Leaf & Dog-Eared Fold**: Subtle page-curl motif representing technical notebooks.
- **Illuminated Code Chevron (`<`)**: Neon amber-to-terracotta glowing code bracket positioned at the core.
- **Color Palette**:
  - Primary Accent: Terracotta Sunset (`#ea580c`) & Fiery Orange (`#f97316`)
  - Highlight Accent: Golden Amber (`#fbbf24`) & Canary Yellow (`#fef08a`)
  - Dark Surface Base: Deep Espresso & Slate (`#0b0f19`, `#111827`, `#1f2937`)

### Visual Aesthetics
- **Dark Mode First**: High-contrast, easy-on-the-eyes dark workspace built with vanilla CSS.
- **Glassmorphic Elevations**: Ambient backdrop filters, translucent borders, and soft radial glow effects.
- **Micro-Interactions**: Smooth hover lifts, animated cart badge counters, pill badges, and accessible focus outlines.

---

## 📂 Project Architecture

```plaintext
REVISE-X-PROJECT/
├── frontend/                     # React 19 Single Page Application
│   ├── public/
│   │   ├── notebooks/            # High-resolution PDF storage for verified downloads
│   │   ├── images/               # App icons, watermarks, and vector assets
│   │   └── favicon.svg           # Custom SVG favicon
│   ├── src/
│   │   ├── assets/               # Local icons and asset bundles
│   │   ├── components/           # Modular React components
│   │   │   ├── CartDrawer.jsx    # Persistent slide-over cart with coupon input
│   │   │   ├── CheckoutModal.jsx # Multi-method simulated payment gateway
│   │   │   ├── FAQSection.jsx    # Collapsible FAQ accordion
│   │   │   ├── Footer.jsx        # Footer links, social buttons & trust guarantees
│   │   │   ├── FreeCheatsheetModal.jsx # 15-page sample giveaway modal
│   │   │   ├── Hero.jsx          # Hero section with interactive code preview card
│   │   │   ├── Logo.jsx          # Custom SVG logo glyph & brand header
│   │   │   ├── Navbar.jsx        # Sticky navigation with live search input & cart button
│   │   │   ├── NoteCard.jsx      # Interactive catalog card with preview & buy actions
│   │   │   ├── NotesCatalog.jsx  # Category filter pills, sorting & grid rendering
│   │   │   └── PreviewModal.jsx  # Multi-page sample preview modal with locked page teaser
│   │   ├── data/
│   │   │   └── notesData.js      # Structured database of notes, syllabus, and sample pages
│   │   ├── App.css               # Design system tokens, layouts, and responsive breakpoints
│   │   ├── App.jsx               # Main state container (cart, modals, search, catalog)
│   │   └── main.jsx              # Vite React entry point
│   ├── index.html                # HTML5 entry with meta descriptions & OpenGraph tags
│   ├── netlify.toml              # Netlify client-side routing and build configurations
│   ├── package.json              # Dependencies and script definitions
│   └── vite.config.js            # Vite configuration
│
└── scripts/                      # Automated Python PDF generation & watermarking engine
    ├── build_typed_notes_suite.py
    ├── watermark_uploaded_notes.py
    ├── generate_digital_notes.py
    ├── generate_js_notes.py
    └── build_all_digital_and_bundles.py
```

---

## 🚀 Quick Start Guide

### Prerequisites
- **Node.js** (v18 or later recommended)
- **npm** or **yarn**
- **Python 3.8+** *(optional, only needed for compiling or watermarking new PDFs)*

### 1. Clone the Repository
```bash
git clone https://github.com/DineshKumar-02/REVISE-X-PROJECT.git
cd REVISE-X-PROJECT/frontend
```

### 2. Install Frontend Dependencies
```bash
npm install
```

### 3. Launch the Development Server
```bash
npm run dev
```

Visit the local URL shown in your terminal (typically `http://localhost:5173`) to view the application.

### 4. Build for Production
```bash
npm run build
```

---

## 🐍 Running the PDF Tooling (Optional)

To regenerate typed PDFs or apply brand watermarks across study guides:

```bash
# From the repository root
pip install reportlab pypdf pillow

# Run the watermarking script
python scripts/watermark_uploaded_notes.py

# Generate typed notes suite
python scripts/build_typed_notes_suite.py
```

---

## 🗺️ Product Roadmap

- [x] Flat ₹50 Pricing Architecture
- [x] Interactive 2-Page Sample Preview Modal
- [x] Live Instant Search & Category Filters
- [x] Persistent LocalStorage Cart Drawer & Promo Code Engine
- [x] Realistic Multi-Channel Checkout Simulation with Instant PDF Delivery
- [x] Free 15-Page Sample Cheatsheet Giveaway Flow
- [x] Automated ReportLab & PyPDF Watermarking Pipeline
- [ ] JavaScript Core & Event Loop Deep Dive Guide
- [ ] System Design & Microservices Cheat Sheet Bundle
- [ ] Production Razorpay Webhook & Payment Gateway Integration
- [ ] User Account Dashboard with Cloud Note Sync

---

## 📄 License & Credits

This project is licensed under the **MIT License**.

Crafted with care for tech students and developers everywhere.  
Developed by [Dinesh Kumar](https://github.com/DineshKumar-02).
