import discord
import requests
import json
import random

# Créez les intentions
intents = discord.Intents.default()
#       intents.message_content = True  # Active l'intention pour envoyer et recevoir des messages
client = discord.Client(intents=intents)

sad_words = ["sad","depressed","unhappy","angry","miserable","depressing"]
starter_encouragements = ["Cheer up!",
                          "Hang in there",
                          "You are a great person ;)"]
a_deviner = ["Banane","Vampire","Smic","Bol","Chaussure"]


def getquote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)


    

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
#Maintenant que on a fait des petits trucs sympa on va faire un penduuuuuu
#Pour se faire on commence par faire une liste de mot que on veut deviner.

#On pourra etoffer plus tard le bestaire
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

async def lancement_pendu(message):
    trouve = []
    rd = random.randint(0, 4)
    await afficher(message, rd, trouve)
    compteur = 0
    while (compteur != len(a_deviner[rd])):
        await message.channel.send("Quelle lettre? \n")
        response = await client.wait_for('message', check=lambda m: m.author == message.author) #Rajouter le delai
        lettre = response.content.lower()  # Convertir la lettre entrée par l'utilisateur en minuscules
        if lettre in a_deviner[rd].lower():
            trouve.append(lettre)
            await ecrire(message, trouve, a_deviner[rd])

        else:
            compteur += 1
            await barre(message, compteur, a_deviner[rd], trouve)


async def afficher(message, indice_mot, trouve):
    mot = a_deviner[indice_mot]
    mot_affiche = ""
    for i, lettre in enumerate(mot):
        if i == 0 and lettre.lower() in trouve:
            mot_affiche += lettre + " "  # Affiche la première lettre si elle a été trouvée
        elif lettre.lower() in trouve:
            mot_affiche += lettre + " "  
        else:
            mot_affiche += "_ "  
    for _ in range(3):
        mot_affiche += "\n"
    await message.channel.send(mot_affiche)

    
async def ecrire(message, trouve, mot):
    mot_affiche = ""
    for i, lettre in enumerate(mot):
        if i == 0 and lettre.lower() in trouve:
            mot_affiche += lettre + " "  # Affiche la première lettre si elle a été trouvée
        elif lettre.lower() in trouve:
            mot_affiche += lettre + " "
        else:
            mot_affiche += "_ "
    await message.channel.send(mot_affiche)



async def barre(message, compteur, mot,trouve):          
    nb_erreur = len(mot) - compteur
    await message.channel.send("Il reste à faire " + str(nb_erreur) + " erreur(es)")
    await ecrire(message,trouve,mot)

async def fini(mot, trouve):
    for lettre in mot:
        if lettre.lower() not in trouve:
            return False
    return True


client.run('Your token')
