"""
carte.py — Visualisation du TP3 « Vitesse Spatiale » (8INF259, A26).

Lit un fichier de planètes et l'affiche sous forme de carte en deux dimensions.
On peut y ajouter :
  - un ou plusieurs fichiers de route, produits par les transactions ?2 et ?3 :
    les chemins sont tracés sur la carte ;
  - un fichier de secteurs, produit par la transaction !S : chaque planète
    prend la couleur de son secteur.
Le type de chaque fichier est reconnu à son premier mot-clé (ROUTE ou SECTEURS).

Le programme ne fait aucun calcul : il affiche uniquement ce que contiennent
les fichiers (coordonnées des planètes, chemins, secteurs, valeurs lues).

Usage :
    python carte.py PLANETES.txt                       (carte seule)
    python carte.py PLANETES.txt FICHIER [FICHIER ...] (routes et/ou secteurs)

Touches : N = noms des planètes (afficher/masquer), Échap = quitter.

Seule la librairie standard de Python est utilisée (tkinter).
"""

import argparse
import colorsys
import os
import sys
import tkinter as tk
from tkinter import font as tkfont

CRITERES = {2: "Plus court chemin", 3: "Moins dispendieux"}
COULEURS_ROUTES = ["#d62728", "#1f77b4", "#2ca02c", "#9467bd", "#ff7f0e"]
COULEURS_NATIONS = ["#4e79a7", "#f28e2b", "#59a14f", "#e15759", "#76b7b2",
                    "#edc948", "#b07aa1", "#ff9da7", "#9c755f", "#bab0ac"]
GRIS_ISOLEE = "#6b7280"    # secteur d'une seule planète
GRIS_ABSENTE = "#2f3546"   # planète absente du fichier de secteurs


class ErreurFormat(Exception):
    pass


def couleur_secteur(i):
    """Couleur bien distincte pour le i-ème secteur (teintes réparties)."""
    r, g, b = colorsys.hsv_to_rgb((i * 0.618034) % 1.0, 0.65, 0.95)
    return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"


# --------------------------------------------------------------------------
# Lecture des fichiers
# --------------------------------------------------------------------------

def lire_planetes(chemin):
    """Retourne {nom: (x, y, population, nation, prix)} dans l'ordre du fichier."""
    planetes = {}
    with open(chemin, encoding="utf-8-sig") as f:
        for no, ligne in enumerate(f, 1):
            t = ligne.split()
            if not t:
                continue
            if len(t) != 6:
                raise ErreurFormat(f"{chemin}, ligne {no} : 6 champs attendus, {len(t)} trouvés")
            try:
                planetes[t[0]] = (float(t[1]), float(t[2]), int(t[3]), t[4], float(t[5]))
            except ValueError:
                raise ErreurFormat(f"{chemin}, ligne {no} : valeur numérique invalide")
    if not planetes:
        raise ErreurFormat(f"{chemin} : aucune planète")
    return planetes


