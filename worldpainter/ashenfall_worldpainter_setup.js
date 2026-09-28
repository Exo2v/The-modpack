// =============================================================================
// ASHENFALL: WorldPainter Turnkey World Synthesis Script (v2.0)
// Auto-Locates Heightmaps in Downloads, Desktop, or prompts with File Picker
// =============================================================================

print("=====================================================================");
print("   ⚔ ASHENFALL — Synthesizing Pre-Populated Master World ⚔");
print("=====================================================================");

function resolveFile(filename) {
    // 1. Check relative to current working directory
    var f = new java.io.File(filename);
    if (f.exists()) {
        print(" -> Found: " + f.getAbsolutePath());
        return f.getAbsolutePath();
    }

    // 2. Check user's Downloads and Desktop folders
    var userHome = java.lang.System.getProperty("user.home");
    var searchPaths = [
        userHome + "/Downloads/" + filename,
        userHome + "/Downloads/ASHENFALL_WORLDPAINTER_SUITE/" + filename,
        userHome + "/Desktop/" + filename,
        userHome + "/Desktop/ASHENFALL_WORLDPAINTER_SUITE/" + filename,
        userHome + "/Documents/" + filename
    ];

    for (var i = 0; i < searchPaths.length; i++) {
        var candidate = new java.io.File(searchPaths[i]);
        if (candidate.exists()) {
            print(" -> Found in: " + candidate.getAbsolutePath());
            return candidate.getAbsolutePath();
        }
    }

    // 3. Fallback: Prompt user with native Windows File Chooser
    print(" -> Prompting for file: " + filename);
    var chooser = new javax.swing.JFileChooser(userHome + "/Downloads");
    chooser.setDialogTitle("Ashenfall: Please select " + filename);
    var result = chooser.showOpenDialog(null);
    if (result == javax.swing.JFileChooser.APPROVE_OPTION) {
        var selected = chooser.getSelectedFile().getAbsolutePath();
        print(" -> Selected: " + selected);
        return selected;
    }

    throw new java.lang.RuntimeException("File not found: " + filename);
}

// 1. Locate and Load 16-Bit Master Heightmap
print("\n[1/4] Locating 16-bit Master Heightmap...");
var heightMapPath = resolveFile("ASHENFALL_HEIGHTMAP_16BIT.png");
var heightMap = wp.getHeightMap()
    .fromFile(heightMapPath)
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
    var popMaskPath = resolveFile("ASHENFALL_POPULATE_MASK.png");
    var popMask = wp.getHeightMap()
        .fromFile(popMaskPath)
        .go();

    var populateLayer = wp.getLayer().withName("Populate").go();

    wp.applyHeightMap(popMask)
        .toWorld(world)
        .toLayer(populateLayer)
        .fromLevels(128, 255).toLevel(1)
        .go();
    print(" [✓] Populate Layer applied across all habitable valleys & plains!");
} catch (e) {
    print(" [!] Notice on Populate Layer: " + e);
}

// 4. Save the Pre-Populated Master Project in the user's Downloads or working dir
var userHome = java.lang.System.getProperty("user.home");
var saveTarget = userHome + "/Downloads/Ashenfall_Continent.world";
print("\n[4/4] Saving Pre-Populated Project: " + saveTarget + "...");

wp.saveWorld(world)
    .toFile(saveTarget)
    .go();

print("\n=====================================================================");
print(" [✓] SUCCESS! Ashenfall continent generated and pre-populated!");
print(" Saved to: " + saveTarget);
print(" You can now open it in WorldPainter and click:");
print(" File -> Export -> Export as Minecraft map...");
print("=====================================================================");
