// =============================================================================
// ASHENFALL — Boss Monologues & Cinematic Encounters
// =============================================================================

var BOSS_ENCOUNTERS = {
    "cataclysm:ignis": {
        name: "Ignis, The Incinerator",
        line: "Ash will cover the world again. Your ember will feed the pyre.",
        sound: "minecraft:entity.ender_dragon.growl"
    },
    "cataclysm:netherite_monstrosity": {
        name: "Netherite Monstrosity",
        line: "The crucible demands another sacrifice.",
        sound: "minecraft:entity.ravager.roar"
    },
    "cataclysm:the_harbinger": {
        name: "The Harbinger",
        line: "Ancient machinery hums with renewed wrath.",
        sound: "minecraft:block.beacon.activate"
    },
    "cataclysm:the_leviathan": {
        name: "The Leviathan of the Abyss",
        line: "The sunken choir sings your drowning hymn.",
        sound: "minecraft:ambient.underwater.loop"
    },
    "irons_spellbooks:dead_king": {
        name: "The Dead King of the Catacombs",
        line: "You seek the lost words of power. They belong to the dust.",
        sound: "minecraft:entity.wither.ambient"
    }
};

EntityEvents.spawned(function(event) {
    var entity = event.entity;
    if (!entity) return;
    var type = entity.type;

    if (BOSS_ENCOUNTERS[type]) {
        var boss = BOSS_ENCOUNTERS[type];
        var level = entity.level;
        if (!level || !level.players) return;

        level.players.forEach(function(player) {
            // Check distance
            var distSq = player.distanceToSqr(entity);
            if (distSq < 64 * 64) {
                // Screen shake & cinematic alert
                player.potionEffects.add("minecraft:slowness", 60, 1, false, false);
                level.server.runCommandSilent("playsound " + boss.sound + " ambient " + player.username + " " + player.x + " " + player.y + " " + player.z + " 1.0 0.8");
                
                level.server.runCommandSilent("title " + player.username + " times 10 60 20");
                level.server.runCommandSilent("title " + player.username + " title {\"text\":\"" + boss.name + "\",\"color\":\"red\",\"bold\":true}");
                level.server.runCommandSilent("title " + player.username + " subtitle {\"text\":\"\\\"" + boss.line + "\\\"\",\"color\":\"gold\",\"italic\":true}");
            }
        });
    }
});
