"""Discord MUD (Multi-User Dungeon) bot.

This application is a discord bot designed to run TinyFugue, a command
line mud/telnet client, and relay input and output back and forth
between the application and discord, allowing users to play via the
chat.

Warnings (SECURITY, PLEASE READ THIS):
    As TinyFugue allows commands that execute to the shell, you really
    need to set the '/restrict shell' command in the local.tf file of
    your tinyfugue install directory. '/restrict file' or '/restrict
    world' may be even better depending on your needs and who has access
    to the bot. Even with these commands, there is no guarantee of the
    security of this bot or of TinyFugue itself. Be careful!
    See this url for information on the /restrict command:
       https://northstar-www.dartmouth.edu/doc/tf/commands/restrict.html

    Unless you want people to have access to run commands on YOUR SERVER
    you will definitely want to follow the above advice!

Notes:
    This requires TinyFugue to work, and by default it expects tinyfugue
    to be installed in PATH and accessible with 'tf'.

    The game sessions are tied to the room they were initiated in. This
    helps allow multiple sessions to run at the same time, but only one
    per room.

    Currently the bot only sends text from the mud every two seconds,
    and immediately after a command is sent to the mud.

    There is no color support.

    A simpler implementation could be done with a telnet library, but it
    would lack some of the functions that tinyfugue provides.

    Currently there are a few extra personal functions I've added to the
    bot that are outside the realistic scope of this project. I plan to
    remove these functions later on.

    One Big File architecture is ugly but I personally prefer it for a
    bot like this.

Installing:
    Install python 3. I suggest using a virtual environment as well.

    I believe only discord.py is required from pip, 'pip install
    discord.py', but I will clean up my environment and if needed create
    a requirements.txt file, which would allow you to install
    dependencies with 'pip install -r requirements.txt'.

    Additionally, tinyfugue will be required. This bot has only been
    tested on debian, where you'd simply use 'sudo apt install tf'. See
    your OS's requirements for installing TinyFugue. I'm not sure how
    difficult it would be to modify this to work on Windows.

    For now, the interactive fiction function uses frobtads, which I
    believe I had to compile myself, but that functionality will likely
    be removed in the future.

    Python 2 might work with little modification, but it has not been
    tested.

Running:
    This bot takes no command line arguments. Simply 'python discordbot.py'
    or 'python3 discordbot.py' depending on your environment to start the
    bot.
    
    It will print out the app id, which you can use to create an invite
    link to invite the bot into servers. You can use
    'https://discordapp.com/oauth2/authorize?client_id=(bot_id)&scope=bot'
    link, substituting your bot id with (bot_id) [no parentheses] to add
    the bot to any servers you admin. You can also generate this link
    via the discord interface.

Chat Commands:
    The default prefix is % for bot commands, and $ for custom commands
    (see the 'prefix' command below, and the 'add' command for info on
    custom commands).

    Syntax in the discord chat is like most bots;
        '(prefix)(commandname) [args]'

    In the list below, (args) are required, and [args] are optional.

    Regular Commands:
        These commands work for everone unless their discord role in the
        server is blacklisted (see 'blacklist' command).

        -- help: Lists commands in the chat.

        -- mudstart: Starts a TinyFugue MUD session tied to the chat
            room. Output from the mud will be fed into only this room.

        -- mudstop: Stops the MUD session in the current room.

        -- md (command): Send command to TinyFugue in the current room
            session. See examples:
            '%md /help': This will send '/help' to TinyFugue, which will
                give general tinyfugue client help.
            '%md /connect discworld.starturtle.net 4242': Connect to the
                discworld MUD.
            '%md look at cabbage': Send the command 'look at cabbage' to
                the connected MUD. Has no effect if not connected to a
                MUD.

        -- / (command): Slightly shorter alias to the 'md' command.

        -- ifstart: (Not fully implemented) Similar to 'mudstart', but
            for interactive fiction via FrobTads. Not tied to a room
            session. It's not even tied to a server. To be removed.

        -- ifstop: End the global IF session.

        -- if: Similar to 'md' command, but sends command to the global
            interactive fiction session.

        -- i: Alias for 'if' command.

        -- say [text]: Make the bot say something. The bot currently
            listens to itself; it can trigger commands from itself.
            This can lead to infinite loops. That will likely be changed
            to default disabled, and only enabled by a command someday.

        -- randchoice (choices): 'Choices' should be separated ny a
            space. The bot will randomly say one of the choices.
            Example:
            '%randchoice yes no maybe': The bot will randomly say one
                of these options.

        -- randint (number, number): Responds with a random number
            between the two given numbers.

        -- roll [(num)d(num)]: Outputs a simulated die roll via the
            standard ndx pattern (sum of n dice x times). Defaults: 2d6.
        
        Custom commands: See 'add' command below. Use the custom command
            prefix to send custom commands. By default the custom prefix
            is '$', so if you created a custom command with '%add blah 
            https://docs.python.org/3/', you'd use '$blah' and the bot
            would respond with 'https://docs.python.org/3/' in the chat.
            Currently, this can be used to make shortcuts to other
            commands. Example:
            '%add roll100 %roll 1d100' would allow you to use
                '$roll100' to make the bot send '%roll 1d100', which
                would result in the bot rolling 1d100 per the '%roll'
                command above.

            This CAN be used to create infinite loops, so it will likely
            be added to an option and disabled by default. Be careful!

    Permission-required Commands:
        These commands can only be executed by the server admin(s) or by
        people with roles that are permitted (see 'perm' command),
        unless blacklisted.

        -- perm (role): Add a discord server role to the permitted list.
            Any member with this role will be able to use these
            permission-required commands, including permitting other
            roles. Be careful!

        -- unperm (role): Remove 'role' from the permitted list.

        -- prefix (character): Sets 'character' to the new prefix.
            Example:
            '%prefix !': The new prefix for standard bot commands will
                now be '!'. To use the say command in this case you
                would now use '!say'.

        -- add (custom command) (output): Add 'custom command' as a
            custom command in the current server which results in the
            bot sending 'output' to the chat. See 'Custom commands'
            above for more examples. Example:
            '%add hello Hi everyone!': Add the custom command 'hello',
                which allows users to type '$hello' (by default) to make
                the bot send 'Hi everyone!' to the chat.

        -- remove (custom command): Remove the custom command 'custom
            command' from the current server.

        -- customprefix (prefix): Change the prefix for custom commands
            to 'prefix'. You can make this the same as the regular
            prefix, it will check for standard commands first.

        -- addrandemotes: (To be removed) This will turn on random
            emotes on this server. Randomly, 1% of the time every
            message from a non-blacklisted member will be reacted by the
            bot with a server emote.

        -- remrandemotes: Remove this server from the random emotes.

        -- blacklist (role): Blacklist members from using the bot if
            they are under the 'role' discord role. This overrides the
            permitted roles as well as ADMIN status. The '@everyone'
            role cannot be added to this list. If you manage to
            blacklist everyone, including the admins, simply
            temporarily remove the discord role from an admin and
            'unblacklist' and/or permit as needed.

        -- unblacklist (role): Remove the discord role 'role' from the
            bot blacklist.

TODO:
    Clean up extra functionality of the bot that is outside the scope
    of the project (interactive fiction games, random emotes, etc).

    Possibly add a warning when run with shell access.

    More comments and documentation (help output, docstrings, etc)!

    Much better handling for incorrect command usage.

    Test if the bot can stay active for weeks at a time or if it
    occasionally disconnects, and find a fix for that if it does.

    Possibly improve telnet output, truncate large output files,
    or move away from using files entirely. If keeping the same
    output system, automatically create the folder for the files.

Bugs:
    Occasionally I have seen an ioctl error, probably related to the
    mud or the client trying to access or adjust terminal settings and
    sending an error message to chat because there is no terminal.
        Currently just filtering the error out of the output.

"""

