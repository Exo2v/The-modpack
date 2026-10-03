// =============================================================================
// ASHENFALL — Admin & In-Game Command Register (Minecraft 1.21.1 / KubeJS)
// =============================================================================

ServerEvents.commandRegistry(function(event) {
    var Commands = event.commands;
    var Arguments = event.arguments;

    event.register(
        Commands.literal("ashenfall")
            .requires(function(source) { return source.hasPermission(2); })
            .then(Commands.literal("standing")
                .then(Commands.argument("player", Arguments.PLAYER.create(event))
                    .then(Commands.argument("faction", Arguments.STRING.create(event))
                        .then(Commands.argument("amount", Arguments.INTEGER.create(event))
                            .executes(function(ctx) {
                                var player = Arguments.PLAYER.getResult(ctx, "player");
                                var faction = Arguments.STRING.getResult(ctx, "faction");
                                var amount = Arguments.INTEGER.getResult(ctx, "amount");
                                if (typeof modifyStanding === "function") {
                                    modifyStanding(player, faction, amount);
                                }
                                return 1;
                            })
                        )
                    )
                )
            )
            .then(Commands.literal("threat")
                .then(Commands.argument("player", Arguments.PLAYER.create(event))
                    .then(Commands.argument("region", Arguments.STRING.create(event))
                        .then(Commands.argument("tier", Arguments.INTEGER.create(event))
                            .executes(function(ctx) {
                                var player = Arguments.PLAYER.getResult(ctx, "player");
                                var region = Arguments.STRING.getResult(ctx, "region");
                                var tier = Arguments.INTEGER.getResult(ctx, "tier");
                                if (typeof setTier === "function") {
                                    setTier(player, region, tier);
                                }
                                return 1;
                            })
                        )
                    )
                )
            )
            .then(Commands.literal("rumour")
                .then(Commands.argument("player", Arguments.PLAYER.create(event))
                    .then(Commands.argument("id", Arguments.STRING.create(event))
                        .executes(function(ctx) {
                            var player = Arguments.PLAYER.getResult(ctx, "player");
                            var id = Arguments.STRING.getResult(ctx, "id");
                            if (typeof tellRumour === "function") {
                                tellRumour(player, id);
                            }
                            return 1;
                        })
                    )
                )
            )
    );
});
