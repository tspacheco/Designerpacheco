---
name: Dra. Angélica Lauermann Gomes
description: A conversa com a Dra. — her practice as the WhatsApp Business chat she already holds with patients, in her own forest, sage and brass.
colors:
  floresta: "#1D3024"
  floresta-2: "#284234"
  floresta-3: "#355440"
  latao: "#B08A4A"
  latao-texto: "#7A5A26"
  latao-sobre-floresta: "#E4CB93"
  latao-marcador: "#D6B774"
  folha: "#F1F4EC"
  folha-2: "#BCC9B5"
  parede: "#E2E8D8"
  parede-risco: "#C8D2BB"
  bolha: "#FFFFFF"
  papel: "#F7F9F3"
  tinta: "#16211A"
  tinta-2: "#485546"
  tinta-3: "#667264"
  linha: "#D3DBC9"
  aviso: "#F2EAD4"
  aviso-texto: "#5B4520"
  link: "#1F5E3D"
  selecao: "#CFE0C2"
typography:
  display:
    fontFamily: "Funnel Display, Segoe UI, system-ui, sans-serif"
    fontSize: "clamp(1.45rem, 5.6vw, 1.9rem)"
    fontWeight: 800
    lineHeight: 1.05
    letterSpacing: "-0.02em"
  headline:
    fontFamily: "Funnel Display, Segoe UI, system-ui, sans-serif"
    fontSize: "1.5rem"
    fontWeight: 800
    lineHeight: 1.1
    letterSpacing: "-0.015em"
  title:
    fontFamily: "Funnel Display, Segoe UI, system-ui, sans-serif"
    fontSize: "19.5px"
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "-0.005em"
  name:
    fontFamily: "Funnel Display, Segoe UI, system-ui, sans-serif"
    fontSize: "16.5px"
    fontWeight: 700
    lineHeight: 1.2
  body:
    fontFamily: "Funnel Sans, Segoe UI, system-ui, -apple-system, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.5
    fontFeature: "tnum"
  body-small:
    fontFamily: "Funnel Sans, Segoe UI, system-ui, -apple-system, sans-serif"
    fontSize: "14.5px"
    fontWeight: 400
    lineHeight: 1.4
  label:
    fontFamily: "Funnel Sans, Segoe UI, system-ui, -apple-system, sans-serif"
    fontSize: "12.5px"
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: "0.02em"
  meta:
    fontFamily: "Funnel Sans, Segoe UI, system-ui, -apple-system, sans-serif"
    fontSize: "11.5px"
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: "0.05em"
  monogram:
    fontFamily: "Pinyon Script, Snell Roundhand, cursive"
    fontSize: "26px"
    fontWeight: 400
rounded:
  tail: "4px"
  pill-notice: "8px"
  card: "10px"
  photo-inner: "11px"
  sheet-note: "12px"
  bubble: "14px"
  portrait: "16px"
  field: "26px"
  full: "99px"
spacing:
  bubble-gap: "0.35rem"
  turn-gap: "1.4rem"
  bubble-pad: "0.55rem 0.8rem 0.5rem"
  photo-pad: "4px"
  row-pad: "0.7rem 0.9rem"
  thread-inline: "clamp(0.8rem, 3vw, 2rem)"
  thread-max: "820px"