import asyncio
import json
import os
import random
import re
import subprocess
import threading
import queue
import discord

srand = random.SystemRandom()

script_path = os.path.dirname(os.path.abspath(__file__))

tiny_fugue_path = "tf"

class BotApp(discord.Client):
    def __init__(self):
        super().__init__()
        self.mycmds = self.init_commands()
        self.restricted = self.init_restricted()
        self.game_sessions = {}
        self.bot_settings = self.load_settings()
        if not self.bot_settings:
            self.bot_settings = self.create_default_settings()
        
    async def on_ready(self):
        print(self.user.id)

    async def on_message(self, message_data):
        perms = self.bot_settings['permissions'].get(str(message_data.guild.id))
        if perms and perms.get('blacklist'):
            for role in message_data.author.roles:
                if str(role) in perms['blacklist']:
                    return
        if str(message_data.guild.id) in self.bot_settings.get('random_emote_servers'):
            if srand.randint(1, 100) == 1:
                emoji = srand.choice(message_data.guild.emojis)
                await message_data.add_reaction(emoji)
        if len(message_data.content.strip()) == 0:
            return
        await self.parse_cmd(message_data)

    async def bot_say(self, message_data):
        rm = message_data.channel
        full_text = message_data.content
        has_no_arg = True if full_text.find(" ") == -1 else False
        if has_no_arg:
            text = random.choice(['Boop', 'Sigh', 'Butt'])
        else:
            text = full_text[full_text.find(" ") + 1:]
        await rm.send(text)

    async def add_command(self, message_data):
        rm = message_data.channel
        if message_data.content.count(" ") < 2:
            await rm.send("Usage: %add [command name] [text]")
            return
        message = message_data.content[message_data.content.find(" ") + 1:]
        commands = self.bot_settings['custom_commands'].get(str(message_data.guild.id))
        if commands is None:
            self.bot_settings['custom_commands'][str(message_data.guild.id)] = {}
            commands = self.bot_settings['custom_commands'][str(message_data.guild.id)]
        command_name = message[:message.find(" ")].lower()
        if command_name in commands:
            await rm.send("Command {} already exists. Use %remove.".format(command_name))
            return
        commands[command_name] = message[message.find(" ") + 1:]
        self.save_settings()
        await rm.send("Command {} added.".format(command_name))

    async def remove_command(self, message_data):
        rm = message_data.channel
        if message_data.content.count(" ") != 1:
            await rm.send("Usage: %remove [command name]")
            return
        message = message_data.content[message_data.content.find(" ") + 1:].strip()
        commands = self.bot_settings['custom_commands'].get(str(message_data.guild.id))
        if commands is None:
            rm.send("No custom commands found.")
        command_name = message.lower()
        if command_name not in commands:
            await rm.send("Command {} not found.".format(command_name))
            return
        commands.pop(command_name)
        self.save_settings()
        await rm.send("Command {} removed.".format(command_name))


    async def list_commands(self, message_data):
        rm = message_data.channel
        prefix = self.get_prefix(message_data.guild.id)
        list1 = []
        for cmd in self.mycmds.keys():
            cmd_str = prefix + cmd
            if cmd not in self.restricted:
                list1.append(cmd_str)
        commands = self.bot_settings['custom_commands'].get(str(message_data.guild.id))
        if not commands:
            await rm.send("```\n" + ", ".join(list1) + "```")
        else:
            list2 = [self.get_prefix(message_data.guild.id, True) + cmd for cmd in commands.keys()]
            result = list1 + list2
            await rm.send("```\n" + ", ".join(result) + "```")
        restricted = [prefix + cmd for cmd in self.restricted]
        await rm.send("```\nPermitted roles only: " + ", ".join(restricted) + "```")

    async def random_choice(self, message_data):
        rm = message_data.channel
        termslist =  message_data.content.split(" ")
        if len(termslist) < 2:
            return
        choices = termslist[1:]
        chosen = random.choice(choices)
        await rm.send(chosen)

    async def random_int(self, message_data):
        rm = message_data.channel
        termslist = message_data.content.split(" ")
        if len(termslist) < 3:
            return
        nums = termslist[1:]
        try:
            num1 = int(nums[0])
            num2 = int(nums[1])
        except ValueError:
            return
        if num1 > num2:
            num1, num2 = num2, num1
        chosen = str(random.randint(num1, num2))
        await rm.send(chosen)

    async def roll_dice(self, message_data):
        rm = message_data.channel
        termslist = message_data.content.split(" ")
        if len(termslist) < 2:
            die_count = 2
            die_size = 6
            prefix = "2d6: "
        else:
            dice = termslist[1]
            dice_split = dice.split("d")
            try:
                die_count = int(dice_split[0])
                die_size = int(dice_split[1])
            except ValueError:
                return
            except IndexError:
                return
            prefix = str(die_count) + "d" + str(die_size) + ": "
        result = str(sum([random.randint(1, die_size) for x in range(die_count)]))
        await rm.send(prefix + result)

    async def add_rand_emote_server(self, message_data):
        servs = self.bot_settings['random_emote_servers']
        if str(message_data.guild.id) in servs:
            await message_data.channel.send("Server already added.")
            return
        servs.append(str(message_data.guild.id))
        await message_data.channel.send("Server added to random emotes.")
        self.save_settings()

    async def rem_rand_emote_server(self, message_data):
        servs = self.bot_settings['random_emote_servers']
        if str(message_data.guild.id) in servs:
            servs.pop(self.bot_settings['random_emote_servers'].index(str(message_data.guild.id)))
            await message_data.channel.send("Server removed from random emotes.")
            self.save_settings()
        else:
            await message_data.channel.send("Server not found.")

    async def start_if(self, message_data):
        rm = message_data.channel
        self.if_queue = queue.Queue()
        f = open("stdout", "w+")
        f2 = open("stdout", "r")
        self.sp = subprocess.Popen(["frob", "-i", "plain", "textgame/1893.gam"],
                stdin=subprocess.PIPE, stdout=f, stderr=subprocess.STDOUT)
        self.if_thread = threading.Thread(target=self.read_if_output, args=(self.sp,f2))
        self.if_thread.start()
        await rm.send("Starting IF game.")
        await self.send_if_output(rm)


    async def kill_if(self, message_data):
        self.sp.terminate()
        await message_data.channel.send("Killing IF game.")


    async def send_if_command(self, message_data):
        rm = message_data.channel
        line = " ".join(message_data.content.split(" ")[1:]) + "\n"
        if line == "esc\n":
            self.sp.stdin.write(b"\x1b")
        else:
            self.sp.stdin.write(line.encode("utf-8"))
        self.sp.stdin.flush()
        await asyncio.sleep(0.2)
        await self.send_if_output(rm)


    def read_if_output(self, process, stdout):
        while True:
            if process.poll() is not None:
                break
            line = stdout.readline()
            if line:
                self.if_queue.put(line)
        print("Thread dead")

    async def send_if_output(self, rm):
        result = []
        while not self.if_queue.empty():
            result.append(self.if_queue.get())
        if len(result) == 0 or not "".join(result).strip():
            print("IF trying to send no output.")
            return
        for i, line in enumerate(result):
            if len(line) > 1 and line[-1:] == "\n":
                result[i] = line[:-1] + " "
        return_string = "".join(result)
        while return_string.find("\n\n\n") != -1:
            return_string = return_string.replace("\n\n\n", "\n\n")
        while len(return_string) > 1700:
            await rm.send("```\n" + return_string[0:1700] + "```")
            return_string = return_string[1700:]
        await rm.send("```\n" + return_string + "```")

    def escape_ansi(self, line):
            ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
            return ansi_escape.sub('', line)

    async def start_mud(self, message_data):
        session = self.game_sessions.get(message_data.channel.id)
        if session:
            await message_data.channel.send("Session already started in this channel.")
            return
        self.game_sessions[message_data.channel.id] = session = {}
        session['queue'] = queue.Queue()
        session['stdout'] = open(os.path.join(script_path, "sessions", str(message_data.channel.id)), "w+")
        session['stdout2'] = open(os.path.join(script_path, "sessions", str(message_data.channel.id)), "r")
        session['sp'] = subprocess.Popen(
            [tiny_fugue_path, "-v"], stdin=subprocess.PIPE, stdout=session['stdout']
            )
        session['thread'] = threading.Thread(target=self.read_mud_output, args=(session,))
        session['thread'].start()
        session['channel'] = message_data.channel
        await session['channel'].send("Starting MUD.")
        await self.send_mud_output(session)


    async def kill_mud(self, message_data):
        session = self.game_sessions.get(message_data.channel.id)
        if session:
            try:
                session['sp'].terminate()
            except Exception as e:
                print(e)

            try:
                session['stdout'].close()
                session['stdout2'].close()
            except Exception as e:
                print(e)

            self.game_sessions.pop(message_data.channel.id)
            await message_data.channel.send("Killing MUD.")
        else:
            await message_data.channel.send("Unable to find session for this channel.")


    async def send_mud_command(self, message_data):
        session = self.game_sessions.get(message_data.channel.id)
        if session:
            line = " ".join(message_data.content.split(" ")[1:]) + "\n"
            session['sp'].stdin.write(line.encode("utf-8"))
            session['sp'].stdin.flush()
            await asyncio.sleep(0.2)
            await self.send_mud_output(session)
        else:
            await message_data.channel.send("No session found for this channel.")


    def read_mud_output(self, session):
        while True:
            if session['sp'].poll() is not None:
                break
            line = session['stdout2'].readline()
            if line:
                ioctl_error = '% TIOCGWINSZ ioctl: Inappropriate ioctl for device'
                if ioctl_error not in line:
                    session['queue'].put(line)
        print("Thread for " + str(session['channel'].id) + " killed.")

    async def send_mud_output(self, session):
        result = []
        while not session['queue'].empty():
            result.append(session['queue'].get())
        if len(result) == 0:
            return
        return_string = self.escape_ansi("".join(result))
        if not return_string.strip():
            return
        while len(return_string) > 1700:
            await session['channel'].send("```\n" + return_string[0:1700] + "```")
            return_string = return_string[1700:]
        await session['channel'].send("```\n" + return_string + "```")


    async def check_muds(self):
        await self.wait_until_ready()
        while not self.is_closed():
            try:
                for k, session in self.game_sessions.items():
                    try:
                        await self.send_mud_output(session)
                    except Exception as e:
                        pass
            except:
                pass
            await asyncio.sleep(2)

    async def add_perm(self, message_data):
        server = message_data.guild.id
        perms = self.bot_settings['permissions'].get(str(server))
        if perms is None:
            perms = self.bot_settings['permissions'][str(server)] = {
                    'perms': [],
                    'blacklist': [],
                    }
        rm = message_data.channel
        termslist = message_data.content.strip().split(" ")
        if len(termslist) == 1:
            if len(perms['perms']) == 0:
                await rm.send("No roles permitted.")
            else:
                await rm.send("Permitted roles: " + ", ".join(perms['perms']))
        else:
            newperm = " ".join(termslist[1:])
            if newperm in perms['perms']:
                await rm.send(newperm + " already in perms list.")
                return
            perms['perms'].append(newperm)
            self.save_settings()
            await rm.send(newperm + " role added to perms list.")

    async def rem_perm(self, message_data):
        server = message_data.guild.id
        perms = self.bot_settings['permissions'].get(str(server))
        if perms is None:
            perms = self.bot_settings['permissions'][str(server)] = {
                    'perms': [],
                    'blacklist': [],
                    }
        rm = message_data.channel
        termslist = message_data.content.strip().split(" ")
        if len(termslist) < 2:
            await rm.send("Enter a role to unpermit.")
            return
        remperm = " ".join(termslist[1:])
        if remperm in perms['perms']:
            perms['perms'].pop(perms['perms'].index(remperm))
            self.save_settings()
            await rm.send(remperm + " removed from perms list.")
        else:
            await rm.send(remperm + " not in perms list.")

    async def blacklist(self, message_data):
        server = message_data.guild.id
        perms = self.bot_settings['permissions'].get(str(server))
        if perms is None:
            perms = self.bot_settings['permissions'][str(server)] = {
                    'perms': [],
                    'blacklist': [],
                    }
        rm = message_data.channel
        termslist = message_data.content.strip().split(" ")
        if len(termslist) == 1:
            if len(perms['blacklist']) == 0:
                await rm.send("No roles blacklisted.")
            else:
                await rm.send("Blacklisted roles: " + ", ".join(perms['blacklist']))
        else:
            newbl = " ".join(termslist[1:])
            if newbl == "@everyone":
                await rm.send("Cannot blacklist @everyone. Please create a role for blacklisting.")
                return
            if newbl in perms['blacklist']:
                await rm.send(newbl + " already in blacklist.")
                return
            perms['blacklist'].append(newbl)
            self.save_settings()
            await rm.send(newbl + " role added to blacklist.")

    async def rem_blacklist(self, message_data):
        server = message_data.guild.id
        perms = self.bot_settings['permissions'].get(str(server))
        if perms is None:
            perms = self.bot_settings['permissions'][str(server)] = {
                    'perms': [],
                    'blacklist': [],
                    }
        rm = message_data.channel
        termslist = message_data.content.strip().split(" ")
        if len(termslist) < 2:
            await rm.send("Enter a role to unblacklist.")
            return
        rembl = " ".join(termslist[1:])
        if rembl in perms['blacklist']:
            perms['blacklist'].pop(perms['blacklist'].index(rembl))
            self.save_settings()
            await rm.send(rembl + " removed from blacklist.")
        else:
            await rm.send(rembl + " not in blacklist.")

    async def set_prefix(self, message_data):
        rm = message_data.channel
        termslist = message_data.content.split(" ")
        if len(termslist) != 2:
            return
        prefix = termslist[1]
        self.bot_settings['prefixes'][str(message_data.guild.id)] = prefix
        self.save_settings()
        await rm.send("Prefix for this server set to " + prefix)


    async def set_custom_prefix(self, message_data):
        rm = message_data.channel
        termslist = message_data.content.split(" ")
        if len(termslist) != 2:
            return
        prefix = termslist[1]
        self.bot_settings['custom_prefixes'][str(message_data.guild.id)] = prefix
        self.save_settings()
        await rm.send("Custom command prefix for this server set to " + prefix)


    async def parse_cmd(self, message_data):
        message = message_data.content
        prefix = self.get_prefix(message_data.guild.id)
        if message.startswith(prefix):
            if message.find(' ') == -1:
                cmd = message[len(prefix):].lower()
            else:
                cmd = message[len(prefix):message.find(' ')].lower()
            if cmd in self.restricted:
                if message_data.author.guild_permissions.administrator:
                    pass
                else:
                    permits = self.bot_settings['permissions'].get(str(message_data.guild.id))
                    if not permits or not permits.get('perms'):
                        return
                    user_roles = [str(x) for x in message_data.author.roles]
                    if not [x for x in permits['perms'] if x in user_roles]:
                            return
            if cmd in self.mycmds:
                await self.mycmds[cmd](message_data)
            return
        custom_prefix = self.get_prefix(message_data.guild.id, True)
        custom_cmds = self.bot_settings['custom_commands'].get(str(message_data.guild.id))
        if custom_cmds:
            if message.startswith(custom_prefix):
                cmd = message[len(custom_prefix):].strip().lower()
                if cmd in custom_cmds:
                    await message_data.channel.send(custom_cmds[cmd])


    def get_prefix(self, guild_id, custom=False):
        prefix_key = 'prefixes'
        default_key = 'default_prefix'
        if custom:
            prefix_key = 'custom_prefixes'
            default_key = 'default_custom_prefix'
        try:
            return self.bot_settings[prefix_key][str(guild_id)]
        except KeyError:
            return self.bot_settings[default_key]


    def create_default_settings(self):
        return {
            'default_prefix': "%",
            'prefixes': {},
            'default_custom_prefix': "$",
            'custom_prefixes': {},
            'custom_commands': {},
            'random_emote_servers': [],
            'permissions': {},
        }

    def save_settings(self):
        try:
            with open(os.path.join(script_path, "bot_settings"), "w+") as f:
                f.write(json.dumps(self.bot_settings))
        except Exception as e:
            print(e)

    def load_settings(self):
        try:
            with open(os.path.join(script_path, "bot_settings")) as f:
                settings = json.loads(f.read())
                if not 'permissions' in settings:
                    settings['permissions'] = {}
                return settings
        except Exception as e:
            print(e)

    def init_commands(self):
        return {
            "say": self.bot_say,
            "prefix": self.set_prefix,
            "customprefix": self.set_custom_prefix,
            "add": self.add_command,
            "remove": self.remove_command,
            "randchoice": self.random_choice,
            "randint": self.random_int,
            "roll": self.roll_dice,
            "addrandemotes": self.add_rand_emote_server,
            "remrandemotes": self.rem_rand_emote_server,
            "i": self.send_if_command,
            "if": self.send_if_command,
            "ifstop": self.kill_if,
            "ifstart": self.start_if,
            "/": self.send_mud_command,
            "md": self.send_mud_command,
            "mudstart": self.start_mud,
            "mudstop": self.kill_mud,
            "perm": self.add_perm,
            "unperm": self.rem_perm,
            "blacklist": self.blacklist,
            "unblacklist": self.rem_blacklist,
            "help": self.list_commands,
            }

    def init_restricted(self):
        return [
        "prefix", "customprefix", "add", "remove",
        "addrandemotes", "remrandemotes",
        "perm", "unperm", "blacklist", "unblacklist",
        ]


if __name__ == "__main__":
    with open(os.path.join(script_path, "bot_key")) as f:
        my_key = f.readline().replace("\n", "")
    bot_app = BotApp()
    bot_app.loop.create_task(bot_app.check_muds())
    bot_app.run(my_key)
    print("Finished processes, exiting.")

