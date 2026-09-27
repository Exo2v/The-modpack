// =============================================================================
// ASHENFALL — NPC Narrative Dialogue Integration
// =============================================================================

var NPC_DIALOGUES = {
    "the_archivist": "ashfall:archivist",
    "norman_elder": "ashfall:norman_elder",
    "drowned_fisherman": "ashfall:drowned_fisherman"
};

EntityEvents.spawned(function(event) {
    var entity = event.entity;
    if (!entity) return;
    
    // Tag specific NPCs for dialogue interaction
    if (entity.tags && entity.tags.contains("ashfall_archivist")) {
        entity.persistentData.putString("adm_dialogue", NPC_DIALOGUES["the_archivist"]);
    }
});

// Global export for Rhino engine (explicit key-value pairs)
global.ASHFALL_DIALOGUE = {
    NPC_DIALOGUES: NPC_DIALOGUES
};
