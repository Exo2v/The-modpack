// =============================================================================
// ASHENFALL — Beach Awakening Cutscene & Shoreline Spawn
// =============================================================================

function buildLighthouse(server, x, y, z) {
    // Build a classic coastal stone lighthouse on the bluff
    for (var dy = 0; dy < 14; dy++) {
        var radius = dy < 8 ? 2 : 1;
        for (var dx = -radius; dx <= radius; dx++) {
            for (var dz = -radius; dz <= radius; dz++) {
                if (Math.abs(dx) === radius && Math.abs(dz) === radius) {
                    server.runCommandSilent("setblock " + (x + dx) + " " + (y + dy) + " " + (z + dz) + " minecraft:mossy_cobblestone");
                } else if (Math.abs(dx) === radius || Math.abs(dz) === radius) {
                    server.runCommandSilent("setblock " + (x + dx) + " " + (y + dy) + " " + (z + dz) + " minecraft:stone_bricks");
                } else {
                    server.runCommandSilent("setblock " + (x + dx) + " " + (y + dy) + " " + (z + dz) + " minecraft:air");
                }
            }
        }
    }

    // Doorway
    server.runCommandSilent("setblock " + x + " " + y + " " + (z + 2) + " minecraft:oak_door[facing=south,half=lower]");
    server.runCommandSilent("setblock " + x + " " + (y + 1) + " " + (z + 2) + " minecraft:oak_door[facing=south,half=upper]");

    // Interior ladder & floors
    for (var ldy = 0; ldy < 13; ldy++) {
        server.runCommandSilent("setblock " + x + " " + (y + ldy) + " " + (z - 1) + " minecraft:ladder[facing=south]");
    }

    // Lantern gallery & beacon on top
    var topY = y + 14;
    for (var bx = -2; bx <= 2; bx++) {
        for (var bz = -2; bz <= 2; bz++) {
            server.runCommandSilent("setblock " + (x + bx) + " " + topY + " " + (z + bz) + " minecraft:smooth_stone_slab");
            if (Math.abs(bx) === 2 || Math.abs(bz) === 2) {
                server.runCommandSilent("setblock " + (x + bx) + " " + (topY + 1) + " " + (z + bz) + " minecraft:iron_bars");
            }
        }
    }

    // Beacon fire at the crown
    server.runCommandSilent("setblock " + x + " " + (topY + 1) + " " + z + " minecraft:soul_campfire[lit=true]");
    server.runCommandSilent("setblock " + x + " " + (topY + 2) + " " + z + " minecraft:tinted_glass");
    server.runCommandSilent("setblock " + x + " " + (topY + 3) + " " + z + " minecraft:stone_brick_slab");

    // Starter Chest inside ground floor
    server.runCommandSilent("setblock " + (x + 1) + " " + y + " " + z + " minecraft:chest[facing=west]");
    server.runCommandSilent("item replace block " + (x + 1) + " " + y + " " + z + " container.0 with minecraft:spyglass");
    server.runCommandSilent("item replace block " + (x + 1) + " " + y + " " + z + " container.1 with minecraft:bread 8");
    server.runCommandSilent("item replace block " + (x + 1) + " " + y + " " + z + " container.2 with minecraft:cooked_cod 4");
    server.runCommandSilent("item replace block " + (x + 1) + " " + y + " " + z + " container.3 with minecraft:torch 12");
    server.runCommandSilent("item replace block " + (x + 1) + " " + y + " " + z + " container.4 with minecraft:flint_and_steel");
    server.runCommandSilent("item replace block " + (x + 1) + " " + y + " " + z + " container.5 with minecraft:potion[potion_contents={potion:\"minecraft:healing\"}]");

    // Signal lantern hanging outside
    server.runCommandSilent("setblock " + x + " " + (y + 3) + " " + (z + 3) + " minecraft:lantern[hanging=true]");
}

PlayerEvents.loggedIn(function(event) {
    var player = event.player;
    var server = event.server;

    if (!player.tags.contains("ashfall_awakened")) {
        player.tags.add("ashfall_awakened");

        // 1. Position player safely on the coastal sands
        var px = Math.floor(player.x);
        var py = Math.floor(player.y);
        var pz = Math.floor(player.z);

        // Build starter lighthouse nearby on cliff/higher ground
        var lx = px + 18;
        var lz = pz + 14;
        var ly = py + 3;
        buildLighthouse(server, lx, ly, lz);

        // 2. Play dramatic opening sound effects
        server.runCommandSilent("playsound minecraft:ambient.underwater.enter ambient " + player.username + " " + px + " " + py + " " + pz + " 1.0 0.8");
        server.runCommandSilent("playsound minecraft:entity.generic.splash ambient " + player.username + " " + px + " " + py + " " + pz + " 1.0 0.7");

        // 3. Apply opening blur / blindness (eyes opening on sand)
        player.potionEffects.add("minecraft:blindness", 120, 0, false, false);
        player.potionEffects.add("minecraft:slowness", 140, 3, false, false);
        player.potionEffects.add("minecraft:water_breathing", 200, 0, false, false);

        // 4. Act I: Awakening on Beach Title
        server.scheduleInTicks(15, function() {
            server.runCommandSilent("title " + player.username + " times 20 60 20");
            server.runCommandSilent("title " + player.username + " title {\"text\":\"ASHENFALL\",\"color\":\"dark_red\",\"bold\":true}");
            server.runCommandSilent("title " + player.username + " subtitle {\"text\":\"You wash ashore on the cold sands...\",\"color\":\"gray\"}");
        });

        // 5. Act II: The Tenth Ember Awakens
        server.scheduleInTicks(80, function() {
            server.runCommandSilent("playsound minecraft:block.campfire.crackle ambient " + player.username + " " + px + " " + py + " " + pz + " 0.8 1.0");
            server.runCommandSilent("title " + player.username + " times 15 50 15");
            server.runCommandSilent("title " + player.username + " title {\"text\":\"The Tenth Ember\",\"color\":\"gold\",\"bold\":true}");
            server.runCommandSilent("title " + player.username + " subtitle {\"text\":\"A faint warmth smolders within your chest.\",\"color\":\"yellow\"}");
        });

        // 6. Act III: Narrative Introduction
        server.scheduleInTicks(140, function() {
            server.runCommandSilent("playsound minecraft:block.bell.use ambient " + player.username + " " + px + " " + py + " " + pz + " 0.7 0.9");
            player.tell(" ");
            player.tell("§8━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
            player.tell("§c⚔ ASHENFALL §8— §7The Pilgrimage Begins");
            player.tell("§e\"Nine sounds broke the Empire in a single night.\"");
            player.tell("§e\"You are not a hero, pilgrim. You are the cause, walking to mend what you shattered.\"");
            player.tell(" ");
            player.tell("§bAbove the shoreline bluff looms the Old Lighthouse beacon.");
            player.tell("§7Scavenge the lighthouse for supplies, then journey inland toward the Norman Remnant.");
            player.tell("§8━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
            player.tell(" ");
        });

        // 7. Starter supplies directly in inventory
        server.scheduleInTicks(150, function() {
            server.runCommandSilent("give " + player.username + " minecraft:leather_boots[custom_name='{\"text\":\"Waterlogged Boots\",\"color\":\"gray\"}']");
            server.runCommandSilent("give " + player.username + " minecraft:compass[custom_name='{\"text\":\"Pilgrim\\'s Compass\",\"color\":\"gold\"}']");
            server.runCommandSilent("give " + player.username + " minecraft:flint");
            server.runCommandSilent("give " + player.username + " minecraft:bread 4");
        });
    }
});
