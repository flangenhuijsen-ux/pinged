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
