# Frei verfügbare Schnittstellen — Apple Health, Strava & Alternativen

## 🔴 Apple HealthKit — Direkter ESP32-Zugang: NICHT MÖGLICH

### Kernproblem
Apple HealthKit ist **nur über native iOS-Apps** mit HealthKit-Entitlement zugänglich:
- **Keine REST-API** für externe Geräte
- **Keine Webhooks** für Daten-Import
- **Kein MQTT/HTTP-Endpoint** von Apple

### Was HealthKit kann
- **Lesen + Schreiben** von Gesundheitsdaten (Herzfrequenz, Schritte, GPS-Routen, Schlaf, etc.)
- **Datentypen:** HKQuantityType (Herzfrequenz, Geschwindigkeit, Distanz), HKWorkoutType (Workouts mit GPS-Routen), HKCategoryType, HKCorrelationType
- **Berechtigungen:** App muss explizit Schreib-Rechte anfragen (HKHealthStore.requestAuthorization)

### Der einzige Weg: iOS-App als Bridge
```
ESP32 → (BLE/WiFi/HTTP) → iOS-App → HealthKit
```

**Erforderlich:**
1. iOS-App mit HealthKit-Entitlement (Apple Developer Account: 99€/Jahr)
2. App muss auf dem iPhone laufen
3. Datenübertragung ESP32 → App via:
   - **BLE (Bluetooth Low Energy):** ESP32 sendet Sensor-Daten an iOS-App
   - **WiFi HTTP/MQTT:** ESP32 als HTTP-Server oder MQTT-Client, iOS-App als Consumer
   - **Apple Shortcuts + HTTP-Shortcut:** Workaround, aber sehr limitiert

### Alternative: Apple Health Shortcuts (begrenzt)
- iOS Shortcuts App kann Health-Daten lesen/schreiben
- Shortcuts können per `shortcuts://` URL aufgerufen werden
- Aber: Automatisierter Daten-Import von externen Geräten ist nicht vorgesehen
- Works for simple data (Schritte, Herzfrequenz), NOT for workout routes

---

## 🟢 Strava API — Voller API-Zugang, KOSTENLOS

### Übersicht
- **URL:** https://developers.strava.com
- **Kostenlos** für alle (Rate Limits gelten)
- **OAuth 2.0** Authentifizierung
- **App erstellen:** https://www.strava.com/settings/api

### Rate Limits
| Zeitraum | Limit |
|----------|-------|
| 15 Minuten | 200 Requests |
| Täglich | 2.000 Requests |

### Daten hochladen: Activity Uploads
Strava unterstützt **Activity Uploads** — das ist der Weg für den ESP32!

**POST** `https://www.strava.com/api/v3/uploads`

Supported File Types:
| Format | Beschreibung |
|--------|-------------|
| **FIT** | Flexible and Interoperable Data Transfer (GARMIN-Standard, **empfohlen!**) |
| **TCX** | Training Center XML |
| **GPX** | GPS Exchange Format |
| **JSON** | Limited support |

### FIT-Datei empfohlen
- FIT ist das Standardformat für Fitness-Geräte
- Enthält: GPS-Track, Herzfrequenz, Geschwindigkeit, Distanz, Höhenprofil, Temperatur
- FIT SDK: https://developer.garmin.com/fit/sdk/ (kostenlos, C/Python/Java)
- Python: `garmin-fit-sdk` oder `fitdecode` Pakete

### OAuth 2.0 Flow (Strava)
1. App registrieren → Client ID + Secret
2. User autorisiert App → Authorization Code
3. Code → Access Token + Refresh Token
4. Access Token für API-Calls (Expires nach 6 Stunden)
5. Refresh Token für neuen Access Token

**Scopes:**
- `read` — Daten lesen
- `read_all` — Alle Daten lesen (inkl. private)
- `profile:read_all` — Profil lesen
- `profile:write` — Profil ändern
- `activity:read` — Activities lesen
- `activity:read_all` — Alle Activities lesen
- `activity:write` — Activities schreiben **← DAS BRAUCHEN WIR**

### Architektur für ESP32 → Strava
```
ESP32 (Ride-Mode Controller)
  → sammelt GPS, Speed, RPM, Herzfreq, Temperatur
  → erzeugt FIT-Datei im Speicher
  → HTTP POST an eigenen Server (z.B. Raspberry Pi oder Mac)

Server (Python/Bridge):
  → empfängt FIT-Datei
  → Strava OAuth Token verwalten (Refresh)
  → POST /api/v3/uploads mit FIT-Datei
  → Activity erscheint in Strava!
```

