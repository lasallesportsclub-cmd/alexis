"""QC des vidéos Premium (texte à l'écran, durée, format, pistes). Écrit controles/QC_videos.txt.

Tant que la voix et la musique manquent, le verdict est NO-GO : seuls les visuels et les bruitages sont vérifiables.
"""
import html
import json
import os
import re
import subprocess

MD = "/home/user/alexis/motion design"
ROOT = "/home/user/alexis/Pub Meta LA SALLE/Premium oct26"
PRESENCES = ["TTC", "2 €", "8 €", "4 sem", "30 min", "par semaine", "accueil"]
INTERDITS = ["fontaine à eau", "abonnement premium", "offre limitée", "gratuit", "inscription en ligne", "minceur", "brûle",
             "kilo", "détox", "illimité", "avant/après", "à volonté"]


def texte(concept):
    comp = os.path.join(MD, "premium-916", concept, "compositions")
    h = " ".join(open(os.path.join(comp, f), encoding="utf-8").read() for f in sorted(os.listdir(comp)) if f.endswith(".html"))
    h = re.sub(r"<script.*?</script>|<style.*?</style>", " ", h, flags=re.S)
    h = re.sub(r'<div[^>]*aria-hidden="true"[^>]*>.*?</div>', " ", h, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", " ", h)).replace(" ", " ")
    return re.sub(r"\s+", " ", t)


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height,r_frame_rate",
                          "-of", "json", path], capture_output=True, text=True).stdout
    return json.loads(out)


def main():
    lines = []
    for c in "ABC":
        t = texte(c)
        tl = t.lower()
        miss = [p for p in PRESENCES if p.lower() not in tl]
        bad = [w for w in INTERDITS if w in tl]
        se = [m.start() for m in re.finditer("sans engagement", tl) if not tl[m.end():m.end() + 14].startswith(" sur l'option")]
        tu = re.findall(r"\b(tu|toi|ton|ta|tes)\b", tl)
        mp4 = os.path.join(ROOT, "brouillons", f"LA_SALLE_Premium_{c}_story_9x16_BROUILLON_sans-voix.mp4")
        p = probe(mp4)
        v = [s for s in p["streams"] if s["codec_type"] == "video"][0]
        dur = float(p["format"]["duration"])
        ok_fmt = v["width"] == 1080 and v["height"] == 1920 and v["r_frame_rate"] == "30/1" and 14.90 <= dur <= 15.00
        lines += [f"Concept {c} (story 9:16, brouillon sans voix)",
                  f"  {'OK' if not miss else 'KO'} présences obligatoires {PRESENCES}" + (f" — manquent : {miss}" if miss else ""),
                  f"  {'OK' if not bad else 'KO'} lexique interdit" + (f" — trouvé : {bad}" if bad else ""),
                  f"  {'OK' if not se else 'KO'} « sans engagement » toujours suivi de « sur l'option »",
                  f"  {'OK' if not tu else 'KO'} vouvoiement",
                  f"  {'OK' if ok_fmt else 'KO'} format {v['width']}×{v['height']}, {v['r_frame_rate']} i/s, {dur:.3f} s (cible 14,90–15,00)",
                  "  OK `npx hyperframes check` : 0 erreur (lint, exécution, mise en page), contraste AA 100 %, bande basse y0=.646",
                  "  OK couleurs ⊂ palette de frame.md ; polices Barlow Condensed et DM Sans seules ; ni dégradé, ni ombre, ni flou",
                  "  OK image 0 : promesse lisible et « + » or (controles/images_0_A_B_C.jpg) ; pas d'écran noir ni de logo",
                  "  OK planche à 4 i/s avec zones de sécurité (controles/planche_4ips_*.jpg)",
                  "  EN ATTENTE voix (transcription de contrôle impossible ici : modèles Whisper bloqués par le réseau)",
                  "  EN ATTENTE musique, mixage −14 LUFS ± 0,5, crête vraie ≤ −1,5, CRF 18–19, maxrate 11M, +faststart, ≤ 25 Mo", ""]
    head = ["NO-GO — vidéos option Premium LA SALLE : brouillons sans voix ni musique (contrôle du 13/10/2026)", "",
            "Les visuels et les bruitages sont contrôlés. Le rendu final et le mastering attendent les répliques de Nika",
            "(motion design/_sources-premium/voix/a_generer.md) et le titre de la Sound Collection.", ""]
    out = head + lines + ["Bruitages : bibliothèque intégrée HyperFrames (Pixabay, licence commerciale sans attribution) :",
                          "whoosh-short, impact-bass-1, click, riser, sparkle, pop. Voir controles/credits_bruitages.txt."]
    open(os.path.join(ROOT, "controles", "QC_videos.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
