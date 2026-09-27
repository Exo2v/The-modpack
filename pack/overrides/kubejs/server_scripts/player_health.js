// =============================================================================
// ASHENFALL — Player Base Health (20 Hearts / 40 Max HP)
// =============================================================================

PlayerEvents.loggedIn(function(event) {
    try {
        var player = event.player;
        if (!player) return;
        var attr = player.getAttribute("minecraft:generic.max_health");
        if (attr) {
            attr.setBaseValue(40.0);
        }
        if (player.health < 40) {
            player.setHealth(40);
        }
    } catch (e) {
        console.error("Health init exception: " + e);
    }
});

PlayerEvents.respawned(function(event) {
    try {
        var player = event.player;
        if (!player) return;
        var attr = player.getAttribute("minecraft:generic.max_health");
        if (attr) {
            attr.setBaseValue(40.0);
        }
        player.setHealth(40);
    } catch (e) {
        console.error("Health respawn exception: " + e);
    }
});

PlayerEvents.changedDimension(function(event) {
    try {
        var player = event.player;
        if (!player) return;
        var attr = player.getAttribute("minecraft:generic.max_health");
        if (attr) {
            attr.setBaseValue(40.0);
        }
    } catch (e) {
        console.error("Health dimension exception: " + e);
    }
});
