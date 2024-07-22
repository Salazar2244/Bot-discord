import discord
import requests
import json
import random

# Créez les intentions
intents = discord.Intents.default()
# intents.message_content = True  # Active l'intention pour envoyer et recevoir des messages
client = discord.Client(intents=intents)
URL_RICK ="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExaXNoNm1iMXF4czh6cnJ3Z2s5d3R1ZnoxeHJwZGIzOWJ4cmk4NXZ5ZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/7Ob5uwAwmTWLe/giphy.webp"

sad_words = [
    "sad", "depressed", "unhappy", "angry", "miserable", "depressing",
    "melancholic", "heartbroken", "despondent", "downcast", "woeful",
    "sorrowful", "glum", "distressed", "forlorn", "triste", "déprimé",
    "malheureux", "misérable", "désespéré", "chagriné", "abattu",
    "accablé", "découragé", "lamentable", "défaitiste", "morne", "répugnant",
    "éploré"
]

starter_encouragements = [
    "Cheer up!", "Hang in there", "You are a great person ;)",
    "Keep going!", "You've got this!", "Stay positive!", "Believe in yourself!",
    "You're doing great!", "Stay strong!", "Don't give up!", "You've come so far!",
    "Things will get better!", "You're amazing!", "You can do it!", "Keep pushing forward!",
    "Stay hopeful!", "You matter!", "Don't lose hope!", "You're a star!", "Everything will be okay!",
    "Reste positif !", "Tu es formidable !", "Continue comme ça !", "Tu peux le faire !",
    "Accroche-toi !", "N'abandonne pas !", "C'est super ce que tu fais !", "Garde espoir !",
    "Tu es incroyable !", "Tout ira bien !", "Tu es fort(e) !", "Crois en toi !", "Tu es sur la bonne voie !",
    "Les choses vont s'améliorer !", "Tu es un champion !", "Reste courageux(se) !"
]

a_deviner = ["Banane", "Vampire", "Smic", "Bol", "Chaussure"]


def getquote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content
    if msg.startswith('$inspire'):
        quote = getquote()
        await message.channel.send(quote)
    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(starter_encouragements))
    if msg.startswith('$hangman'):
        await lancement_pendu(message)
    if message.author.id == 1230759955808649247:
        await reactionClaire(message)
    if  message.author.id == 345595984212131840:
        await reactionNoé(message)
    if (messageContainRick(message) == True) :
        message.channel.send(URL_RICK)


async def messageContainRick(message):
    compteur = 0  
    messageContent = message.content.lower()

    if 'r' in messageContent:
        compteur += 1
    if 'i' in messageContent:
        compteur += 1
    if 'c' in messageContent:
        compteur += 1
    if 'k' in messageContent:
        compteur += 1
        
    if(compteur == 4):
        return True
    else:
        return False
    
async def reactionNoé(message):
    nombre = random.randint(0,100)
    if (nombre > 75) : 
        await message.add_reaction('💪')
    if(nombre <50):
        if(nombre <25):
            await message.add_reaction('👑')
        if(nombre<12):
            await message.add_reaction('😘')
        
        else:
            await message.add_reaction('🫡')
        
async def reactionClaire(message):
    nombre = random.randint(0,100)
    if (nombre > 75) : 
        await message.add_reaction('👀')
    if(nombre<50):
        if(nombre<25):
            await message.add_reaction('🥶')
        else:
            await message.add_reaction('😈')

        
        
async def lancement_pendu(message):
    trouve = []
    rd = random.randint(0, 4)
    await afficher(message, rd, trouve)
    compteur = 0
    while compteur != len(a_deviner[rd]):
        await message.channel.send("Quelle lettre? \n")
        response = await client.wait_for('message', check=lambda m: m.author == message.author)
        lettre = response.content.lower()
        if lettre in a_deviner[rd].lower():
            trouve.append(lettre)
            await ecrire(message, trouve, a_deviner[rd])
            if await fini(a_deviner[rd], trouve):
                await message.channel.send("Bravo, vous avez deviné le mot!")
                return
        else:
            compteur += 1
            await barre(message, compteur, a_deviner[rd], trouve)
            if compteur == len(a_deviner[rd]):
                await message.channel.send("Désolé, vous avez perdu. Le mot était: " + a_deviner[rd])
                return


async def afficher(message, indice_mot, trouve):
    mot = a_deviner[indice_mot]
    mot_affiche = ""
    for lettre in mot:
        if lettre.lower() in trouve:
            mot_affiche += lettre + " "
        else:
            mot_affiche += "_ "
    await message.channel.send(mot_affiche)


async def ecrire(message, trouve, mot):
    await afficher(message, a_deviner.index(mot), trouve)


async def barre(message, compteur, mot, trouve):
    nb_erreur = len(mot) - compteur
    await message.channel.send("Il vous reste " + str(nb_erreur) + " erreur(s)")
    await ecrire(message, trouve, mot)


async def fini(mot, trouve):
    for lettre in mot:
        if lettre.lower() not in trouve:
            return False
    return True


client.run('key')
