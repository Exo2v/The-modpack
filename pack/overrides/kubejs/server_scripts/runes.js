// =============================================================================
// ASHENFALL — The Nine Ember Runes System
// =============================================================================

var RUNES = [
    { id: "norman", item: "ashfall:rune_of_the_norman", nation: "norman_remnant", name: "Rune of Salt & Iron" },
    { id: "seljuk", item: "ashfall:rune_of_the_seljuk", nation: "seljuk_expanse", name: "Rune of Amber Sands" },
    { id: "choir", item: "ashfall:rune_of_the_choir", nation: "byzantine_choir", name: "Rune of Resonant Hymns" },
    { id: "witchbane", item: "ashfall:rune_of_the_witchbane", nation: "witchbane_watch", name: "Rune of the Cold Pyre" },
    { id: "merchants", item: "ashfall:rune_of_the_merchants", nation: "cogwork_march", name: "Rune of Gilded Cog & Steam" },
    { id: "ash", item: "ashfall:rune_of_the_ash", nation: "cathedral_of_ash", name: "Rune of the First Flame" },
    { id: "frostfall", item: "ashfall:rune_of_the_frostfall", nation: "frostfall", name: "Rune of Glacial Spires" },
    { id: "sunken", item: "ashfall:rune_of_the_sunken", nation: "sunken_throne", name: "Rune of the Abyss" },
    { id: "hermit", item: "ashfall:rune_of_the_hermit", nation: "hermits_reach", name: "Rune of Silent Peaks" }
];

function hasRune(player, runeId) {
    var r = null;
    for (var i = 0; i < RUNES.length; i++) {
        if (RUNES[i].id === runeId) {
            r = RUNES[i];
            break;
        }
    }
    if (!r) return false;
    
    // Check persistentData
    if (player.persistentData.getBoolean("has_rune_" + runeId)) {
        return true;
    }
    
    // Check if player has the item in inventory
    var inventory = player.inventory;
    if (inventory && inventory.find(r.item) !== -1) {
        player.persistentData.putBoolean("has_rune_" + runeId, true);
        return true;
    }
    return false;
}

function runeCount(player) {
    var count = 0;
    for (var i = 0; i < RUNES.length; i++) {
        if (hasRune(player, RUNES[i].id)) {
            count++;
        }
    }
    return count;
}
