---
workflow: general-video
flow: automation
storyboard: no
format: story 1080×1920, 4 images + 4 vidéos de 5 s
---

# Brief : stories « Nutrimuscle et Nutripure, disponibles à l'accueil »

- **Demande d'Alexis (20/10/2026) :**
  - « sur le drive on a de la documentation pour nutrimuscle et nutripure prépare des story basé la dessus pour communiquer sur le fait que ses marques sont disponibles à l'accueil » ;
  - puis « base toi sur la direction artistique de nutripure et nutrimuscle disponible en analysant leur site et instagram ».
- **Compte :** LA SALLE (Urban Valley, Conflans-Sainte-Honorine), en vouvoiement.
- **Message unique :** les deux marques sont disponibles à l'accueil.
- **Sources :**
  - Drive « Partagés avec moi » : le dossier partenaire Nutripure ;
  - l'état du stock au 30/09/2026 ;
  - les commandes Nutrimuscle Pro et Nutripure (Gmail, lecture seule) ;
  - la photo du rayon de l'accueil.
- **Direction artistique :** voir `frame.md`. Les sites et Instagram des marques sont inaccessibles depuis la session.
- **Musique :** aucune. Elle s'ajoute dans Instagram. MusicGen est exclu.
- **Livraison :** « Pub Meta LA SALLE/Nutrition accueil oct26/ ». Les JPG et MP4 sont hors git, car ils contiennent le visuel partenaire avec des modèles.

Reconstruire : `python3 tools/build.py`, puis `npm run render -- --quality delivery -o renders/nutrition.mp4`, puis `python3 tools/livrer.py`.
