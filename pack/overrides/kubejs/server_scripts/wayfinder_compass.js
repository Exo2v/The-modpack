// =============================================================================
// ASHENFALL — 5-Location Wayfinder Teleportation Compass (KubeJS 1.21.1)
// =============================================================================

var DESTINATIONS = [
    { id: 1, code: "coast", name: "The Forgotten Coast", tag: "Spawn / South", coords: "0 68 2500", x: 0, y: 68, z: 2500, color: "green", expected: "Plains, Meadow, Forest" },
    { id: 2, code: "cogwork", name: "The Cogwork March", tag: "West", coords: "-2000 85 0", x: -2000, y: 85, z: 0, color: "gold", expected: "Windswept Hills, River, Badlands" },
    { id: 3, code: "caldera", name: "The Ashen Caldera", tag: "Center", coords: "0 80 0", x: 0, y: 80, z: 0, color: "dark_red", expected: "Basalt Deltas, Blackstone, Crater" },
    { id: 4, code: "glacial", name: "The Solitary Glacial Spine", tag: "North", coords: "0 160 -2500", x: 0, y: 160, z: -2500, color: "aqua", expected: "Frozen Peaks, Snowy Slopes, Grove" },
    { id: 5, code: "gilded", name: "The Gilded Dunes", tag: "East", coords: "2500 75 0", x: 2500, y: 75, z: 0, color: "yellow", expected: "Desert, Badlands, Terracotta" }
];

function giveWayfinderCompass(player, server) {
    if (!player || !server) return;
    try {
        var cmd = "give " + player.username + " minecraft:compass[custom_name='{\"text\":\"🧭 Ashenfall Wayfinder Compass\",\"color\":\"gold\",\"bold\":true}',lore=['{\"text\":\"Right-click to open 5-nation teleport menu\",\"color\":\"yellow\"}','{\"text\":\"Inspects biome generation at key landmarks\",\"color\":\"gray\"}']]";
        server.runCommandSilent(cmd);
    } catch (e) {
        console.error("Failed to give Wayfinder Compass: " + e);
    }
}

