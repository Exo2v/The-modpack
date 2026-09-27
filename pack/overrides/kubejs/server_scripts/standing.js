// =============================================================================
// ASHENFALL — Nine Nations Standing System (-100 to +100)
// =============================================================================

var NATIONS = [
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

var CROSS_FACTION = true;
var CHAMPION_THRESHOLD = 80;
var MAX_NATIONS_CHAMPION = 3;

function getStanding(player, faction) {
    var key = "standing_" + faction;
    if (!player.persistentData.contains(key)) {
        player.persistentData.putInt(key, 0); // Neutral
    }
    return player.persistentData.getInt(key);
}

function modifyStanding(player, faction, delta) {
    var key = "standing_" + faction;
    var current = getStanding(player, faction);
    var updated = Math.max(-100, Math.min(100, current + delta));
    player.persistentData.putInt(key, updated);

    var prefix = delta >= 0 ? "§a+" : "§c";
    var factionLabel = faction.replace(/_/g, " ").replace(/\b\w/g, function(l) { return l.toUpperCase(); });
    player.tell("§8[§6Faction Rep§8] §f" + factionLabel + ": " + prefix + delta + " §7(Current: " + updated + ")");
}

// Global export for Rhino engine (explicit key-value pairs)
global.ASHFALL_STANDING = {
    NATIONS: NATIONS,
    CROSS_FACTION: CROSS_FACTION,
    CHAMPION_THRESHOLD: CHAMPION_THRESHOLD,
    MAX_NATIONS_CHAMPION: MAX_NATIONS_CHAMPION,
    getStanding: getStanding,
    modifyStanding: modifyStanding
};

global.getStanding = getStanding;
global.modifyStanding = modifyStanding;
