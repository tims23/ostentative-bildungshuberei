# Ostentative Bildungshuberei

Ein Claude-Code-Skill namens `/richard`. Er macht Claude zu „Richard“, deinem persönlichen, an Richard David Precht angelehnten Gesprächspartner: Antworten mit einem Hauch ostentativ verschachtelter Bildungshuberei, mit Schachtelsätzen, gelehrten Einschüben und den Ritualen aus „Lanz + Precht“. Der Sachgehalt bleibt dabei vollständig erhalten.

> „Richard, wo erreiche ich dich?“
> „Zu Hause. In der Kemenate.“

## Installation

Verlinke den Skill in dein persönliches Skill-Verzeichnis. Dann steht `/richard` in allen Claude-Code-Projekten zur Verfügung:

```sh
ln -s "$(pwd)/skills/richard" ~/.claude/skills/richard
```

Weil der Skill per Symlink eingebunden ist, wirken Änderungen im Repo sofort.

## Nutzung

- `/richard`: Richard begrüßt dich und fragt nach dem Thema.
- `/richard warum läuft mein useEffect in einer Endlosschleife?`: Richard beantwortet die Frage in seinem Ton.
- Der Skill greift auch, wenn du Claude mit „Richard“ ansprichst, etwa mit „Schönen guten Morgen, Richard.“
- Beenden kannst du die Rolle zum Beispiel mit „Danke, Richard.“ Richard antwortet dann: „In diesem Sinne. Ich danke dir auch, Markus.“

Code, Commit-Messages, PR-Beschreibungen und Dateien bleiben nüchtern. Die Persona gilt nur für die Prosa im Chat.

## Aufbau

```
skills/richard/
├── SKILL.md                 # Persona, Dosierung, Rituale, Grenzen, Beispiele
└── references/
    ├── repertoire.md        # verifizierter Fundus: Rituale, Satzbaukasten, Aphorismen, Werk, Referenzen, No-Gos
    └── quellen.md           # Belege mit URLs zu jedem Eintrag
scripts/
└── transkripte_laden.py     # lädt die Podcast-Transkripte nach transkripte/ (nicht im Repo)
```

## Transkripte

Die offiziellen Transkripte von „Lanz + Precht“ (Ausgabe 169 bis heute) lädt ein Skript aus dem RSS-Feed des Podcasts. Es braucht nur Python 3:

```sh
python3 scripts/transkripte_laden.py
```

Die Dateien landen in `transkripte/`, zusammen mit der Übersicht `index.tsv` (Datei, Titel, Datum, URL). Vorhandene Dateien überspringt das Skript, `--neu` lädt alles erneut. Die Transkripte sind maschinell erstellt und enthalten Erkennungsfehler, etwa „Cheminate“ statt „Kemenate“. Sie sind urheberrechtlich geschützt und deshalb per `.gitignore` vom Repo ausgeschlossen.

## Herkunft des Repertoires

Das Repertoire stammt aus einer Multi-Agent-Webrecherche vom 31.10.2026, bei der jeder Eintrag adversarial geprüft wurde. Grundlage waren die offiziellen Podcast-Transkripte der Ausgaben 169–269, die Bücher, Interviews, Rezensionen und Satire. Von 197 Einträgen wurden 188 bestätigt, 8 gelten als plausibel und 1 wurde verworfen. Erfundene Precht-Zitate sind ausdrücklich ausgeschlossen. Heikle Kontroversen stehen auf einer No-Go-Liste und werden nie als Pointe verwendet.

## Hinweis

Richard ist eine liebevolle Hommage für den privaten Gebrauch. Er steht in keiner Verbindung zu Richard David Precht, Markus Lanz oder dem ZDF und gibt sich nicht als Precht aus.
