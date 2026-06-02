# Rétrospective entraînement — Corsica 555 Gravel 2026

Bilan des 6 mois (décembre 2025 → mai 2026) qui ont mené à la **7e place
scratch** au BikingMan Corsica 555 Gravel (29/05/2026, 489 km / 10 241 m D+,
28h48). Document de référence : ce qui a marché, ce qui a calé, et quoi
réutiliser pour la suite de saison (Ascend Xtri juillet, TPR septembre) et la
saison prochaine.

> Sources : API wellness intervals.icu (CTL/ATL/TSB, eFTP, charge, 6 mois) +
> **API Garmin Connect** (volume réel par sport, qu'intervals.icu masque),
> snapshots `daily/`, `context.md`, `decisions.md`, et l'analyse de course
> (`corsica-555-2026/comparison-analysis.md` + onglet Flyby du dashboard).

## 1. Résultat et profil de course

- **7e scratch**, 28h48 (26h12 mobile + 2h00 d'arrêts).
- **Grimpe régulière** : VAM ~759 m/h **constante du km 0 au km 489** (pas de
  fade de fin de course → bonne durabilité).
- **Descente / plat = points forts** (33 km/h en descente, 21 km/h au plat).
- **Limiteur du jour** : puissance de grimpe (déficit uniforme ~20 W vs le
  top 4), pas la fatigue ni le matériel. Détail dans `comparison-analysis.md`.
- **Pauses quasi toutes justifiées** (météo CP1, reset CP2, 2 micro-siestes,
  ravito) → ~15-25 min récupérables seulement.

## 2. L'arc de forme sur 6 mois (CTL / ATL / TSB)

| Date | CTL (fitness) | ATL (fatigue) | TSB (forme) | eFTP Ride |
|---|---|---|---|---|
| 15 nov 2025 | 66 | 40 | +26 | 277 W |
| 1 déc | 64 | 55 | +10 | 282 W |
| 1 jan 2026 | 66 | 75 | −9 | 277 W |
| 1 fév | 70 | 90 | −20 | 273 W |
| 1 mar | **85** | 107 | **−21.5** | 273 W |
| 1 avr | 95 | 104 | −9 | 283 W |
| 1 mai | **101** | 108 | −7 | 279 W |
| 28 mai (veille) | 90 | 65 | **+25.5** | — |

**Lecture :** montée de CTL **66 → 101 en ~5,5 mois** (+53%), construite par un
**bloc de surcharge profond février-mars** (TSB tenu à −20/−21 pendant des
semaines, ATL ~105-107) puis un **maintien haut en avril-mai** avant
l'affûtage. La fitness a été bâtie par l'accumulation, pas par des pics isolés.

### Volume réel par sport (Garmin Connect, 1 déc → 29 mai)

| Sport | Séances | Heures | km | D+ |
|---|---|---|---|---|
| **Vélo** | 234 | **303 h** | 6 821 | **96 865 m** |
| Course à pied | 59 | 40 h | 387 | 6 003 |
| Renforcement | 68 | 29 h | — | — |
| Ski de piste | 6 | 13 h | 162 | 14 870 |
| Yoga / mobilité | 20 | 12 h | — | — |
| Marche / rando | 8 | 5 h | 30 | 526 |
| Ski de rando | 1 | 3 h | 17 | 1 254 |
| Natation | 9 | 2 h | 8 | — |
| **TOTAL** | **405** | **408 h** | **7 425** | **119 518 m** |

Lecture :
- **Le vélo est le moteur** : 303 h (74% du temps) et surtout **96 865 m de D+
  en entraînement** (~16 000 m/mois). Cette énorme base de grimpe explique la
  **durabilité** observée en course (VAM constante sur 27h).
- **Renfo 29 h + yoga 12 h = pilier prévention** (épaule/nuque/genou) assumé et
  régulier → **zéro incident épaule en course**. À conserver tel quel.
- **Natation 2 h sur 6 mois = micro-dose**, exactement la consigne `context.md`
  (ne pas empiler nage + posture vélo + force sur une épaule fragile).
- **13 h de ski de piste** l'hiver = volume de descente / cross-training sans
  charge posture vélo — entretien sympa de la base sans stress épaule.
- **Nuance clé** : la base de grimpe (volume + D+) était énorme, mais la
  **puissance de grimpe haute** n'a pas été développée (eFTP plat, aucun test
  max — cf. §3). Beaucoup de dénivelé en Z2, peu de seuil/PMA en côte.

### Charge & séances clés

- Charge hebdo moyenne ~**660**, profil en vagues (3-4 semaines montantes, 1
  plus basse). Pics : **mi-mars (~995)**, mi-avril (~950), fin février (~860).
- Sorties longues structurantes (Garmin) :

| Date | Sortie | Durée | Distance | D+ |
|---|---|---|---|---|
| 18 avr | **BRM ~400 (Gillonnay)** | 13.7 h | 399 km | 3 798 m |
| 21 mar | Crozet montagne | 9.3 h | 208 km | 3 938 m |
| 3 avr | Crozet | 8.9 h | 194 km | 3 743 m |
| 20 fév | Crozet | 8.2 h | 237 km | 1 490 m |

Le **BRM 400 du 18 avril** est le pic de spécificité (charge 571) — et la
source de la fatigue retardée gérée pendant l'affûtage (cf. §4).

### Répartition par type de séance (export 6 mois, 483 activités)

| Type | Séances | Heures | Charge |
|---|---|---|---|
| Vélo base Z1-Z2 / divers | 220 | 227 h | 8 309 |
| Endurance / sorties longues | 18 | 68 h | 2 917 |
| Course à pied | 78 | 55 h | 2 717 |
| SST / seuil | 36 | 49 h | 2 945 |
| Renfo / workout | 69 | 41 h | 492 |
| Ski | 10 | 16 h | 215 |
| Yoga | 21 | 14 h | 86 |
| Intervalles / VO2 | 16 | 13 h | 937 |
| Heat training | 6 | 5 h | 165 |
| Natation | 10 | 2 h | 69 |

### Distribution d'intensité — vélo (le point clé)

En classant chaque sortie vélo par intensité (IF×100) :

| Zone | Part du temps vélo |
|---|---|
| Récup / très facile (<60) | 32% |
| Endurance Z2 (60-70) | 43% |
| Tempo (70-78) | 18% |
| **Seuil / SST (78-88)** | **5%** |
| **VO2 et + (≥88)** | **2%** |

**~75% du temps vélo sous 70 IF, et seulement ~7% à seuil ou au-dessus**
(22 sorties sur 254). C'est une distribution **très polarisée vers le bas** —
parfaite pour bâtir la base d'endurance (et ça a marché : durabilité), mais
elle explique objectivement pourquoi le **plafond de puissance de grimpe** n'a
pas progressé. Le travail à haute intensité était quasi absent du plan.

## 3. eFTP : la vérité à retenir

L'**eFTP est resté à plat (~273-284 W, effectif ~278 W) sur les 6 mois**, mais
**aucun test maximal n'a été fait** sur la saison → le modèle extrapole à partir
de séances sous-maximales et **sous-estime probablement**. Référence : **FTP
2024 = 310 W** (−11,5% aujourd'hui).

**Implication course :** l'analyse comparative montre qu'à forme 2024 (310 W),
la VAM serait passée de 759 à ~846 m/h → ~80 min gagnés en montée → **3e/4e au
lieu de 7e**. Le plafond de puissance de grimpe est LE levier pour monter au
classement. Ce n'est pas un déficit de durabilité (déjà bonne) ni de pacing.

## 4. L'affûtage (taper) — cette fois il a parfaitement marché

C'est le point que je voulais documenter : **le meilleur taper jusqu'ici**.

| | Début taper (~14 mai) | Veille course (28 mai) | Δ |
|---|---|---|---|
| CTL (fitness) | ~98 | 90 | **−8% seulement** (fitness conservée) |
| ATL (fatigue) | ~95 | 65 | **−32%** (fatigue évacuée) |
| TSB (forme) | +3 | **+25.5** | montée propre et progressive |

**Pourquoi ça a marché :**

1. **Fatigue évacuée sans perdre la fitness** : ATL −32% pendant que CTL ne
   perd que 8% → arrivée à +25 de TSB avec 89% du pic de CTL. C'est la
   signature d'un bon affûtage (delester l'ATL, garder le CTL).
2. **Une frayeur convertie en fraîcheur** : début mai, SST raté + mauvaise
   réponse au heat training. Interprété (à juste titre) comme **fatigue
   retardée** du BRM 400 + semaine >19h qui suivait, **pas une perte de
   forme**. Décision clé : **ne pas courir après la qualité manquée**, mais
   transformer la charge en fraîcheur. C'est exactement ce qui a produit le
   +25 de TSB.
3. **Maintien de l'intensité légère, baisse du volume** : sur la fenêtre
   d'affûtage, des touches courtes (heat training home-trainer ~135 bpm, SST
   2x20, runs taper) maintenaient le système éveillé sans recharger l'ATL.
