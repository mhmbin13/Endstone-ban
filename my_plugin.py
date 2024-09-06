from endstone.event import event_handler, PlayerJoinEvent
from endstone.plugin import Plugin
from endstone.command import Command, CommandSender
from endstone import Server
from endstone import ColorFormat
import ast

class MyPlugin(Plugin):
    api_version = "0.5"
    newbanlist = []

    def on_load(self) -> None:
        self.logger.info("Ban Plugin Loaded")
    def on_enable(self) -> None:
        self.logger.info("Ban Plugin Enabled")
        self.register_events(self)
        self.save_default_config()
    def on_disable(self) -> None:
        self.logger.info("Ban Plugin Disabled")


    commands = {
        "ban": {
            "description": "Bans a player",
            "usages": ["/ban [player: str]"],
            "permissions": ["ban.command.bans"]
        },
        "unban": {
            "description": "Unbans a player",
            "usages": ["/unban [player: str]"],
            "permissions": ["unban.command.unbans"]
        },
        "readblist": {
            "description": "See a list of banned players",
            "usages": ["/readblist"],
            "permissions": ["blist.command.readblist"]
        }
    }

    permissions = {
        "ban.command.bans": {
            "description": "Allow users to use the /ban command.",
            "default": "op",
        },
        "unban.command.unbans": {
            "description": "Allow users to use the /unban command.",
            "default": "op",
        },
        "blist.command.readblist": {
            "description": "Allow users to use the /readblist command.",
            "default": "op",
        }
    }

    @event_handler
    def on_player_join(self, event: PlayerJoinEvent):
        playername = event.player.name.lower()
        with open("plugins/ban/config.toml", "r") as f:
            bandataimp = f.read().lstrip('banlistdata=')
            if playername in ast.literal_eval(bandataimp):
                event.player.kick('§l§cYOU ARE BANNED FROM THIS GAME')


    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        if command.name == "ban":
            if len(args) == 0:
                sender.send_message("§cInvalid Argument. Try /ban [player]")
            else:
                sender.send_message("§l§aBanned: " + args[0].lower())
                newbanlist = ast.literal_eval(str(self.config.get('banlistdata')))
                newbanlist.append(args[0].lower())
                f = open("plugins/ban/config.toml", "w")
                f.write("banlistdata=" + str(newbanlist))
                f.close()
                self.server.dispatch_command(self.server.command_sender, f"kick {args[0].lower()} §l§cBANNED BY {sender.name}")


        if command.name == "readblist":
            try:
               with open("plugins/ban/config.toml", "r") as f:
                    sender.send_message(f"Banned players list: {ast.literal_eval(f.read().lstrip('banlistdata='))}")
            except FileNotFoundError:
                sender.send_message("§cNOT A VALID FILE: PLUGINS/BAN/CONFIG")


        if command.name == "unban":
            if len(args) == 0:
                sender.send_message("§cInvalid Argument. Try /unban [valid banned player]")
            else:
                plyrname = args[0].lower()
                newbanlist = ast.literal_eval(str(self.config.get('banlistdata')))
                if str(plyrname) in newbanlist:
                    newbanlist.remove(plyrname)
                    f = open("plugins/ban/config.toml", "w")
                    f.write("banlistdata=" + str(newbanlist))
                    f.close()
                    sender.send_message(f"§l§pUnbanned: {plyrname}")
                    return True
                sender.send_message('§c' + plyrname + ' is not a banned player')

        return True
    # ...