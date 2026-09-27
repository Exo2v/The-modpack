// =============================================================================
// ASHENFALL — Player Base Health (20 Hearts / 40 Max HP)
// =============================================================================

PlayerEvents.loggedIn(function(event) {
    var player = event.player;
    var server = event.server;
    
    // Set base max health to 40.0 (20 full hearts)
    server.runCommandSilent("attribute " + player.username + " minecraft:generic.max_health base set 40");
    
    // Top up health on login if needed
    if (player.health < 40) {
        player.setHealth(40);
    }
});

PlayerEvents.respawned(function(event) {
    var player = event.player;
    var server = event.server;
    
    // Re-apply 20 hearts upon respawn
    server.runCommandSilent("attribute " + player.username + " minecraft:generic.max_health base set 40");
    player.setHealth(40);
});

PlayerEvents.changeDimension(function(event) {
    var player = event.player;
    var server = event.server;
    
    // Maintain 20 hearts across dimension transitions
    server.runCommandSilent("attribute " + player.username + " minecraft:generic.max_health base set 40");
});
