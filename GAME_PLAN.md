# Story Game Architecture Plan

## Overview
A **scene-based narrative game** where the player moves through a story via choices, actions, and consequences. Each scene is self-contained but linked to others through a game state.

## Core Architecture

```
Game Engine (handles flow)
    ↓
Scene System (each scene is a story moment)
    ↓
Game State (tracks what happened, what player has)
    ↓
Visual Rendering (YOUR CUSTOM DRAWINGS HERE)
```

## File Structure (Recommended)

```
story-game/
├── index.html          # Main entry - loads everything
├── js/
│   ├── engine.js       # Game engine (scene manager, state)
│   ├── story.js        # Story data (all scenes, choices, outcomes)
│   └── renderer.js     # How to draw each scene (you customize)
├── css/
│   └── style.css       # Styling
└── art/
    ├── characters/     # Your character drawings
    ├── backgrounds/    # Your backgrounds
    └── items/          # Collectibles, objects
```

## How It Works: Flow

```
1. INTRO SCENE
   "You find a sad duck by the pond"
   [Text + YOUR DRAWING of kid + sad duck]
   
2. CHOICE SCENE
   "What do you do?"
   [Button: "Give it food"]  [Button: "Play with it"]
   
3. ACTION SCENE (based on choice)
   If "Give food": "Find berries in the forest"
      [Mini-task: tap bushes to collect 3 berries]
   If "Play": "Play a game with the duck"
      [Mini-game: match sounds]
   
4. OUTCOME SCENE
   "The duck is happy! 🦆"
   [Congratulations + YOUR DRAWING of happy duck]
   
5. NEXT SCENE
   Story continues...
```

## Game State Example

```javascript
state = {
  currentScene: 'intro',
  inventory: ['berry', 'leaf'],
  friendsMet: ['duck'],
  choices: {
    duckAction: 'feedIt'  // tracks what player chose
  },
  unlockedScenes: ['intro', 'duckChoice', 'duckFeed']
}
```

The game checks state to decide what to show next.

## Scene Types

### 1. **Narrative Scene** (Tell story)
```
Shows: Text + YOUR ART
Does: Displays story moment, waits for "Next" button
Leads to: Next scene OR choice scene
```

### 2. **Choice Scene** (Player decides)
```
Shows: Question + buttons
Does: Waits for player to pick an option
Leads to: Different scenes based on choice
```

### 3. **Action Scene** (Player does something)
```
Shows: Task description + interactive elements
Does: Player collects items, solves puzzle, taps targets
Leads to: Outcome scene when task completes
```

### 4. **Outcome Scene** (Show result)
```
Shows: Result of player's choice/action + YOUR ART
Does: Celebrates or explains consequence
Leads to: Next story beat
```

## Story Data Structure

```javascript
const STORY = {
  intro: {
    type: 'narrative',
    text: "You find a sad duck by the pond...",
    art: 'duckSad',  // YOUR DRAWING KEY
    next: 'duckChoice'
  },
  
  duckChoice: {
    type: 'choice',
    text: "What do you do?",
    art: 'duckSad',
    choices: [
      { text: "Give it food", leads: 'duckFeed' },
      { text: "Play with it", leads: 'duckPlay' }
    ]
  },
  
  duckFeed: {
    type: 'action',
    text: "Find 3 berries in the forest",
    task: 'collect',
    goal: 3,
    item: 'berry',
    art: 'forest',
    onComplete: 'duckHappy'
  },
  
  duckHappy: {
    type: 'narrative',
    text: "The duck is so happy now!",
    art: 'duckHappy',  // YOUR HAPPY DRAWING
    next: 'scene2intro'
  }
}
```

## Where YOUR Art Goes

Mark placeholders in the renderer:
```javascript
// renderer.js
function drawScene(scene, state) {
  if (scene.art === 'duckSad') {
    // YOUR CUSTOM DRAWING HERE
    // Replace with: <img>, <canvas>, or SVG
    drawCustomArt('duckSad');
  }
}
```

## Example Game Flow (For Your Reference)

**"Help the Forest Friends" - 5 scenes, ~10 min playtime**

```
SCENE 1: Intro
  "You're walking in the forest..."
  → Next

SCENE 2: Meet Duck
  "A sad duck is by the pond"
  → Choice: Help it? Yes/No

SCENE 3a (if Yes): Collect Berries
  "Find 3 berries" [tap 6 bushes, 3 have berries]
  → Collect 3 → Continue

SCENE 3b (if No): Come Back Later
  "The duck looks at you sadly..."
  → Go to another scene

SCENE 4: Duck Happy
  "Duck eats berries, is so happy!"
  → Next

SCENE 5: Meet Rabbit
  "A rabbit hops over..."
  → New choice...

SCENE 6: Outcome / Win
  "You helped all the forest friends!"
  → Play again?
```

## Implementation Steps

1. **Build engine.js**
   - Scene manager (load scene by ID)
   - State tracker (what player did)
   - Choice handler (process player clicks)

2. **Define story.js**
   - All scenes as data (not code)
   - Choices and outcomes
   - Easy to modify/extend

3. **Create renderer.js**
   - Draw current scene
   - Show text
   - Place YOUR ART here (as placeholders)

4. **Add your visuals**
   - Draw the kid character
   - Draw each animal/scene
   - Drop them into the renderer

5. **Connect it**
   - index.html loads all files
   - Engine ties story to visuals
   - Done!

## Key Design Principle

**Separate data from display:**
- Story lives in `story.js` (easy to edit, shows structure)
- Visuals live in `renderer.js` (easy to customize)
- Engine stays generic (works for any story)

This way, you can change the story or art without touching the engine.

---

## Next Steps

1. I'll build a **working prototype** showing this in action
2. You'll see how scenes flow, how choices work, how state changes
3. You'll see exactly where to drop YOUR drawings
4. You modify the story and add art
