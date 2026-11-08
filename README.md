# POP PUNK 101 – Instagram automation

Daily package of 24 Instagram posts for the POP PUNK 101 radio.

- `tools/` – image template (poppunk101.com look), renderer, fonts, logo
- `data/songliste.csv` – song list (artist, song)
- `data/used.json` – songs already used (rotation state)
- `data/bios.json` – verified release years and short bios per song/band
- `images/YYYY-MM-DD/` – rendered post images (public, linked from the Publer CSV)
- `publer/YYYY-MM-DD.csv` – Publer bulk upload file for that day

## News posts
- `tools/template_news.html`, `tools/render_news.py`, `tools/build_news.py` – NEWS image template (release / tour / just announced) and builder
- `data/news_used.json` – news items already posted (rotation state)
- `images/news/YYYY-MM-DD/` – rendered news images
- `publer/news-YYYY-MM-DD.csv` – Publer bulk upload file with 3 news posts (08:00, 12:00, 15:00)

## Ablaufregeln (Stand 08.11.2026)

**Upload-Rhythmus:** Julian lädt zweimal pro Woche hoch, sonntags und mittwochs. Die Pakete werden vorher geprüft und in Publer von Julian selbst freigegeben (Create, Bulk Options, Import CSV, Instagram-Konto wählen, prüfen, Submit). Bei jedem fertigen Paket kommt eine Push-Erinnerung (vom News-Task).

**Abdeckung:** Sonntag-Paket = Mo bis Mi, Mittwoch-Paket = Do bis So. Übergang: Lauf am Mo 09.11. deckt Di 10.11. bis Mi 11.11.

**Now-Playing:** ein Post alle 2 Stunden, immer xx:30, rund um die Uhr, lückenlos (Anschluss = letzter geplanter Post + 2 h; endet jedes Paket um 22:30). 36 bis 48 Posts je Paket. Task: täglich 05:53, erzeugt nur, wenn der letzte geplante Post vor MORGEN 14:00 liegt.

**News:** je Tag bis zu 3 Posts, 08:00 NEW RELEASE, 12:00 TOUR NEWS, 15:00 JUST ANNOUNCED. Leere Slots entfallen. Task: täglich 06:41, erzeugt nur, wenn die letzte News-CSV vor MORGEN liegt. Kollisionen mit Now-Playing schiebt build_news.py um volle Stunden.

**Inhalt News:** Redaktioneller Ton, keine Werbung für Festivals oder Tickets, zeitlos formuliert (kein "today/just/now"). Pro Festival und Tag ein Post mit 1 bis 2 Bands. Band-Sperre 3 Tage, Event-Sperre 3 Tage. Metal/Metalcore/Hardcore außerhalb der Prioritätsliste wird nicht genommen. Fakten nur aus den geprüften Projekt-Feeds.

**Inhalt Now-Playing:** Typo-Cover mit Logo und Pegelausschlag, keine Bandfotos. Jahr = erste offizielle Veröffentlichung, nur mit Quelle. Nichts Unbelegtes, englisch, keine Songtexte, keine Gedankenstriche.

**Qualität vor Tempo:** Wird ein Lauf knapp, wird das Paket gekürzt (volle Tage), nie die Prüfung.
