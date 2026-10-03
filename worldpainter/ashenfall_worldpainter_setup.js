// =============================================================================
// ASHENFALL: WorldPainter JSR223 API Automated Synthesis Script
// World: Ashfall_Continent
// Dimensions: Y=-64 to Y=320 | Sea Level: Y=62
// Built with WorldPainter API Integration Engine v2.5
// =============================================================================

print("=====================================================================");
print("   ⚔ ASHENFALL — WorldPainter JSR223 API Synthesis ⚔");
print("   World: Ashfall_Continent");
print("   Elevation Range: [-64 -> 320] | Sea Level: 62");
print("=====================================================================");

// -----------------------------------------------------------------------------
// Smart Path Resolver (Inspects relative dir, Downloads, Desktop, or prompts)
// -----------------------------------------------------------------------------
function resolveFile(filename) {
    var f = new java.io.File(filename);
    if (f.exists()) {
        print(" -> Located file: " + f.getAbsolutePath());
        return f.getAbsolutePath();
    }

    var userHome = java.lang.System.getProperty("user.home");
    var searchPaths = [
        filename,
        "worldpainter/" + filename,
        "../worldpainter/" + filename,
        userHome + "/Downloads/" + filename,
        userHome + "/Downloads/ASHENFALL_WORLDPAINTER_SUITE/" + filename,
        userHome + "/Desktop/" + filename,
        userHome + "/Desktop/ASHENFALL_WORLDPAINTER_SUITE/" + filename,
        userHome + "/Documents/" + filename
    ];

    for (var i = 0; i < searchPaths.length; i++) {
        var candidate = new java.io.File(searchPaths[i]);
        if (candidate.exists()) {
            print(" -> Located file: " + candidate.getAbsolutePath());
            return candidate.getAbsolutePath();
        }
    }

    // Headless / GUI Fallback
    try {
        if (!java.awt.GraphicsEnvironment.isHeadless()) {
            print(" -> Prompting for file: " + filename);
            var chooser = new javax.swing.JFileChooser(userHome + "/Downloads");
            chooser.setDialogTitle("WorldPainter API: Please select " + filename);
            var result = chooser.showOpenDialog(null);
            if (result == javax.swing.JFileChooser.APPROVE_OPTION) {
                return chooser.getSelectedFile().getAbsolutePath();
            }
        }
    } catch (guiErr) {
        // Headless execution mode
    }

    throw new java.lang.RuntimeException("WorldPainter API Error: Could not locate " + filename);
}

function resolveTargetFilePath(target) {
    var userHome = java.lang.System.getProperty("user.home");
    var expanded = target.replace(/^~/, userHome);
    var targetFile = new java.io.File(expanded);
    if (targetFile.getParentFile() != null && !targetFile.getParentFile().exists()) {
        targetFile.getParentFile().mkdirs();
    }
    return targetFile.getAbsolutePath();
}

function resolveTargetDirectory(target) {
    var userHome = java.lang.System.getProperty("user.home");
    var expanded = target.replace(/^~/, userHome);
    var targetDir = new java.io.File(expanded);
    if (!targetDir.exists()) {
        targetDir.mkdirs();
    }
    return targetDir.getAbsolutePath();
}

// -----------------------------------------------------------------------------
// STEP 1: Load 16-Bit Master Topographic Heightmap
// -----------------------------------------------------------------------------
print("\n[1/5] Loading 16-bit Master Heightmap...");
var heightMapFile = resolveFile("worldpainter/ASHFALL_HEIGHTMAP_16BIT.png");
var heightMap = wp.getHeightMap()
    .fromFile(heightMapFile)
    .go();

// -----------------------------------------------------------------------------
// STEP 2: Create 3D World (Y=-64 to Y=320, Water=62)
// -----------------------------------------------------------------------------
print("\n[2/5] Sculpting 3D Continent Dimensions...");
var world = wp.createWorld()
    .fromHeightMap(heightMap)
    .scale(100)
    .shift(0, 0)
    .fromLevels(0, 65535).toLevels(-64, 320)
    .withWaterLevel(62)
    .withLowerBuildLimit(-64)
    .withUpperBuildLimit(320)
    .go();
print(" [✓] 3D World geometry initialized.");

// Optional Terrain Stratification
    wp.applyHeightMap(heightMap)
        .toWorld(world)
        .applyToTerrain()
        .fromLevels(-64, 64).toTerrain(36) // Ocean Floor & Coast
        .fromLevels(65, 140).toTerrain(0) // Fertile Lowlands & Valleys
        .fromLevels(141, 190).toTerrain(3) // Subalpine Heathlands
        .fromLevels(191, 250).toTerrain(74) // High Crags & Bare Rock
        .fromLevels(251, 320).toTerrain(40) // Glacial Summits & Permafrost
        .go();
    print(" [✓] Terrain stratification successfully applied.");


// -----------------------------------------------------------------------------
// STEP 3: Apply Still Life Pre-Population Layer (Foliage, Towns, Caverns)
// -----------------------------------------------------------------------------
print("\n[3/5] Applying Still Life Pre-Population Layer...");
try {
    var popMaskFile = resolveFile("worldpainter/ASHFALL_POPULATE_MASK.png");
    var popMask = wp.getHeightMap().fromFile(popMaskFile).go();
    var populateLayer = wp.getLayer().withName("Populate").go();

    wp.applyHeightMap(popMask)
        .toWorld(world)
        .applyToLayer(populateLayer)
        .fromLevels(128, 255).toLevel(1)
        .go();
    print(" [✓] Populate Layer applied across all valleys, forests, and settlements!");
} catch (e) {
    print(" [!] Note on Populate Layer: " + e);
}



// -----------------------------------------------------------------------------
// STEP 4: Apply High-Altitude Glacial Frost Layer
// -----------------------------------------------------------------------------
print("\n[4/5] Applying High-Altitude Glacial Frost Layer (Y >= 210)...");
try {
    var frostLayer = wp.getLayer().withName("Frost").go();
    wp.applyHeightMap(heightMap)
        .toWorld(world)
        .applyToLayer(frostLayer)
        .fromLevels(0, 209).toLevel(0)
        .fromLevels(210, 320).toLevel(1)
        .go();
    print(" [✓] Glacial Frost layer painted across high mountain peaks!");
} catch (e) {
    print(" [!] Note on Frost Layer: " + e);
}



// -----------------------------------------------------------------------------
// STEP 5: Save WorldPainter Master Project File (.world)
// -----------------------------------------------------------------------------
var saveTarget = resolveTargetFilePath("~/Downloads/Ashfall_Continent.world");
print("\n[5/5] Saving WorldPainter Master Project: " + saveTarget + "...");
wp.saveWorld(world).toFile(saveTarget).go();
print("\n=====================================================================");
print(" [✓] SUCCESS! Ashenfall continent project created and configured!");
print(" Saved to: " + saveTarget);
print("=====================================================================");