// =============================================================================
// ASHENFALL — Custom Soulslike & Narrative Items Register (KubeJS Startup)
// =============================================================================

StartupEvents.registry('item', event => {
    // NOTE: Minecraft 1.21.1 Rarity enum only accepts:
    // 'common', 'uncommon', 'rare', 'epic'

    // 1. The Ember Flask (Key soulslike healing item)
    event.create('ashfall:ember_flask')
        .displayName('Ember Flask')
        .maxStackSize(1)
        .rarity('epic')
        .glow(true)
        .tooltip('§6A heavy ceramic flask bound in dark iron.')
        .tooltip('§7Smolders with residual warmth of the First Ember.')
        .tooltip('§8Rekindled only when resting at an ember site.');

    // 2. The Nine Ember Runes
    const RUNES = [
        { id: 'norman', name: 'Rune of Salt & Iron', lore: 'Kept by the Norman vanguard against the sea.' },
        { id: 'seljuk', name: 'Rune of Amber Sands', lore: 'Unearthed from the deep glass vaults beneath the dunes.' },
        { id: 'choir', name: 'Rune of Resonant Hymns', lore: 'Vibrates faintly with the lost psalm of the Empire.' },
        { id: 'witchbane', name: 'Rune of the Cold Pyre', lore: 'Cold iron branded with the oath of the marsh hunters.' },
        { id: 'merchants', name: 'Rune of Gilded Coin', lore: 'Weighed in silver, sealed in red wax of the high guild.' },
        { id: 'ash', name: 'Rune of the First Flame', lore: 'Charred stone that refuses to cool.' },
        { id: 'frostfall', name: 'Rune of Glacial Spires', lore: 'Etched in blue rime from the permafrost peaks.' },
        { id: 'sunken', name: 'Rune of the Abyss', lore: 'Dripping with abyssal salt from the drowned floor.' },
        { id: 'hermit', name: 'Rune of Silent Peaks', lore: 'Carved by those who walked into the clouds and forgot speech.' }
    ];

    RUNES.forEach(rune => {
        event.create('ashfall:rune_of_the_' + rune.id)
            .displayName(rune.name)
            .maxStackSize(1)
            .rarity('epic')
            .glow(true)
            .tooltip('§e' + rune.lore)
            .tooltip('§8Part of the Ninefold Sound of Creation.');
    });

    // 3. Narrative Items & Quest Artifacts
    event.create('ashfall:pilgrim_codex')
        .displayName('Pilgrim\'s Codex')
        .maxStackSize(1)
        .rarity('rare')
        .tooltip('§7A leather-bound journal inscribed with nine chapter slots.');

    event.create('ashfall:shattered_talisman')
        .displayName('Shattered Talisman')
        .maxStackSize(1)
        .rarity('uncommon')
        .tooltip('§8Fragments of the ancient ward that failed.');
});
