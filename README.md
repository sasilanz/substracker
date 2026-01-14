# 💳 Substracker

Eine einfache Web-Anwendung zur Verwaltung deiner Subscriptions und Abos. Übersicht über Kosten, Fälligkeitsdaten und Login-Informationen an einem zentralen Ort.

## Features

- ✅ Subscriptions hinzufügen, bearbeiten und löschen
- 📅 Automatische Sortierung nach Fälligkeitsdatum
- 💰 Übersicht über monatliche und jährliche Kosten
- 📝 Speicherung von Login-Daten und Notizen
- 🐳 Vollständig dockerisiert

## Tech Stack

- **Backend**: Flask (Python)
- **Datenbank**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Containerization**: Docker & Docker Compose

## Installation & Setup

### Lokal (ohne Docker)

```bash
# Repository klonen
git clone <repo-url>
cd substracker

# Virtual Environment erstellen
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# oder
venv\Scripts\activate  # Windows

# Abhängigkeiten installieren
pip install -r requirements.txt

# App starten
python app.py
```

Die App läuft dann auf `http://localhost:5000`

### Mit Docker

```bash
# Docker Image bauen und Container starten
docker-compose up --build

# Im Browser öffnen
http://localhost:5000
```

Um den Container zu stoppen:
```bash
docker-compose down
```

## Verwendung

1. **Dashboard**: Beim Start siehst du eine Übersicht aller Subscriptions
2. **Neue Subscription hinzufügen**: Klick auf "+ Neue Subscription"
3. **Bearbeiten**: Klick auf "✏️ Bearbeiten" neben einer Subscription
4. **Löschen**: Klick auf "🗑️ Löschen" (mit Bestätigung)

### Datenfelder

- **Name**: Name des Abos (z.B. Netflix, Spotify)
- **Betrag**: Monatlicher/Jährlicher Preis in Euro
- **Zyklus**: Monatlich, Jährlich oder Quartalsweise
- **Fälligkeitsdatum**: Wann ist die nächste Zahlung fällig
- **Login**: E-Mail oder Benutzername für das Abo
- **Passwort**: Passwort (Warnung: wird unverschlüsselt gespeichert!)
- **Notizen**: Zusätzliche Informationen

## Projektstruktur

```
substracker/
├── app.py                 # Flask Hauptanwendung
├── models.py             # Datenbankmodelle (SQLAlchemy)
├── requirements.txt      # Python Abhängigkeiten
├── Dockerfile            # Docker Image Definition
├── docker-compose.yml    # Docker Compose Setup
├── README.md             # Diese Datei
├── templates/            # HTML Templates
│   ├── base.html        # Basis-Layout
│   ├── index.html       # Dashboard
│   ├── add.html         # Form zum Hinzufügen
│   └── edit.html        # Form zum Bearbeiten
├── static/               # CSS & JavaScript
│   ├── style.css        # Styling
│   └── script.js        # Zusätzliches JavaScript
└── .gitignore
```

## Konfiguration

### Datenbank

Die Datenbank wird automatisch als `subscriptions.db` erstellt und speichert die Daten lokal.

Für Production sollte folgendes geändert werden:

1. `app.py`: Ändere `SECRET_KEY` auf einen sicheren Wert
2. Verwende eine externe Datenbank (PostgreSQL)
3. Verschlüssele die Passwort-Speicherung

### Umgebungsvariablen

```bash
FLASK_ENV=production  # oder development
FLASK_APP=app.py
```

## Sicherheit & TODOs

⚠️ **Wichtig**: Diese App ist für persönliche Nutzung gedacht. Für Production sollte folgendes verbessert werden:

- [ ] Passwort-Verschlüsselung implementieren
- [ ] Benutzer-Authentifizierung hinzufügen
- [ ] HTTPS erzwingen
- [ ] Sichere Secret-Management (Environment Variablen)
- [ ] Datenbank-Backups implementieren
- [ ] Audit-Logs für Änderungen

## Development

### Hot Reload aktivieren

Beim lokalen Starten mit `python app.py` ist Hot Reload bereits aktiv.

### Datenbank zurücksetzen

```bash
rm subscriptions.db
python app.py  # Neue Datenbank wird erstellt
```

## API (zukünftig)

Geplant für spätere Version:
- RESTful API für externe Integration
- Mobile App
- Backup/Export Funktionalität

## Lizenz

MIT

## Support & Fragen

Für Fragen oder Verbesserungsvorschläge: GitHub Issues erstellen
