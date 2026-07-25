"""Genere le logo du projet : une pousse verte, sobre.

Style volontairement minimal : aplats, une seule couleur verte, texte sombre,
aucun degrade ni effet. Produit docs/logo.png, le logo horizontal (marque +
texte) sur fond transparent, utilise dans le README, le rapport et la vitrine.

Dessine a grande echelle puis reduit, pour des bords nets (anticrenelage).
"""

from PIL import Image, ImageDraw, ImageFont

VERT = (46, 125, 50)        # #2E7D32
VERT_CLAIR = (232, 245, 233)  # #E8F5E9
TERRE = (121, 85, 72)       # #795548
SOMBRE = (33, 33, 33)       # #212121
GRIS = (117, 117, 117)      # #757575

S = 4  # facteur de suragrandissement


def _police(gras, taille):
    chemin = "C:/Windows/Fonts/arialbd.ttf" if gras else "C:/Windows/Fonts/arial.ttf"
    return ImageFont.truetype(chemin, taille * S)


def dessiner_marque(d, ox, oy, cote):
    """Dessine la marque dans un carre de cote donne, coin haut-gauche (ox, oy).

    Une pousse simple a deux feuilles symetriques, posee sur une ligne de sol.
    """
    r = cote // 5
    # Tuile arrondie vert clair.
    d.rounded_rectangle([ox, oy, ox + cote, oy + cote], radius=r, fill=VERT_CLAIR)

    cx = ox + cote // 2
    sol = oy + int(cote * 0.76)
    haut_tige = oy + int(cote * 0.24)

    # Tige.
    largeur_tige = max(2, cote // 18)
    d.line([(cx, sol), (cx, haut_tige)], fill=VERT, width=largeur_tige)

    # Deux feuilles symetriques, en forme de goutte, attachees en haut de la tige.
    def feuille(cote_gauche):
        L, H = int(cote * 0.30), int(cote * 0.16)
        calque = Image.new("RGBA", (L * 2, H * 2), (0, 0, 0, 0))
        ImageDraw.Draw(calque).ellipse([0, 0, L - 1, H - 1], fill=VERT)
        angle = 40 if cote_gauche else -40
        calque = calque.rotate(angle, expand=True, resample=Image.BICUBIC)
        bbox = calque.getbbox()
        calque = calque.crop(bbox)
        if cote_gauche:
            px = cx - calque.width + largeur_tige // 2
        else:
            px = cx - largeur_tige // 2
        py = haut_tige - calque.height // 3
        d._image.paste(calque, (px, py), calque)

    feuille(True)
    feuille(False)

    # Ligne de sol.
    d.line([(ox + r, sol), (ox + cote - r, sol)], fill=TERRE, width=max(2, cote // 36))


def generer_logo(largeur=1400, hauteur=420):
    img = Image.new("RGBA", (largeur * S, hauteur * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d._image = img

    cote = int(hauteur * 0.82)
    ox = int(hauteur * 0.09)
    oy = int(hauteur * 0.09)
    dessiner_marque(d, ox * S, oy * S, cote * S)

    tx = (ox + cote + int(hauteur * 0.14)) * S
    d.text((tx, int(hauteur * 0.28) * S), "AgroPredict", font=_police(True, 72), fill=SOMBRE)
    largeur_titre = d.textlength("AgroPredict", font=_police(True, 72))
    d.text((tx + largeur_titre + 16 * S, int(hauteur * 0.28) * S), "SN",
           font=_police(True, 72), fill=VERT)
    d.text((tx, int(hauteur * 0.60) * S), "Simulateur de rendement agricole",
           font=_police(False, 30), fill=GRIS)

    img = img.resize((largeur, hauteur), Image.LANCZOS)
    img.save("docs/logo.png")


if __name__ == "__main__":
    generer_logo()
    print("Logo genere : docs/logo.png")
