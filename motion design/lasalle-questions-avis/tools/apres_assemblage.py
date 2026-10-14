"""Retouche index.html après assemble-index.mjs (à relancer après chaque assemblage).

- GSAP en local (assets/vendor/gsap.min.js) : les CDN sont bloqués dans le conteneur.
- Langue du document : français.
Idempotent.

Usage : python3 tools/apres_assemblage.py
"""
import os
import re

ICI = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(ICI, "..", "index.html")

html = open(INDEX, encoding="utf-8").read()
html = re.sub(r'<script src="https://cdn\.jsdelivr\.net/npm/gsap@[^"]+"[^>]*></script>',
              '<script src="assets/vendor/gsap.min.js"></script>', html)
html = html.replace('<html lang="en">', '<html lang="fr">')
open(INDEX, "w", encoding="utf-8").write(html)
print("index.html : GSAP local, lang=fr")
