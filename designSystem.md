# HRMS Design System Reference

## 1. Core Aesthetics & Layout Rules
*   **Theme**: Light mode only.
*   **Design Style**: Flat Design (No Shadows) except for subtle hover states on cards.
*   **Container Bases**:
    *   Main Content Container: `#FFFFFF` (White)
    *   Sidebar Base: `#F5F7FA` (Cool Gray)
*   **Layout Separation**: Avoid heavy borders. Use subtle borders (`border-gray-200` / `#E5E7EB`) or background surface color variations for visual separation.
*   **Border Radius**: Container corners should be `rounded-lg` or `rounded-xl` (base `radius: 0.5rem` / `8px`).

---

## 2. Color System

### A. Brand Colors
*   **Primary Orange (`#FF7700`)**: Core brand accent.
    *   *Default*: `#FF7700` (Tailwind Class: `bg-primary` or custom class)
    *   *Hover / Pressed*: Slight dark/pressed states (e.g., hover state color `#E06600`)
*   **Secondary Blue (`text-blue-700`)**: Supplementary accents, links, and highlights.
    *   *Text Class*: `text-blue-700`
    *   *Base Subtle Blue*: `bg-blue-50` / `bg-blue-100`
    *   *Blue Gradient*: `bg-linear-to-b from-blue-100 to-blue` (tailwind)

### B. Neutrals (Grays 100 to 900)
Used for backgrounds, borders, text, and structure.
*   `gray-50` (`#F9FAFB`): Secondary backgrounds / surfaces.
*   `gray-100` (`#F3F4F6`): Neutral borders, disabled states.
*   `gray-200` (`#E5E7EB`): Primary layout borders.
*   `gray-500` (`#6B7280`): Muted meta text, placeholder text.
*   `gray-900` (`#111827`): Primary text / headers.

### C. Semantic Colors
Use both subtle background tints and dark text for messages, statuses, and badges:
*   **Success (Green)**: `bg-green-50` with `text-green-700`
*   **Warning (Amber/Yellow)**: `bg-amber-50` with `text-amber-700`
*   **Error/Destructive (Red)**: `bg-red-50` with `text-red-700`
*   **Info (Blue)**: `bg-blue-50` with `text-blue-700`

---

## 3. Typography Scale
*   **Primary Font**: `Instrument Sans` (sans-serif)
*   **Weights**: Regular (400), Medium (500), SemiBold (600), Bold (700)

| UI Element | Size (px) | Tailwind Utility | Description / Usage |
| :--- | :--- | :--- | :--- |
| **Micro / Caption** | 10px | `text-2xs` | Inline tags, micro metadata, superscript |
| **Detail / Small Body** | 12px | `text-xs` | Dense table cells, form helper text, side-labels |
| **Body (Base)** | 14px | `text-sm` | Default page text, input values, primary list text |
| **Lead / Subheading** | 16px | `text-base` | Section titles, sidebar main items, card headers |
| **Section Title** | 20px | `text-xl` | Small section headers, dashboard card headers |
| **Page Title** | 24px | `text-2xl` | Main page titles, key metric numbers |
| **Hero Title** | 28px | `text-3xl` | Primary dashboard metrics, modal alert titles |
| **Display Title** | 32px | `text-4xl` | Large landing statistics, splash screens |

---

## 4. UI Components & Iconography

### A. Badges & Status Indicators
*   Clean, pill-shaped tags (`rounded-full`).
*   Always use high-contrast combinations (e.g., subtle bg + dark text).

### B. Icons
*   **Primary Icon Set**: `@untitledui/icons`
*   **Secondary / Fallback**: `lucide-react`
*   Keep icon sizing standard (`w-5 h-5`).

---

## 5. Spacing & Density
*   **Spacing**: Use standard Tailwind spacing scales (`p-*`, `m-*`, `gap-*`).
*   **Density Strategy**: Condensed layouts.
    *   Prefer `p-3` over `p-4` for components.
    *   Prefer `gap-2` over `gap-4` for element grids.
    *   Purpose: Maximize information density and dashboard scannability.