class Lecteur:
    """Lecture ligne à ligne d'un fichier à mots-clés (route ou secteurs)."""

    def __init__(self, chemin):
        self.chemin = chemin
        with open(chemin, encoding="utf-8-sig") as f:
            self.lignes = [(no, l.split()) for no, l in enumerate(f, 1) if l.strip()]
        self.i = 0
        if not self.lignes:
            raise ErreurFormat(f"{chemin} : fichier vide")

    def premier_mot(self):
        return self.lignes[0][1][0]

    def suivant_est(self, mot):
        return self.i < len(self.lignes) and self.lignes[self.i][1][0] == mot

    def ligne(self, mot=None, nb=None, min_nb=None):
        """Retourne (no, champs) de la ligne courante, après vérification."""
        if self.i >= len(self.lignes):
            raise ErreurFormat(f"{self.chemin} : fin de fichier inattendue"
                               + (f", ligne « {mot} » attendue" if mot else ""))
        no, t = self.lignes[self.i]
        if mot is not None:
            if t[0] != mot:
                raise ErreurFormat(f"{self.chemin}, ligne {no} : « {mot} » attendu")
            t = t[1:]
        if nb is not None and len(t) != nb:
            raise ErreurFormat(f"{self.chemin}, ligne {no} : {nb} champ(s) attendu(s)"
                               + (f" après « {mot} »" if mot else ""))
        if min_nb is not None and len(t) < min_nb:
            raise ErreurFormat(f"{self.chemin}, ligne {no} : au moins {min_nb} champ(s) attendu(s)")
        self.i += 1
        return no, t

    def nombre(self, texte, no, type_=float):
        try:
            return type_(texte)
        except ValueError:
            raise ErreurFormat(f"{self.chemin}, ligne {no} : nombre invalide « {texte} »")

    def entete(self, donnees):
        """Lignes communes : PLANETES, VAISSEAU (et CONFLIT plus tard)."""
        _, (donnees["planetes"],) = self.ligne("PLANETES", 1)
        no, (donnees["modele"], cap) = self.ligne("VAISSEAU", 2)
        donnees["capacite"] = self.nombre(cap, no)

    def conflits(self):
        liste = []
        while self.suivant_est("CONFLIT"):
            _, (n1, n2) = self.ligne("CONFLIT", 2)
            liste.append((n1, n2))
        return liste

    def fin(self):
        if self.i < len(self.lignes):
            raise ErreurFormat(f"{self.chemin}, ligne {self.lignes[self.i][0]} : "
                               "contenu inattendu en fin de fichier")


def lire_route(lec):
    route = {"fichier": lec.chemin, "chemin": [], "total": None}
    no, (c,) = lec.ligne("ROUTE", 1)
    route["critere"] = lec.nombre(c, no, int)
    if route["critere"] not in CRITERES:
        raise ErreurFormat(f"{lec.chemin}, ligne {no} : critère 2 ou 3 attendu")
    lec.entete(route)
    _, (route["depart"],) = lec.ligne("DEPART", 1)
    _, (route["arrivee"],) = lec.ligne("ARRIVEE", 1)
    route["conflits"] = lec.conflits()
    no, (k,) = lec.ligne("CHEMIN", 1)
    for _ in range(lec.nombre(k, no, int)):
        no, (nom, d, c) = lec.ligne(nb=3)
        route["chemin"].append((nom, lec.nombre(d, no), lec.nombre(c, no)))
    if route["chemin"]:
        no, (d, c, e) = lec.ligne("TOTAL", 3)
        route["total"] = (lec.nombre(d, no), lec.nombre(c, no), lec.nombre(e, no, int))
    lec.fin()
    return route


def lire_secteurs(lec):
    sect = {"fichier": lec.chemin, "secteurs": []}
    no, (n,) = lec.ligne("SECTEURS", 1)
    n = lec.nombre(n, no, int)
    lec.entete(sect)
    sect["conflits"] = lec.conflits()
    for _ in range(n):
        no, t = lec.ligne("SECTEUR", min_nb=2)
        k = lec.nombre(t[0], no, int)
        if len(t) - 1 != k:
            raise ErreurFormat(f"{lec.chemin}, ligne {no} : SECTEUR {k} annonce {k} "
                               f"planète(s), {len(t) - 1} trouvée(s)")
        sect["secteurs"].append(t[1:])
    lec.fin()
    return sect


def lire_fichier(chemin):
    """Retourne ("ROUTE", route) ou ("SECTEURS", secteurs) selon le premier mot-clé."""
    lec = Lecteur(chemin)
    mot = lec.premier_mot()
    if mot == "ROUTE":
        return mot, lire_route(lec)
    if mot == "SECTEURS":
        return mot, lire_secteurs(lec)
    raise ErreurFormat(f"{chemin} : le fichier doit commencer par ROUTE ou SECTEURS")


# --------------------------------------------------------------------------
# Affichage
# --------------------------------------------------------------------------

