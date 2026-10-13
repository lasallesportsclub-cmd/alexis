"""Construit les projets d'images HyperFrames (scènes figées d'une seconde) à partir des cadres validés (frames.py).

Chaque image devient compositions/frames/NN.html (sous-composition), montée dans index.html à t = N−1 s.
Usage : python3 build_images.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import frames as F  # noqa: E402

MD = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CSS = open(os.path.join(MD, "_sources-premium", "shared", "premium.css"), encoding="utf-8").read()

PROJECTS = {
    "premium-visuels-916": (1920, [
        ("01", F.S1, "LA_SALLE_Premium_A_story_9x16"),
        ("02", F.S2, "LA_SALLE_Premium_B_story_9x16"),
        ("03", F.S3, "LA_SALLE_Premium_C_story_9x16"),
        ("04", F.S4, "LA_SALLE_Premium_offre_story_9x16"),
    ]),
    "premium-visuels-45": (1350, [
        ("01", F.P1, "LA_SALLE_Premium_A_post_4x5"),
        ("02", F.P2, "LA_SALLE_Premium_B_post_4x5"),
        ("03", F.P3, "LA_SALLE_Premium_C_post_4x5"),
        ("04", F.K1, "LA_SALLE_Premium_carrousel_1"),
        ("05", F.K2, "LA_SALLE_Premium_carrousel_2"),
        ("06", F.K3, "LA_SALLE_Premium_carrousel_3"),
        ("07", F.K4, "LA_SALLE_Premium_carrousel_4"),
        ("08", F.K5, "LA_SALLE_Premium_carrousel_5"),
    ]),
}


def frame_file(cid, h, inner):
    p45 = " p45" if h == 1350 else ""
    # le trait du carrousel déborde volontairement du cadre : décor seul, marqué comme tel
    inner = inner.replace('<svg class="a" style="left:0;top:0;width:1080px;height:1350px;overflow:visible"',
                          '<svg class="a" data-layout-allow-overflow style="left:0;top:0;width:1080px;height:1350px;overflow:visible"')
    return f"""<!doctype html>
<html lang="fr">
  <head><meta charset="UTF-8" /></head>
  <body>
    <template id="{cid}-template">
      <style>
{CSS}
        #root {{ position: absolute; inset: 0; }}
      </style>
      <div id="root" data-composition-id="{cid}" data-width="1080" data-height="{h}" data-duration="1">
        <div id="{cid}-fond" class="fr{p45} clip" data-start="0" data-duration="1" data-track-index="0">{inner}</div>
      </div>
      <script>
        const tl = gsap.timeline({{ paused: true }});
        window.__timelines["{cid}"] = tl;
      </script>
    </template>
  </body>
</html>
"""


def index_file(h, items):
    hosts = "\n".join(
        f'      <div id="h-{n}" data-composition-id="img-{n}" data-composition-src="compositions/frames/{n}.html" '
        f'data-start="{i}" data-duration="1" data-track-index="1" data-width="1080" data-height="{h}"></div>'
        for i, (n, _, _) in enumerate(items))
    return f"""<!doctype html>
<html lang="fr" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height={h}" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: {h}px; overflow: hidden; background: #0D0D0D; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #0D0D0D; }}
      [data-composition-id="main"] > div[data-composition-src] {{ position: absolute; inset: 0; }}
    </style>
  </head>
  <body>
    <!-- Images fixes : une scène figée d'une seconde par image, exportée par snapshot au milieu de la scène -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{len(items)}" data-width="1080" data-height="{h}" data-fps="30">
{hosts}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""


def main():
    for proj, (h, items) in PROJECTS.items():
        root = os.path.join(MD, proj)
        os.makedirs(os.path.join(root, "compositions", "frames"), exist_ok=True)
        for n, fn, _ in items:
            open(os.path.join(root, "compositions", "frames", f"{n}.html"), "w", encoding="utf-8").write(
                frame_file(f"img-{n}", h, fn()))
        open(os.path.join(root, "index.html"), "w", encoding="utf-8").write(index_file(h, items))
        print(proj, len(items), "images")


if __name__ == "__main__":
    main()
