# BOT_DBS
Bot discord prévu pour l'association UTC Décibels
Le bot permet 4 services : 
- redirection des mails dans un channel discord
- gestion des events avec une fonction de rappel de calendrier
- renommage des gens qui saisissent les mots 'je suis'
- gestion du rôle admin pour les futurs présidents 

## Technologies utilisées 

- Python (discord.py ...)
- Github actions pour la CI/CD
- Docker pour la conteneurisation et la facilité de déploiement
- MySQL pour la base de données 

## Installation en local
- Veuillez noter que le fichier de configuration `.env.default` donne une idée des informations à fournir depuis le `.env`
- Exécuter la commande `pip install -r requirements.txt` pour installer les dépendances en local dans un environnement python virtualvenv

## Déploiement
>Le déploiement s'éffectue de façon automatique grâce à un runner installé sur le serveur distant. Ce runner vérifier qu'aucune action n'a été déclenchée sur github régulièrement. Si c'est le cas alors il va exécuter ces actions. 
- Fichier qui permet le déploiement `deploy.yml`

## Attention
Ce bot n'a pas pour but d'être diffusé ou utilisé par d'autres personnes que l'association Décibels UTC-PAE. Vous noterez que dans les fichiers les messages ont étés configurés pour être envoyés dans des channels textuels précis. Si vous voulez réutiliser des parties, vous devrez changer l'id des channels dans lesquels les messages sont envoyés.

