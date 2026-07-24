"""Rend la racine du projet importable depuis les tests.

Sans ce fichier, `pytest tests/` place seulement `tests/` dans le chemin
d'import et `import models` echoue. Avec `python -m pytest` le probleme est
masque, car le dossier courant est ajoute automatiquement : la commande de la
CI et celle du poste de travail ne se comportaient donc pas pareil.

La seule presence de ce fichier a la racine suffit a la corriger.
"""
