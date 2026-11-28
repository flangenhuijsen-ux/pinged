# Productiestandaard PINGED en ELAPSED (vastgelegd 27 nov 2026)

Elke nieuwe video volgt deze regels. Ze komen uit de data van de eerste Shorts:
56,6% swipete weg in de eerste seconde, en 37% van de weergaven kwam via de kanaalpagina.

## 1. Eerste beeld (Shorts-feed)
- Geen inblending vanuit zwart. Beeld 0 is volledig zichtbaar.
- De haak (het kerngetal) staat vanaf beeld 0 in beeld. Het geluid ervan valt op 0,35 s.
- Klokken, tellers en afstanden staan in beeld 0 al op hun echte waarde (geen "0 KM", geen halve cijferwissel).
- PINGED: `engine/v2look.py` doet dit automatisch (haakkaart op -0,3 s, fade_in = 1.0, klok stil tot 0,2 s, tl.json houdt het geluid op 0,35 s).
- ELAPSED: zelfde regels per script (geen `img *= min(1, t/...)` aan het begin, klok `max(0, t - V[i])`).
- Controle voor levering: beeld 0 bekijken op volle grootte.

## 2. Cover (kanaalpagina, zoeken)
- 1080x1920, gemaakt met `engine/covers/make_covers.py`.
- Bovenste melding: alleen het feit (wie, het getal, hoe lang).
- Onderste melding: op slot en wazig, alleen de vraag (WHAT CAUSED IT, THE CAUSE ...).
- Nooit de clou op de cover. Onderste 15% leeg (daar staan de weergaven).

## 3. Titel en beschrijving
- Geen clou in titel of beschrijving. De laatste zin van de video staat nergens in tekst.
- Elke Short met een lange versie: eerste regel van de beschrijving `Full story (8 min): <link>` plus een vastgezette reactie met dezelfde link.

## 4. Lange video's
- Ontworpen miniatuur 1280x720: groot getal links, beeld rechts, één witte balk. Geen still uit de video.
- Begin vanuit zwart mag (de miniatuur is de eerste indruk), maar de eerste minuut heeft beweging.

## 5. Plaatsen via vidIQ
- Gratis plan: 3 YouTube-uploads per dag, reset om 08:00 UTC.
- Een conceptwijziging zonder publishAt wist de geplande tijd: stuur publishAt altijd in dezelfde wijziging mee.
- Na het plaatsen controleren met vidiq_user_videos dat privacy = private en scheduledPublishAt klopt.
- Niets plaatsen zonder akkoord van Ferry op die versie.

## 6. Altijd
- Feiten tegen de bron; wat getekend of samengevat is, staat erbij.
- Geluid: gemeten, niet gehoord. 432 Hz-muziek.

## ELAPSED — beeldregels (vanaf Halifax v2, 27 nov 2026)
- **Tempo als PINGED:** 20–25 shots per Short, nooit langer dan ~4 s hetzelfde beeld (meetlat: max stilstand ≤ 4,5 s, ≥ 55 gebeurtenissen/min). Harde cuts met whoosh/thump.
- **Afwisseling per Short:** klok (seven-segment), bewegende kaart, echte archieffoto's (alleen push, nooit bewerkt of iets op getekend), eigen krant "The Elapsed Record" kort en ingezoomd, echte krantenscan met rode markering/stempel, teller, telegram/ticker.
- **Optie 2 — bewegende illustraties (standaard):** 2–4 eigen illustraties in gravure/krantenstijl die bewegen (rook, vlammen, golven, roeiboot, menigte). Altijd label **ILLUSTRATION** in beeld. **Geen fotorealistische AI-beelden.**
- **Echt vs. reconstructie:** echte foto's krijgen "PHOTOGRAPH · bron"; kaarten "DIAGRAM, NOT TO SCALE"; eindkaart vermeldt dat krant en illustraties reconstructies zijn.
- **Cijfers in beeld:** als bronnen verschillen, zeg dat ("Estimates vary; X is the figure most often cited").
- **Geen anachronismen:** een foto van na het moment komt niet in onze krant van dat moment.
- **Audio:** stem + 432 Hz-pad 12 dB onder de stem, eindmix genormaliseerd op −14 LUFS, true peak ≤ −1 dBTP.
- **Slot met trailerstem (vanaf 27 nov):** elke ELAPSED-video eindigt met de verteller ("Follow, …"), dan 0,15 s stilte en een bioscoopklap (braam + subdrop, 432 Hz), waarna een zware, warme trailerstem zegt: "Elapsed. — Every second. — Is on the record." Stem: Kokoro am_onyx, snelheid 0,78, −2 halve tonen, warme EQ, compressie, lichte saturatie en hallgalm. Eindkaart toont ELAPSED met gloed en de slogan woord voor woord op de stem. Bestanden: engine/elapsed/slogan/.

