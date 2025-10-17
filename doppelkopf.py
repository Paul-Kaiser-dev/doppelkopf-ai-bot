import random

# ---- 1. Kartenstruktur ----
class Karte:
    """
    Repräsentiert eine Karte im Spiel.
    - `farbe`: Die Farbe der Karte (Kreuz, Pik, Herz, Karo).
    - `wert`: Der Name der Karte (Neun, Zehn, Bube, Dame, König, Ass).
    - `punkte`: Die Punktzahl der Karte.
    """
    def __init__(self, farbe, wert, punkte, trumpf=0, t=False):
        self.farbe = farbe
        self.wert = wert
        self.punkte = punkte
        self.trumpf = trumpf
        self.t = t

    def __repr__(self):
        return f"{self.wert} von {self.farbe}"

# ---- 2. Spielerstruktur ----
class Spieler:
    """
    Repräsentiert einen Spieler im Spiel.
    - `name`: Der Name des Spielers.
    - `hand`: Die Karten, die der Spieler auf der Hand hat.
    - `stiche`: Die Stiche, die der Spieler gewonnen hat.
    - `team`: Das Team des Spielers (Re oder Contra).
    """
    def __init__(self, name):
        self.name = name
        self.hand = []  # Karten, die der Spieler hält
        self.stiche = []  # Gewonnene Stiche
        self.team = None  # Re oder Contra

    def spiele_karte(self, karte):
        "Spielt eine Karte aus der Hand."
        self.hand.remove(karte)
        return karte

