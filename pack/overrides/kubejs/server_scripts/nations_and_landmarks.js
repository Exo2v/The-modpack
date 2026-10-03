// =============================================================================
// ASHENFALL — The Nine Nations & Landmark Discovery System
// =============================================================================

var NATIONS = [
    {
        id: "norman_remnant",
        name: "The Norman Remnant",
        subtitle: "Frontier of Salt, Stone, and Iron",
        color: "aqua",
        biomes: ["minecraft:beach", "minecraft:stony_shore", "minecraft:windswept_hills", "minecraft:plains"],
        lore: "The last bastion of coastal knights holding watch against the rising tide."
    },
    {
        id: "seljuk_expanse",
        name: "The Seljuk Expanse",
        subtitle: "Scorched Steppes & Ancient Sun Vaults",
        color: "gold",
        biomes: ["minecraft:desert", "minecraft:badlands", "minecraft:eroded_badlands", "minecraft:savanna"],
        lore: "Nomadic riders and glass citadels buried beneath centuries of amber sand."
    },
    {
        id: "byzantine_choir",
        name: "The Byzantine Choir",
        subtitle: "Gilded Basilicas & Resonant Arches",
        color: "light_purple",
        biomes: ["minecraft:cherry_grove", "minecraft:meadow", "minecraft:flower_forest"],
        lore: "Scholars of the high empire whose harmonic chants once bound the world."
    },
    {
        id: "witchbane_watch",
        name: "The Witchbane Watch",
        subtitle: "Dark Thickets & The Silent Inquisition",
        color: "dark_green",
        biomes: ["minecraft:dark_forest", "minecraft:swamp", "minecraft:mangrove_swamp"],
        lore: "Hunters bound by iron oaths to cleanse the corrupted flora of the blight."
    },
    {
        id: "cogwork_march",
        name: "The Cogwork March",
        subtitle: "Steam Cities, Skyward Airships & Brass Canals",
        color: "gold",
        biomes: ["minecraft:windswept_hills", "minecraft:windswept_gravelly_hills", "minecraft:badlands", "minecraft:wooded_badlands", "minecraft:river", "minecraft:stony_shore"],
        lore: "The smog-choked industrial heartland of Vantyra. Massive steam cities, clunking brass cogwheels, and iron airships dominate the skyline, while forgotten foundries rust beneath."
    },
    {
        id: "cathedral_of_ash",
        name: "The Cathedral of Ash",
        subtitle: "Heart of the Blight — Seat of the First Ember",
        color: "dark_red",
        biomes: ["minecraft:nether_wastes", "minecraft:basalt_deltas", "minecraft:crimson_forest"],
        lore: "The charred epicenter where the first sound tore through the veil of reality."
    },
    {
        id: "frostfall",
        name: "The Frostfall",
        subtitle: "Glacial Spires & The Permafrost Gate",
        color: "blue",
        biomes: ["minecraft:snowy_slopes", "minecraft:frozen_peaks", "minecraft:ice_spikes", "minecraft:snowy_plains"],
        lore: "Eternal blizzards shielding the northern ruins of the Celestial Aether."
    },
    {
        id: "sunken_throne",
        name: "The Sunken Throne",
        subtitle: "Abyssal Trenches & The Drowned Choir",
        color: "dark_aqua",
        biomes: ["minecraft:deep_ocean", "minecraft:ocean", "minecraft:deep_cold_ocean"],
        lore: "Cathedrals submerged in deep trenches where the drowned clergy still pray."
    },
    {
        id: "hermits_reach",
        name: "The Hermit's Reach",
        subtitle: "Isolated Pinnacles & Silent Monasteries",
        color: "gray",
        biomes: ["minecraft:jagged_peaks", "minecraft:stony_peaks"],
        lore: "Ascetic hermits guarding forgotten scrolls beyond the reach of kings."
    }
];

// Check territory every 100 ticks (5 seconds)
PlayerEvents.tick(function(event) {
    try {
        var player = event.player;
        if (!player || player.age % 100 !== 0) return;
        if (!player.level) return;

        var biome = player.level.getBiome(player.blockPosition()).unwrapKey().get().location().toString();
        
        for (var i = 0; i < NATIONS.length; i++) {
            var nation = NATIONS[i];
            if (nation.biomes.indexOf(biome) !== -1) {
                var tag = "visited_nation_" + nation.id;
                if (!player.tags.contains(tag)) {
                    player.tags.add(tag);
                    
                    var server = player.level.server;
                    if (server) {
                        // Audio sting
                        server.runCommandSilent("playsound minecraft:ui.toast.challenge_complete ambient " + player.username + " " + player.x + " " + player.y + " " + player.z + " 0.8 1.1");
                        
                        // Territory banner
                        server.runCommandSilent("title " + player.username + " times 10 70 20");
                        server.runCommandSilent("title " + player.username + " title {\"text\":\"" + nation.name + "\",\"color\":\"" + nation.color + "\",\"bold\":true}");
                        server.runCommandSilent("title " + player.username + " subtitle {\"text\":\"" + nation.subtitle + "\",\"color\":\"gray\",\"italic\":true}");
                    }
                    
                    // Lore entry in chat
                    player.tell(" ");
                    player.tell("§8[§6Codex Discovered§8] §f" + nation.name);
                    player.tell("§7\"" + nation.lore + "\"");
                    player.tell(" ");
                }
                break;
            }
        }
    } catch (e) {
        // Silently prevent tick failure
    }
});
