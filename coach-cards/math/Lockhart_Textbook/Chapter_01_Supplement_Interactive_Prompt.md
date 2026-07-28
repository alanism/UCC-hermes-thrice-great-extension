# Chapter 1 Supplement: Interactive HTML Explainer — The Jungle and the Stones

> **Level:** 9-year-old  
> **Tech stack:** three.js (WebGL), d3.js, vanilla HTML/CSS/JS  
> **Prompt for:** Google AI Studio or any AI coding agent  
> **Target concept:** Counting, grouping, place value, and that base systems are human inventions

---

## The Prompt

```text
Build a single self-contained HTML file that teaches a 9-year-old about counting, grouping, and why different base systems work, using Paul Lockhart's playful "tribes" metaphor. The file must be completely self-contained (no external dependencies except CDN-loaded libraries). Use three.js for 3D interactive scenes and d3.js for any 2D data visualization.

## DESIGN PHILOSOPHY
- Lockhart's voice: "Arithmetic is the artful rearrangement of information"
- No jargon, no formulas. Talk about "handfuls", "grouping", "leftovers", "trading up"
- Bright, playful colors — think illustrated storybook meets interactive museum exhibit
- The child plays as a translator between imaginary tribes
- Everything is clickable, draggable, explorable

## SCENES (tab-navigated)

### SCENE 1: "The Perception Problem" — Why We Need Grouping
- A 3D (three.js) table scattered with ~40 colorful rocks/gems
- Text: "Can you tell how many rocks there are just by looking? No? That's the PERCEPTION PROBLEM!"
- Three buttons: [12 rocks] [24 rocks] [37 rocks] — each scatters a different number
- Each time, the child must guess, then click to reveal the count
- The "aha" moment: "Humans can only see up to about 5 things at once. We need to GROUP them!"

### SCENE 2: "The Hand People" — Grouping by Fives
- Rocks on a 3D table. The child clicks rocks to drag them into groups of 5.
- Each group of 5 glows and becomes a "handful" (a cluster with a hand-icon floating above it)
- A counter at the top shows: "You have [X] handfuls and [Y] leftovers"
- Text: "The Hand People group everything by FIVES. They count like this: thump (5), thump-thump (10)..."
- Let the child group up to 50 rocks, watching the handfuls stack up

### SCENE 3: "The Banana People" — Grouping by Fours
- Same rocks, but now they snap into groups of 4
- A different counter: "You have [X] bunches and [Y] leftovers"
- Text: "The Banana People group by FOURS. They say 'ba' for a bunch of four!"
- The child sees the SAME pile of rocks looks different counted in fours vs. fives
- A Fun Fact button: "There is nothing special about the number 10. We use it because we have 10 fingers!"

### SCENE 4: "The Tree People" — Grouping by Sevens
- Rocks group into 7s
- Text: "The Tree People group by SEVENS! For them, 70 is a beautiful round number."
- d3.js bar chart beside the 3D scene: compares how many groups each tribe makes for the same number
- Bar 1: Hand People groups of 5
- Bar 2: Banana People groups of 4
- Bar 3: Tree People groups of 7
- This visual comparison is the key insight — different groupings, same total

### SCENE 5: "The Trading Game" — Place Value as Cashing In
- The core interactive. A 3D abacus with two grooves (ONES and TENS).
- The child clicks to add individual rocks to the ONES groove
- A "CASH IN" button: when 10 rocks are in ONES, it animates them disappearing and 1 rock appearing in TENS
- Text: "10 ones = 1 ten! When you have 10 rocks in the ones groove, you trade them up!"
- Challenges appear: "Can you make the number 37?" (child must figure out 3 tens + 7 ones)
- A counter shows: "37 = [3] tens + [7] ones"
- Level 2: Three grooves (ONES, TENS, HUNDREDS). "Make 142!"
- d3.js overlay shows the digit breakdown as a horizontal stacked bar

### SCENE 6: "Design Your Own Base" — The Sandbox
- The child picks a base number (4, 5, 6, 7, 8, 10, 12) using a slider
- The abacus automatically reconfigures: grooves change labels (e.g., "ONES", "FIVES", "TWENTY-FIVES" for base-5)
- A number input: "Show me 37 in base [X]"
- The abacus animates showing the correct grouping
- Text: "All bases work the same way. You just trade up at different numbers!"

## THREE.JS REQUIREMENTS
- Use CDN script tag for three.js
- Include OrbitControls for rotating the rock/gem table scenes
- Use MeshPhysicalMaterial for the rocks (sparkly, gem-like, different colors)
- PointLight + AmbientLight for warm lighting
- Smooth camera transitions between scenes
- Rocks should be randomly shaped (slightly irregular spheres or dodecahedra)
- Grouping animation: rocks smoothly slide together into clusters

## D3.JS REQUIREMENTS
- Use CDN script tag for d3.js
- Scene 4: Bar chart comparing tribe groupings for the same total
- Scene 5: Stacked bar showing digit breakdown (ones, tens, hundreds)
- Scene 5: Animated transition when trading up (d3 transitions)
- Scene 6: Data display for the custom base system

## UI/UX REQUIREMENTS
- Full-screen, responsive (iPad-friendly)
- Top nav: [Perception Problem] [Hand People] [Banana People] [Tree People] [Trading Game] [Sandbox]
- Each nav item is a colorful rounded pill button
- Current scene highlighted
- A Lockhart character (stick figure with glasses and wild hair) in the corner that occasionally says things like:
  - "The numbers themselves don't care about your silly pet names for them!"
  - "Arithmetic is just the artful rearrangement of information!"
  - "There's nothing special about ten. It's just an accident of our fingers!"
- Clicking on individual rocks shows a tooltip: "I'm just information!"
- A "Reset" button to return to Scene 1

## INTERACTIONS
- Click to select and drag rocks into groups (Scene 2-4)
- Click to add rocks to abacus grooves (Scene 5)
- Slider to choose base number (Scene 6)
- "CASH IN" button for trading up (Scene 5)
- Drag to rotate 3D scenes (OrbitControls)
- Hover effects: rocks glow slightly

## ACCESSIBILITY
- All text has good contrast
- Lockhart quotes in a distinct styled box
- Large click targets for children
- Simple language throughout

## PERFORMANCE
- Target 60fps on iPad and laptop
- Pool objects — cap at ~80 rocks at a time
- Particle effects in background (optional)

## THE THREE LOCKHART QUOTES (display at key moments)
1. "The artful rearrangement of numerical information — in particular, the translation among different grouping sizes — is the soul and essence of arithmetic."
2. "That's what numbers are, really: information. The replacement of caribou by rocks doesn't change the information."
3. "There is nothing sacrosanct about this Hindu-Arabic symbolic encoding. Six is six. The numbers themselves don't care about your silly pet names for them."

Output the complete, working HTML file. Do not use any build tools, bundlers, or file dependencies. Everything must load from CDN script tags.
```

---

## How to Use This Prompt

1. Copy the entire prompt above
2. Paste it into **Google AI Studio** (or Claude, ChatGPT, or any AI coding agent)
3. Ask it to generate the single HTML file
4. Save the output as `Chapter_01_Interactive_Explainer.html`
5. Open in a browser — no server needed

---

## What the Explainer Teaches (Learning Objectives)

| Scene | Concept | Lockhart Metaphor |
|-------|---------|-------------------|
| 1 | The perception problem — why we need grouping | Humans can only see ~5 at once |
| 2 | Grouping by fives (base-5) | Hand People, "thumps" and "claps" |
| 3 | Grouping by fours (base-4) | Banana People, "ba" and "bana" |
| 4 | Different bases, same number | Bar chart comparison makes it visible |
| 5 | Place value as trading up | "Cash in 10 ones for 1 ten" |
| 6 | Any base works — design your own | Sandbox mode for creative exploration |

---

## Tech Stack Notes

- **three.js** (`https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js`)
- **OrbitControls** (`https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js`)
- **d3.js** (`https://cdnjs.cloudflare.com/ajax/libs/d3/6.7.0/d3.min.js`)
- All CDN-loaded — no build step, no bundler
