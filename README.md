# Syteme_de_surveillance

Ce projet consiste en la création d'un système de surveillance avancé utilisant la reconnaissance faciale. Le système est conçu pour identifier les visages connus et inconnus en temps réel, en utilisant une combinaison de Python, OpenCV, et Face Recognition.

1. Fonctionnalités:
   
Reconnaissance de visages connus et inconnus : Le système distingue entre les visages déjà enregistrés dans la base de données et les nouveaux visages.

Stockage des données : Utilisation de SQLite3 pour stocker les informations des visages connus et des Firebase pour les visages inconnus.

Mise à jour en temps réel : Les visages capturés par la caméra sont analysés en temps réel, avec une mise à jour instantanée des bases de données.

Interface utilisateur graphique : Affichage des informations et des images capturées via une interface utilisateur graphique intuitive.


2.Technologies utilisées: 

    Python : Langage de programmation principal.
    
    OpenCV : Bibliothèque pour le traitement d'images et de vidéos.
    
    Face Recognition : Bibliothèque de reconnaissance faciale pour Python.
    
    Firebase : Base de données en ligne pour stocker les visages inconnus.
    
    SQLite3 : Base de données locale pour les visages connus.
