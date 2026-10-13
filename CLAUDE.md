# HyperFrames (vidéo HTML → MP4)

Les 21 skills HyperFrames de HeyGen sont installés dans `.claude/skills/` et suivis dans `skills-lock.json`.
Point d'entrée : `/hyperframes`, qui oriente vers le bon workflow (`/motion-graphics`, `/product-launch-video`, `/general-video`, etc.).
Pour les mettre à jour : `npx skills update -p -y`.

## En session cloud

- Avant le premier rendu, lancer `npx hyperframes browser ensure`. Cette commande télécharge Chrome Headless Shell (~114 Mo), qui n'est pas conservé d'une session à l'autre.
- Le proxy bloque les CDN (`cdn.jsdelivr.net`, `unpkg.com`, `cdnjs.cloudflare.com`) ; seul le registre npm passe. Une composition qui charge GSAP depuis un CDN échoue au rendu avec `sub_timeline_script_failure`. Il faut alors copier GSAP dans le projet :

  ```sh
  npm pack gsap@3.14.2 && tar -xzf gsap-3.14.2.tgz package/dist/gsap.min.js \
    && mkdir -p vendor && mv package/dist/gsap.min.js vendor/ && rm -rf package gsap-3.14.2.tgz
  ```

  Remplacer ensuite l'URL du CDN par `vendor/gsap.min.js` dans `index.html`, et par `../vendor/gsap.min.js` dans `compositions/*.html`.
- Avec `npx hyperframes init`, ajouter `HYPERFRAMES_SKIP_SKILLS=1` pour qu'il ne réinstalle pas les skills.
