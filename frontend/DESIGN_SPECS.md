# 🎨 PLAUGE Frontend - Design Specifications

## Overview
This document provides clear specifications for the PLAUGE frontend design, ensuring consistency and maintaining the premium aesthetic.

---

## 🎨 Color Palette

### Primary Colors
```css
Primary Blue:    #667eea
Primary Purple:  #764ba2
Accent Pink:     #f093fb
```

### Status Colors
```css
Success (Low Risk):     #10b981  /* Emerald Green */
Success Dark:           #059669

Warning (Medium Risk):  #f59e0b  /* Amber */
Warning Dark:           #d97706

Danger (High Risk):     #ef4444  /* Red */
Danger Dark:            #dc2626
```

### Background Colors
```css
Background:        #0a0e27  /* Deep Navy */
Background Dark:   #070a1f
Background Alt:    #1a1f3a
```

### Surface Colors (Glass Effect)
```css
Surface:           rgba(255, 255, 255, 0.05)
Surface Hover:     rgba(255, 255, 255, 0.08)
Border:            rgba(255, 255, 255, 0.1)
Border Hover:      rgba(255, 255, 255, 0.2)
```

### Text Colors
```css
Text Primary:    #ffffff
Text Muted:      rgba(255, 255, 255, 0.7)
Text Dim:        rgba(255, 255, 255, 0.5)
```

### Gradients
```css
/* Primary Gradient (Buttons, Logo) */
linear-gradient(135deg, #667eea 0%, #764ba2 100%)

/* Background Gradient */
linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%)

/* Status Gradients */
Success:  linear-gradient(135deg, #10b981 0%, #059669 100%)
Warning:  linear-gradient(135deg, #f59e0b 0%, #d97706 100%)
Danger:   linear-gradient(135deg, #ef4444 0%, #dc2626 100%)
```

---

## 📐 Spacing System

### Scale (rem units)
```
xs:  0.5rem  (8px)   - Tight spacing, small gaps
sm:  1rem    (16px)  - Default gap between related items
md:  1.5rem  (24px)  - Section spacing
lg:  2rem    (32px)  - Large gaps
xl:  3rem    (48px)  - Section padding
2xl: 4rem    (64px)  - Major section spacing
```

### Usage Guidelines
- **xs**: Icon-to-text gaps, badge padding
- **sm**: Button padding, card gaps
- **md**: Section margins, grid gaps
- **lg**: Card padding, container padding
- **xl**: Large card padding, hero spacing
- **2xl**: Major section spacing

---

## 🔤 Typography

### Font Families
```css
Primary:   'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif
Monospace: 'JetBrains Mono', 'Courier New', monospace
```

### Font Weights
```
Light:       300  - Subtle text
Regular:     400  - Body text
Medium:      500  - Emphasized text
Semi-Bold:   600  - Subheadings
Bold:        700  - Headings
Extra-Bold:  800  - Hero text, titles
```

### Type Scale
```css
/* Hero / Display */
Hero Title:        clamp(2.5rem, 5vw, 4rem)  /* 40-64px */
                   Font-weight: 800
                   Line-height: 1.1

/* Headings */
h1 / Page Title:   2rem (32px)
                   Font-weight: 700
                   
h2 / Section:      1.75rem (28px)
                   Font-weight: 700

h3 / Subsection:   1.5rem (24px)
                   Font-weight: 600

h4 / Card Title:   1.25rem (20px)
                   Font-weight: 600

/* Body */
Body Large:        1.125rem (18px)
                   Font-weight: 400
                   Line-height: 1.7

Body Normal:       1rem (16px)
                   Font-weight: 400
                   Line-height: 1.6

Body Small:        0.95rem (15px)
                   Font-weight: 400

/* Meta */
Caption:           0.875rem (14px)
                   Font-weight: 400

Small:             0.75rem (12px)
                   Font-weight: 500
```

---

## 🎯 Border Radius

### Scale
```css
sm:   0.5rem  (8px)   - Buttons, small cards
md:   1rem    (16px)  - Standard cards
lg:   1.5rem  (24px)  - Large cards, modals
xl:   2rem    (32px)  - Hero sections
full: 9999px          - Pills, badges, circular
```

