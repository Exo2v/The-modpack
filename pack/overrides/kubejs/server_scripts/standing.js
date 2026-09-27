// =============================================================================
// ASHENFALL — Nine Nations Standing System (-100 to +100)
// =============================================================================

const FACTIONS = [
    "norman_remnant",
    "seljuk_expanse",
    "byzantine_choir",
    "witchbane_watch",
    "guild_of_merchants",
    "cathedral_of_ash",
    "frostfall",
    "sunken_throne",
    "hermits_reach"
];

function getStanding(player, faction) {
    let key = `standing_${faction}`;
    if (!player.persistentData.contains(key)) {
        player.persistentData.putInt(key, 0); // Neutral
    }
    return player.persistentData.getInt(key);
}

function modifyStanding(player, faction, delta) {
    let key = `standing_${faction}`;
    let current = getStanding(player, faction);
    let updated = Math.max(-100, Math.min(100, current + delta));
    player.persistentData.putInt(key, updated);

    let prefix = delta >= 0 ? "§a+" : "§c";
    let factionLabel = faction.replace(/_/g, " ").replace(/\b\w/g, l => l.toUpperCase());
    player.tell(`§8[§6Faction Rep§8] §f${factionLabel}: ${prefix}${delta} §7(Current: ${updated})`);
}

// Global helper for scripts and commands
global.getStanding = getStanding;
global.modifyStanding = modifyStanding;
