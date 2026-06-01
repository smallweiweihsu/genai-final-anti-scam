# 完整專案 Prompt：看懂可疑信件 - 深色系互動式專題展示網站

**此文件可直接複製貼到 ChatGPT 中，用於重現或改進本設計系統。**

---

## 📋 目錄

1. [專案概述](#專案概述)
2. [設計系統](#設計系統)
3. [技術棧](#技術棧)
4. [完整程式碼](#完整程式碼)
5. [頁面結構](#頁面結構)
6. [互動邏輯](#互動邏輯)
7. [色彩系統](#色彩系統)
8. [動畫指引](#動畫指引)
9. [使用指南](#使用指南)

---

## 專案概述

### 核心定位
本專案是一個**深色系互動式專題展示網站**，旨在展示「生成式 AI 輔助一般使用者辨識釣魚郵件的互動介面設計」。

### 主要特點
- **設計哲學**：賽博安全稜鏡 (Cyber-Security Prism) - 新未來主義與科幻賽博風格
- **視覺風格**：極致深色系（#070A12 背景）+ 高飽和度紫藍配色
- **互動體驗**：微發光邊框、物理按壓感、平滑輪播、即時分析 Demo
- **響應式設計**：完全 RWD，支援行動裝置

### 頁面清單
- `/` - 首頁（Hero + 分析器 Demo + 特色功能 + 案例研究 + 推薦語輪播）
- `/workflow` - 系統流程
- `/interface` - 介面設計案例
- `/model` - 模型說明
- `/dataset` - 資料集設計

---

## 設計系統

### 設計哲學：賽博安全稜鏡 (Cyber-Security Prism)

#### 核心原則
1. **視覺對比**：利用極深的背景與亮紫、亮藍的發光元素，引導使用者的視覺焦點。
2. **數據具象化**：將抽象的安全指標、風險分數，轉化為直觀、動態的物理化圖表。
3. **信任感建立**：通過嚴謹的佈局、細邊框與冷色調，傳遞專業與安全防護的信賴感。

#### 佈局範式
- **首頁 Hero**：不對稱網格，左側強烈的主副標題與 CTA，右側不對稱懸浮的「模擬分析預覽卡片」
- **分析器區塊**：雙欄儀表板，左欄為輸入與操作，右欄為 AI 分析結果的可視化控制台
- **功能卡片**：網格式排列，hover 時向上浮起並產生微光邊框

#### 招牌視覺元素
- **微發光邊框 (Glow Borders)**：卡片在 hover 時，邊框會產生由紫到藍的漸層微光
- **動態風險儀 (Risk Meter)**：進度條隨風險分數動態變化，顏色從綠→黃→紅
- **安全行動清單 (Checklist)**：帶有動畫勾選效果的互動卡片

---

## 技術棧

### 前端框架
- **React 19** - UI 框架
- **Tailwind CSS 4** - 樣式系統
- **Wouter** - 輕量級路由
- **Lucide React** - Icon 庫
- **Sonner** - Toast 通知

### 開發工具
- **Vite** - 快速開發伺服器
- **TypeScript** - 型別安全
- **shadcn/ui** - UI 元件庫

### 部署
- 靜態網站（無後端）
- 支援 Vite 開發模式與生產打包

---

## 完整程式碼

### 1. 全局樣式系統 (client/src/index.css)

```css
@import "tailwindcss";
@import "tw-animate-css";

@custom-variant dark (&:is(.dark *));

@theme inline {
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-popover: var(--popover);
  --color-popover-foreground: var(--popover-foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-accent: var(--accent);
  --color-accent-foreground: var(--accent-foreground);
  --color-destructive: var(--destructive);
  --color-destructive-foreground: var(--destructive-foreground);
  --color-border: var(--border);
  --color-input: var(--input);
  --color-ring: var(--ring);
  --radius: 0.75rem;
}

/* 
 * DESIGN SYSTEM: Cyber-Security Prism (賽博安全稜鏡)
 * Base theme variables mapped to modern dark-mode palettes
 */
:root {
  --background: #070A12; /* 深邃黑夜藍 */
  --foreground: #F8FAFC; /* 極地白 */
  
  --card: #111827; /* 暗灰藍 */
  --card-foreground: #F8FAFC;
  
  --popover: #111827;
  --popover-foreground: #F8FAFC;
  
  --primary: #7C3AED; /* 極光紫 */
  --primary-foreground: #FFFFFF;
  
  --secondary: #1E3A8A; /* 深海藍 */
  --secondary-foreground: #CBD5E1;
  
  --muted: #151B2E; /* 輔助深藍 */
  --muted-foreground: #94A3B8;
  
  --accent: #6D5DF6; /* 冷調紫藍 */
  --accent-foreground: #FFFFFF;
  
  --destructive: #EF4444; /* 警告紅 */
  --destructive-foreground: #FFFFFF;
  
  --border: rgba(255, 255, 255, 0.12); /* 細微半透明白邊 */
  --input: rgba(255, 255, 255, 0.08);
  --ring: #7C3AED;
  
  --radius: 0.75rem;
}

.dark {
  /* This is a dark-first project, so the variables are the same */
  --background: #070A12;
  --foreground: #F8FAFC;
  --card: #111827;
  --card-foreground: #F8FAFC;
  --popover: #111827;
  --popover-foreground: #F8FAFC;
  --primary: #7C3AED;
  --primary-foreground: #FFFFFF;
  --secondary: #1E3A8A;
  --secondary-foreground: #CBD5E1;
  --muted: #151B2E;
  --muted-foreground: #94A3B8;
  --accent: #6D5DF6;
  --accent-foreground: #FFFFFF;
  --destructive: #EF4444;
  --destructive-foreground: #FFFFFF;
  --border: rgba(255, 255, 255, 0.12);
  --input: rgba(255, 255, 255, 0.08);
  --ring: #7C3AED;
}

@layer base {
  * {
    @apply border-border outline-ring/50;
  }
  body {
    @apply bg-background text-foreground antialiased;
    font-family: 'Inter', 'Noto Sans TC', system-ui, -apple-system, sans-serif;
    background-image: 
      radial-gradient(at 0% 0%, rgba(124, 58, 237, 0.08) 0px, transparent 50%),
      radial-gradient(at 100% 100%, rgba(30, 58, 138, 0.1) 0px, transparent 50%);
    background-attachment: fixed;
  }
  
  /* Smooth transitions for interactive elements */
  a, button, input, textarea, select {
    @apply transition-all duration-200 ease-out;
  }
  
  /* Custom Focus Ring */
  *:focus-visible {
    @apply outline-none ring-2 ring-primary/50 ring-offset-2 ring-offset-background;
  }
}

@layer components {
  .container {
    width: 100%;
    margin-left: auto;
    margin-right: auto;
    padding-left: 1.25rem;
    padding-right: 1.25rem;
  }

  .flex {
    min-height: 0;
    min-width: 0;
  }

  @media (min-width: 640px) {
    .container {
      padding-left: 2rem;
      padding-right: 2rem;
    }
  }

  @media (min-width: 1024px) {
    .container {
      padding-left: 3rem;
      padding-right: 3rem;
      max-width: 1280px;
    }
  }

  /* Custom Glassmorphism Utility */
  .glass-panel {
    @apply bg-card/80 backdrop-blur-md border border-white/10 shadow-xl;
  }
  
  /* Cyber Security Glow Hover effect */
  .cyber-glow-hover {
    @apply transition-all duration-300 ease-out;
  }
  .cyber-glow-hover:hover {
    @apply -translate-y-1.5 shadow-2xl;
    box-shadow: 0 10px 30px -10px rgba(124, 58, 237, 0.3), 0 1px 1px 0 rgba(255, 255, 255, 0.1) inset;
    border-color: rgba(124, 58, 237, 0.4);
  }

  /* Button Press Physics Effect */
  .btn-press-effect:active {
    transform: scale(0.97);
  }
}
```

### 2. HTML 入口 (client/index.html)

```html
<!doctype html>
<html lang="zh-Hant">

  <head>
    <meta charset="UTF-8" />
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1.0, maximum-scale=1" />
    <title>看懂可疑信件 - AI 輔助釣魚郵件辨識互動介面</title>    
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Noto+Sans+TC:wght@300;400;500;700;900&display=swap" rel="stylesheet" />
  </head>

  <body class="dark">
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>

</html>
```

### 3. 路由設定 (client/src/App.tsx)

```typescript
import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFound from "@/pages/NotFound";
import { Route, Switch } from "wouter";
import ErrorBoundary from "./components/ErrorBoundary";
import { ThemeProvider } from "./contexts/ThemeContext";
import Home from "./pages/Home";
import Workflow from "./pages/Workflow";
import Interface from "./pages/Interface";
import Model from "./pages/Model";
import Dataset from "./pages/Dataset";

function Router() {
  return (
    <Switch>
      <Route path="/" component={Home} />
      <Route path="/workflow" component={Workflow} />
      <Route path="/interface" component={Interface} />
      <Route path="/model" component={Model} />
      <Route path="/dataset" component={Dataset} />
      <Route path="/404" component={NotFound} />
      {/* Final fallback route */}
      <Route component={NotFound} />
    </Switch>
  );
}

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider defaultTheme="dark">
        <TooltipProvider>
          <Toaster />
          <Router />
        </TooltipProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;
```

### 4. 導覽列組件 (client/src/components/Navbar.tsx)

```typescript
/**
 * DESIGN SYSTEM: Cyber-Security Prism (賽博安全稜鏡)
 * Component: Navbar
 * Features: Pure text links, active states, responsive mobile menu, hover animations.
 */
import { Link, useLocation } from "wouter";
import { useState } from "react";
import { Menu, X } from "lucide-react";

export default function Navbar() {
  const [location] = useLocation();
  const [isOpen, setIsOpen] = useState(false);

  const navItems = [
    { name: "分析 Demo", path: "/" },
    { name: "系統流程", path: "/workflow" },
    { name: "介面設計", path: "/interface" },
    { name: "模型說明", path: "/model" },
    { name: "資料集", path: "/dataset" },
  ];

  return (
    <nav className="sticky top-0 z-50 w-full border-b border-white/10 bg-background/80 backdrop-blur-md">
      <div className="container flex h-16 items-center justify-between">
        {/* Brand Logo */}
        <Link href="/" className="flex items-center space-x-2">
          <span className="text-lg font-extrabold tracking-wider bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            看懂可疑信件
          </span>
        </Link>

        {/* Desktop Navigation */}
        <div className="hidden md:flex items-center space-x-1">
          {navItems.map((item) => {
            const isActive = location === item.path;
            return (
              <Link
                key={item.path}
                href={item.path}
                className={`px-4 py-2 text-sm font-medium transition-all duration-200 rounded-md btn-press-effect ${
                  isActive
                    ? "text-primary bg-primary/10 border border-primary/20"
                    : "text-muted-foreground hover:text-foreground hover:bg-white/5"
                }`}
              >
                {item.name}
              </Link>
            );
          })}
          <a
            href="https://github.com/smallweiweihsu/genai-final-anti-scam"
            target="_blank"
            rel="noopener noreferrer"
            className="px-4 py-2 text-sm font-medium text-muted-foreground hover:text-foreground hover:bg-white/5 rounded-md transition-all duration-200"
          >
            GitHub
          </a>
        </div>

        {/* Mobile Navigation Trigger */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="md:hidden p-2 text-muted-foreground hover:text-foreground focus:outline-none"
          aria-label="Toggle Menu"
        >
          {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
        </button>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <div className="md:hidden border-b border-white/10 bg-background/95 px-4 py-4 space-y-2 animate-in fade-in slide-in-from-top-5 duration-200">
          {navItems.map((item) => {
            const isActive = location === item.path;
            return (
              <Link
                key={item.path}
                href={item.path}
                onClick={() => setIsOpen(false)}
                className={`block px-4 py-2.5 text-base font-medium rounded-md ${
                  isActive
                    ? "text-primary bg-primary/10 border border-primary/20"
                    : "text-muted-foreground hover:text-foreground hover:bg-white/5"
                }`}
              >
                {item.name}
              </Link>
            );
          })}
          <a
            href="https://github.com/smallweiweihsu/genai-final-anti-scam"
            target="_blank"
            rel="noopener noreferrer"
            onClick={() => setIsOpen(false)}
            className="block px-4 py-2.5 text-base font-medium text-muted-foreground hover:text-foreground hover:bg-white/5 rounded-md"
          >
            GitHub
          </a>
        </div>
      )}
    </nav>
  );
}
```

### 5. 推薦語輪播組件 (client/src/components/TestimonialCarousel.tsx)

```typescript
/**
 * DESIGN SYSTEM: Cyber-Security Prism (賽博安全稜鏡)
 * Component: TestimonialCarousel
 * Features: Auto-playing carousel with smooth CSS transitions, custom navigation buttons.
 */
import { useState, useEffect, useRef } from "react";
import { ChevronLeft, ChevronRight, Quote } from "lucide-react";

interface Testimonial {
  role: string;
  content: string;
}

export default function TestimonialCarousel() {
  const testimonials: Testimonial[] = [
    {
      role: "一般使用者視角",
      content: "「比起只告訴我這是不是詐騙，我更需要知道哪裡可疑、下一步該怎麼做。」",
    },
    {
      role: "資安教育視角",
      content: "「這個介面把釣魚郵件的判斷重點拆成可疑特徵、話術與安全行動，比單純分類更適合教學展示。」",
    },
    {
      role: "模型串接視角",
      content: "「只要模型回傳固定 JSON schema，前端就能把結果轉成一致的視覺化說明。」",
    },
  ];

  const [activeIndex, setActiveIndex] = useState(0);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const autoPlayRef = useRef<NodeJS.Timeout | null>(null);

  const handleNext = () => {
    if (isTransitioning) return;
    setIsTransitioning(true);
    setActiveIndex((prev) => (prev + 1) % testimonials.length);
  };

  const handlePrev = () => {
    if (isTransitioning) return;
    setIsTransitioning(true);
    setActiveIndex((prev) => (prev - 1 + testimonials.length) % testimonials.length);
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsTransitioning(false);
    }, 400); // matches transition duration
    return () => clearTimeout(timer);
  }, [activeIndex]);

  // Auto-play setup
  useEffect(() => {
    autoPlayRef.current = setInterval(handleNext, 6000);
    return () => {
      if (autoPlayRef.current) clearInterval(autoPlayRef.current);
    };
  }, []);

  const resetAutoPlay = () => {
    if (autoPlayRef.current) clearInterval(autoPlayRef.current);
    autoPlayRef.current = setInterval(handleNext, 6000);
  };

  return (
    <section className="py-20 border-t border-white/5 bg-background relative overflow-hidden">
      {/* Background radial highlight */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-primary/5 rounded-full blur-[120px] pointer-events-none" />

      <div className="container max-w-4xl relative z-10">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-foreground to-muted-foreground bg-clip-text text-transparent">
            使用者與評審回饋
          </h2>
          <p className="text-sm text-muted-foreground mt-2">
            展示專案設計概念在實際情境與教學上的回饋
          </p>
        </div>

        {/* Carousel Outer Wrapper */}
        <div className="relative glass-panel rounded-2xl p-8 md:p-12 border border-white/10 shadow-2xl">
          <Quote className="absolute top-6 left-6 h-12 w-12 text-primary/10 pointer-events-none" />

          {/* Testimonial Display Area */}
          <div className="min-h-[160px] flex flex-col justify-center items-center text-center px-4 md:px-12">
            <div
              className={`transition-all duration-400 ease-out transform ${
                isTransitioning
                  ? "opacity-0 translate-y-2 scale-95"
                  : "opacity-100 translate-y-0 scale-100"
              }`}
            >
              <p className="text-lg md:text-xl font-medium text-foreground leading-relaxed mb-6">
                {testimonials[activeIndex].content}
              </p>
              <span className="inline-block px-3 py-1 rounded-full text-xs font-semibold tracking-wider uppercase bg-primary/10 text-primary border border-primary/20">
                {testimonials[activeIndex].role}
              </span>
            </div>
          </div>

          {/* Controls */}
          <div className="flex justify-between items-center mt-8">
            {/* Left arrow */}
            <button
              onClick={() => {
                handlePrev();
                resetAutoPlay();
              }}
              className="p-2 rounded-full border border-white/10 bg-white/5 hover:bg-white/10 text-muted-foreground hover:text-foreground transition-all duration-200 btn-press-effect"
              aria-label="Previous feedback"
            >
              <ChevronLeft className="h-5 w-5" />
            </button>

            {/* Indicator dots */}
            <div className="flex space-x-2">
              {testimonials.map((_, index) => (
                <button
                  key={index}
                  onClick={() => {
                    if (isTransitioning) return;
                    setIsTransitioning(true);
                    setActiveIndex(index);
                    resetAutoPlay();
                  }}
                  className={`h-2.5 rounded-full transition-all duration-300 ${
                    activeIndex === index
                      ? "w-8 bg-primary"
                      : "w-2.5 bg-white/20 hover:bg-white/40"
                  }`}
                  aria-label={`Go to feedback ${index + 1}`}
                />
              ))}
            </div>

            {/* Right arrow */}
            <button
              onClick={() => {
                handleNext();
                resetAutoPlay();
              }}
              className="p-2 rounded-full border border-white/10 bg-white/5 hover:bg-white/10 text-muted-foreground hover:text-foreground transition-all duration-200 btn-press-effect"
              aria-label="Next feedback"
            >
              <ChevronRight className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
```

### 6. 分析器 Demo 組件 (client/src/components/AnalyzerDemo.tsx) - 核心互動

此組件包含：
- 文字/圖片輸入 Tab 切換
- 三個預設範例快速載入
- 模擬 AI 分析（2 秒延遲）
- 完整的風險評估輸出（風險分數、信心度、可疑特徵、詐騙話術、安全建議）
- 進度條視覺化
- Toast 通知

**完整代碼請參考原始專案檔案 `client/src/components/AnalyzerDemo.tsx`**

### 7. 頁腳組件 (client/src/components/Footer.tsx)

```typescript
/**
 * DESIGN SYSTEM: Cyber-Security Prism (賽博安全稜鏡)
 * Component: Footer
 * Features: Structured layout, required project links, GitHub repo, disclaimer.
 */
import { Link } from "wouter";

export default function Footer() {
  return (
    <footer className="w-full border-t border-white/10 bg-[#04070d] py-12 text-muted-foreground">
      <div className="container grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Column 1: Brand & Purpose */}
        <div className="space-y-4">
          <h3 className="text-lg font-bold text-foreground tracking-wide">
            看懂可疑信件
          </h3>
          <p className="text-sm text-muted-foreground leading-relaxed max-w-xs">
            生成式 AI 輔助一般使用者辨識釣魚郵件的互動介面設計。把複雜的模型判斷，轉換成一般使用者看得懂、做得到的安全行動。
          </p>
        </div>

        {/* Column 2: Navigation Links */}
        <div className="space-y-4">
          <h4 className="text-sm font-semibold text-foreground uppercase tracking-wider">
            專案導覽
          </h4>
          <ul className="space-y-2 text-sm">
            <li>
              <Link href="/" className="hover:text-primary transition-colors">
                分析 Demo
              </Link>
            </li>
            <li>
              <Link href="/workflow" className="hover:text-primary transition-colors">
                系統流程
              </Link>
            </li>
            <li>
              <Link href="/interface" className="hover:text-primary transition-colors">
                介面設計
              </Link>
            </li>
            <li>
              <Link href="/model" className="hover:text-primary transition-colors">
                模型說明
              </Link>
            </li>
            <li>
              <Link href="/dataset" className="hover:text-primary transition-colors">
                資料集設計
              </Link>
            </li>
            <li>
              <a
                href="https://github.com/smallweiweihsu/genai-final-anti-scam"
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-primary transition-colors"
              >
                GitHub 專案倉庫
              </a>
            </li>
          </ul>
        </div>

        {/* Column 3: Disclaimer */}
        <div className="space-y-4">
          <h4 className="text-sm font-semibold text-foreground uppercase tracking-wider">
            免責聲明
          </h4>
          <div className="rounded-lg border border-white/5 bg-white/5 p-4 text-xs leading-relaxed text-muted-foreground">
            本專案僅供期末專題展示與輔助判斷，不應作為資安、法律或金融決策的唯一依據。
          </div>
        </div>
      </div>

      <div className="container mt-8 pt-8 border-t border-white/5 text-center text-xs">
        <p>© 2026 看懂可疑信件 專題小組. All rights reserved.</p>
      </div>
    </footer>
  );
}
```

---

## 頁面結構

### 首頁 (Home.tsx) - 完整架構

```
首頁
├── Navbar (導覽列)
├── Hero 區塊
│   ├── 左側：主標題、副標、雙 CTA 按鈕
│   └── 右側：不對稱懸浮的模擬分析預覽卡片
├── 3 大核心功能網格
│   ├── 可疑信件分析
│   ├── 白話風險解釋
│   └── 安全行動建議
├── AI 分析器 Demo
│   ├── 文字/圖片 Tab 切換
│   ├── 預設範例快速載入
│   └── 詳細分析結果輸出
├── 專題設計案例研究 (3 張卡片)
│   ├── 介面設計 → /interface
│   ├── 模型說明 → /model
│   └── 資料集設計 → /dataset
├── 推薦語輪播 (TestimonialCarousel)
└── Footer (頁腳)
```

### 子頁面結構

- **`/workflow`** - 系統流程（4 步驟時間軸）
- **`/interface`** - 介面設計案例（4 大設計決策）
- **`/model`** - 模型說明（指標對比表、JSON Schema）
- **`/dataset`** - 資料集設計（3 大安全原則）

---

## 色彩系統

### 主要色彩

| 用途 | 色值 | 說明 |
|------|------|------|
| 背景 | `#070A12` | 深邃黑夜藍，極致暗色基底 |
| 卡片 | `#111827` | 暗灰藍，與背景拉開層次 |
| 主色（紫） | `#7C3AED` | 極光紫，代表 AI 分析 |
| 輔色（藍） | `#1E3A8A` | 深海藍，代表穩固與防護 |
| 強調色（淺紫） | `#6D5DF6` | 冷調紫藍，用於次要元素 |
| 警告紅 | `#EF4444` | 危險等級指示 |
| 警告黃 | `#F59E0B` | 可疑等級指示 |
| 安全綠 | `#10B981` | 安全等級指示 |
| 文字 | `#F8FAFC` | 極地白，高對比易讀 |
| 次文字 | `#CBD5E1` | 板岩灰 |
| 邊框 | `rgba(255,255,255,0.12)` | 細微半透明白邊 |

### Tailwind 配置

所有色彩已映射至 Tailwind CSS 變數：
- `bg-background` / `text-foreground`
- `bg-card` / `text-card-foreground`
- `bg-primary` / `text-primary-foreground`
- `bg-secondary` / `text-secondary-foreground`
- `bg-accent` / `text-accent-foreground`
- `bg-destructive` / `text-destructive-foreground`

---

## 互動邏輯

### 1. 卡片 Hover 效果 (cyber-glow-hover)

```css
.cyber-glow-hover:hover {
  transform: translateY(-6px);
  box-shadow: 0 10px 30px -10px rgba(124, 58, 237, 0.3), 
              0 1px 1px 0 rgba(255, 255, 255, 0.1) inset;
  border-color: rgba(124, 58, 237, 0.4);
  transition: all 300ms cubic-bezier(0.23, 1, 0.32, 1);
}
```

### 2. 按鈕按壓效果 (btn-press-effect)

```css
.btn-press-effect:active {
  transform: scale(0.97);
}
```

### 3. 推薦語輪播轉場

- 自動播放間隔：6 秒
- 轉場時間：400ms
- 轉場動畫：淡入淡出 + Y 軸微移 + 縮放
- 緩動函數：`ease-out`

### 4. 分析器 Demo 流程

1. 使用者輸入信件或上傳圖片
2. 點擊「開始 AI 分析」按鈕
3. 按鈕進入 Loading 狀態（2 秒模擬延遲）
4. 分析結果以淡入動畫呈現
5. 顯示完整的風險評估、特徵標籤、建議清單

---

## 動畫指引

### 全局轉場時間

- **快速互動**（按鈕、連結）：100-160ms
- **卡片懸浮**：200-300ms
- **輪播切換**：400ms
- **頁面轉場**：300-500ms

### 緩動函數

- **進入/離開**：`cubic-bezier(0.23, 1, 0.32, 1)` (ease-out)
- **移動/變形**：`cubic-bezier(0.77, 0, 0.175, 1)` (ease-in-out)

### 禁止過度動畫

- 尊重 `prefers-reduced-motion` 媒體查詢
- 避免在高頻互動（hover）上使用複雜動畫
- 保留動畫用於低頻事件（模態框、通知）

---

## 使用指南

### 如何在 ChatGPT 中使用本 Prompt

1. **複製整份文件**到 ChatGPT
2. **提出您的需求**，例如：
   - "請幫我將這套設計系統應用到一個新的『資安培訓平台』專案"
   - "請修改色彩系統，改用深綠色主題"
   - "請為這個系統增加暗黑模式切換功能"
   - "請優化分析器 Demo 的互動邏輯"

3. **ChatGPT 將能夠**：
   - 理解完整的設計哲學與技術實現
   - 生成符合風格的新組件
   - 修改現有代碼以滿足新需求
   - 提供最佳實踐建議

### 快速開發步驟

1. **初始化 React 19 + Tailwind 4 + Wouter 專案**
   ```bash
   npm create vite@latest my-project -- --template react-ts
   cd my-project
   npm install tailwindcss wouter lucide-react sonner
   ```

2. **複製 `index.css` 中的色彩系統**

3. **複製 Navbar、Footer、TestimonialCarousel 等共用組件**

4. **根據需求建立新頁面**

5. **在 `App.tsx` 中設定路由**

### 自訂色彩系統

若要改變主色調，只需修改 `index.css` 中的 CSS 變數：

```css
:root {
  --primary: #YOUR_NEW_COLOR;
  --accent: #YOUR_NEW_COLOR;
  /* ... 其他顏色 */
}
```

所有使用 `bg-primary`、`text-primary` 等 Tailwind 類別的元素都會自動更新。

---

## 常見問題

### Q: 如何添加新的頁面？

A: 在 `client/src/pages/` 建立新的 `.tsx` 檔案，然後在 `App.tsx` 中添加路由：
```typescript
<Route path="/new-page" component={NewPage} />
```

### Q: 如何修改卡片的 Hover 效果？

A: 編輯 `index.css` 中的 `.cyber-glow-hover:hover` 規則，或在組件中添加自訂 className。

### Q: 如何集成真實的 AI 模型？

A: 目前為靜態模擬。若要集成真實 LLM，需要升級為全端專案，在後端撰寫 API 端點。

### Q: 如何支援淺色主題？

A: 在 `App.tsx` 中的 `ThemeProvider` 添加 `switchable` 屬性，然後在 `index.css` 中定義淺色 CSS 變數。

---

## 總結

本設計系統提供了一套完整的、可重複使用的深色系互動式網站框架。通過嚴格的色彩系統、流暢的動畫、清晰的佈局與豐富的互動，實現了「賽博安全稜鏡」的設計哲學。

所有代碼均已模組化，易於擴展與客製化。您可以直接將本 Prompt 提交給 ChatGPT，以快速建立類似的專案或進行深度改進。

**祝您開發順利！** 🚀
