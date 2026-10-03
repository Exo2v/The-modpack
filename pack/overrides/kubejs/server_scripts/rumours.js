// =============================================================================
// ASHENFALL — The Rumour Register System
// =============================================================================

var RUMOURS = [
    {
        id: "cold_tower",
        speaker: "Inuit Elder",
        text: "There is a tower in the far north that doesn't melt, even when struck by dragonfire.",
        landmark: "L1 — The Cold Tower",
        gate: "chapter_2"
    },
    {
        id: "drowned_choir",
        speaker: "Drowned Fisherman",
        text: "The Choir's cathedral drowned in the abyss. It never stopped praying.",
        landmark: "L7 — The Otherside Rift",
        gate: "codex_drowned_choir"
    },
    {
        id: "jungle_vault",
        speaker: "Seljuk Scout",
        text: "A sandstone fortress lies swallowed by the jungle vines. Whatever you do, do not enter at night.",
        landmark: "L3 — Jungle Vault",
        gate: "none"
    },
    {
        id: "hidden_cathedral",
        speaker: "The Archivist",
        text: "They say there is a second Cathedral... buried beneath the foundations of the world.",
        landmark: "L★ — The Hidden Cathedral",
        gate: "all_9_runes"
    },
    {
        id: "arcane_catacombs",
        speaker: "Tavern Keeper",
        text: "Wizards buy raw essence at great cost. Wizards also die down in the catacombs.",
        landmark: "L7b — The Catacombs",
        gate: "essence_held"
    },
    {
        id: "clunker_behemoth",
        speaker: "Disgraced Aeronaut",
        text: "The brass airships fell from the sky when the Ancient Factory woke. A metal monster with three cannons sweeps lasers across the rusted foundries. None who entered ever returned.",
        landmark: "L8 — The Ancient Foundry (Cogwork March)",
        gate: "none"
    },
    {
        id: "dragon_dens",
        speaker: "Wandering Hunter",
        text: "The true dragons do not wander the plains like beasts. They sleep miles below the crust in ancient volcanic dens, guarded by oceans of lava.",
        landmark: "Deep Dens — 2,500 Blocks Past Spawn",
        gate: "tier_3"
    },
    {
        id: "tenth_scion",
        speaker: "The Blind Archivist",
        text: "Valerius had ten scions, not nine. The tenth was cast into the sea with ash burned into their chest. They say when the tenth walks again, the Hearth either rekindles or dies forever.",
        landmark: "L★ — The Crucible of Ash",
        gate: "all_9_runes"
    }
];

function tellRumour(player, rumourId) {
    var rumour = null;
    for (var i = 0; i < RUMOURS.length; i++) {
        if (RUMOURS[i].id === rumourId) {
            rumour = RUMOURS[i];
            break;
        }
    }
    if (!rumour) return;

    player.tell(" ");
    player.tell("§6[Rumour] §e" + rumour.speaker + " §7whispers:");
    player.tell("§f\"" + rumour.text + "\"");
    player.tell("§8Related Landmark: §b" + rumour.landmark);
    player.tell(" ");
}
