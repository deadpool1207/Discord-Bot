import discord
from discord.ext import commands
from discord import app_commands
import config  # Importiere die Konfigurationsdaten

intents = discord.Intents.default()
intents.members = True  # Aktiviert Member-Events

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot ist online als {bot.user}!")
    try:
        synced = await bot.tree.sync()
        print(f"Slash Commands synchronisiert: {len(synced)} Befehle")
    except Exception as e:
        print(f"Fehler beim Synchronisieren der Slash Commands: {e}")


        
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(config.WELCOME_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="Willkommen!",
            description=f"Hey {member.mention}, willkommen auf **{member.guild.name}**! 🎉",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Hinweis:", value="Vergiss nicht, die Regeln zu lesen!")
        await channel.send(embed=embed)
    
    role = member.guild.get_role(config.DEFAULT_ROLE_ID)
    if role:
        await member.add_roles(role)
        print(f"Rolle {role.name} zu {member.name} hinzugefügt.")

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(config.LEAVE_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="Auf Wiedersehen!",
            description=f"{member.mention} hat den Server verlassen. 😢",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=member.avatar.url)
        await channel.send(embed=embed)


@bot.tree.command(name="setup_verification", description="Sende eine Verifizierungsnachricht.")
async def setup_verification(interaction: discord.Interaction):
    """Slash Command für die Verifizierungsnachricht."""
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Du hast keine Berechtigung, diesen Befehl zu verwenden.", ephemeral=True)
        return

    embed = discord.Embed(
        title="Verifiziere dich!",
        description="Klicke auf den Button unten, um dich zu verifizieren und Zugriff auf den Server zu erhalten.",
        color=discord.Color.blue()
    )

    button = discord.ui.Button(label="Verifizieren", style=discord.ButtonStyle.green, emoji="✅")

    async def button_callback(interaction: discord.Interaction):
        role = interaction.guild.get_role(config.VERIFY_ROLE_ID)
        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("Du wurdest erfolgreich verifiziert!", ephemeral=True)
            print(f"{interaction.user.name} wurde verifiziert.")
        else:
            await interaction.response.send_message("Die Verifizierungsrolle wurde nicht gefunden.", ephemeral=True)

    button.callback = button_callback
    view = discord.ui.View()
    view.add_item(button)

    await interaction.response.send_message(embed=embed, view=view)


bot.run(config.TOKEN)