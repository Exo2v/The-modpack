// =============================================================================
// ASHENFALL — Threat Tier Scaling Engine (Tiers I–VII)
// =============================================================================

var MAX_TIER = 7;

var REGIONS = [
    "norman_coast",
    "seljuk_desert",
    "byzantine_hills",
    "witchbane_woods",
    "cogwork_march",
    "merchant_rivers",
    "cathedral_depths",
    "frostfall_peaks",
    "sunken_abyss",
    "hermit_highlands"
];

function tierOf(player, region) {
    var key = "threat_tier_" + region;
    if (!player.persistentData.contains(key)) {
        player.persistentData.putInt(key, 1);
    }
    return player.persistentData.getInt(key);
}

function setTier(player, region, tier) {
    var clamped = Math.max(1, Math.min(MAX_TIER, tier));
    var key = "threat_tier_" + region;
    player.persistentData.putInt(key, clamped);
    player.tell("§8[§6Threat Scaled§8] §f" + region + " §7is now set to Threat Tier: §6" + clamped);
}

function regionOf(entity) {
    if (!entity || !entity.level) return "norman_coast";
    var dim = entity.level.dimension.toString();
    if (dim === "minecraft:the_nether") return "cathedral_depths";
    if (dim === "minecraft:the_end") return "sunken_abyss";

    var biome = entity.level.getBiome(entity.blockPosition()).unwrapKey().get().location().toString();
    if (biome.indexOf("desert") !== -1 || biome.indexOf("badlands") !== -1) return "seljuk_desert";
    if (biome.indexOf("dark_forest") !== -1 || biome.indexOf("swamp") !== -1) return "witchbane_woods";
    if (biome.indexOf("snow") !== -1 || biome.indexOf("ice") !== -1 || biome.indexOf("frozen") !== -1) return "frostfall_peaks";
    if (biome.indexOf("ocean") !== -1) return "sunken_abyss";
    if (biome.indexOf("jagged") !== -1 || biome.indexOf("stony_peaks") !== -1) return "hermit_highlands";
    if (biome.indexOf("cherry") !== -1 || biome.indexOf("meadow") !== -1) return "byzantine_hills";
    if (biome.indexOf("river") !== -1) return "merchant_rivers";
    return "norman_coast";
}