components:
  bubble-her:
    backgroundColor: "{colors.floresta}"
    textColor: "{colors.folha}"
    typography: "{typography.body}"
    rounded: "{rounded.bubble}"
    padding: "{spacing.bubble-pad}"
  bubble-patient:
    backgroundColor: "{colors.bolha}"
    textColor: "{colors.floresta}"
    typography: "{typography.title}"
    rounded: "{rounded.bubble}"
    padding: "{spacing.bubble-pad}"
  date-pill:
    backgroundColor: "{colors.papel}"
    textColor: "{colors.tinta-2}"
    rounded: "{rounded.pill-notice}"
    padding: "0.3rem 0.75rem"
  system-notice:
    backgroundColor: "{colors.aviso}"
    textColor: "{colors.aviso-texto}"
    rounded: "{rounded.card}"
    padding: "0.5rem 0.9rem"
  chip-quick-reply:
    backgroundColor: "{colors.bolha}"
    textColor: "{colors.floresta}"
    rounded: "{rounded.full}"
    padding: "0.45rem 0.9rem"
    height: "40px"
  list-message-header:
    backgroundColor: "{colors.floresta}"
    textColor: "{colors.folha}"
    padding: "0.7rem 0.9rem 0.55rem"
  list-message-row:
    backgroundColor: "{colors.bolha}"
    textColor: "{colors.tinta}"
    padding: "{spacing.row-pad}"
  link-card:
    backgroundColor: "{colors.floresta-2}"
    textColor: "{colors.folha}"
    rounded: "{rounded.card}"
    padding: "0.6rem 0.75rem 0.65rem"
  composer-field:
    backgroundColor: "{colors.bolha}"
    textColor: "{colors.tinta}"
    rounded: "{rounded.field}"
    padding: "0.35rem 0.5rem 0.35rem 1rem"
  composer-send:
    backgroundColor: "{colors.floresta}"
    textColor: "{colors.folha}"
    rounded: "{rounded.full}"
    size: "54px"
  composer-send-hover:
    backgroundColor: "{colors.floresta-3}"
  contact-sheet-button:
    backgroundColor: "{colors.floresta}"
    textColor: "{colors.folha}"
    rounded: "{rounded.bubble}"
    height: "54px"
  contact-sheet-button-hover:
    backgroundColor: "{colors.floresta-3}"
---

# Design System: Dra. Angélica Lauermann Gomes

## Overview

**Creative North Star: "A conversa com a Dra."**

The whole surface is a WhatsApp Business chat held by the dentist herself, rebuilt in her identity rather than the messenger's. Her contact header proves who she is, her forest bubbles answer what patients ask, the patient's white bubbles are the questions (and the section headings), and the composer at the bottom is the call to action, already written for the topic the visitor chose. Nothing on the page is a "website section"; everything is a message, a system notice, a list message, a link preview or the contact-info sheet.

Density is chat density: tight bubble gaps inside a turn, a clear breath between turns, one reading column capped at 820px. The material is flat paper on a pale sage wallpaper with an authored line-doodle pattern (tooth, sparkle, brush, drop, smile, floss mark); depth is only the hairline lift a messenger gives its bubbles. Her colours come from her façade, sign and monogram: deep forest green, warm brass, off-white. It refuses the dental-category default of a stock-smile hero, tooth-icon service cards and a floating "Agende" button.

**Key Characteristics:**
- Every block is a chat primitive: bubble, photo bubble, album, link preview, list message, quick-reply chip, date pill, system notice, composer, contact sheet.
- Her voice is forest on sage; the patient's voice is white. Speaker is carried by side, colour and tail together, never colour alone.
- Brass is the accent of trust marks: read ticks, stars, list markers, focus rings, caret, the send pulse.
- One entrance moment, then everything is at rest.
- Mobile is one column with a fixed composer; desktop at 1024px becomes two panes, contact sheet left, conversation right.

## Colors

A narrow forest-and-brass palette on sage paper, drawn from her façade, sign and monogram; no WhatsApp green anywhere.

### Primary
- **Consultório Forest** (floresta): her bubbles, the sticky contact header, the list-message header, the send button, the contact-sheet button, the desktop top band and the browser theme colour. It is the dentist's voice.
- **Forest Lamp** (floresta-2): link-preview cards nested inside her bubbles (Google rating, map).
- **Forest Moss** (floresta-3): hover state of forest buttons, photo placeholders behind images, scrollbar thumb.

### Secondary
- **Sign Brass** (latao): read ticks, stars, focus outline, caret, the composer focus border, the send-button pulse and the question highlight ring, the monogram tooth outline. Decorative and non-text only.
- **Brass Ink** (latao-texto): brass at text contrast on light surfaces: the CRO number, chip icons, list-row chevrons.
- **Brass on Forest** (latao-sobre-floresta): links inside her bubbles.
- **Brass Marker** (latao-marcador): ordered and bullet list markers inside her bubbles.

### Neutral
- **Leaf** (folha): text on forest surfaces.
- **Pale Leaf** (folha-2): secondary text on forest (header subtitle, card domain line), typing dots.
- **Sage Wallpaper** (parede): the conversation background and composer fade.
- **Doodle Line** (parede-risco): stroke of the wallpaper doodle pattern; nothing else.
- **Bubble White** (bolha): patient bubbles, chips, list message body, composer field, contact sheet.
- **Notice Paper** (papel): the profile card at the top of the thread and the date pill.
- **Ink** (tinta), **Ink 2** (tinta-2), **Ink 3** (tinta-3): body text, secondary text, timestamps/labels on light surfaces.
- **Hairline** (linha): dividers between list rows and contact-sheet rows, desktop pane border.
- **Notice Cream** (aviso) with **Notice Ink** (aviso-texto): the centered system notice.
- **Link Green** (link): default links on light surfaces.