4. **Discipline HRV/sommeil** : décisions pilotées par la réponse du lendemain
   (genou/épaule/nuque) + HRV comme signal d'alerte, jamais comme feu vert
   isolé. Ex. le 13/05, HRV 61 < seuil → 2x20 au lieu de 3x20, pas de 3e rep.

**À répliquer :** ~2 semaines, CTL qu'on laisse glisser de ≤10%, ATL qu'on
casse de ~30%, viser TSB +20 à +25 la veille, intensité courte conservée,
zéro session "de rattrapage".

## 5. Heat training & acclimatation chaleur

Pilier souvent oublié et pourtant central ici : un **bloc d'acclimatation
chaleur** qui a fait **double emploi — préparer la chaleur corse ET servir de
stimulus d'affûtage** (faible stress mécanique → ne recharge pas l'ATL, protège
genou/épaule). C'est en partie ce qui rend le taper du §4 aussi propre.

**Protocole** (home-trainer, environnement chaud) :
- 45-52 min, départ ~180 W puis **step-down progressif pour plafonner la FC à
  ~135 bpm** — objectif "stress thermique, pas charge d'entraînement", sortir
  **frais, pas vidé**.
- **Hydratation pendant la séance** (500-750 ml + sel), pas après — pratique
  opérationnelle répétée pour la course.