# ---- 3. Spielstruktur ----
class DoppelkopfSpiel:
    """
    Hauptklasse für das Doppelkopf-Spiel.
    Verantwortlich für das Erstellen des Decks, Verteilen der Karten
    und den Ablauf des Spiels.
    """
    def __init__(self):
        self.deck = self.kartendeck_erstellen()
        self.spieler = [KI(f"Spieler {i+1}") for i in range(4)]  # 4 Spieler
        self.gespielte_karten = []
        self.startspieler_index = 0  # Startspieler (wird nach jedem Stich aktualisiert)
        
    def verteile_teams(self):
        """
        Weist die Teams (Re und Contra) basierend auf der Kreuz-Dame zu.
        Spieler mit einer Kreuz-Dame sind Re, alle anderen Contra.
        """
        
        for spieler in self.spieler:
            kreuz_dame_gefunden = False
            for karte in spieler.hand:

                if karte.farbe == "Kreuz" and karte.wert == "Dame":
                    spieler.team = "Re"
                    #kreuz_dame.append(spieler)
                    print(f"{spieler.name} hat die Kreuz-Dame und ist Re team.")
                    kreuz_dame_gefunden = True  # Kreuz-Dame gefunden
                    break  # Verlasse die innere Schleife, sobald die Kreuz-Dame gefunden wurde
        
            if not kreuz_dame_gefunden:
                # Wenn die Kreuz-Dame nicht gefunden wurde, setze das Team auf "Contra"
                spieler.team = "Contra"
                print(f"{spieler.name} ist im Contra-Team.")




    def trumpf_wertigkeit(self, karte):
        """
        Berechnet die Trumpf-Wertigkeit basierend auf der Trumpf-Ordnung.
        Höherer Wert bedeutet höhere Priorität.
        """
        trumpf_reihenfolge = {
            "Kreuz": 4,
            "Pik": 3,
            "Herz": 2,
            "Karo": 1
        }
        if karte.wert == "Bube":
            return 4 + trumpf_reihenfolge[karte.farbe]  # 
        if karte.wert == "Dame":
            return 8 + trumpf_reihenfolge[karte.farbe]  # 
        if karte.farbe == self.trumpf_farbe:
            return trumpf_reihenfolge[karte.farbe]  # Andere Trumpfkarten
        return 0  # Nicht-Trumpfkarten

    def kartendeck_erstellen(self):
        """
        Erstellt das Kartendeck mit 48 Karten (2x Neun bis Ass pro Farbe).
        """
        farben = ["Kreuz", "Pik", "Herz", "Karo"]
        werte = [
            ("Neun", 0, 0),
            ("König", 4, 1),
            ("Zehn", 10, 2),
            ("Ass", 11, 3),
            ("Bube", 2, 8),
            ("Dame", 3, 12),
        ]

        deck = []
        for _ in range(2):  # Jede Karte doppelt
            bonus = 4
            for farbe in farben:
                bonus -= 1
                for wert, punkte, trumpf in werte:
                    # Trumpf wird später spezifiziert
                    trumpstaerke = trumpf
                    t = False
                    if wert == "Bube":
                        trumpstaerke += bonus
                        t = True
                    elif wert == "Dame":
                        trumpstaerke += bonus
                        t = True
                    elif farbe == "Karo":
                        trumpstaerke += 4
                        t = True
                    deck.append(Karte(farbe, wert, punkte, trumpstaerke, t))
                    print((farbe, wert, punkte, trumpstaerke))
        random.shuffle(deck)
        return deck

    def karten_verteilen(self):
        """
        Teilt die Karten an die Spieler aus (jeweils 12 Karten).
        """
        for i, karte in enumerate(self.deck):
            self.spieler[i % 4].hand.append(karte)

    def zeige_haende(self):
        """
        Zeigt die Karten der Spieler (nur für Debugging).
        """
        for spieler in self.spieler:
            print(f"{spieler.name}: {spieler.hand}")

    def wer_gewinnt_stich(self, stich):
        """
        Bestimmt den Gewinner des Stichs basierend auf Trumpf- und Farbregeln.
        """
        winner = None
        winner_karte = None
        farbe = None
        for spieler, karte in stich:
            if not winner:
                winner = spieler
                winner_karte = karte
                farbe = karte.farbe
            else:
                if karte.trumpf < 4 and karte.farbe == farbe and winner_karte.trumpf < karte.trumpf:
                    winner = spieler
                    winner_karte = karte
                if winner_karte.trumpf < karte.trumpf and (karte.farbe == farbe or karte.farbe == "Karo"):
                    winner = spieler
                    winner_karte = karte
        return winner

    def spiele_stich(self):
        """
        Simuliert einen Stich, bei dem jeder Spieler eine Karte spielt.
        Der Startspieler wird durch `startspieler_index` bestimmt.
        """
        stich = []
        angespielte_farbe = None
        ob_trumpf_angespielt = None
        # Spieler in der richtigen Reihenfolge (beginnend mit dem Startspieler)
        reihenfolge = self.spieler[self.startspieler_index:] + self.spieler[:self.startspieler_index]

        for spieler in reihenfolge:
            karte = spieler.waehle_karte(angespielte_farbe, stich, ob_trumpf_angespielt)
            print(f"{spieler.name} spielt: {karte.farbe} {karte.wert}, {karte.trumpf}.")
            if not angespielte_farbe:
                angespielte_farbe = karte.farbe
                ob_trumpf_angespielt = karte.t
            spieler.hand.remove(karte)
            stich.append((spieler, karte))

        gewinner = self.wer_gewinnt_stich(stich)
        if gewinner:
            print(f"{gewinner.name} gewinnt den Stich mit {[karte for _, karte in stich]}, {[karte.trumpf for _, karte in stich]}.")
            gewinner.stiche.append(stich)

            # Aktualisiere den Startspieler für den nächsten Stich
            self.startspieler_index = self.spieler.index(gewinner)

    def berechne_punkte(self):
        """
        Berechnet die Punkte für Re und Contra.
        """
        re_punkte = 0
        contra_punkte = 0
        for spieler in self.spieler:
            for stich in spieler.stiche:
                for _, karte in stich:
                    if spieler.team == "Re":
                        re_punkte += karte.punkte
                    else:
                        contra_punkte += karte.punkte
        return re_punkte, contra_punkte

# ---- 4. Einfache KI für Spieler ----
class KI(Spieler):
    """
    Ein einfacher KI-Spieler, der immer die erste Karte in seiner Hand spielt.
    Später kann die Logik verbessert werden.
    """
    def waehle_karte(self, angespielte_farbe, aktuelle_stich_karten, ob_trumpf_angespielt):
        """
        Wählt eine Karte basierend auf der aktuellen Spielsituation.
        """
        legale_karten = self.legale_karten(angespielte_farbe, ob_trumpf_angespielt)

        # Wenn es legale Karten gibt, spiele die höchste
        if legale_karten:
            return max(legale_karten, key=lambda k: k.punkte)
        
        # Falls keine legale Karte, spiele eine beliebige Karte
        return min(self.hand, key=lambda k: k.punkte)

    def legale_karten(self, angespielte_farbe, ob_trumpf_angespielt):
        """
        Gibt die Liste der Karten zurück, die der Spieler für den aktuellen Stich
        legal spielen darf. Dabei wird berücksichtigt, ob die angespielte Farbe
        bedient werden muss oder nicht.
        """
        if angespielte_farbe:
            # Der Spieler muss die angespielte Farbe bedienen, falls möglich
            if not ob_trumpf_angespielt:

                passende_karten = [karte for karte in self.hand if karte.farbe == angespielte_farbe and karte.t == ob_trumpf_angespielt]
                if passende_karten:
                    return passende_karten  # Rückgabe der Karten der angespielten Farbe
  
            else:
                passende_karten = [karte for karte in self.hand if karte.t == ob_trumpf_angespielt]
                if passende_karten:
                    return passende_karten



        # Wenn keine angespielte Farbe, kann jede Karte gespielt werden
        return self.hand




