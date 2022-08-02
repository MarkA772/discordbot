This is a python Discord Bot I made a few years ago. Random reactions, play MUDs
or Text Adventures in discord!

## Notes
The goal of this bot was to be able to play MUDs through discord via
chat commands you send to the bot. It uses a command line client called
TinyFugue. Later I added FrobTads client connectivity for playing
Interactive Fiction games through discord as well, but it's not fully
supported.

Some games will not work through Frobtads very well, or won't display
properly in plain text output, which is what the bot is able to parse.
Currently changing games requires changing settings on the clients
themselves.

The bot will also rarely add a random reaction from the server on any
message that comes in. This can be disabled through bot commands, but
it has proven to be quite entertaining.

--------------

## Warnings (SECURITY, PLEASE READ THIS):
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

### Notes:
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
    
### Installing:
  Install python 3. I suggest using a virtual environment as well.
  I believe only discord.py is required from pip, 'pip install
  discord.py', but I will clean up my environment and if needed create
  a requirements.txt file, which would allow you to install
  dependencies with 'pip install -r requirements.txt'.
  
  Additionally, tinyfugue will be required. This bot has only been
  tested on debian, where you'd simply use 'sudo apt install tf'. See
  your OS's requirements for installing TinyFugue. I'm not sure how
  difficult it would be to modify this to work on Windows.
  
### Running:
  This bot takes no command line arguments. Simply 'python discordbot.py'
  or 'python3 discordbot.py' depending on your environment to start the
  bot.

  It will print out the app id, which you can use to create an invite
  link to invite the bot into servers. You can use
  'https://discordapp.com/oauth2/authorize?client_id=(bot_id)&scope=bot'
  link, substituting your bot id with (bot_id) [no parentheses] to add
  the bot to any servers you admin. You can also generate this link
  via the discord interface.
    
### Chat Commands:
The default prefix is % for bot commands, and $ for custom commands
(see the 'prefix' command below, and the 'add' command for info on
custom commands).

Syntax in the discord chat is like most bots;
    '(prefix)(commandname) [args]'
    
In the list below, (args) are required, and [args] are optional.

#### Regular Commands:

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
        for interactive fiction via FrobTads. Currently not tied to a
        room session or server.
        
    -- ifstop: End the global IF session.
    
    -- if: Similar to 'md' command, but sends command to the global
        interactive fiction session.
        
    -- i: Alias for 'if' command.
    
    -- say [text]: Make the bot say something. The bot currently
        listens to itself; it can trigger commands from itself.
        This can lead to infinite loops. That will likely be changed
        to default disabled.
        
    -- randchoice (choices): 'Choices' should be separated ny a
        space. The bot will randomly say one of the choices.
        
        Example:
        
        '%randchoice yes no maybe': The bot will randomly say one
            of these options.
            
    -- randint (number, number): Responds with a random number
        between the two given numbers.
        
    -- roll [(num)d(num)]: Outputs a simulated die roll via the
        standard ndx pattern (sum of n dice x times). Defaults: 2d6.
        

#### Custom commands:
    
    See 'add' command below. Use the custom command
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

    This CAN be used to create infinite loops.
        
#### Permission-required Commands:

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

        
Bugs:
    Occasionally I have seen an ioctl error, probably related to the
    mud or the client trying to access or adjust terminal settings and
    sending an error message to chat because there is no terminal.
        Currently just filtering the error out of the output.
