---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Richard, schreib mir bitte eine Commit-Message für folgende Änderung: Der Token-Refresh läuft jetzt vor jedem API-Request, wenn das Access-Token in weniger als 60 Sekunden abläuft. Vorher sind Requests mit abgelaufenem Token mit 401 gescheitert und der Nutzer wurde ausgeloggt.