class Carte(tk.Tk):
    MARGE = 40

    def __init__(self, planetes, routes, secteurs, nom_planetes):
        super().__init__()
        self.title(f"Vitesse Spatiale — {nom_planetes}")
        self.geometry("1250x800")
        self.planetes = planetes
        self.routes = routes
        self.secteurs = secteurs
        self.voir_noms = True
        nations = list(dict.fromkeys(p[3] for p in planetes.values()))
        self.couleur_nation = {n: COULEURS_NATIONS[i % len(COULEURS_NATIONS)]
                               for i, n in enumerate(nations)}

        # Couleur de remplissage de chaque planète : par secteur s'il y a un
        # fichier de secteurs, sinon par nation.
        if secteurs:
            self.remplissage = {nom: GRIS_ABSENTE for nom in planetes}
            for i, membres in enumerate(secteurs["secteurs"]):
                coul = GRIS_ISOLEE if len(membres) == 1 else couleur_secteur(i)
                for nom in membres:
                    self.remplissage[nom] = coul
        else:
            self.remplissage = {nom: self.couleur_nation[p[3]] for nom, p in planetes.items()}

        self.canvas = tk.Canvas(self, bg="#0f1424", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.panneau = tk.Text(self, width=46, wrap="word", bg="#f7f7f7",
                               relief="flat", padx=10, pady=10,
                               font=("Consolas", 10))
        self.panneau.pack(side="right", fill="y")
        self.remplir_panneau()

        self.canvas.bind("<Configure>", lambda e: self.dessiner())
        self.bind("<KeyPress-n>", lambda e: self.basculer("voir_noms"))
        self.bind("<Escape>", lambda e: self.destroy())

    def basculer(self, attribut):
        setattr(self, attribut, not getattr(self, attribut))
        self.dessiner()

    # ----- Panneau d'information -----
    def remplir_panneau(self):
        t = self.panneau
        gras = tkfont.Font(family="Consolas", size=10, weight="bold")
        t.tag_configure("gras", font=gras)

        for route, couleur in self.routes:
            t.tag_configure(couleur, foreground=couleur, font=gras)
            t.insert("end", f"■ ?{route['critere']} — {CRITERES[route['critere']]}\n", couleur)
            t.insert("end", f"{os.path.basename(route['fichier'])}\n")
            t.insert("end", f"Vaisseau : {route['modele']} (capacité {route['capacite']:g})\n")
            t.insert("end", f"{route['depart']} → {route['arrivee']}\n")
            for n1, n2 in route["conflits"]:
                t.insert("end", f"Conflit : {n1} / {n2}\n")
            if not route["chemin"]:
                t.insert("end", "Aucune route.\n", "gras")
            else:
                d, c, e = route["total"]
                t.insert("end", f"Distance : {d:.2f}   Escales : {e}\nCoût : {c:.2f}\n", "gras")
                for no, (nom, dd, cc) in enumerate(route["chemin"]):
                    t.insert("end", f"  {no:>2}. {nom:<18} {dd:>8.2f} {cc:>10.2f}\n")
            t.insert("end", "\n")

        if self.secteurs:
            s = self.secteurs
            t.insert("end", f"■ !S — {len(s['secteurs'])} secteur(s)\n", "gras")
            t.insert("end", f"{os.path.basename(s['fichier'])}\n")
            t.insert("end", f"Vaisseau : {s['modele']} (capacité {s['capacite']:g})\n")
            for n1, n2 in s["conflits"]:
                t.insert("end", f"Conflit : {n1} / {n2}\n")
            for i, membres in enumerate(s["secteurs"]):
                coul = GRIS_ISOLEE if len(membres) == 1 else couleur_secteur(i)
                t.tag_configure(f"s{i}", foreground=coul, font=gras)
                t.insert("end", "● ", f"s{i}")
                t.insert("end", f"Secteur {i + 1} ({len(membres)}) : ", "gras")
                t.insert("end", " ".join(membres) + "\n")
            t.insert("end", "\n")
        else:
            t.insert("end", "Nations :\n", "gras")
            for n, coul in self.couleur_nation.items():
                t.tag_configure("n_" + n, foreground=coul, font=gras)
                t.insert("end", "  ● ", "n_" + n)
                t.insert("end", f"{n}\n")
            t.insert("end", "\n")

        t.insert("end", "Touches : N = noms, Échap = quitter\n")
        t.configure(state="disabled")
        t.see("1.0")  # afficher le haut du panneau

    # ----- Carte -----
    def transformation(self):
        xs = [p[0] for p in self.planetes.values()]
        ys = [p[1] for p in self.planetes.values()]
        w = max(self.canvas.winfo_width(), 100) - 2 * self.MARGE
        h = max(self.canvas.winfo_height(), 100) - 2 * self.MARGE
        lx = max(max(xs) - min(xs), 1e-9)
        ly = max(max(ys) - min(ys), 1e-9)
        e = min(w / lx, h / ly)  # même échelle en X et en Y
        ox = self.MARGE + (w - e * lx) / 2
        oy = self.MARGE + (h - e * ly) / 2
        # Y vers le haut, comme dans un repère mathématique
        return lambda x, y: (ox + (x - min(xs)) * e, oy + (max(ys) - y) * e)

    def dessiner(self):
        cv = self.canvas
        cv.delete("all")
        T = self.transformation()

        # Chemins (décalés légèrement pour rester visibles s'ils se superposent)
        for k, (route, couleur) in enumerate(self.routes):
            dec = (k - (len(self.routes) - 1) / 2) * 4
            pts = [T(*self.planetes[n][:2]) for n, _, _ in route["chemin"] if n in self.planetes]
            for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
                cv.create_line(x1 + dec, y1 + dec, x2 + dec, y2 + dec, fill=couleur,
                               width=3, arrow="last", arrowshape=(12, 14, 5))

        # Planètes
        depart_arrivee = set()
        for route, _ in self.routes:
            depart_arrivee.update((route["depart"], route["arrivee"]))
        r_base = 5 if self.secteurs else 4
        for nom, (x, y, _, _, _) in self.planetes.items():
            px, py = T(x, y)
            r = 7 if nom in depart_arrivee else r_base
            cv.create_oval(px - r, py - r, px + r, py + r, fill=self.remplissage[nom],
                           outline="white" if nom in depart_arrivee else "")
            if self.voir_noms or nom in depart_arrivee:
                cv.create_text(px + 8, py - 8, text=nom, anchor="sw",
                               fill="white" if nom in depart_arrivee else "#9aa3c0",
                               font=("Segoe UI", 9, "bold" if nom in depart_arrivee else "normal"))

        # Étiquettes Départ / Arrivée
        for route, couleur in self.routes[:1]:
            for nom, texte in ((route["depart"], "DÉPART"), (route["arrivee"], "ARRIVÉE")):
                if nom in self.planetes:
                    px, py = T(*self.planetes[nom][:2])
                    cv.create_text(px + 8, py + 6, text=texte, anchor="nw",
                                   fill="#ffd166", font=("Segoe UI", 8, "bold"))


def main():
    ap = argparse.ArgumentParser(description="Visualisation du TP3 (8INF259).")
    ap.add_argument("planetes", help="fichier de planètes (la carte)")
    ap.add_argument("fichiers", nargs="*",
                    help="fichier(s) de route (?2, ?3) et/ou de secteurs (!S), facultatif")
    args = ap.parse_args()
    for flux in (sys.stdout, sys.stderr):  # console Windows (cp1252) : pas de plantage
        flux.reconfigure(errors="replace")

    try:
        planetes = lire_planetes(args.planetes)
        lus = [lire_fichier(f) for f in args.fichiers]
    except (ErreurFormat, OSError) as e:
        print(f"Erreur : {e}", file=sys.stderr)
        sys.exit(1)

    routes = [d for type_, d in lus if type_ == "ROUTE"]
    secteurs = [d for type_, d in lus if type_ == "SECTEURS"]
    if len(secteurs) > 1:
        print("Erreur : un seul fichier de secteurs peut être affiché à la fois.", file=sys.stderr)
        sys.exit(1)

    avec_couleurs = [(r, COULEURS_ROUTES[k % len(COULEURS_ROUTES)])
                     for k, r in enumerate(routes)]
    Carte(planetes, avec_couleurs, secteurs[0] if secteurs else None,
          os.path.basename(args.planetes)).mainloop()


if __name__ == "__main__":
    main()
