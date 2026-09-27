#!/usr/bin/env python3
"""
Generate ASHENFALL_STORY_IMPLEMENTATION_BLUEPRINT.md
A master technical and creative design blueprint for implementing the Ashenfall story in Minecraft.
"""

import os

blueprint_content = """# ASHENFALL: TECHNICAL & NARRATIVE IMPLEMENTATION BLUEPRINT
### *Translating the Epic of the Tenth Scion into Playable Minecraft Systems*

---

> *"A story in Minecraft cannot be told through twenty-minute unskippable cutscenes or walls of forced exposition.*  
> *It must be told through the soil. Through the rust on an iron gear. Through the stained glass with the scratched-out face. Through the desperate inscription on the sole of a drowned man's boot.*  
> *The player must not merely read the story—they must exhume it."*  
> — **Design Philosophy of the Ashenfall Team**

---

## TABLE OF CONTENTS
1. [The Narrative Medium: Philosophy of Environmental Game Design](#1-the-narrative-medium-philosophy-of-environmental-game-design)
2. [The Finite World & The Veil of Salt (World Border Architecture)](#2-the-finite-world--the-veil-of-salt-world-border-architecture)
3. [Architectural Archaeology: Environmental Storytelling Without Dialogue](#3-architectural-archaeology-environmental-storytelling-without-dialogue)
4. [The FromSoftware Item Lore System (KubeJS Tooltip Engine)](#4-the-fromsoftware-item-lore-system-kubejs-tooltip-engine)
5. [The Living World: Dynamic NPC Gossip & The 5 Wandering Questlines](#5-the-living-world-dynamic-npc-gossip--the-5-wandering-questlines)
6. [Cinematic Boss Staging & Phase Choreography](#6-cinematic-boss-staging--phase-choreography)
7. [The Resonance Stelae: In-Game Interactive Lore Markers](#7-the-resonance-stelae-in-game-interactive-lore-markers)
8. [The Crucible Altar: Executing the Four Dynamic Endings](#8-the-crucible-altar-executing-the-four-dynamic-endings)
9. [Mod Synergy Matrix: How Each Mod Serves the Story](#9-mod-synergy-matrix-how-each-mod-serves-the-story)
10. [Implementation Roadmap: Step-by-Step Production Plan](#10-implementation-roadmap-step-by-step-production-plan)

---

## 1. THE NARRATIVE MEDIUM: PHILOSOPHY OF ENVIRONMENTAL GAME DESIGN

In open-world masterpieces like *Elden Ring*, *Dark Souls*, and *Shadow of the Colossus*, lore is not delivered via linear quest logs that tell the player where to go with floating compass markers. The world itself is a crime scene, and the player is a forensic archaeologist piecing together what happened before they arrived.

To implement the **Cixin Liu 10-dimensional collapse** and the **George R.R. Martin dynastic fall** in Minecraft, we establish four core design rules:

```
┌────────────────────────────────────────────────────────────────────────┐
│                      THE FOUR CARDINAL NARRATIVE RULES                 │
├────────────────────────────────────────────────────────────────────────┤
│ 1. SHOW BEFORE TELLING: If a player can deduce a story point by seeing │
│    a pipe connecting a factory to a dragon's ribcage, write NO text.  │
│                                                                        │
│ 2. REWARD CURIOSITY: Every secret room, drowned cellar, and mountain   │
│    crag must contain an item with an inscription that adds a piece to  │
│    the cosmic puzzle.                                                  │
│                                                                        │
│ 3. GROUNDED MARTIAL COMBAT: The player possesses 20 Hearts (40 HP)     │
│    because they are the Tenth Scion, but combat remains strict Vanilla:│
│    tactical spacing, shield timing, sweeping strikes, and criticals.   │
│                                                                        │
│ 4. PERMANENT CAUSALITY: Decisions, boss kills, and the chosen ending   │
│    must physically alter the world's sky, health, and terrain.         │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. THE FINITE WORLD & THE VEIL OF SALT (WORLD BORDER ARCHITECTURE)

### The Lore Rationale
When the higher dimensions collapsed on the Night of Nine Sounds, the universe did not remain infinite. Ashenfall was crushed into a finite, three-dimensional continental sanctuary floating inside an unravelled cosmic void. Beyond its borders lies **The Veil of Salt**—the ragged perimeter where the laws of three-dimensional physics break down into unmade nothingness.

### Technical Implementation

#### A. Hard Continental Bounding
* **Border Diameter:** Set to **8,000 x 8,000 blocks** (-4,000 to +4,000 in both X and Z axes, centered at `0, 0`).
* **Why 8,000 blocks?**
  1. *Exploration Density:* 64 square kilometers is large enough to contain all Nine Nations, massive Create rail networks, oceanic bays, and mountain ranges, but dense enough that every journey feels meaningful.
  2. *Distant Horizons Synergy:* The entire 8,000 x 8,000 region can have its LODs (Level of Detail) pre-generated or cached smoothly without infinite disk bloat or memory leaks. A player standing on the Solitary Spine summit can see the distant smoking chimneys of Vantyra and the glowing crater of the Caldera across the continent.
  3. *Zero World Drift:* Prevents players from wandering into generic, empty vanilla generation 20,000 blocks away that lacks custom landmarks.

#### B. The KubeJS "Veil of Salt" Perimeter Handler
In `pack/overrides/kubejs/server_scripts/world_border.js`:
```javascript
// =============================================================================
// ASHENFALL — The Veil of Salt Perimeter Controller
// =============================================================================

ServerEvents.loaded(event => {
    let server = event.server;
    // Configure Minecraft vanilla worldborder to 8,000 blocks
    server.runCommandSilent("worldborder center 0 0");
    server.runCommandSilent("worldborder set 8000");
    server.runCommandSilent("worldborder damage buffer 10");
    server.runCommandSilent("worldborder damage amount 2");
    server.runCommandSilent("worldborder warning distance 60");
    server.runCommandSilent("worldborder warning time 10");
});

// Proximity Warning & Atmospheric VFX
PlayerEvents.tick(event => {
    let player = event.player;
    if (player.age % 40 !== 0) return; // Check every 2 seconds

    let dist = Math.max(Math.abs(player.x), Math.abs(player.z));
    if (dist >= 3940 && dist < 4000) {
        // Warning zone: within 60 blocks of the Veil of Salt
        player.tell("§8[§c!§8] §7The air tastes of bitter brine... The Veil of Salt turns you back.");
        player.potionEffects.add("minecraft:slowness", 60, 0, false, false);
        event.server.runCommandSilent("playsound minecraft:ambient.underwater.loop ambient " + player.username + " ~ ~ ~ 0.8 0.5");
        event.server.runCommandSilent("particle minecraft:ash ~ ~1 ~ 1 1 1 0.05 30");
    } else if (dist >= 4000) {
        // Breaching the boundary: dimensional unravelling
        player.tell("§4[§c☠§4] §cYou have reached the unravelled edge of the three dimensions. Existence cannot hold you here.");
        player.potionEffects.add("minecraft:blindness", 80, 0, false, false);
        event.server.runCommandSilent("playsound minecraft:entity.elder_guardian.curse ambient " + player.username + " ~ ~ ~ 1.0 0.6");
    }
});
```

---

## 3. ARCHITECTURAL ARCHAEOLOGY: ENVIRONMENTAL STORYTELLING WITHOUT DIALOGUE

The strongest stories are discovered through geometry and observation. Below is how our custom structures communicate the lore without dialogue:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                             ARCHAEOLOGICAL DISCOVERY SITES                              │
├──────────────────────────┬──────────────────────────┬───────────────────────────────────┤
│ Site                     │ Visual Composition       │ Hidden Lore Revelation            │
├──────────────────────────┼──────────────────────────┼───────────────────────────────────┤
│ The Submerged Basilicas  │ Stained glass murals of  │ In all 10 windows, the 10th baby │
│ of Port Ostraka          │ 10 infants.              │ has had its face chiselled off.   │
├──────────────────────────┼──────────────────────────┼───────────────────────────────────┤
│ Siphon Line Delta        │ Massive brass Create     │ The pipes descend into the        │
│ (Vantyra Under-City)     │ pipes with pressure dial │ ribcage of sleeping Stage 5 Wyrm  │
│                          │ gauges.                  │ Fulmortis—Otto was draining gods. │
├──────────────────────────┼──────────────────────────┼───────────────────────────────────┤
│ The Watchtowers of       │ Ironclast ballistas and  │ The ballistas face INWARD toward  │
│ General Douglas          │ arrow slits.             │ the capital to kill deserters,   │
│                          │                          │ not outward against invaders.     │
├──────────────────────────┼──────────────────────────┼───────────────────────────────────┤
│ The Imperial Nursery     │ 9 gilded golden cribs,   │ Emperor Valerius hid his 10th     │
│ (Palace Summit)          │ 1 crude charred pine     │ child closest to the furnace to   │
│                          │ crib marked "X".         │ protect them from the princes.    │
├──────────────────────────┼──────────────────────────┼───────────────────────────────────┤
│ The Hiroshima Ash Walls  │ Basalt walls with white  │ Citizens were vaporized mid-step  │
│ of the Caldera           │ quartz silhouette outlines│ during the Ninth Sound in a single│
│                          │ of fleeing citizens.     │ night of dimensional collapse.    │
└──────────────────────────┴──────────────────────────┴───────────────────────────────────┘
```

### 1. The Stained-Glass Heresy of Ostraka
* **Structure:** A partially submerged Byzantine cathedral along the coast of Port Ostraka.
* **The Puzzle:** Inside the flooded nave, ten arched stained-glass windows line the clerestory. Each window depicts Emperor Valerius presenting an infant prince crowned in gold.
* **The Clue:** In nine of the windows, the glass is intact. In the tenth window, the glass depicting the child’s face and name has been violently smashed out with an iron chisel, and the lead frame has been bent back.
* **The Drop:** Diving beneath the collapsed pulpit, the player finds a waterlogged chest containing **Page Ten of the Imperial Genealogy**, stained with a single drop of dried golden blood.

### 2. Siphon Line Delta (The Clockwork Parasite)
* **Structure:** The lowest subterranean levels of the Cogwork March in Vantyra.
* **The Puzzle:** The player follows a colossal four-block-wide conduit of Create brass fluid pipes labeled *Siphon Line Delta*. The pipe hums with erratic blue electrical sparks.
* **The Clue:** Following the line down into a natural bedrock cavern, the pipe terminates not in an aquifer or oil deposit, but directly into the open, bleeding dorsal vertebrae of **Fulmortis the Storm-Bane**—the Stage 5 Lightning Wyrm chained beneath the city.
* **The Realization:** Otto Vance’s industrial revolution was never powered by steam engines alone; his city was a parasite draining the lifeblood of a living tectonic deity.

### 3. The Ash Shadows of the Caldera
* **Structure:** The ruined imperial avenues surrounding the Crucible of Ash.
* **The Visual:** Smooth basalt walls feature white quartz tile silhouettes in the shape of kneeling priests, mothers holding infants, and soldiers dropping their swords.
* **The Realization:** Like the nuclear shadows of Hiroshima or the plaster voids of Pompeii, these outlines prove that the cataclysm did not take centuries of war—the Ninth Sound flash-vaporized the capital’s population in less than a second.

---

## 4. THE FROMSOFTWARE ITEM LORE SYSTEM (KUBEJS TOOLTIP ENGINE)

Every item in *Elden Ring* contains historical truth in its description. We implement this using KubeJS's `ItemEvents.tooltip` event. When the player hovers over an item, they see its base stats; holding **Shift** unfolds the historical lore.

### Technical Implementation: `pack/overrides/kubejs/client_scripts/item_lore.js`

```javascript
// =============================================================================
// ASHENFALL — Cryptic FromSoftware Item Lore System
// =============================================================================

ItemEvents.tooltip(event => {
    // Helper function to format multi-line Elden-Ring style lore tooltips
    function addLore(itemId, title, category, quote, loreLines) {
        event.addAdvanced(itemId, (item, advanced, text) => {
            if (!event.isShift()) {
                text.add(Component.darkGray("Hold [") + Component.yellow("Shift") + Component.darkGray("] to inspect inscriptions..."));
                return;
            }

            text.add(Component.darkRed("━ " + title + " ━"));
            text.add(Component.gray("Type: ") + Component.aqua(category));
            text.add(Component.empty());
            if (quote) {
                text.add(Component.italic(Component.gold("\"" + quote + "\"")));
                text.add(Component.empty());
            }
            loreLines.forEach(line => {
                text.add(Component.darkGray(line));
            });
            text.add(Component.darkRed("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"));
        });
    }

    // 1. Waterlogged Boots (Starter Gear)
    addLore("minecraft:leather_boots", 
        "Waterlogged Boots", 
        "Armor (Footwear)", 
        "Even the deep ocean grew tired of holding their guilt.",
        [
            "Salt-stiffened leather worn by an exile who walked into",
            "the sea before the world fell into ruin.",
            "The stitching bears the seal of the Tenth Imperial House,",
            "crudely scraped away with a dull executioner's knife.",
            "The lead weights in the heels were meant to ensure the",
            "wearer never rose to the surface again."
        ]
    );

    // 2. Pilgrim's Compass
    addLore("minecraft:compass",
        "Pilgrim's Compass",
        "Ancient Navigation Relic",
        "It points not to the pole, but to the sin of the world.",
        [
            "A heavy brass instrument salvaged from the lighthouse bluff.",
            "Its needle does not seek magnetic north.",
            "Instead, the lodestone trembles toward the heaviest concentration",
            "of unquenched ash on the continent: the Crucible of Valerius."
        ]
    );

    // 3. The Overclocked Heart-Governor (The Harbinger Drop)
    addLore("minecraft:clock",
        "The Overclocked Heart-Governor",
        "Relic of the Rogue Titan",
        "Daddy... the fire's out... can I come inside now?",
        [
            "The mechanical core of Unit-00 Prime.",
            "Inside the brass housing, sealed within preserving oil,",
            "sits a child's heart completely entwined with copper wires.",
            "It continues to beat at 200 pulses per minute,",
            "powered solely by the terror of filial disappointment."
        ]
    );

    // 4. Heart of Ancient Netherite (Seljuk Drop)
    addLore("minecraft:netherite_ingot",
        "Slag-Forged Heart of Seljuk",
        "Cursed Sovereign Core",
        "Gold melts. Power endures.",
        [
            "Indestructible black alloy harvested from the chest cavity",
            "of the Netherite Monstrosity.",
            "If pressed against the ear, one can still hear the muffled,",
            "gurgling voice of a king counting his gold while drowning",
            "in boiling volcanic slag."
        ]
    );
});
```

---

## 5. THE LIVING WORLD: DYNAMIC NPC GOSSIP & THE 5 WANDERING QUESTLINES

Instead of static quest menus, players interact with world denizens through standard right-clicks that trigger localized narrative events.

```
                    [ 5 WANDERING SOULS & THEIR PATHS ]
                                     │
       ┌──────────┬──────────┬───────┴──┬──────────┬──────────┐
       │          │          │          │          │          │
    Sister     Master     Knight       Salt      Scholar
    Elenor     Kaelen    Rickard     Merchant     Vhol
    (Chimes)  (Pistons)  (Guilt)      (Memory)   (Dragons)
       │          │          │          │          │
     Petrifies  Jumps in   Attacks     Ascends   Turns into
     to Salt    Furnace   at Caldera  to Stardust Wyrm-Beast
```

### Implementation Architecture: KubeJS Persistent Data Engine
Each player’s progress along the 5 NPC questlines is tracked in `player.persistentData.ashenfall`:

```javascript
// Example: Interacting with Master Smith Kaelen
ItemEvents.entityInteracted(event => {
    let player = event.player;
    let target = event.target;
    let server = event.server;

    // Check if right-clicking an Armorer Villager tagged as "Kaelen"
    if (target.type === "minecraft:villager" && target.tags.contains("npc_kaelen")) {
        let questStage = player.persistentData.getInt("quest_kaelen_stage");

        if (questStage === 0) {
            // Stage 0: First meeting in storm cellar
            player.tell("§e[Master Smith Kaelen] §7\"Keep your voice down! Do you hear the pistons grinding? That beast isn't a machine... it was young Marcus! Otto made me weld the skull-screws into the boy's head!\"");
            player.tell("§e[Master Smith Kaelen] §7\"If you're going into the Abandoned Foundry... bring me his heart. Put the child out of his misery.\"");
            player.persistentData.putInt("quest_kaelen_stage", 1);
        } else if (questStage === 1) {
            // Stage 1: Checking for Heart-Governor
            let heldItem = player.mainHandItem;
            if (heldItem.id === "minecraft:clock" && heldItem.hasCustomHoverName()) {
                heldItem.count--;
                player.tell("§e[Master Smith Kaelen] §7*(Kaelen collapses to his knees, clutching the brass heart to his chest as tears cut through the soot on his cheeks)*");
                player.tell("§e[Master Smith Kaelen] §7\"Marcus... my boy... forgive us. Take this, stranger. The last honest thing I'll ever forge.\"");
                server.runCommandSilent("give " + player.username + " minecraft:shield[custom_name='{\"text\":\"Piston-Driven Greatshield\",\"color\":\"gold\"}']");
                player.persistentData.putInt("quest_kaelen_stage", 2);
            } else {
                player.tell("§e[Master Smith Kaelen] §7\"The foundry is in Sub-Sector 4. Listen for the screams through the steam exhaust.\"");
            }
        }
    }
});
```

---

## 6. CINEMATIC BOSS STAGING & PHASE CHOREOGRAPHY

To achieve the dramatic gravity of *Dark Souls* and *Elden Ring* within Minecraft’s sandbox, boss fights utilize choreographed triggers:
1. **Fog Gate Sealing:** Iron bars or stone barriers emerge behind the player when crossing the arena threshold.
2. **Title & Stinger:** Displaying dramatic title cards with `title @p times` and deep bell tolls (`playsound block.bell.use`).
3. **50% HP Phase Shift:** Mid-fight cinematic shift with particle bursts, localized screen blur (`EasyMotionBlur`), and desperate dialogue.
4. **Death Epilogue:** The boss delivers a final tragic monologue as the room falls dead silent.

### The Harbinger Encounter Implementation (`boss_monologue.js`)

```javascript
// Phase Shift Trigger when Harbinger reaches 50% HP
EntityEvents.hurt(event => {
    let entity = event.entity;
    let server = event.server;

    if (entity.tags.contains("boss_harbinger")) {
        let currentHp = entity.health;
        let maxHp = entity.maxHealth;

        if (currentHp <= maxHp * 0.5 && !entity.persistentData.getBoolean("phase_2_triggered")) {
            entity.persistentData.putBoolean("phase_2_triggered", true);

            // 1. Sonic Boom & Boiler Rupture
            server.runCommandSilent("playsound minecraft:entity.generic.explode ambient @a " + entity.x + " " + entity.y + " " + entity.z + " 1.5 0.7");
            server.runCommandSilent("playsound minecraft:block.lava.extinguish ambient @a " + entity.x + " " + entity.y + " " + entity.z + " 1.2 0.5");

            // 2. Superheated Steam Particle Cloud
            server.runCommandSilent("particle minecraft:campfire_signal_smoke " + entity.x + " " + entity.y + " " + entity.z + " 3 2 3 0.1 200");

            // 3. Boss Cinematic Broadcast
            server.runCommandSilent("title @a times 10 40 10");
            server.runCommandSilent("title @a title {\"text\":\"BOILER OVERHEAT\",\"color\":\"red\",\"bold\":true}");
            server.runCommandSilent("title @a subtitle {\"text\":\"The governor gear shatters! Berserk sequence initiated.\",\"color\":\"gold\"}");

            // 4. Buffs: Movement Speed & Fire Resistance
            entity.potionEffects.add("minecraft:speed", 9999, 1, false, false);
            entity.potionEffects.add("minecraft:strength", 9999, 1, false, false);
        }
    }
});
```

---

## 7. THE RESONANCE STELAE: IN-GAME INTERACTIVE LORE MARKERS

Scattered across the Nine Realms are nine **Resonance Stelae**—chiselled stone obelisks embedded with lodestones. When the player right-clicks an obelisk with an empty hand, they hear a low harmonic drone, and a piece of the world's ancient history is inscribed into their chat log.

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             THE 9 STELAE LOCATIONS                               │
├────┬─────────────────────────────┬───────────────────────────────────────────────┤
│ #  │ Location                    │ Historical Record                             │
├────┼─────────────────────────────┼───────────────────────────────────────────────┤
│ 1  │ Grey Coast Lighthouse       │ The First Sound & The Drowning of Ostraka     │
│ 2  │ Ironclast Fortress Trench   │ Douglas's Final Order from the Emperor        │
│ 3  │ Sunken Basilica Clerestory  │ Sophia's Confession of the Deep Salt Hymn     │
│ 4  │ Vantyra Sub-Sector 4        │ Vance's Siphon Blueprint & Marcus's Diagnosis │
│ 5  │ Witchbane Execution Pit     │ Morvath's Letter: "The Tenth Shall Strike"    │
│ 6  │ Al-Qadira Glass Dune Peak   │ The Liquefaction of the Southern Desert       │
│ 7  │ Solitary Spine Glacier Rope │ The Vow of Mute Asceticism                    │
│ 8  │ Whispering Fen Heartwood    │ Belen's Communion with the Primordial Mycelium│
│ 9  │ Caldera Throne Antechamber  │ Valerius's Unspoken Apology to his Tenth Child│
└────┴─────────────────────────────┴───────────────────────────────────────────────┘
```

### Technical Implementation
In `pack/overrides/kubejs/server_scripts/stelae.js`:
```javascript
BlockEvents.rightClicked("minecraft:chiseled_stone_bricks", event => {
    let block = event.block;
    let player = event.player;
    let server = event.server;

    // Check specific landmark coordinates (e.g., Stela #1 at Lighthouse)
    if (block.x === 18 && block.z === 14) {
        event.cancel();
        server.runCommandSilent("playsound minecraft:block.bell.resonate ambient " + player.username + " ~ ~ ~ 1.0 0.8");
        player.tell("§8━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
        player.tell("§6§l[STELA OF THE FIRST SOUND — THE DROWNED SHORE]");
        player.tell("§7\"When the bell rang beneath the bedrock, the sea did not rise as a wave.");
        player.tell("§7It rose as a hand, gently pulling our churches into the dark.");
        player.tell("§7The emperor promised eternity. He gave us sixty fathoms of black water.\"");
        player.tell("§8━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    }
});
```

---

## 8. THE CRUCIBLE ALTAR: EXECUTING THE FOUR DYNAMIC ENDINGS

At the climax of the game, after defeating Emperor Valerius IX in the Crucible of Ash, the player stands before the **Altar of the Ten Embers** (a custom obsidian altar block at `x: 0, y: -20, z: 0`). The ending is determined by what item the player uses on the altar.

```
                                  [ THE ALTAR OF ASH ]
                                            │
        ┌───────────────────┬───────────────┴───────────────┬───────────────────┐
        ▼                   ▼                               ▼                   ▼
  [EMPEROR'S SEAL]   [ABYSSAL BRINE]             [HEART-GOVERNOR]        [STARTER SWORD]
     Ending I:          Ending II:                  Ending III:             Ending IV:
     The Tyrant's Dawn  The Drowned Peace           The Brass Revolution    The True Pilgrimage
     • White Sun Fire   • Continental Flooding      • Endless Cogwheels     • Altar Shatters
     • Mortals turn to  • Painless Deep Rest        • Flesh replaced by     • Health drops to
       Golden Statues     beneath moonlit sea         Steam & Airships        10 Mortal Hearts
```

### Script Execution: `pack/overrides/kubejs/server_scripts/endings.js`

```javascript
BlockEvents.rightClicked(event => {
    let block = event.block;
    let player = event.player;
    let server = event.server;
    let item = player.mainHandItem;

    if (block.id === "minecraft:crying_obsidian" && block.tags.contains("crucible_altar")) {
        event.cancel();

        // ENDING I: The Age of the Unbroken Flame
        if (item.id === "minecraft:nether_star" && item.hasCustomHoverName()) {
            server.runCommandSilent("time set day");
            server.runCommandSilent("weather clear");
            server.runCommandSilent("title @a times 20 100 30");
            server.runCommandSilent("title @a title {\"text\":\"AGE OF THE UNBROKEN FLAME\",\"color\":\"gold\",\"bold\":true}");
            server.runCommandSilent("title @a subtitle {\"text\":\"The sun shall never set. Mortality is forged into gold.\",\"color\":\"yellow\"}");
            server.runCommandSilent("particle minecraft:totem_of_undying 0 -18 0 10 5 10 0.2 500");
        }

        // ENDING II: The Age of Deep Salt
        else if (item.id === "minecraft:potion" && item.nbt && item.nbt.ashenfall_type === "abyssal_brine") {
            server.runCommandSilent("weather thunder");
            server.runCommandSilent("title @a times 20 100 30");
            server.runCommandSilent("title @a title {\"text\":\"AGE OF DEEP SALT\",\"color\":\"dark_blue\",\"bold\":true}");
            server.runCommandSilent("title @a subtitle {\"text\":\"The fires die. Sleep peacefully beneath the silent sea.\",\"color\":\"aqua\"}");
            server.runCommandSilent("particle minecraft:splash 0 -18 0 10 5 10 0.5 500");
        }

        // ENDING III: The Brass Revolution
        else if (item.id === "minecraft:clock" && item.hasCustomHoverName()) {
            server.runCommandSilent("title @a times 20 100 30");
            server.runCommandSilent("title @a title {\"text\":\"THE BRASS REVOLUTION\",\"color\":\"dark_gray\",\"bold\":true}");
            server.runCommandSilent("title @a subtitle {\"text\":\"Steel needs no god. The endless gears begin to turn.\",\"color\":\"gold\"}");
            server.runCommandSilent("playsound create:steam_whistle ambient @a 0 -18 0 2.0 1.0");
        }

        // ENDING IV: The True Pilgrimage (Secret Ending)
        else if (item.id === "minecraft:iron_sword" && player.persistentData.getInt("quest_kaelen_stage") >= 2) {
            // Shatter the altar
            server.runCommandSilent("setblock 0 -20 0 minecraft:air destroy");
            server.runCommandSilent("playsound minecraft:block.glass.break ambient @a 0 -20 0 2.0 0.5");
            server.runCommandSilent("title @a times 20 120 40");
            server.runCommandSilent("title @a title {\"text\":\"THE MENDED SILENCE\",\"color\":\"white\",\"bold\":true}");
            server.runCommandSilent("title @a subtitle {\"text\":\"The crown is broken. Dawn breaks over mortal hands.\",\"color\":\"gray\"}");

            // The Tenth Ember leaves the player: Reset health from 20 hearts to 10 mortal hearts
            player.attributes.removeAttributeModifiers("minecraft:generic.max_health");
            player.health = 20; // 10 red hearts
            player.tell("§7Your veins cool. The molten gold drains into the soil.");
            player.tell("§fYou are no longer a scion of gods. You are an ordinary man beneath an honest sky.");
        }
    }
});
```

---

## 9. MOD SYNERGY MATRIX: HOW EACH MOD SERVES THE STORY

| Mod Installed | Creative Narrative Function | Technical Role in the Tale |
| :--- | :--- | :--- |
| **Create (6.0.10)** | Embodies **The Hammer Faction (Otto Vance)**: steam engines, clunkers, automated foundries, suspended railways, and the tragic machine-god hubris. | Kinetic automation, moving train contraptions, pneumatic fluid siphons, and mechanical puzzles. |
| **Ice and Fire CE** | Embodies **The Colossus Faction & Tectonic Anchors**: the Three Stage 5 Primordial Apex Dragons sleeping in continental faults. | Terrifying, rare endgame encounters requiring strategic planning, fire/frost resistance, and melee precision. |
| **Distant Horizons (3.3.1)** | Renders the vast, scarred continental scale across the 8,000x8,000 block finite world. | Allows the player to see smoking factory chimneys, glacial spires, and the ash crater from anywhere on the map. |
| **EasyMotionBlur** | Cinematic sensory disorientation. | Automatically pulses subtle motion blur during boss phase-shifts, near the Veil of Salt, and during the beach awakening. |
| **AI Improvements (0.5.3)** | Eliminates CPU thread lag during high-density sieges. | Keeps server tick-rate at a rock-solid 20 TPS during boss fights and sprawling Create factory operations. |
| **KubeJS 1.21.1** | The narrative central nervous system. | Handles player 20-heart biology, boss dialogues, NPC rumours, cryptic item tooltips, stelae, and the 4 endings. |

---

## 10. IMPLEMENTATION ROADMAP: STEP-BY-STEP PRODUCTION PLAN

```
┌────────────────────────────────────────────────────────────────────────┐
│                        FIVE PRODUCTION PHASES                          │
├────────────────────────────────────────────────────────────────────────┤
│ PHASE 1: GEOMETRY & BOUNDS (Immediate)                                │
│ • Deploy world_border.js: enforce 8,000 x 8,000 Veil of Salt perimeter.│
│ • Configure Distant Horizons LOD generator within the finite boundary. │
│                                                                        │
│ PHASE 2: FORENSIC ARCHAEOLOGY (Structures)                             │
│ • Place Siphon Line Delta connecting Create pipes to dragon dens.      │
│ • Build the submerged basilica of Ostraka with chiselled 10th window.  │
│ • Inscribe the Hiroshima Ash Shadows along the Caldera avenues.       │
│                                                                        │
│ PHASE 3: THE CODEX OF OBJECTS (Item Tooltips)                          │
│ • Expand client_scripts/item_lore.js with all 30 FromSoftware items.   │
│ • Implement the Shift-to-reveal inspection mechanic.                   │
│                                                                        │
│ PHASE 4: THE DIALOGUE OF THE DEAD (NPCs & Stelae)                      │
│ • Tag the 5 Wandering Pilgrims and configure persistent data states.   │
│ • Deploy the 9 Resonance Stelae across the Nine Realm coordinates.     │
│                                                                        │
│ PHASE 5: THE FINAL CURTAIN (Boss Choreography & Endings)               │
│ • Finish the 2-phase triggers for Harbinger, Seljuk, and Valerius.     │
│ • Wire the Altar of Ash at (0, -20, 0) to execute the 4 Endings.       │
└────────────────────────────────────────────────────────────────────────┘
```

---
*The Ashenfall Story Implementation Blueprint — Preserved for the builders of Vantyra.*
"""

output_path = "/home/user/The-modpack/ASHENFALL_STORY_IMPLEMENTATION_BLUEPRINT.md"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(blueprint_content)
print(f"Generated {output_path} successfully ({len(blueprint_content)} characters)")
