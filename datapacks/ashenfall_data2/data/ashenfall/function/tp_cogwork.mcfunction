tp @s -2000 85 0
playsound minecraft:item.chorus_fruit.teleport ambient @s -2000 85 0 1.0 1.0
title @s times 10 50 15
title @s title {"text":"The Cogwork March","color":"gold","bold":true}
title @s subtitle {"text":"[West] (-2000, 85, 0)","color":"gray"}
tellraw @s ["",{"text":"[Wayfinder] ","color":"gold"},{"text":"Arrived at The Cogwork March (-2000, 85, 0). Expected: Windswept Hills, River Canyons, Badlands.","color":"gold"}]