### Named Rules
**The Not-WhatsApp Rule.** The grammar is WhatsApp Business; the colours are hers. WhatsApp's own greens and logo never appear; the send icon is a paper plane.

**The Two Voices Rule.** Forest bubble on the left with the top-left tail is her; white bubble on the right with the top-right tail and brass ticks is the patient. Never swap, never add a third bubble colour.

## Typography

**Display Font:** Funnel Display (with Segoe UI, system-ui)
**Body Font:** Funnel Sans (with Segoe UI, system-ui, -apple-system)
**Script:** Pinyon Script, only for the AL monogram

**Character:** A contemporary grotesk pair that reads as a well-made app, not a clinic brochure; Funnel Display carries names and questions, Funnel Sans carries her messages at a size older patients can read.

### Hierarchy
- **Display** (800, clamp(1.45rem, 5.6vw, 1.9rem), 1.05): her name, the single h1, in the profile card at the top of the thread.
- **Headline** (800, 1.5rem, 1.1): the contact sheet title.
- **Title** (600, 19.5px, 1.3): the patient's questions, which are the h2 of each topic.
- **Name** (700, 16.5px, 1.2): her name in the sticky header and the monogram caption.
- **Body** (400, 17px, 1.5, tabular numerals): every message. 17px is the floor for body text.
- **Body small** (400, 14.5px, 1.4): list-row descriptions, profession line, card lines.
- **Label** (12.5px, +0.02em): field captions in the contact sheet, date pill, notices.
- **Meta** (11.5px, +0.05em): timestamps and the composer caption.

### Named Rules
**The Script-Is-a-Signature Rule.** Pinyon Script exists only inside the AL monogram. Never set a heading, quote or name in it.

**The Questions-Are-Headings Rule.** Topic headings are the patient's own questions in a white bubble; no labels above them, no eyebrows.

## Layout

A single chat thread, max 820px, centered, with inline padding clamp(0.8rem, 3vw, 2rem). Inside a turn, bubbles stack at 0.35rem; each new patient question opens a turn with 1.4rem above it. Her bubbles are capped at min(78%, 520px) (88% under 420px), photo bubbles at 360px, albums at 420px (2-up square grid, 4px gutter), list messages at min(92%, 520px). The sticky header sits on top; scroll offsets are 84px so answers land below it.

Mobile (below 1024px): one column; the contact sheet follows the conversation as a white block; the composer is fixed to the bottom with a sage fade and safe-area padding, and the thread reserves its height.