**Déroulé :** séances actives dès début mai → **bloc dédié 11-17 mai** →
entretien jusqu'au 22-23 mai (dernière séance active 40') → **maintien passif
en Corse J-4 à J-1** (exposition chaleur douce, sans chercher la dérive cardio).
Le sauna prévu en fin de bloc a été annulé, compensé par l'exposition sur place.

**Signaux d'adaptation captés :**
- **+7 W à cardio constant** entre deux séances (5 mai) = tolérance chaleur en
  hausse.
- **Dérive cardio retardée** de J1 à J2 (apparition min 20 → min 28-30) à NP
  inférieure et FC contrôlée.

**Le gain opérationnel #1 — le sweat rate mesuré :**
- **~1.6 L/h à jeun** (vrai baseline) vs **~1.9 L/h en post-prandial**.
- Hydratation entraînée à **750-870 ml/h ingérés** → cible course atteinte
  *avant* la course, restait à valider la tolérance gastrique sur la durée
  (rôle de la sortie longue + des ravitos).

**Leçons notées (à appliquer la prochaine fois) :**
- **Faire le heat à jeun**, pas après le petit-déj (pattern récurrent corrigé).
- **Cadence trop basse** en heat (73) → viser 80-85.
- Le 7 mai, séance heat "très dure" (−13 W, +6 bpm) = **symptôme de la fatigue
  retardée du BRM 400**, pas un échec d'acclimatation. À ne pas mal lire.

## 6. Gestion des limiteurs (le vrai garde-fou)

Le limiteur n'est pas cardio mais **durabilité épaule / nuque / haut du dos**
(tendinopathie coiffe traitée depuis oct. 2025 ; DNF Graaalps 2025 sur descente
MTB) + **genou** (chondropathie fémoro-patellaire post-Saintelyon 2024).

