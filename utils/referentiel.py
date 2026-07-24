"""Source unique des valeurs autorisees en entree du modele.

Le modele est entraine sur des libelles sans accent (Thies, Mais, Sedhiou).
L'interface, elle, affiche les libelles corrects en francais (Thies -> Thies).
Ce module fait le lien entre les deux et interdit toute valeur inconnue.

Sans ce module, une valeur non reconnue par l'encodeur produisait un vecteur
nul et donc une prediction silencieusement fausse.
"""


# Cle = valeur apprise par le modele, valeur = libelle affiche a l'utilisateur.
REGIONS = {
    "Thies":       "Thiès",
    "Fatick":      "Fatick",
    "Kaolack":     "Kaolack",
    "Saint-Louis": "Saint-Louis",
    "Kaffrine":    "Kaffrine",
    "Tambacounda": "Tambacounda",
    "Sedhiou":     "Sédhiou",
}

CULTURES = {
    "Arachide": "Arachide",
    "Mil":      "Mil",
    "Mais":     "Maïs",
    "Riz":      "Riz",
    "Sorgho":   "Sorgho",
}

SOLS = {
    "Sableux":        "Sableux",
    "Argileux":       "Argileux",
    "Sablo-argileux": "Sablo-argileux",
    "Laterite":       "Latérite",
}

IRRIGATIONS = {
    "Pluviale":        "Pluviale (sans irrigation)",
    "Aspersion":       "Aspersion",
    "Goutte-a-goutte": "Goutte à goutte",
    "Submersion":      "Submersion",
}

# Coordonnees et altitude de chaque region, utilisees comme variables du modele.
COORDONNEES = {
    "Thies":       (14.79, -16.93, 70),
    "Fatick":      (14.34, -16.41, 20),
    "Kaolack":     (14.15, -16.07, 15),
    "Saint-Louis": (16.02, -16.49, 5),
    "Kaffrine":    (14.10, -15.55, 40),
    "Tambacounda": (13.77, -13.67, 130),
    "Sedhiou":     (12.71, -15.56, 25),
}

# Variete locale par defaut pour chaque culture.
VARIETES_DEFAUT = {
    "Arachide": "55-437",
    "Mil":      "Souna III",
    "Mais":     "DK 8031",
    "Riz":      "Sahel 108",
    "Sorgho":   "CE 145-66",
}

_REFERENTIELS = {
    "region":          REGIONS,
    "crop":            CULTURES,
    "soil_type":       SOLS,
    "irrigation_type": IRRIGATIONS,
}


def libelles(referentiel):
    """Liste des libelles a afficher dans un menu deroulant."""
    return list(referentiel.values())


def vers_canonique(referentiel, libelle):
    """Convertit un libelle affiche en valeur connue du modele.

    Accepte aussi une valeur deja canonique, pour que la fonction soit
    utilisable des deux cotes sans precaution particuliere.
    """
    if libelle in referentiel:
        return libelle
    for canonique, affiche in referentiel.items():
        if affiche == libelle:
            return canonique
    raise ValueError(f"Valeur inconnue : {libelle!r}. Attendu : {list(referentiel)}")


def valider(champ, valeur):
    """Verifie qu'une valeur est connue du modele et la renvoie sous forme canonique.

    Leve ValueError si la valeur est inconnue, plutot que de laisser passer une
    prediction fausse.
    """
    referentiel = _REFERENTIELS.get(champ)
    if referentiel is None:
        raise ValueError(f"Champ inconnu : {champ!r}. Attendu : {list(_REFERENTIELS)}")
    return vers_canonique(referentiel, valeur)


def valeurs_attendues(champ):
    """Valeurs canoniques autorisees pour un champ, triees."""
    return sorted(_REFERENTIELS[champ])
