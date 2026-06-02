# Analyse comparative — Corsica 555 Gravel 2026

Comparaison de ma course (7e au scratch) avec les concurrents classés 2e à 6e,
à partir de leurs traces GPX. Données générées par
`scripts/race/build_flyby_data.py` et visualisables dans l'onglet **Flyby**.

> **Note méthodo.** Les fichiers GPX des concurrents stockent l'heure locale
> (CEST) avec un suffixe `Z`, soit +2h de décalage par rapport à ma trace
> (vrai UTC). Toutes les comparaisons sont donc faites en **temps écoulé
> depuis le départ de chacun** (départ groupé), ce qui élimine le décalage.
> Les deltas de temps par segment ne lisent que des différences internes à
> chaque trace → fiables quel que soit le fuseau.

## Tableau récapitulatif

| Coureur | Dist | D+ | Temps total | Temps mobile | Vit. mobile | Pauses | Temps pauses |
|---|---|---|---|---|---|---|---|
| Mathis (2e) | 486 km | 10 063 m | 26h02 | 23h51 | **20.4 km/h** | 13 | 1h44 |
| Clément (3e) | **501 km** | 10 557 m | 26h16 | 24h52 | 20.2 km/h | 8 | **1h02** |
| Benoît (4e) | 488 km | 10 165 m | 26h59 | 25h00 | 19.5 km/h | 9 | 1h37 |
| Laurianne (5e) | 485 km | 9 913 m | 27h28 | **26h33** | 18.2 km/h | 3 | **0h38** |
| Aurelio (6e) | 486 km | 10 354 m | 28h08 | 25h20 | 19.2 km/h | 13 | 2h11 |
| **Moi (7e)** | 489 km | 10 241 m | **28h48** | 26h12 | 18.6 km/h | 18 | **2h00** |

## Les deux enseignements majeurs

### 1. Mes arrêts m'ont coûté ~1h20 vs le 2e-4e

J'ai cumulé **2h00 de pauses** (18 arrêts), dont deux très longs aux
checkpoints :

- **CP1 Ghisoni (km 164) : 34 min** — Laurianne n'y est restée que **11 min**.
- **CP2 Crocicchia (km 333) : 37 min** — Laurianne **22 min**, Mathis encore
  moins.

À eux seuls, mes deux CP représentent **1h11**. Clément (3e) n'a posé que
1h02 de pauses *au total*. Si j'avais géré mes CP comme Laurianne (qui en a
fait le minimum), j'économisais ~40 min — sans rouler plus vite d'un seul
watt. **C'est le levier #1, et c'est gratuit : moins de temps à l'arrêt.**

### 2. Je roule bien en descente/plat roulant, je perds en grimpe longue

Mon temps **mobile** (26h12) est correct, mais ma vitesse mobile (18.6 km/h)
est la 2e plus basse. Le détail par segment montre un schéma net :

- **Je gagne du temps** sur les descentes et plats roulants : km 175-200 je
  reprends **18 min à Mathis**, km 375-400 je reprends **23 min à Laurianne**,
  km 350-375 je reprends **33 min à Aurelio**.
- **Je perds gros sur les grimpes longues** et la fin de course :
  - **Séquence C (km 425-450, +911 m)** : c'est mon pire secteur. Je tombe à
    **9.6 km/h** ; j'y perds **70 min sur Clément**, **39 min sur Benoît**.
    Fin de course + gros dénivelé + fatigue = effondrement du rythme.
  - **Montée CP1 (km 150-175, +631 m)** : −48 min sur Clément, −28 min sur
    Laurianne, à 12.5 km/h contre 16-21 km/h pour eux.
  - **km 250-275 (+700 m)** : −16 min sur Mathis.

Autrement dit : la pénalité n'est pas le pneu (cf. `tyre-selection-alt.md`,
validée), c'est le **rythme en montée longue sous fatigue**, surtout en
seconde moitié de course.

## Détail par concurrent

### Mathis — 2e (26h02)
Le plus rapide en mobile (20.4 km/h). M'a pris l'avantage surtout sur les
secteurs roulants de la 2e moitié (km 325-350 : +23 min) et les grosses
montées (km 250-275, 350-375). Je lui ai rerepris du temps en descente
(km 175-200, +18 min pour moi). Écart final ~2h41 : moitié pauses, moitié
rythme grimpe.

### Clément — 3e (26h16) — ⚠ détour de ~13 km
Sa trace fait **501 km contre 489 pour moi** (+12 km). La cause est visible :
entre **km 49 et 63**, il s'écarte de ma ligne jusqu'à **~2 km** (deux runs
de 6-7 km détectés). C'est soit une variante de tracé, soit une erreur de
navigation précoce — il a roulé ~13 km de plus. **Et malgré ça il finit 3e**,
parce qu'il pause très peu (1h02) et tient un rythme grimpe énorme : il me
prend **70 min sur la seule Séquence C**. C'est le coureur le plus instructif :
il montre ce que coûte ma fin de course.

### Benoît — 4e (26h59)
Profil proche du mien en vitesse mobile (19.5 vs 18.6) mais 23 min de pauses
en moins et bien plus solide en fin de course (Séquence C : +39 min sur moi).
Sur la montée CP1 (km 150-175) c'est le seul que je devance légèrement
(+16 min pour moi).

### Laurianne — 5e (27h28)
Le contraste le plus parlant côté **discipline d'arrêt** : seulement **38 min
de pauses** (3 arrêts) contre mes 2h00. Sa vitesse mobile est pourtant la plus
basse (18.2 km/h, < la mienne). **Elle finit 1h20 devant moi presque
uniquement parce qu'elle ne s'arrête pas.** Je la reprends nettement en
descente (km 375-400 : +23 min), elle me reprend en montée (km 150-175 :
−28 min).

### Aurelio — 6e (28h08)
Le plus proche de moi (40 min devant). Il a pausé encore plus que moi (2h11)
mais roulé un peu plus vite en mobile. Je le bats largement sur la descente
km 350-375 (+33 min pour moi), il me reprend sur les plats roulants.

## Ce que j'en retire pour la prochaine

1. **Discipline aux CP** : objectif 12-15 min par checkpoint, pas 35. Gain
   potentiel ~40-50 min sans effort supplémentaire.
2. **Rythme grimpe longue en seconde moitié** : travailler la capacité à
   tenir 13-15 km/h sur les cols après km 300 (fueling, gestion d'effort,
   pacing). C'est là que se jouent les places.
3. **Mon point fort à garder** : la descente et le plat roulant, où je suis
   compétitif avec le top 4. Ne pas le gâcher en sur-freinant.