Ce qui a protégé la ligne d'arrivée :
- **Course conduite intelligemment** : sur la Séquence C (descente la plus
  dangereuse pour l'épaule), ralenti volontaire en amont, positions déjà
  acquises → fraîcheur pour descendre en sécurité. Lucidité tactique = atout.
- **Matériel verrouillé** (09/05) : pas de prolongateurs, cintre rehaussé
  (potence inversée), Race King 2.2 @ 1.5 bar. Validé : plus confortable sur
  gravel, endurance route pas pénalisée, épaule 1/10 à H+2-4.
- **Changements de position toutes les 20-30 min** (assis / mains hautes /
  danseuse) : le limiteur est la **durée en position**, pas le cockpit.
- **Natation en micro-dose** seulement, **renfo** prudent → ne pas empiler
  charge posture longue + nage + force.

## 7. Ce qui a marché (à garder)

- **Construction longue et patiente** du CTL (66→101) par vagues, sans pic
  héroïque isolé.
- **Bloc de surcharge fév-mars** assumé (TSB −20 plusieurs semaines) puis
  maintien — la fitness de mai en découle directement.
- **Affûtage discipliné** (cf. §4) — le plus réussi à ce jour.
- **Durabilité** : VAM constante sur 27h, zéro fade → bâtie sur 303 h de vélo
  et ~97 000 m de D+ d'entraînement.
- **Pilier prévention** : 29 h de renfo + 12 h de yoga répartis sur 6 mois,
  nage en micro-dose → aucun incident épaule/nuque/genou en course.
- **Bloc heat à double emploi** : acclimatation chaleur + stimulus d'affûtage
  sans charge mécanique, avec **sweat rate mesuré (1.6 L/h à jeun)** qui a
  calibré l'hydratation course en amont. Modèle à reprendre.
- **Pilotage par la réponse du lendemain + HRV en garde-fou**, pas en feu vert.
- **Décisions matériel/posture** centrées sur l'épaule → aucun incident
  épaule/nuque en course.

## 8. Ce qu'il faut améliorer (prochaine cible)

1. **Relever le plafond de puissance de grimpe** : objectif retour vers
   **FTP ~300-310 W** (niveau 2024). C'est ~20 W en montée tenus toute la
   course = 1 à 3 places. Le déficit est uniforme → c'est du seuil/PMA, pas
   du pacing.
2. **Tester l'eFTP pour de vrai** : aucun test max sur 6 mois → modèle
   sous-estimé et pilotage à l'aveugle. Programmer un ramp test ou 20 min
   all-out **2-3 semaines après Corsica** (fatigue retombée), puis re-caler les
   zones avant le bloc Ascend.
3. **Convertir le volume D+ en puissance, pas seulement en endurance** : 96 865 m
   de D+ grimpés en 6 mois, mais **seulement ~7% du temps vélo à seuil ou
   au-dessus** (cf. distribution §2). Grosse base, plafond non poussé. Ajouter
   des **blocs seuil/PMA en côte** (cols en Z3 bas/SST, VO2 courts) **sans
   augmenter le volume total** — viser ~15-20% du temps vélo à ≥78 IF au lieu
   de 7%. Le dénivelé est déjà là, il manque l'intensité dessus.
4. **Garder les points forts** : descente, plat roulant, durabilité, et le
   pilier prévention (renfo 29h + yoga 12h) — ne rien sacrifier de ce côté en
   cherchant les watts.

## 9. Template réutilisable (prochains gros objectifs)

- **~5-6 mois** de construction CTL par vagues 3:1 ; viser un CTL cible
  cohérent avec l'épreuve (ici 100 a suffi pour finir fort en endurance).
- **Bloc de surcharge** assumé à mi-prépa (TSB −15/−20 quelques semaines),
  suivi d'un **maintien haut** plutôt que d'une nouvelle surcharge tardive.
- **1-2 épreuves longues spécifiques** (type BRM 400) ~4-6 semaines avant, en
  sachant qu'elles laissent une **fatigue retardée de 1-2 semaines** → la
  planifier, ne pas la confondre avec une perte de forme.
- **Affûtage 2 semaines** : −≤10% CTL, −~30% ATL, TSB +20/+25 la veille,
  intensité courte maintenue, aucune séance de rattrapage.
- **Bloc heat (~1-2 semaines) si épreuve par temps chaud** : home-trainer 45-50',
  cap FC ~135 bpm, hydratation pendant, sortir frais. Double bénéfice
  acclimatation + stimulus taper-compatible. **Mesurer le sweat rate à jeun**
  pour caler l'hydratation course. Le placer pendant l'affûtage, pas avant.
- **Garde-fous limiteurs** en continu : réponse du lendemain = juge de paix,
  HRV = alerte, matériel/posture verrouillés tôt, micro-dose nage/force.
- **Tester l'eFTP** au moins une fois par cycle pour ne pas piloter à l'aveugle.

---
*Généré le 2026-06-02 à partir des données intervals.icu + journal
d'entraînement. Métriques de course : voir
`corsica-555-2026/comparison-analysis.md` et le dashboard public.*