### Usage
- **Small**: Action buttons, close buttons
- **Medium**: Upload cards, feature cards
- **Large**: Modals, main containers
- **XL**: Hero upload areas
- **Full**: Badges, pills, avatar placeholders

---

## ✨ Effects & Shadows

### Box Shadows
```css
/* Elevation Levels */
sm:  0 2px 8px rgba(0, 0, 0, 0.1)   - Subtle lift
md:  0 4px 16px rgba(0, 0, 0, 0.2)  - Card hover
lg:  0 8px 32px rgba(0, 0, 0, 0.3)  - Modals
xl:  0 16px 64px rgba(0, 0, 0, 0.4) - Focused elements

/* Button Glow (on hover) */
Primary: 0 8px 24px rgba(102, 126, 234, 0.4)
Success: 0 8px 24px rgba(16, 185, 129, 0.4)
```

### Glassmorphism
```css
background: rgba(255, 255, 255, 0.05);
backdrop-filter: blur(20px);
border: 1px solid rgba(255, 255, 255, 0.1);
box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
```

### Backdrop Blur
```css
Card Blur:    blur(20px)
Modal Blur:   blur(10px)
```

---

## ⏱️ Animation Timings

### Duration
```css
Fast:    150ms  - Hover states, simple transitions
Base:    250ms  - Standard transitions
Slow:    400ms  - Complex animations

/* Specific Animations */
Modal:   300ms
Fade:    600ms
Slide:   500ms
```

### Easing Functions
```css
Standard:     ease-in-out  - Most transitions
Smooth:       cubic-bezier(0.4, 0, 0.2, 1)  - Material design
Bounce:       cubic-bezier(0.34, 1.56, 0.64, 1)  - Playful
```

### Key Animations

**Fade In Up**
```css
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
/* Duration: 0.8s, Stagger: 0.2s per item */
```

**Pulse**
```css
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.8; transform: scale(1.05); }
}
/* Duration: 2s infinite */
```

**Float** (Background Orbs)
```css
@keyframes float {
    0%, 100% { transform: translate(0, 0) scale(1); }
    33% { transform: translate(100px, -100px) scale(1.1); }
    66% { transform: translate(-100px, 100px) scale(0.9); }
}
/* Duration: 20s infinite */
```

---

## 🎭 Component Specifications

### Buttons

**Primary Button**
```css
Padding:     1rem 1.5rem  (16px 24px)
Background:  linear-gradient(135deg, #667eea 0%, #764ba2 100%)
Color:       #ffffff
Border:      none
Radius:      1rem
Font-size:   1rem
Font-weight: 600

Hover:
  transform: translateY(-2px)
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4)
```

**Secondary Button**
```css
Padding:     1rem 1.5rem
Background:  transparent
Color:       #ffffff
Border:      1px solid rgba(255, 255, 255, 0.2)
Radius:      1rem
Font-size:   0.95rem
Font-weight: 500

Hover:
  background: rgba(255, 255, 255, 0.05)
  border-color: rgba(255, 255, 255, 0.3)
```

**Nav Button**
```css
Padding:     0.5rem 1.5rem  (8px 24px)
Background:  transparent
Border:      1px solid transparent
Radius:      9999px
Font-size:   0.9rem
Font-weight: 500

Hover:
  background: rgba(255, 255, 255, 0.05)
```

### Cards

**Feature Card**
```css
Padding:     2rem  (32px)
Background:  rgba(255, 255, 255, 0.05)
Backdrop:    blur(20px)
Border:      1px solid rgba(255, 255, 255, 0.1)
Radius:      1.5rem
Shadow:      0 8px 32px rgba(0, 0, 0, 0.3)

Hover:
  background: rgba(255, 255, 255, 0.08)
  border-color: rgba(255, 255, 255, 0.2)
```

**Upload Card**
```css
Max-width:   700px
Padding:     3rem  (48px)
Background:  rgba(255, 255, 255, 0.05)
Backdrop:    blur(20px)
Border:      1px solid rgba(255, 255, 255, 0.1)
Radius:      1.5rem
```

### Icons

