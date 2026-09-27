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
    "cataclysm:sunken_city": { nation: "sunken_throne", name: "Submerged Cathedral of the Abyss" }
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