## Stemmen (vanaf 27 nov 2026, via vidIQ voiceover, 28 credits per 1.000 tekens)
- **PINGED:** Daniel — Steady Broadcaster (voiceId onwK4e9ZLuTAKqWW03F9). Hele vertelling.
- **ELAPSED:** Bill — Wise, Mature, Balanced (voiceId pqHfZKP75CvOlQylNhV4). Hele vertelling + vaste slogan-opname (engine/elapsed/slogan/bill.wav, hergebruiken, kost niets).
- Genereren met scriptLines (één regel per zin) → regeltijden opslaan → Ferry downloadt de mp3 (vidIQ-servers zijn vanuit de werkomgeving niet bereikbaar) → knippen op de opgeslagen starttijden.

## Vaste slotzin — ALTIJD, in elke video (vastgelegd 27 nov 2026)
Geen video gaat naar Ferry of online zonder het slot van zijn kanaal. Controle vóór elke oplevering: laatste 4 s bekijken én meten (de slotzin moet hoorbaar zijn).
- **PINGED Shorts:** laatste 1,2 s gaan over in de PINGED-eindkaart ("New story tomorrow.") met Daniel: *"Follow, and get pinged tomorrow."* Automatisch via engine/outro/outro_v2.py (render_v2.sh roept hem aan; eindbestand = v2_final.mp4). Opname: outro/vo_daniel.wav — één keer gemaakt, altijd hergebruiken (0 credits).
- **PINGED lange video's:** zelfde slotzin van Daniel + eindkaart in 16:9, na de laatste scène.
- **ELAPSED Shorts en lange video's:** bioscoopklap + Bill: *"Elapsed. Every second… is on the record."* met de ELAPSED-eindkaart (engine/elapsed/slogan/endcard.py, opname bill.wav/tr5.wav, 0 credits).
- Wie een video opnieuw maakt (nieuwe stem, nieuwe look), zet het slot er opnieuw achter — het slot hoort bij het eindbestand, niet bij een losse stap.

## Pakket-check vóór inplannen (vastgelegd 27 nov 2026, ook in het dashboard → Productie)
1. **Slotzin** zit erachter en is hoorbaar (zie hierboven).
2. **Titeltest** met vidIQ (vidiq_score_title, type short, met channelId en videoId): doel ≥ 85. Lager → vidiq_generate_titles (6 stuks), hashtags uit de titel halen, de opties zonder clou opnieuw scoren, beste kiezen. Ferry keurt de titel goed.
3. **Cover v3** (engine/covers/make_covers_v3.py): getal groot, weinig lege ruimte, rode cirkel + pijl naar de verborgen melding, clou verborgen. vidIQ-coverscore is gemaakt voor 16:9-thumbnails → alleen als grove richtlijn gebruiken (v2 → v3: 28 → 35, lege-ruimte-straf weg).
4. **Na inplannen:** in YouTube tijd, tags en cover nakijken (vidIQ laat soms tags vallen; bij wijzigen altijd privacy + publishAt meesturen).

## Hook v3: de eerste 3 seconden (vastgelegd 28 nov 2026, beide kanalen)
Aanleiding: Nvidia-Short presteerde in de opening op 0,75 van vergelijkbare Shorts, aan het eind op 0,94; 37% engaged views. Het gemiddelde wegswipen gebeurt na ±1,7 s.
1. Stem begint op 0,0 s. Eerste zin max. 8 woorden en max. 2,5 s, met een open vraag of tegenstrijdigheid (geen datum- of contextzin als opener).
2. Geluidsklap op frame 0 (alarm, inslag, notificatiepiep). Geen stilte, geen fade.
3. Frame 0 toont de inzet in reuzenletters (getal of situatie) en beweegt al. Het onderwerp is in het eerste beeld leesbaar.
4. Minstens 3 beeldwissels in de eerste 3 s.
5. Het slot sluit aan op het begin (herhaald kijken).
6. Meten: hookscore = engaged views ÷ views per Short (dashboard → Leerlus). Na 7 dagen vergelijken met de Shorts van vóór Hook v3.