**Alternative (direkt vom ESP32):**
- ESP32 mit WiFi → direkt HTTP POST an Strava API
- Problem: OAuth Token-Management auf ESP32 ist aufwendig
- Besser: Eigenen kleinen Server als Bridge

---

## 🟡 Strava → Apple Health (indirekt)

### Automatischer Sync
Strava-App auf dem iPhone **synced automatisch** mit Apple Health:
- Einstellungen → Strava App → Health → Datenzugriff erlauben
- Strava-Workouts erscheinen dann autom. in Apple Health

### Pfad für Ride-Mode Controller:
```
ESP32 → Server → Strava API (Activity Upload)
                    ↓
                Strava iPhone App
                    ↓ (autom. Sync)
                Apple Health ✅
```

**Das ist der einfachste Weg!** Kein iOS-Bridge-App nötig — Strava als Proxy.

---

## 🔵 Google Fit API — Alternative zu Apple Health

- **URL:** https://developers.google.com/fit
- **REST-API** verfügbar (im Gegensatz zu HealthKit!)
- Daten lesen UND schreiben über API
- OAuth 2.0 Authentifizierung
- ESP32 kann direkt (über Server) Daten pushen
- **Aber:** Nur für Android-Nutzer relevant, nicht für iPhone

---

## 📊 Zusammenfassung: Welcher Weg für den Ride-Mode Controller?

| Weg | Aufwand | Apple Health | Strava | Empfehlung |
|-----|---------|-------------|--------|-------------|
| ESP32 → Strava API | Mittel | ❌ Indirekt (über Strava App) | ✅ Direkt | **⭐ BESTE OPTION** |
| ESP32 → iOS App → HealthKit | Hoch | ✅ Direkt | ❌ | Nur wenn HealthKit zwingend |
| ESP32 → Server → Strava → Health | Mittel | ✅ Auto-Sync | ✅ Direkt | **⭐ PRAKTISCH** |
| ESP32 → Google Fit | Mittel | ❌ | ❌ | Nur für Android |

### Empfehlung für AQL Ride-Mode Controller

**Architektur:**
1. ESP32 sammelt Sensordaten (GPS, Speed, RPM, Temperatur)
2. Nach Fahrtende: ESP32 erzeugt FIT-Datei
3. FIT-Datei → HTTP POST an Python-Bridge-Server
4. Bridge-Server → Strava API (Activity Upload mit OAuth)
5. Strava App auf iPhone → autom. Sync → Apple Health

**Vorteile:**
- Keine iOS-App nötig
- Kein Apple Developer Account (99€/Jahr) nötig
- Strava ist kostenlos
- Apple Health bekommt die Daten automatisch
- FIT-Datei kann auch lokal gespeichert werden als Backup

---

## 🔧 Technische Details für Implementation

### FIT-Datei erzeugen (Python)
```bash
pip install garmin-fit-sdk
# oder
pip install fitdecode
```

### Strava Upload (Python Beispiel)
```python
import requests

# OAuth tokens müssen vorher über OAuth-Flow geholt werden
ACCESS_TOKEN = "..."

headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
files = {"file": ("ride.fit", open("ride.fit", "rb"), "application/octet-stream")}
data = {
    "data_type": "fit",
    "activity_type": "ride",
    "name": "NX650 Ride",
    "description": "Ride-Mode Controller Log"
}

response = requests.post(
    "https://www.strava.com/api/v3/uploads",
    headers=headers,
    files=files,
    data=data
)
print(response.json())
```

### Garmin FIT SDK (C, für ESP32)
- https://developer.garmin.com/fit/sdk/
- C-Implementierung verfügbar — direkt auf ESP32 nutzbar
- FIT-Datei im ESP32-Flash erzeugen und per WiFi senden

---

## Quellen
- Strava API Docs: https://developers.strava.com/docs/
- Strava Uploads: https://developers.strava.com/docs/uploads/
- Apple HealthKit: https://developer.apple.com/documentation/healthkit
- Garmin FIT SDK: https://developer.garmin.com/fit/sdk/
- Google Fit API: https://developers.google.com/fit