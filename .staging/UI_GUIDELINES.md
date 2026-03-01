# UI/UX Design Guidelines for CustomTkinter

## 1. Minimalist & Modern Aesthetics
- **Color Palette**: Use a cohesive Dark/Light mode theme. For dark mode, use deep grays (`#2b2b2b`, `#1e1e1e`) instead of harsh black. Use a primary accent color (e.g., modern blue `#1f6aa5` or an energetic green `#2fa572`) for primary actions (like "Show Answer", "Extract", or "Correct").
- **Typography**: Use clean, modern, sans-serif fonts. Increase font sizes significantly for flashcard words (e.g., 36px+ bold) so they are immediately readable. Secondary text (definitions, examples) should be smaller but legible (e.g., 14px-18px) and slightly dimmed to establish visual hierarchy.

## 2. Layout & Spacing
- **Whitespace is King**: Do not cram UI elements together. Use generous padding (e.g., `padx=20, pady=20`) around main containers and between buttons.
- **Card-Based Design**: For the flashcard view, visually emulate a physical card using a distinct frame with a slightly lighter background color than the main window, complete with subtle corner radiuses (`corner_radius=15`).
- **Sidebar Navigation**: Keep the left sidebar clean. Use clear, large buttons for navigation (`Dashboard`, `Add Word`, `Review Queue`, `AI Extract`). Highlight the active tab.

## 3. Interaction & Affordance
- **Clear Call to Actions (CTAs)**: Primary buttons ("Show Answer") must stand out immediately. Secondary buttons ("Skip", "Cancel") should be more subtle (e.g., border-only or muted colors).
- **Leitner Buttons**: When the answer is revealed, "Correct" (Green) and "Incorrect" (Red) buttons should be large, symmetrically placed, and impossible to miss.
- **Feedback**: After an action (like adding a word or finishing a review session), provide subtle visual feedback (a temporary label or progress bar update), rather than disruptive popup alerts, unless an error occurs.