Desktop (1024px and up): two panes in a 1380px frame, contact sheet left (minmax(340px, 400px), sticky, full height, own scroll) and conversation right; the composer becomes sticky at the bottom of the right pane; a forest band 128px tall runs behind the top of the page on a deeper sage (#CFD8C4 in source) body. At 1440px the frame drops 18px from the top.

## Elevation & Depth

Flat messenger paper. Depth is the one-pixel lift every chat bubble carries plus two functional shadows for things that float over the thread: the sticky header and the composer.

### Shadow Vocabulary
- **Bubble lift** (`box-shadow: 0 1px 1px rgba(22,33,26,.1)`; .06 to .08 on pills and notices): every bubble, pill and profile card.
- **Header drop** (`box-shadow: 0 6px 18px -12px rgba(9,20,13,.7)`): sticky contact header only.
- **Composer float** (`0 2px 10px -4px rgba(22,33,26,.35)` on the field, `0 6px 16px -8px rgba(9,20,13,.8)` on send): the composer only.
- **Frame** (`0 18px 40px -24px rgba(9,20,13,.55)`): the desktop app frame.

### Named Rules
**The Hairline Lift Rule.** Content surfaces never rise above a 1px bubble shadow. Bigger shadows belong only to what floats: header, composer, desktop frame.

## Shapes

Rounded rectangles with a messenger tail: bubbles are 14px with the corner nearest the speaker cut to 4px on the first bubble of a run; follow-on bubbles round fully. Photos inside bubbles sit in a 4px frame with 11px inner corners. Chips and the send button are full pills and circles; the composer field is a 26px capsule. Cards and notices use 8 to 12px; the contact portrait 16px. Borders are rare: 1.5px on chips and the composer (transparent until focus), 1px hairlines between rows. Icons are inline line SVG, 1.6 to 2px stroke, round caps.

## Components

### Bubbles
Her bubble: forest, leaf text, left, top-left tail. Patient bubble: white, right, top-right tail, carries the h2 question and brass double ticks. Photo bubble and 2-up album with a gradient caption strip. Link preview (Google rating, map) nests a forest-2 card inside her bubble, with the domain line in pale leaf.

### Chips (quick replies)
- **Style:** white pill, forest text 15.5px/500, 1.5px sage border, brass-ink line icon, 40px minimum height.
- **State:** hover darkens the border to forest; active scales to 0.97. Tapping scrolls to her answer, flashes a brass ring on the question (1.6s) and rewrites the composer.

### List message (treatments)
White bubble with a forest header line; rows are full-width buttons (16.5px/600 title, 14.5px description, brass-ink chevron) divided by hairlines. Hover tints the row; the selected row gets a sage tint, forest title, `aria-pressed`, and its chevron redraws as a brass check.

### Composer (the primary CTA)
- **Style:** white 26px capsule with a meta caption ("Mensagem para a Dra. Angélica · pelo WhatsApp") over a 16.5px textarea that grows to about four lines; 54px forest circle send button with a paper-plane icon.
- **Focus:** brass border on the capsule, brass caret; global focus is a 2.5px brass outline, 2px offset.
- **Behaviour:** the text is pre-written; chips and treatment rows retype it (2 characters every 14ms), then the send button pulses a brass ring once. Send opens wa.me with the exact text; Enter sends.

### System notices
Date pill ("Hoje") on notice paper, and a cream notice with a line glyph for instructions. Centered, never full width.

### Navigation (contact header)
Sticky forest bar: 42px round avatar with a brass hairline ring, name and "Cirurgiã-Dentista · CRO-SP 139651" (which reads "digitando…" during the entrance), round 42px icon buttons for map and contact info (the latter hidden on desktop, where the sheet is always visible).

### Contact sheet ("Dados do contato")
White panel: AL monogram (brass tooth outline, script letters), headline, 4:3 portrait, "Recado" note with her bio, a hairline-divided list of fields (icon, label, selectable value) for CRO, Google rating, address, phone, Instagram and hours, then a full-width 54px forest "Conversar no WhatsApp" button, then legal lines.

### Motion
One entrance, first viewport only: the typing indicator (three pale-leaf dots on a forest bubble) precedes each of the first messages, which arrive with a 0.6s rise, blur-to-sharp and fade on `cubic-bezier(.16,1,.3,1)`. Afterwards everything is visible at rest; the only other motion is the composer retype, the send pulse, the question highlight and 0.25s hover transitions. Under `prefers-reduced-motion` all animation and transitions are off, entrance messages show immediately, the typing indicator is hidden, and the composer text swaps without typing.

## Do's and Don'ts

### Do:
- **Do** express every new piece of content as a chat primitive: her bubble, patient question bubble, photo bubble, list message, link preview, chip, pill or notice.
- **Do** keep her voice forest (floresta) and the patient's white (bolha), with the tail on the speaker's side.
- **Do** route every call to action into the composer text or the contact sheet's WhatsApp button, both opening wa.me with a written message.
- **Do** keep brass (latao) for trust marks and state: ticks, stars, markers, focus, caret, pulse.
- **Do** keep body text at 17px and tap targets at 40px or more.
- **Do** keep the entrance as the only choreographed moment and honour reduced motion exactly as above.

### Don't:
- **Don't** use WhatsApp's own green or logo anywhere.
- **Don't** add a floating "Agende" button, a booking calendar or any CTA competing with the composer.
- **Don't** show prices, discounts, promotions, result promises or review quotes.
- **Don't** show patient mouths, smiles or before/after photos without written authorisation.
- **Don't** set anything but the AL monogram in Pinyon Script.
- **Don't** use tooth-icon service cards or a stock-smile hero; treatments live in the list message.
- **Don't** lift content surfaces above the 1px bubble shadow.
