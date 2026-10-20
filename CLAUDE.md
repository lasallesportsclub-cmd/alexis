# HyperFrames (vidéo HTML → MP4)

Les 21 skills HyperFrames de HeyGen sont installés dans `.claude/skills/` et suivis dans `skills-lock.json`.
Point d'entrée : `/hyperframes`, qui oriente vers le bon workflow (`/motion-graphics`, `/product-launch-video`, `/general-video`, etc.).
Pour les mettre à jour : `npx skills update -p -y`. La commande range les skills mis à jour dans `.agents/skills/` et laisse des liens symboliques dans `.claude/skills/`. Il faut les remplacer par de vraies copies, comme dans le reste du dépôt :

```sh
cd .claude/skills && for d in *; do [ -L "$d" ] && t=$(readlink -f "$d") && rm "$d" && cp -r "$t" "$d"; done; cd ../.. && rm -rf .agents
```

Pour vérifier qu'aucun skill nouveau n'est sorti : `npx skills add heygen-com/hyperframes --list`, à comparer avec `skills-lock.json`.

Tous les projets HyperFrames du dépôt sont figés sur `hyperframes@0.8.181` (vérifié le 20/10/2026, `check` OK sur les 17). Pour monter de version : `npx hyperframes@latest upgrade --project <dossier>`, puis `check`. GSAP reste en 3.14.2, la version que suivent les skills HyperFrames.

## Nouveautés des skills à appliquer (mise à jour du 20/10/2026)

- **Effets sonores :**
  - `media-use` cherche d'abord sur Openverse (CC0 / CC BY, sans compte). Openverse est bloqué en session cloud.
  - En repli : la bibliothèque intégrée, `.claude/skills/media-use/audio/assets/sfx/`, avec 19 sons Pixabay (whoosh, impacts, riser, pop…). Leur licence permet l'usage commercial sans attribution.
  - Pour une pub publiée : seulement nos sons synthétisés, la bibliothèque Pixabay ou du CC0. Un son CC BY impose un crédit là où la vidéo est publiée : à éviter en pub Meta. Jamais de NC, SA ou ND.
- **Vérification :**
  - Regarder les images en pleine résolution, pas seulement la planche : le début, chaque scène et chaque moment signalé.
  - Comparer l'aperçu (`snapshot`) et le rendu décodé aux mêmes instants. Exemple de test SSIM : `lasalle-nutrition-916/tools/livrer.py`.
  - Mettre les captures jetables dans un dossier temporaire, puis supprimer ce dossier. Ne jamais supprimer tout `.hyperframes`, qui contient l'historique du projet.
- **Storyboard :** la planche est maintenant `boards/storyboard.html`, avec des images dans `boards/stills/` capturées par `snapshot` à partir des cadres posés dans la composition. Il n'y a plus de croquis dessinés à part.
- **Suivi de consommation :** `npx hyperframes usage --json` renvoie aussi un champ `spend` (pour les forfaits facturés à l'usage).

## En session cloud

- Avant le premier rendu, lancer `npx hyperframes browser ensure`. Cette commande télécharge Chrome Headless Shell (~114 Mo), qui n'est pas conservé d'une session à l'autre.
- Le proxy bloque les CDN (`cdn.jsdelivr.net`, `unpkg.com`, `cdnjs.cloudflare.com`) ; seul le registre npm passe. Une composition qui charge GSAP depuis un CDN échoue au rendu avec `sub_timeline_script_failure`. Il faut alors copier GSAP dans le projet :

  ```sh
  npm pack gsap@3.14.2 && tar -xzf gsap-3.14.2.tgz package/dist/gsap.min.js \
    && mkdir -p vendor && mv package/dist/gsap.min.js vendor/ && rm -rf package gsap-3.14.2.tgz
  ```

  Remplacer ensuite l'URL du CDN par `vendor/gsap.min.js` dans `index.html`, et par `../vendor/gsap.min.js` dans `compositions/*.html`.
- Avec `npx hyperframes init`, ajouter `HYPERFRAMES_SKIP_SKILLS=1` pour qu'il ne réinstalle pas les skills.
- Outils audio locaux (whisper.cpp, Kokoro, MusicGen) : `bash "motion design/_outils/installer_audio_local.sh"` en début de session (≈ 10 min). Il faut `NODE_USE_ENV_PROXY=1` pour que `hyperframes transcribe` télécharge ses modèles à travers le proxy.
- MusicGen (`facebook/musicgen-small`) est sous licence CC-BY-NC 4.0 : jamais dans une vidéo publiée, maquettes internes seulement. Kokoro (Apache-2.0) et whisper.cpp (MIT) sont utilisables commercialement.
- Voix clonée : Chatterbox (MIT), dans son propre environnement (`bash "motion design/_outils/installer_chatterbox.sh"`, ≈ 10 min), puis `$CHATTERBOX_PYTHON "motion design/_outils/voix_clone.py" --ref ref.wav --texte "…" -o sortie.wav`. Référence : uniquement la voix d'une personne qui a signé `motion design/_voix-clone/Autorisation_clone_voix_A_SIGNER.pdf`. Enregistrements sur le Drive du club, jamais dans ce dépôt (public) : en session, les garder hors du dépôt (`~/voix-clone/`).
- Chatterbox laisse parfois une fin coupée, un débris en fin de fichier ou une pause trop longue : `voix_clone.py` applique `finition_voix.py` par défaut. Contrôler chaque réplique avec `whisper-cli` (texte complet) et `ressemblance_voix.py` (même voix ≈ 0,95 ; voix étrangère ≈ 0,65).