function teleportToDestination(player, server, dest) {
    if (!player || !server || !dest) return;
    try {
        var u = player.username;
        server.runCommandSilent("tp " + u + " " + dest.coords);
        server.runCommandSilent("playsound minecraft:item.chorus_fruit.teleport ambient " + u + " " + dest.coords + " 1.0 1.0");
        server.runCommandSilent("playsound minecraft:ui.toast.challenge_complete ambient " + u + " " + dest.coords + " 0.8 1.2");
        server.runCommandSilent("title " + u + " times 10 50 15");
        server.runCommandSilent("title " + u + " title {\"text\":\"" + dest.name + "\",\"color\":\"" + dest.color + "\",\"bold\":true}");
        server.runCommandSilent("title " + u + " subtitle {\"text\":\"[" + dest.tag + "] (" + dest.coords.replace(/ /g, ", ") + ")\",\"color\":\"gray\"}");
        player.tell(" ");
        player.tell("§8━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
        player.tell("§6🧭 WAYFINDER ARRIVAL: §f" + dest.name + " §8[" + dest.tag + "]");
        player.tell("§7Coordinates:      §bX: " + dest.x + ", Y: " + dest.y + ", Z: " + dest.z);
        player.tell("§7Expected Biomes:  §e" + dest.expected);
        player.tell("§dℹ Tip: Press F3 to inspect the active biome name in the debug overlay.");
        player.tell("§8━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
        player.tell(" ");
    } catch (e) {
        console.error("Teleportation error: " + e);
    }
}

function showWayfinderMenu(player, server) {
    if (!player || !server) return;
    try {
        var u = player.username;
        server.runCommandSilent("playsound minecraft:item.lodestone_compass.lock ambient " + u + " ~ ~ ~ 1.0 1.0");
        server.runCommandSilent("tellraw " + u + " \"\"");
        server.runCommandSilent("tellraw " + u + " [\"\",{\"text\":\"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\",\"color\":\"dark_gray\"}]");
        server.runCommandSilent("tellraw " + u + " [\"\",{\"text\":\"🧭 \",\"color\":\"gold\"},{\"text\":\"ASHENFALL WAYFINDER MENU\",\"color\":\"gold\",\"bold\":true},{\"text\":\" — Choose a destination:\",\"color\":\"yellow\"}]");
        server.runCommandSilent("tellraw " + u + " [\"\",{\"text\":\"Click any option below to instantly teleport and inspect biomes:\",\"color\":\"gray\",\"italic\":true}]");
        server.runCommandSilent("tellraw " + u + " \"\"");
        for (var i = 0; i < DESTINATIONS.length; i++) {
            var d = DESTINATIONS[i];
            var btnJson = JSON.stringify([
                "",
                {"text": " [" + d.id + "] ", "color": "yellow", "bold": true},
                {"text": d.name + " ", "color": d.color, "bold": true},
                {"text": "(" + d.tag + ") ", "color": "dark_gray"},
                {"text": "➡ [CLICK TO TELEPORT]", "color": "aqua", "bold": true,
                 "clickEvent": {"action": "run_command", "value": "/wayfinder " + d.id},
                 "hoverEvent": {"action": "show_text", "contents": "Teleport to " + d.name + "\nCoords: (" + d.coords.replace(/ /g, ", ") + ")\nExpected: " + d.expected}}
            ]);
            server.runCommandSilent("tellraw " + u + " " + btnJson);
        }
        server.runCommandSilent("tellraw " + u + " \"\"");
        server.runCommandSilent("tellraw " + u + " [\"\",{\"text\":\"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\",\"color\":\"dark_gray\"}]");
        server.runCommandSilent("tellraw " + u + " \"\"");
    } catch (e) {
        console.error("Wayfinder menu error: " + e);
    }
}

ItemEvents.rightClicked(function(event) {
    try {
        var item = event.item;
        if (!item) return;
        if (item.id === "minecraft:compass") {
            var player = event.player;
            if (!player) return;
            var server = event.server || (player.level && player.level.server);
            if (!server) return;
            showWayfinderMenu(player, server);
            event.cancel();
        }
    } catch (e) {
        console.error("Item right-click error: " + e);
    }
});

PlayerEvents.loggedIn(function(event) {
    try {
        var player = event.player;
        if (!player) return;
        var server = event.server || (player.level && player.level.server);
        if (!server) return;
        if (!player.tags.contains("has_wayfinder_compass")) {
            player.tags.add("has_wayfinder_compass");
            server.scheduleInTicks(40, function() {
                giveWayfinderCompass(player, server);
                player.tell("§8[§6Wayfinder§8] §eYou have received the §6🧭 Ashenfall Wayfinder Compass§e! Right-click it anytime to teleport between nations.");
            });
        }
    } catch (e) {
        console.error("Wayfinder login error: " + e);
    }
});

ServerEvents.commandRegistry(function(event) {
    var Commands = event.commands;
    var Arguments = event.arguments;
    function reg(cmdName) {
        event.register(
            Commands.literal(cmdName)
                .executes(function(ctx) {
                    var player = ctx.source.player;
                    var server = ctx.source.server;
                    if (player && server) showWayfinderMenu(player, server);
                    return 1;
                })
                .then(Commands.literal("give")
                    .executes(function(ctx) {
                        var player = ctx.source.player;
                        var server = ctx.source.server;
                        if (player && server) giveWayfinderCompass(player, server);
                        return 1;
                    })
                )
                .then(Commands.argument("option", Arguments.STRING.create(event))
                    .executes(function(ctx) {
                        var player = ctx.source.player;
                        var server = ctx.source.server;
                        var opt = Arguments.STRING.getResult(ctx, "option").toLowerCase();
                        if (!player || !server) return 0;
                        for (var i = 0; i < DESTINATIONS.length; i++) {
                            var d = DESTINATIONS[i];
                            if (opt === String(d.id) || opt === d.code || opt.indexOf(d.code) !== -1) {
                                teleportToDestination(player, server, d);
                                return 1;
                            }
                        }
                        player.tell("§cUnknown destination. Type /" + cmdName + " to open the menu.");
                        return 1;
                    })
                )
        );
    }
    reg("wayfinder");
    reg("tp_nation");
});
