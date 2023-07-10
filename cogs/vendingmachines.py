from discord import app_commands
from discord.ext import commands, tasks
import discord
import json
from typing import List
from rustplus import RustMarker, convert_xy_to_grid, RustSocket


class vending(commands.Cog):
    def __init__(self, client):
        print("[Cog] Vending Machines has been initiated")
        self.client = client
        self.sockets = {}

    with open("./json/config.json", "r") as f:
        config = json.load(f)
    with open("./json/items.json", "r") as f:
        items_list = json.load(f)

    server_names = []
    count = 1
    for server in config['servers']:
        servername = server['name']
        server_names.append(app_commands.Choice(
            name=f"{servername}", value=count))
        count += 1

    @ commands.Cog.listener()
    async def on_ready(self):
        print("Establishing Rust+ connections..")
        servers = self.config['servers']
        for server in servers:
            new_socket = RustSocket(server['server_ip'], server['server_port'],
                                    server['rust_plus_steamid'], server['rust_plus_player_token'])
            await new_socket.connect()
            self.sockets[server['name']] = {"socket": new_socket, "map_size": (await new_socket.get_info()).size}
        print("Rust+ connections established.")
        await self.vendtester.start()

    async def autocomplete(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        choices = []
        for item in self.items_list:
            choices.append(self.items_list[item]['name'])
        if current:
            return [
                app_commands.Choice(name=choice, value=choice)
                for choice in choices if current.lower() in choice.lower()
            ]
        else:
            default = choices[:25]
            return [app_commands.Choice(name=d, value=d) for d in default]

    @ app_commands.command(name="vendingsearch", description="Searches The Rust Server's Vending Machine")
    @ app_commands.guild_only()
    @ app_commands.describe(item="List of items")
    @ app_commands.describe(server="Select a server")
    @ app_commands.choices(server=[*server_names])
    @app_commands.autocomplete(item=autocomplete)
    async def search(self, interaction: discord.Interaction, server: app_commands.Choice[int], item: str):
        await interaction.response.defer()
        item = item.lower()

        embed = discord.Embed(title=f"Showing vending machine data for: '**{item}**'", color=int(
            self.config['cogs']['color'], base=16))
        for i in self.items_list:
            if self.items_list[i]['name'].lower() == item or self.items_list[i]['shortname'].lower() == item:
                embed.set_thumbnail(url=self.items_list[i]['link'])
                break
        for socket in self.sockets:
            if str(server.name).lower() == str(socket).lower():
                servername = socket
                sock = self.sockets[servername]['socket']
                socketmarkers = await sock.get_markers()
                markers = []
                for marker in socketmarkers:
                    markers.append(marker)
                item_list = None
                for marker in markers:
                    if marker.type != RustMarker.VendingMachineMarker:
                        continue
                    for sell_order in marker.sell_orders:
                        if str(sell_order.item_id) in self.items_list:
                            sell_order_item = str(
                                self.items_list[f"{sell_order.item_id}"]['name']).lower()
                        else:
                            sell_order_item = None

                        if sell_order_item == item:
                            grid = convert_xy_to_grid(
                                (marker.x, marker.y), self.sockets[servername]['map_size'], False)
                            grid = ''.join(str(item) for item in grid)
                            currency_name = self.items_list[f"{sell_order.currency_id}"]['name']
                            if item_list:
                                item_list += f"\n[Grid: {grid}] - Selling for: {sell_order.cost_per_item} {currency_name}"
                            else:
                                item_list = f"[Grid: {grid}] - Selling for: {sell_order.cost_per_item} {currency_name}"

                if item_list:
                    embed.add_field(name=f"{servername} vending machine data!",
                                    value=f"```{item_list}```", inline=False)
                else:
                    embed.add_field(name=f"{servername} vending machine data!",
                                    value=f"```Item not being sold on this server. Start capitalizing on this right now!```", inline=False)
        embed.set_footer(
            text="Discord bot created by Gnomeslayer, using Rust+ wrapper created by Ollie.")
        await interaction.followup.send(embed=embed)
        
        
async def setup(client):
    await client.add_cog(vending(client))
