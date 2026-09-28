tp @s 2500 75 0
playsound minecraft:item.chorus_fruit.teleport ambient @s 2500 75 0 1.0 1.0
title @s times 10 50 15
title @s title {"text":"The Gilded Dunes","color":"yellow","bold":true}
title @s subtitle {"text":"[East] (2500, 75, 0)","color":"gray"}
tellraw @s ["",{"text":"[Wayfinder] ","color":"gold"},{"text":"Arrived at The Gilded Dunes (2500, 75, 0). Expected: Desert, Badlands, Terracotta Mesas.","color":"yellow"}]
