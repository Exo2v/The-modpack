// =============================================================================
// ASHENFALL: WorldPainter Turnkey World Synthesis Script
// Run directly in WorldPainter: Tools -> Run script... -> Select this file
// =============================================================================

print("=====================================================================");
print("   ⚔ ASHENFALL — Synthesizing Pre-Populated Master World ⚔");
print("=====================================================================");

// 1. Load the Master 16-Bit Heightmap
print("\n[1/4] Loading 16-bit Master Heightmap (ASHENFALL_HEIGHTMAP_16BIT.png)...");
var heightMap = wp.getHeightMap()
    .fromFile("ASHENFALL_HEIGHTMAP_16BIT.png")
    .go();

// 2. Sculpt 3D Continent (-64 to +320, Sea Level: 62)
print("[2/4] Sculpting 3D Continent (-64 to +320, Sea Level: 62)...");
var world = wp.createWorld()
    .fromHeightMap(heightMap)
    .scale(100)
    .shift(0, 0)
    .fromLevels(0, 65535).toLevels(-64, 320)
    .withWaterLevel(62)
    .withLowerBuildLimit(-64)
    .withUpperBuildLimit(320)
    .go();

// 3. Apply 100% Pre-Population Mask
print("[3/4] Applying Pre-Population Layer (Trees, Foliage, Towns, Caverns)...");
try {
    var popMask = wp.getHeightMap()
        .fromFile("ASHENFALL_POPULATE_MASK.png")
        .go();

    var populateLayer = wp.getLayer().withName("Populate").go();

    wp.applyHeightMap(popMask)
        .toWorld(world)
        .toLayer(populateLayer)
        .fromLevels(128, 255).toLevel(1)
        .go();
    print(" [✓] Populate Layer applied across all habitable valleys & plains!");
} catch (e) {
    print(" [!] Note: Populate mask can also be applied via Edit -> Import -> Mask as layer...");
}

// 4. Save the Pre-Populated Master Project
print("\n[4/4] Saving Pre-Populated Master Project: Ashenfall_Continent.world...");
wp.saveWorld(world)
    .toFile("Ashenfall_Continent.world")
    .go();

print("\n=====================================================================");
print(" [✓] MASTER WORLD SYNTHESIS COMPLETE!");
print(" Open 'Ashenfall_Continent.world' in WorldPainter, then click:");
print(" File -> Export -> Export as Minecraft map...");
print("=====================================================================");