**Sizes**
```css
Small:   16px  - Inline icons
Medium:  20px  - Button icons
Large:   24px  - Feature icons
XL:      40px  - Logo
2XL:     80px  - Upload area
```

---

## 📊 Layout Specifications

### Breakpoints
```css
Mobile:      < 768px
Tablet:      768px - 1024px
Desktop:     > 1024px
Wide:        > 1440px
```

### Container
```css
Max-width:   1200px
Padding:     0 1.5rem  (0 24px)
Margin:      0 auto
```

### Grid Systems

**Features Grid**
```css
display: grid;
grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
gap: 1.5rem;
```

**Stats Grid**
```css
display: grid;
grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
gap: 1.5rem;
```

---

## 🎨 Status Indicators

### Risk Levels

**Low Risk** (< 50%)
```css
Color:      #10b981
Icon:       🟢
Gradient:   linear-gradient(135deg, #10b981 0%, #059669 100%)
```

**Medium Risk** (50-79%)
```css
Color:      #f59e0b
Icon:       🟡
Gradient:   linear-gradient(135deg, #f59e0b 0%, #d97706 100%)
```

**High Risk** (≥ 80%)
```css
Color:      #ef4444
Icon:       🔴
Gradient:   linear-gradient(135deg, #ef4444 0%, #dc2626 100%)
```

### Progress Steps

**Active Step**
```css
Icon Background:  linear-gradient(135deg, #667eea 0%, #764ba2 100%)
Border:           2px solid #667eea
Opacity:          1
Animation:        pulse-ring 1.5s infinite
```

**Completed Step**
```css
Icon Background:  linear-gradient(135deg, #10b981 0%, #059669 100%)
Border:           2px solid #10b981
Opacity:          1
```

**Inactive Step**
```css
Icon Background:  rgba(255, 255, 255, 0.05)
Border:           2px solid rgba(255, 255, 255, 0.1)
Opacity:          0.5
```

---

## ♿ Accessibility

### Minimum Standards
- Text contrast ratio: **4.5:1** (WCAG AA)
- Interactive target size: **44×44px** minimum
- Focus indicators: **2px outline** with offset
- Keyboard navigation: **Full support**

### Focus States
```css
outline: 2px solid #667eea;
outline-offset: 2px;
border-radius: inherit;
```

### Screen Reader Text
```css
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
}
```

---

## 📱 Responsive Design

### Mobile Adjustments (< 768px)

**Typography**
```css
Hero Title:  2rem (32px)  /* Down from 64px */
h1:          1.5rem
h2:          1.25rem
```

**Spacing**
```css
Container padding:  1rem
Card padding:       1.5rem  /* Down from 3rem */
Section spacing:    2rem    /* Down from 4rem */
```

**Layout**
```css
Features Grid:     1 column
Score Container:   Stacked (not side-by-side)
Progress Steps:    Hidden (show bar only)
```

---

## 🎯 Best Practices

### Do's ✅
- Use design tokens (CSS variables)
- Maintain consistent spacing
- Follow the type scale
- Use semantic HTML
- Add smooth transitions
- Test on multiple devices

### Don'ts ❌
- Don't use arbitrary values
- Don't mix px and rem inconsistently
- Don't skip hover states
- Don't forget focus indicators
- Don't use absolute positioning excessively
- Don't ignore mobile users

---

## 📐 Example Usage

### Creating a New Card
```html
<div class="glass-card" style="padding: var(--spacing-lg); border-radius: var(--radius-md);">
    <h3 style="font-size: 1.25rem; font-weight: 600; margin-bottom: var(--spacing-sm);">
        Card Title
    </h3>
    <p style="color: var(--clr-text-muted);">
        Card content goes here
    </p>
</div>
```

### Adding a Status Badge
```html
<span style="
    padding: 0.25rem 0.75rem;
    background: rgba(16, 185, 129, 0.2);
    color: var(--clr-success);
    border-radius: var(--radius-full);
    font-size: 0.875rem;
    font-weight: 600;
">
    🟢 Low Risk
</span>
```

---

## 🔄 Version History

**v1.0** - Initial release
- Complete design system
- All components defined
- Accessibility standards set
- Responsive specifications

---

**Last Updated**: January 29, 2026
**Maintained by**: PLAUGE Development Team
