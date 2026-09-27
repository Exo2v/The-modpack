// =============================================================================
// ASHENFALL — Structure Province & Landmark Registry
// =============================================================================

var STRUCTURE_PROVINCES = {
    "structory:settlements/coastal": { nation: "norman_remnant", name: "Norman Coastal Outpost" },
    "towns_and_towers:ocean/village": { nation: "norman_remnant", name: "Norman Port Village" },
    "structory:settlements/desert": { nation: "seljuk_expanse", name: "Seljuk Caravan Camp" },
    "dungeons_and_taverns:desert_pyramid": { nation: "seljuk_expanse", name: "Sunken Desert Crypt" },
    "graveyard:lich_prison": { nation: "frostfall", name: "Citadel of the Cold Tower" },
    "cataclysm:burning_arena": { nation: "cathedral_of_ash", name: "Crucible of Ash" },
    "cataclysm:sunken_city": { nation: "sunken_throne", name: "Submerged Cathedral of the Abyss" },
    "cataclysm:ancient_factory": { nation: "cogwork_march", name: "The Abandoned Foundry — Domain of the Clunker Behemoth" },
    "when_dungeons_arise:heavenly_challenger": { nation: "cogwork_march", name: "Imperial Brass Airship Dreadnought" },
    "when_dungeons_arise:corsair_corvette": { nation: "cogwork_march", name: "Skyward Raider Airship" },
    "when_dungeons_arise:aviary": { nation: "cogwork_march", name: "Aeronautics Clockwork Spire" }
};

function getProvinceForStructure(structureId) {
    return STRUCTURE_PROVINCES[structureId] || null;
}

// Global export for Rhino engine (explicit key-value pairs)
global.ASHFALL_STRUCTURES = {
    STRUCTURE_PROVINCES: STRUCTURE_PROVINCES,
    getProvinceForStructure: getProvinceForStructure
};

global.getProvinceForStructure = getProvinceForStructure;
