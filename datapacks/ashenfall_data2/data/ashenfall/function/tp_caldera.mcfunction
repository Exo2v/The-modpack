tp @s 0 80 0
playsound minecraft:item.chorus_fruit.teleport ambient @s 0 80 0 1.0 1.0
title @s times 10 50 15
title @s title {"text":"The Ashen Caldera","color":"dark_red","bold":true}
title @s subtitle {"text":"[Center] (0, 80, 0)","color":"gray"}
tellraw @s ["",{"text":"[Wayfinder] ","color":"gold"},{"text":"Arrived at The Ashen Caldera (0, 80, 0). Expected: Basalt Deltas, Blackstone, Crater.","color":"dark_red"}]
