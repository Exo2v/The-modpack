tp @s 0 68 2500
playsound minecraft:item.chorus_fruit.teleport ambient @s 0 68 2500 1.0 1.0
title @s times 10 50 15
title @s title {"text":"The Forgotten Coast","color":"green","bold":true}
title @s subtitle {"text":"[Spawn] (0, 68, 2500)","color":"gray"}
tellraw @s ["",{"text":"[Wayfinder] ","color":"gold"},{"text":"Arrived at The Forgotten Coast (0, 68, 2500). Expected: Plains, Meadow, Forest.","color":"green"}]
