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

## Les enseignements

### 1. Mes pauses sont peu compressibles

J'ai cumulé **2h00 de pauses** (18 arrêts), mais une fois triées par
compressibilité, presque tout est justifié :

- **CP1 Ghisoni (~20 min)** : attente volontaire que la pluie passe, pour ne
  pas entamer la nuit trempé (risque hypothermie). Décision météo, défendable.
- **CP2 Crocicchia (~37 min)** : reset complet — manger solide, lavage,
  hygiène du cuissard. Investissement qui protège la 2e moitié sur 30h.
- **2 mini-siestes (~10 min)** : gérer l'endormissement, sécurité.
- **Le reste (~50 min)** : ravitaillement et remplissage de bouteilles,
  incompressible.

**Temps réellement récupérable : 15-25 min au mieux.** Contrairement à ce que
suggère l'arithmétique brute, les pauses **ne sont pas le levier** pour gagner
des places ici : elles étaient quasi toutes justifiées. Le levier est ailleurs.

### 2. Ma grimpe est régulière — la durabilité est une force

La moitié de mon temps en mouvement (13h04 sur 26h12) se passe en montée
(>3%), et c'est là que se joue tout l'écart avec les places devant. Mais ma
**VAM est remarquablement stable du départ à l'arrivée** :

| Portion | Temps grimpe | Ascension | VAM |
|---|---|---|---|
| Course live (km 0-420) | 11h18 | 8 621 m | **763 m/h** |
| Zone Séquence C (km 420-460) | 1h32 | 1 115 m | 730 m/h |
| Total | 13h04 | 9 926 m | 759 m/h |

Pas d'effondrement de fin de course : 730 m/h sur Seq C contre 763 en course
live. Les `9.6 km/h` sur la Séquence C, c'est une pente plus raide (911 m /
13.6 km) à VAM quasi normale — pas un coup de moins bien. **Et ce ralenti
était tactique** : positions verrouillées (6e à +15 km imprenable, 8e à
−20 km à l'abri), donc j'ai levé le pied pour être frais sur la descente de
Seq C, la plus dangereuse pour mon épaule. Bonne gestion, pas une faiblesse.

### 3. Le déficit est un écart de puissance de grimpe uniforme

Je roule bien en descente (33 km/h) et correctement au plat (21 km/h). Je
gagne même du temps là-dessus : +18 min sur Mathis (km 175-200), +33 min sur
Aurelio (km 350-375). Le déficit n'est donc **pas** un trou localisé ni un
problème de pneu (cf. `tyre-selection-alt.md`, validée) : c'est un **manque de
puissance de grimpe réparti sur toute la course**. Je grimpe à ~760 m/h là où
il faudrait ~810 (6e) à ~835 (4e), soit **~20 W de plus en montée tenus du
début à la fin**.

## Puissance & forme 2024

Estimation de ma puissance de grimpe de course : **~2.6 W/kg (~237 W)** à
~91 kg système chargé, soit ~85% de mon eFTP 2026 (278 W) — cohérent pour de
la montée fractionnée sur 27h.

| Cible | VAM requise | Puissance montée | Temps mobile à gagner |
|---|---|---|---|
| 6e | 810 m/h (+7%) | ~253 W / 2.78 W/kg | 49 min |
| 4e | 833 m/h (+10%) | ~260 W / 2.86 W/kg | 69 min |
| 2e | 922 m/h (+21%) | ~285 W / 3.15 W/kg | 138 min |

**Forme 2024 (FTP 310 W vs 278 aujourd'hui, +11.5%)** : à %FTP égal, ma
puissance de grimpe serait passée à ~263 W, ma VAM à **~846 m/h**, gagnant
**~80 min sur la montée**. De quoi finir **3e/4e au lieu de 7e** — à condition
d'exprimer ce surplus dans les 2/3 où la course était encore ouverte. Le 2e
restait hors d'atteinte même à 310 W ce jour-là.

Comme mon déficit est **uniforme** et ma durabilité déjà bonne, une FTP plus
haute le comblerait partout de la même façon : c'est un **plafond aérobie**
qu'il faut relever (volume Z2 long + blocs grimpe), pas un problème de pacing
ni de fin de course.

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
parce qu'il pause très peu (1h02) et tient une puissance de grimpe supérieure
sur l'ensemble du parcours. (Le `+70 min` sur la Séquence C est trompeur :
j'y roulais en mode tactique, positions déjà acquises.)

### Benoît — 4e (26h59)
Profil proche du mien en vitesse mobile (19.5 vs 18.6) mais 23 min de pauses
en moins. Sur la montée CP1 (km 150-175) c'est le seul que je devance
légèrement (+16 min pour moi). L'écart se fait sur un cumul de petites montées,
pas sur un secteur unique.

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

1. **Le levier #1 est la puissance de grimpe, pas les pauses.** Mes arrêts
   étaient quasi tous justifiés (météo, reset CP2, sommeil, ravito) :
   ~15-25 min récupérables au mieux. Le vrai gain est de monter ~20 W en
   montée, tenus toute la course → +1 à 2 places.
2. **Relever le plafond aérobie** : mon déficit est uniforme (VAM stable
   ~760 m/h), donc c'est la FTP/le seuil qu'il faut remonter, via volume Z2
   long + blocs grimpe. À forme 2024 (310 W) j'étais 3e/4e sur ce même
   parcours.
3. **Garder mes points forts** : descente et plat roulant (compétitif avec le
   top 4), durabilité (VAM constante sur 27h), et la lucidité tactique de fin
   de course (gestion d'épaule sur Seq C). Rien à changer là-dessus.
