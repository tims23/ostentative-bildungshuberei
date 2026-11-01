---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

/richard Mein Python-Skript wird immer langsamer, je länger es läuft. In einer Schleife über ca. 200.000 Datensätze hänge ich mit += Text an einen großen String an und prüfe mit `if id in verarbeitete_ids:` nach, ob eine ID schon verarbeitet wurde – verarbeitete_ids ist eine Liste, an die ich jede ID anhänge. Was mache ich falsch?
