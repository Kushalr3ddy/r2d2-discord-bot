import os
import discord
from discord.ext import commands
from random import randint,choice
from tester import check
import keep_alive
import wikipedia
import datetime as dt
import praw
import requests
from bs4 import BeautifulSoup as bs

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5)",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "accept-charset": "cp1254,ISO-8859-9,utf-8;q=0.7,*;q=0.3",
    "accept-encoding": "gzip,deflate,sdch",
    "accept-language": "en-US,en;q=0.8",
}

mods = []
cmd =";"
t = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
intents=discord.Intents.all()
client = commands.Bot(command_prefix= cmd,intents=intents)
#####events
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,activity=discord.Game(f"{cmd}help"))
    print(f"logged in as {client.user}")

@client.event
async def on_member_join(member):
    with open("joined.log","a") as f:
        f.write(f"{t}:{member} has joined\n")
    await member.send(f"Welcome! to DSU2024\nmake sure you select the role as per your section by reacting to the message in #section-roles")


@client.event
async def on_member_remove(member):
    with open("left.log","a") as f:
        f.write(f"\n{t}:{member} has left")
    #await member.send("Welcome! to DSU2024")

@client.event
async def on_message(ctx):
    
    if str(ctx.author) == str(client.user):
        return
    if str(ctx.author) in mods:
        return
    if ctx.content.startswith("http"):
            return
    #print(f"{now.strftime("%d/%m/%Y %H:%M:%S")}|{ctx.author}:{ctx.author.id}:{ctx.content}")
    """file1 = open("myfile.txt", "a")  # append mode 
    file1.write(f"{t}|:{id}{ctx.channel.id}:{ctx.author}:{ctx.content}\n")
    try:
        result = check(str(ctx.content))
    
        if result == True:
            with open("bad_language.txt","a") as f:
                f.write(f"{t}|{ctx.author}:{ctx.author.id}:{ctx.channel.id}:{ctx.content}")
            #me = await client.get_user_info(ctx.author)
            #await ctx.send_message(ctx.author, "#The message")
    except:
        pass"""
    await client.process_commands(ctx)
@client.command()
async def status(ctx):
    await ctx.send("https://r2d2-1610468848531.site24x7signals.com/")
###

#####commands
@client.command()
async def hello(ctx):
    """returns hello"""
    await ctx.send(f"hello there {ctx.author}")

@client.command()
async def joined(ctx,member:discord.Member):
    """Shows when a user joined the server"""
    await ctx.send(f"{member.name} joined on {member.joined_at}")

@client.command()
async def repeat(ctx,message,no=1):
    """Repeats a message
    usage:\n;repeat <your-message>"""
    if no <20:
        await ctx.send(f"{message}\n"*no)
    else:
        await ctx.send("max no of times a message can be repeated is 20")

@client.command()
async def roll(ctx):
    """random number between 1 to 6"""
    await ctx.send(f"{ctx.author} rolled a {randint(1,7)}")

@client.command()
async def flip(ctx):
    """flips a coin\nreturns heads or tails"""
    coin = ["heads","tails"]
    await ctx.send(f"{ctx.author} flipped {choice(coin)}")

@client.command()
async def source(ctx):
    """source code for the bot"""
    await ctx.send("https://github.com/kushalr3ddy/DSU2024-bot")

@client.command()
async def wiki(ctx,query,lines=2):
    """does wikipedia search (still under development)"""
    try:
        if len(query) == 0:
            await ctx.send("usage ;wiki [search]")
        else:
            await ctx.send(wikipedia.summary(query,lines))
    except:
        return
        #await ctx.send("search not found or some error has occured")

@client.command()
async def ping(ctx):
    """returns latency of the bot"""
    await ctx.send(f'Pong! {round(client.latency, 2)}')
    
@client.command()
async def meme(ctx):
    "gives a random meme from r/memes"

    reddit = praw.Reddit(client_id="if9tH2HtQ8NooA",
    client_secret=os.getenv("CLIENT_SECRET"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent="getmemes")
    subreddit = reddit.subreddit("memes")
    top = subreddit.top(limit=50)
    memes =[]
    for _ in top:
        memes.append(_)
    img = choice(memes)
    title = img.title
    src = img.url
    em = discord.Embed(title=title)
    em.set_image(url =src)
    await ctx.send(embed=em)

@client.command()
async def shorten(ctx,link):
    """shorten url"""
    re =requests.get(f"https://tinyurl.com/api-create.php?url={link}")
    await ctx.send(re.text)

@client.command()
async def insta(ctx,userid):
    """info related to insta_id (does not work for now)"""
    url = "https://instagram.com/{}".format(userid)
    re = requests.get(url,headers=headers)
    print(f"getting info {userid}")
    soup =bs(re.text,"html.parser")
    meta = soup.find("meta", property ="og:description")
    await ctx.send(meta.attrs['content'])

@client.command()
async def random(ctx,*,text:str):
    """returns text in RAnDOm case"""
    result =""
    for i in text:
        r = choice([1,0])
        if r == 1:
            i = i.upper()
            result+=i
        else:
            i = i.lower()
            result+=i
    await ctx.send(result)
###


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx,amount=1):
    """clears specified no of messages (default is 1)\n
    usage: ;clear <no-of-messages>"""
    await ctx.channel.purge(limit=amount+1)

def owner():
    async def predicate(ctx):
        return ctx.author.id == 679525489228251146
    return commands.check(predicate)


@client.command()
@owner()
async def set_prefix(ctx,prefix):
    """changes the command prefix of the bot"""
    client.command_prefix=prefix
    await ctx.send(f"prefix set to ```{prefix}```")

@set_prefix.error
async def clear_error(ctx, error):
    await ctx.send('command resticted only to developer (for now)')

@client.command()
@commands.has_permissions(manage_messages=True)
async def getusers(ctx, role: discord.Role):
    """gives a text file containing specified users having specified role"""
    members = role.members
    with open(f"{role}.txt","w") as log:
        log.write(f"members in the server as of:{t}\n")
        for member in members:
            log.write(f'{member.display_name}:{member.id}\n')
    
        await ctx.send('done')
    await ctx.send(file=discord.File(f'{role}.txt'))

@client.command()
@commands.has_permissions(manage_messages=True)
async def get_members(ctx):
    """gives a text file containing username of everyone in the server"""
    with open('members.txt','w') as f:
        f.write(f"{t}\n")
        async for member in ctx.guild.fetch_members(limit=None):
            print("{},{}".format(member,member.id), file=f,)
    await ctx.send(file=discord.File('members.txt'))
    print("done")



######error_handling
@client.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("arguments missing")
    elif isinstance(error,commands.MissingPermissions):
        await ctx.send("you're not allowed to do that")
    elif isinstance(error,commands.CommandNotFound):
        await ctx.send("command not found\ntype ;help for more info")




keep_alive.keep_alive()
client.run(os.getenv("TOKEN"))