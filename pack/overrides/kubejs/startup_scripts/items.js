// =============================================================================
// ASHENFALL — Custom Item Registry (Startup Script)
// Minecraft 1.21.1 NeoForge / KubeJS
// =============================================================================

StartupEvents.registry('item', event => {
    // NOTE: Minecraft 1.21.1 Rarity enum only accepts:
    // 'common', 'uncommon', 'rare', 'epic'
    // ('legendary' does NOT exist in vanilla Rarity enum and will throw IllegalArgumentException)

    // 1. The Ember Flask (Key soulslike healing item)
    event.create('ashfall:ember_flask')
        .displayName('§6Ember Flask')
        .rarity('epic')
        .maxStackSize(1)
        .glow(true)
        .tooltip('§7A brass vessel housing a captive flame.')
        .tooltip('§eRefills only when resting at a Campfire or Waystone.');

    // 2. The Nine Ember Runes
    const RUNES = [
        { id: 'rune_of_flame', name: '§cRune of Flame', lore: 'Ember of the First Fall' },
        { id: 'rune_of_salt', name: '§bRune of Salt', lore: 'Ember of the Norman Bastion' },
        { id: 'rune_of_sand', name: '§eRune of the Sun', lore: 'Ember of the Seljuk Dunes' },
        { id: 'rune_of_whispers', name: '§dRune of Whispers', lore: 'Ember of the Byzantine Choir' },
        { id: 'rune_of_witchbane', name: '§2Rune of Witchbane', lore: 'Ember of the Inquisition' },
        { id: 'rune_of_gold', name: '§6Rune of Commerce', lore: 'Ember of the Merchant Guild' },
        { id: 'rune_of_frost', name: '§9Rune of Frost', lore: 'Ember of the Glacial Gate' },
        { id: 'rune_of_abyss', name: '§1Rune of the Abyss', lore: 'Ember of the Sunken Throne' },
        { id: 'rune_of_peaks', name: '§7Rune of the Peaks', lore: 'Ember of the Hermit Sanctuary' }
    ];

    RUNES.forEach(rune => {
        event.create(`ashfall:${rune.id}`)
            .displayName(rune.name)
            .rarity('epic')
            .maxStackSize(1)
            .glow(true)
            .tooltip(`§8${rune.lore}`);
    });

    // 3. Narrative Items & Artifacts
    event.create('ashfall:labyrinth_thread')
        .displayName('§eAriadne\'s Thread')
        .rarity('rare')
        .maxStackSize(16)
        .tooltip('§7Phosphorescent thread that marks paths in deep catacombs.');

    event.create('ashfall:pilgrims_journal')
        .displayName('§6The Pilgrim\'s Journal')
        .rarity('epic')
        .maxStackSize(1)
        .tooltip('§7Waterlogged pages recording the Nine Sounds of Vantyra.');

    event.create('ashfall:codex_fragment')
        .displayName('§fCodex Fragment')
        .rarity('uncommon')
        .maxStackSize(64)
        .tooltip('§7Ancient parchment inscribed with fragmented imperial annals.');
});