class regelbasiert(KI):
    """
    regelbasierter KI-Spieler.
    """
    def waehle_karte(self, angespielte_farbe, aktuelle_stich_karten, ob_trumpf_angespielt):
        """
        Wählt eine Karte basierend auf der aktuellen Spielsituation.
        """
        legale_karten = self.legale_karten(angespielte_farbe, ob_trumpf_angespielt)

        if not angespielte_farbe: #sprich spieler kommt raus
            for karte in self.hand:
                if karte.wert == "Ass" and (angespielte_farbe is None or karte.farbe == angespielte_farbe):
                    print(f"{self.name} spielt das Ass von {karte.farbe}.")
                    return self.spiele_karte(karte)
        
        if legale_karten:
            return max(legale_karten, key=lambda k: k.punkte)
        
        # Falls keine legale Karte, spiele eine beliebige Karte
        return min(self.hand, key=lambda k: k.punkte)


class MonteCarloKI(KI):
    """
    Monte-Carlo-KI für Doppelkopf. Diese KI simuliert mehrere Spiele, um den besten Zug zu finden.
    """
    def waehle_karte(self, angespielte_farbe, aktuelle_stich_karten, ob_trumpf_angespielt):
        """
        Wählt die Karte basierend auf Monte-Carlo-Simulationen.
        """
        # Anzahl der Simulationen für die Monte-Carlo-Methode
        simulationen = 1000
        best_karte = None
        best_punkte = -float('inf')
        
        # Simuliere mehrere Spiele
        for karte in self.hand:
            punkte_summe = 0
            for _ in range(simulationen):
                # Kopiere die aktuelle Spielsituation und führe eine Simulation durch
                simulation = self.simuliere_spiel(karte, angespielte_farbe, aktuelle_stich_karten, ob_trumpf_angespielt)
                punkte_summe += simulation["punkte"]

            # Berechne den Durchschnitt der Punkte für diese Karte
            durchschnitt_punkte = punkte_summe / simulationen
            if durchschnitt_punkte > best_punkte:
                best_punkte = durchschnitt_punkte
                best_karte = karte

        return best_karte

    def simuliere_spiel(self, gewaehlte_karte, angespielte_farbe, aktuelle_stich_karten, ob_trumpf_angespielt):
        """
        Simuliert das Spiel mit der gewählten Karte.
        """
        # Kopiere die Hand und die Spielsituation
        simulation_spiel = DoppelkopfSpiel()  # Erstelle eine neue Instanz des Spiels
        simulation_spiel.karten_verteilen()
        simulation_spiel.verteile_teams()

        # Führe den aktuellen Stich durch
        simulation_spiel.spieler[self.spieler.index(self)].spiele_karte(gewaehlte_karte)  # Simuliere den Zug

        # Berechne nach der Simulation die Punkte
        re_punkte, contra_punkte = simulation_spiel.berechne_punkte()

        # Rückgabe der Punkte aus der Simulation
        return {"punkte": re_punkte if self.team == "Re" else contra_punkte}




# ---- Hauptprogramm ----
if __name__ == "__main__":
    spiel = DoppelkopfSpiel()
    spiel.karten_verteilen()
    spiel.verteile_teams()

    print("--- Kartenverteilung ---")
    spiel.zeige_haende()
    for i in range(12):
        print(f"\n--- Der {i+1}. Stich wird gespielt ---")
        spiel.spiele_stich()

    print("\n--- Spiel beendet ---")
    for spieler in spiel.spieler:
        print(f"{spieler.name} ({spieler.team}) hat {len(spieler.stiche)} Stiche gewonnen.")

    re_punkte, contra_punkte = spiel.berechne_punkte()
    if re_punkte > contra_punkte:
        print("Re hat gewonnen")
    else:
        print("Contra hat gewonnen")
    print(f"\nPunkte: Re = {re_punkte}, Contra = {contra_punkte}")