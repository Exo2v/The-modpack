// =============================================================================
// ASHENFALL — Soulslike Rest, Ember Flask, & Hollow Death Penalty
// =============================================================================

var HOLLOW_CAP = 5;
var REST_TAGS = [
    "minecraft:campfires",
    "minecraft:beds"
];

function getHollow(player) {
    if (!player.persistentData.contains("ashfall_hollow")) {
        player.persistentData.putInt("ashfall_hollow", 0);
    }
    return player.persistentData.getInt("ashfall_hollow");
}

function setHollow(player, val) {
    var clamped = Math.max(0, Math.min(HOLLOW_CAP, val));
    player.persistentData.putInt("ashfall_hollow", clamped);
}

// On player respawn: hollow penalty increments
PlayerEvents.respawned(function(event) {
    try {
        var player = event.player;
        if (!player) return;
        var hollow = getHollow(player);
        if (hollow < HOLLOW_CAP) {
            setHollow(player, hollow + 1);
            player.tell("§8[§cDeath§8] §7Your ember fades slightly. Hollow tier: §c" + (hollow + 1) + "§7/" + HOLLOW_CAP);
        }
    } catch (e) {
        // Silently prevent respawn error
    }
});
