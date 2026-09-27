// =============================================================================
// ASHENFALL — The Rumour Register System
// =============================================================================

const RUMOURS = [
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
    }
];

function tellRumour(player, rumourId) {
    let rumour = RUMOURS.find(r => r.id === rumourId);
    if (!rumour) return;

    player.tell(" ");
    player.tell(`§6[Rumour] §e${rumour.speaker} §7whispers:`);
    player.tell(`§f"${rumour.text}"`);
    player.tell(`§8Related Landmark: §b${rumour.landmark}`);
    player.tell(" ");
}

global.tellRumour = tellRumour;
