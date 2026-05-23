# Corsica 555 - Roadbook / Projection

Generated 2026-05-11 from BRM 400, Morocco 2024 and Graaalps DNF data,
plus `terrain_analysis.md`.

Updated 2026-05-15 with the race-site terrain-aware pacing model
(`corsica_555_race_king_30h`) and the current carried nutrition plan.

## TL;DR

- **Départ**: vendredi 29 mai 07:00, Porto-Vecchio
- **Pacing site race**: modèle terrain-aware Race King, **28h58 roulées**
  théoriques + **1h15 arrêts lean** = arrivée ~**samedi 13h10** si `r=1.00`.
- **Scénario mental par défaut**: `r_global ≈ 0.90` = arrivée
  ~**samedi 16h25** avec les mêmes arrêts lean. C'est le bon scénario robuste.
- **Scénario dégradé acceptable**: 36-37 h = arrivée samedi soir, toujours large
  vs cutoff.
- **Nutrition embarquée**: 11 sachets × 90 g + 17 gels × 45 g =
  **1 755 g glucides**, soit **29h15 à 60 g/h**. Solide route = marge, sel,
  texture, moral.
- **Cutoff officiel**: 60 h (marge ~24-26 h)

Marges:
- Scénario clean, sans sommeil planifié, arrêts tenus: 30-31 h → arrivée sam
  13-14h.
- Scénario robuste data-calibré / `r_global ~0.90`: 33-34 h → arrivée sam
  16-17h.
- Scénario épaule réagit / météo dégradée: 36-37 h → arrivée sam 19-20h.

Lecture tactique:
- **Mode site race 30h**: possible si tout est propre: sec, lucidité haute,
  épaule/nuque calmes, aucune dérive gastrique. Ne pas le chasser à la pédale.
- **Mode par défaut `r=0.90`**: rouler régulier, arrêts efficaces, sommeil court
  seulement si le signal qualité baisse. C'est le scénario à piloter.
- **Mode sécurité**: si erreurs de ligne, somnolence, épaule/nuque qui montent
  ou pluie sur Sequence C, accepter 36-37 h. Le cutoff n'est pas le problème.

## Course Summary

| Métrique | Valeur |
|---|---:|
| Distance | 487.1 km |
| D+ smoothed | 9 875 m |
| D- smoothed | 9 884 m |
| Point culminant | 1 300 m (km 174) |
| Surface non-pavée confirmée/suspecte | ~72 km (~15%) |
| Checkpoints | CP1 Ghisoni km 164, CP2 Crocicchia km 333 |
| Cutoff officiel | 60 h |

## Timeline cible par km

Heures depuis un départ vendredi 29 mai à 07:00. La colonne `site 30h` utilise
le modèle de l'app race avec les arrêts lean intégrés. La colonne `r=0.90`
applique le même modèle avec un rythme réel 10 % plus lent, ce qui est le
scénario mental par défaut.

| Km | Étape | Site 30h | r=0.90 | Notes opérationnelles |
|---:|---|---|---|---|
| 0 | Départ Porto-Vecchio | Ven 07:00 | Ven 07:00 | Petit-déj 5h45-6h00: 500 ml glucidique + banane + café. |
| 17 | Début Sequence A — gravel précoce | Ven 08:02 | Ven 08:09 | Manger AVANT entrée. Assis, contained, RPE 4. |
| 31.9 | Premier water check | Ven 09:14 | Ven 09:29 | Refill si un bidon <60 %. |
| 42 | Fin Sequence A | Ven 10:12 | Ven 10:34 | Premier vrai point de contrôle du pacing rough. |
| 59.6 | Zonza — ravito optionnel | Ven 11:07 | Ven 11:34 | Tout est probablement ouvert. Stop seulement si chaleur, faim ou bidons bas. |
| **78** | **Serra — stop solide clé** | **Ven 12:20** | **Ven 12:55** | Proxi probablement fermé à midi; viser A Scopa / point chaud. Vrai salé + backup. |
| 95 | Top 1ère paved climb majeure | Ven 13:23 | Ven 14:05 | Chaleur attendue, hydratation stricte. |
| 132.3 | Eau avant track km 136-147 | Ven 15:32 | Ven 16:28 | Plein avant long suspect track. |
| 137 | Entrée Sequence B — long suspect track | Ven 15:52 | Ven 16:49 | Climb postural endurance, cadence relax. |
| 146 | Top track 1 276 m | Ven 16:46 | Ven 17:50 | Première grosse altitude. Rester calme en descente. |
| **164** | **CP1 Ghisoni — ravito nuit** | **Ven 17:48** | **Ven 18:56** | **Stop obligatoire: eau, sel, vrai solide, 2 solides de nuit, couches up.** |
| 174 | High point 1 300 m | Ven 18:48 | Ven 20:03 | Nuit proche/installée selon scénario. |
| 182.2 | Le Chalet — bonus fragile | Ven 19:08 | Ven 20:25 | Ferme probablement à 19h. Ne pas compter dessus. |
| 200.5 | Eau avant gap nuit | Ven 20:15 | Ven 21:39 | Plein complet avant ~50 km. |
| 251 | Top 2e altitude block | Ven 23:20 | Sam 01:04 | Nuit profonde. Caffeine si vraie somnolence. |
| 305.5 | Convenience/water bonus | Sam 02:18 | Sam 04:22 | Solide incertain; traiter comme eau/reset. |
| 313 | Sequence rough courte | Sam 02:50 | Sam 04:58 | Cocottes, vitesse plafonnée. |
| **333.4** | **CP2 Crocicchia — reset** | **Sam 04:05** | **Sam 06:20** | **Base vie 24h: café, petit-déj simple, 15 min mini, check épaule/nuque.** |
| 337.8 | Fontaine CP2 area | Sam 04:20 | Sam 06:37 | Dernier vrai plein avant long gap. |
| 377.8 | Boulangerie/alimentation | Sam 06:34 | Sam 09:06 | Si rapide: trop tôt. Si `r=0.90`: très bon ravito solide. |
| 387.9 | Eau avant mixed track | Sam 07:08 | Sam 09:42 | Plein juste avant km 389-411. |
| 389 | Entrée late mixed track corridor | Sam 07:11 | Sam 09:45 | Manger AVANT. 13 km rough rolling. |
| 419 | Fin rough -8.7 % | Sam 08:55 | Sam 11:41 | Speed cap absolu. Walk OK si dégradé. |
| **428.5** | **Nonza — A Matsuletta** | **Sam 09:29** | **Sam 12:18** | **Stop clé final: salé léger + Coca/café + eau avant Sequence C.** |
| **433.3** | **Last fuel pre-Sequence C** | **Sam 09:55** | **Sam 12:46** | Convenience ouverte dans les deux scénarios. Dernier reset mental. |
| 440.1 | Début gravel climb 8 % | Sam 10:30 | Sam 13:25 | Le climb le plus engageant de la course. |
| 447 | Top 955 m | Sam 11:24 | Sam 14:26 | Walking subsections valide si surface/épaule dégradées. |
| 455 | Fin descente gravel | Sam 11:49 | Sam 14:53 | Le gros technique est passé. |
| 462.5 | Urban resupply starts | Sam 12:04 | Sam 15:10 | Urgence seulement. Un stop max dans l'urbain. |
| **487.1** | **Arrivée Biguglia** | **Sam 13:12** | **Sam 16:25** | Finish. |

## Pace par type de segment

Vitesses cibles raffinées avec les données Morocco 2024 (cf section
"Morocco calibration" plus bas).

| Segment | Distance | Vitesse cible | Notes |
|---|---:|---:|---|
| Uphill ≥+6% (paved) | 43 km | 8-9 km/h | Morocco: 8.0 km/h moyenne sur durée |
| Uphill +3 à +6% | 90 km | 11-12 km/h | Morocco: 11.1 km/h |
| Uphill +1 à +3% | 70 km | 16-17 km/h | Morocco: 16.6 km/h |
| Flat ±1% (paved) | 83 km | 23-25 km/h | Morocco: 24.9 km/h |
| Downhill -1 à -3% | 70 km | 28-30 km/h | Morocco: 29.4 km/h |
| Downhill -3 à -6% | 91 km | 29-31 km/h | Morocco: 30.1 km/h |
| Steep downhill ≤-6% | 39 km | 35-42 km/h | Morocco: 40.6 km/h, prudence cocottes |
| Gravel sections | 72 km | 10-13 km/h | Cocottes systématiques, Sequence C plus lent |
| **Moyenne mouvement robuste** | 487 km | **16.0-16.5 km/h** | Référence Morocco conservatrice |
| **Moyenne mouvement optimiste** | 487 km | **17.5 km/h** | Conditions parfaites / très peu d'arrêts |

## Morocco calibration — application des vitesses observées à Corse

Morocco 2024 = 913 km / 22.0 km/h moving / 87% paved / 71 km rough finis sans
incident épaule majeur. La table des vitesses par grade est la meilleure
référence pour projeter Corse.

Application directe des speeds Morocco à la grade distribution Corse:

| Grade | Corse km | Morocco speed | Temps projeté |
|---|---:|---:|---:|
| ≤ -6% | 39 | 40.6 km/h | 0h58 |
| -6 à -3% | 91 | 30.1 km/h | 3h01 |
| -3 à -1% | 70 | 29.4 km/h | 2h23 |
| flat ±1% | 83 | 24.9 km/h | 3h20 |
| +1 à +3% | 70 | 16.6 km/h | 4h13 |
| +3 à +6% | 90 | 11.1 km/h | 8h06 |
| ≥ +6% | 43 | 8.0 km/h | 5h22 |
| **Total paved-equivalent** | **487** | | **27h23** → **17.8 km/h** |

Si Corse était 100% paved comme Morocco, le moving avg serait 17.8 km/h.
Mais Corse a 72 km de gravel **concentré** (vs Morocco étalé),
notamment 14 km à grade extrême sur Sequence C.

Pénalité gravel estimée: +2-3 h sur le moving time → moving avg réaliste
**16.0-16.5 km/h**. Le site race affine ensuite cette référence avec le
modèle terrain-aware + `r_global`.

Validation croisée — ce que Morocco confirme:
- 913 km / 61h45 / 2 nuits finis = moteur ultra confirmé
- 71 km rough absorbés sans drame épaule = **70 km est ton plafond de
  tolérance posturale si étalé**. Corse a la même exposition rough mais
  concentrée → discipline encore plus stricte sur les 72 km Corse.
- 20h09 non-moving sur 913 km = ratio standard ultra (~32%). Sur Corse
  comprimée, viser plutôt 18-22% non-moving (6-7 h sur 33-35 h total).

## Budget temps — modèle site race

Le site race n'est pas un plan à forcer: c'est le modèle de référence que
l'app adaptera avec `r_global`. Le modèle statique donne:

| Poste | Site 30h (`r=1.00`) | Robuste (`r=0.90`) |
|---|---:|---:|
| Temps roulé terrain-aware | 28h58 | 32h11 |
| Arrêts lean intégrés | 1h15 | 1h15 |
| Sommeil planifié | 0h00 | 0h00 |
| **Total projeté** | **30h12** | **33h25** |
| **Arrivée** | **Sam ~13h10** | **Sam ~16h25** |

Arrêts lean du modèle:

| Km | Durée | Fonction |
|---:|---:|---|
| 60 | 6 min | Stop optionnel eau/café après Sequence A. |
| 110 | 9 min | Ajustement / eau après premier gros bloc. |
| 164 | 18 min | CP1, ravito nuit, couches. |
| 200 | 3 min | Eau avant gap nocturne. |
| 333 | 18 min | CP2, petit-déj/reset. |
| 385 | 9 min | Ravito solide si ouvert. |
| 433 | 12 min | Dernier reset avant Sequence C. |

Utilisation:
- Si `r_global` reste proche de 1.00: ne pas ajouter d'arrêt inutile. Les
  commerces trop tôt fermés le matin ne valent pas une attente.
- Si `r_global` glisse vers 0.90: c'est normal et probablement optimal. Les
  ravitos de 377-385 deviennent utilisables, ce qui compense le rythme plus
  bas.
- Si sommeil ou météo ajoute 1-3 h: rester propre. Le vrai objectif est
  jugement + épaule/nuque + alimentation, pas l'heure d'arrivée.

## Indicateurs de validation en course

Cocher mentalement vs le plan — si en retard ne PAS compenser par accélération:

- ☐ **Km 164 (CP1) vers Ven 18:00-19:00** = scénario robuste parfaitement on plan.
- ☐ **Km 333 (CP2) vers Sam 04:00-06:30** = excellent, même sans sommeil.
- ☐ **Km 440 vers Sam 10:30-13:30** = Sequence C largement en journée.
- ☐ **Km 487 (arrivée) vers Sam 13:00-16:30** = fenêtre site/r=0.90.

Garde-fous conservateurs:

- CP1 après Ven 20:30 = scénario lent, mais pas grave. Ne pas forcer.
- CP2 après Sam 10:00 = accepter 36-37 h si besoin, protéger Sequence C.
- Km 440 avant Sam 16:00 = lumière du jour encore garantie sur le gros final.
- Arrivée avant Sam 20:00 = scénario worst-case toujours acceptable.

Si retard >2 h sur CP1: garder le rythme. Le temps total montera de 2-3 h,
pas plus, sauf vrai problème mécanique/corporel.

## Triggers de décision épaule (apprentissage Graaalps)

| Signal | Action |
|---|---|
| Épaule 1/10 avant km 100 | Normal sur ultra. Continuer. |
| Épaule **2/10 avant CP1** (km 164) | Réduire puissance sur climbs paved suivants. Pas de drops. Plus de rotations position. |
| Épaule **2/10 entre CP1 et CP2** | Reset complet à CP2 (≥15 min épaule au repos, étirements doux). |
| Épaule **3/10 avant km 433** | Walking subsections de km 447-455 = OPTION VALIDÉE. Pas un échec. |
| Épaule **≥4/10 avant km 200** | Considérer DNF. C'est le critère Graaalps. |
| Épaule **≥3/10 avant km 433 + incapacité cocottes** | DNF justifié. |

DNF est une décision valide, pas un échec. À se rappeler en état dégradé.

## Décisions critiques en course

**Sommeil — défaut site race**: aucun sommeil planifié. Le modèle part du
principe que les arrêts sont courts et que le sommeil n'est déclenché que par
le signal qualité.

**Sommeil opportuniste**:
- 10-20 min si somnolence légère ou baisse de vigilance.
- 30-45 min si vraie dette de lucidité, micro-erreurs, ou besoin de reset
  épaule/nuque.
- Pas de sommeil imposé si tu es lucide, alimenté, et mécaniquement stable.
- Vrai bloc 2-3 h uniquement si continuer devient unsafe: dérive de trajectoire,
  erreurs de ligne sur terrain facile, incapacité à manger, ou épaule/nuque qui
  demande un arrêt long.

**Météo Sequence C** (km 440-455) — vérifier la veille du départ:
- Sec: gravel à -8.9% OK avec speed cap
- Mouillé: walk les portions techniques. +1-2h sur le temps total.
- Si météo annonce orage samedi midi: viser CP2 plus tôt pour passer Sequence C avant.

**Position vélo**:
- Setup verrouillé: pas de barres aero, potence inversée, RaceKing 45 mm @ 1.5 bar
- Rotation position toutes les 20-30 min sur asphalte (alarme Wahoo)
- Cocottes par défaut sur toute section rough listée. Jamais drops sur track.

## Race week — taper J-12 à J-0

Calé sur les références Corse 2024 (finished, Form race-day +29 = trop frais, 4-5h démarrage difficile), Morocco 2024 (finished, Form +20 = bien dès le départ — modèle visé) et BRM 400 (finished, Form +11). **Cible Form race-day +18-22**, HRV 65-75, RHR ≤ 42.

| Jour | Date | Activité | Heat | Load |
|---|---|---|---|---:|
| J-12 | Dim 17/05 | 3h gravel 250W bosses (fait) | — | 145 |
| J-11 | Lun 18/05 | Recovery + mobility | — | 5-15 |
| J-10 | Mar 19/05 | Heat 45-50' + run easy 6-7 km | Heat (HT) | 50-70 |
| J-9 | Mer 20/05 | SST taper 2x20 ou 3x12-15 | — | 80-100 |
| J-8 | Jeu 21/05 | Run easy 6-8 km ou mobilité | — | 40-60 |
| J-7 | Ven 22/05 | Heat 40-45' ou endurance facile | Heat (HT) | 30-50 |
| J-6 | Sam 23/05 | Ride 2h30-3h "répétition générale" matin **+ sauna 15-20' aprem** | Sauna passive | 100-150 |
| J-5 | Dim 24/05 | Recovery 45-75' ou repos | — | 0-30 |
| **J-4** | **Lun 25/05** | Travel Corse + **vélo 30-45' Z2 aprem** | Soleil naturel | 30-50 |
| **J-3** | **Mar 26/05** | **Drive recon Sequence C** (1-1h30 RT) + **ride 75-90' final 25 km du parcours** depuis Biguglia + 3 openers 30" | Soleil naturel aprem | 60-80 |
| **J-2** | **Mer 27/05** | **Openers matin 30-40' (5x1' @ 350-380W)** + repos aprem (option marche 30' soleil) | Soleil léger | 50-70 |
| **J-1** | **Jeu 28/05** | Spin 20-30' easy + 3-4 sprints 10" + repos. Repas tôt, hydratation/sodium, dodo tôt. | — | 5-15 |
| **J-0** | **Ven 29/05** | **RACE Corsica 555 — départ 07:00 Porto-Vecchio** | Race | 1 500+ |

### Stratégie heat retention (sans HT/bain disponibles)

Bloc heat fait 11-17/05. Race day = J+12 depuis fin bloc. Fenêtre d'effet ~7-14 jours, donc en limite haute. **Retention assurée par**:
- **22/05 (J-7)**: dernière séance heat sur HT à domicile
- **23/05 (J-6)**: **sauna 15-20' à 80-90°C** après la sortie matin. Top up passif (Zurawlew et al.). Hydratation post stricte 500-700 ml + sel. Pas de douche froide post (annule l'effet plasmatique).
- **25-27/05 (J-4 à J-2)**: exposition naturelle soleil corse (rides aprem). Modéré mais cumulé sur 3 jours.

Pas de HT, pas de bain chaud disponible sur place — accepté. Concentration de l'effort retention sur **un seul shot bien placé** (sauna 23/05), reste en naturel.

### Pattern slow-start race-day

Données: 2024 Corse trop frais (+29) = pas bien 4-5h de course. Morocco (+20) = bien dès le départ. **Tu es slow-starter à fortiori si trop reposé.**

Implication mentale pour 29/05:
- **Heures 0-4**: probablement sensations "ordinaires". **Ne PAS paniquer.** Ne pas attendre l'élan magique. Le moteur ne se juge pas avant CP1 (km 164, h12-13).
- Heures 4-14: ouverture progressive.
- Heures 14-25: vrai régime, après la nuit.
- Heures 25-34: gestion fatigue posturale, Sequence C.

### Petit-déj race-day — testé et verrouillé

Format validé sur la 3h gravel du 17/05 (250W bosses, "bonnes sensations", pas de démarrage dur):
- **6h00 (60 min avant départ)**: **thé + 2 tartines beurre d'amande + 1 pancake**
- **7h00**: départ
- **7h15**: **premier gel** (15 min de course)
- Ensuite cible 60 g CHO/h selon refueling_strategy.md

### Logistique Corse (J-4 à J-0)

- **Hébergement**: site d'arrivée Biguglia.
- **J-3 recon Sequence C**: déplacement voiture nécessaire au point de départ de la reco (km ~430-440), retour idem. ~25-30 km depuis Biguglia.
- **J-3 ride aprem**: 75-90' depuis Biguglia sur les derniers 25 km du parcours en sens inverse (familiarisation portion finale).

## Nutrition / hydratation rappel

Cible carbs: **60 g/h en roulant** (calibrée post-incident gut BRM 400 à 90 g/h).
Portage actuel: **11 sachets × 90 g + 17 gels × 45 g = 1 755 g glucides**,
soit **29h15 à 60 g/h**.

Lecture pratique:
- Le fuel embarqué couvre quasiment exactement le modèle site race:
  28h58 roulées théoriques → ~1 738 g à 60 g/h.
- En scénario `r=0.90`, le solide route doit fournir la marge glucidique,
  mais surtout le sel, la texture, le confort gastrique et le moral.
- Ne pas utiliser les commerces comme source principale de glucides rapides:
  gels/poudre restent la base contrôlée.

Cible fluides: **500-750 ml/h**, plus si chaud.
Sodium: sel de régime ajouté aux bidons selon sueur.

### Ravito solide prioritaire

| Km | Statut | Passage attendu | Action |
|---:|---|---|---|
| 59.6 Zonza | Optionnel | Ven 11:07-11:34 | Tout est ouvert. Stop seulement si chaleur, faim ou bidons bas. |
| **78 Serra** | **Stop clé 1** | Ven 12:20-12:55 | Proxi fermé à midi; viser A Scopa / point chaud. Manger 1 salé et embarquer 1 backup. |
| **164 CP1 Ghisoni** | **Stop obligatoire** | Ven 17:48-18:56 | Base vie + Da beie e da manghjà. Eau/sel, vrai solide, café si utile, **2 solides de nuit**. |
| 182 Le Chalet | Bonus fragile | Ven 19:08-20:25 | Probablement fermé. Ne pas compter dessus. |
| 305.5 | Bonus incertain | Sam 02:18-04:22 | Traiter comme eau/reset, pas comme ravito solide. |
| **333 CP2** | **Stop obligatoire** | Sam 04:05-06:20 | Base vie 24h. Petit-déj simple, café, check épaule/nuque. |
| 377-385 | Opportunité rythme-dépendante | Sam 06:34-09:42 | Si rapide, trop tôt. Si `r=0.90`, très bon stop solide avant late rough. |
| **428-433 Nonza** | **Stop clé 3** | Sam 09:29-12:46 | A Matsuletta + convenience. Salé léger, Coca/café, plein eau avant Sequence C. |
| 462+ urbain | Urgence seulement | Sam 12:04-15:10 | Un stop max si vide: Coca froid + eau + snack, puis finish. |

Règle simple: **CP1 sécurise jusqu'à CP2; Nonza sécurise le final technique.**
Le km 377-385 est un bonus selon l'heure, pas un pilier.

Complément général dans [refueling_strategy.md](refueling_strategy.md), mais le
portage actuel et les fenêtres de ravito ci-dessus font foi pour la course.

## Références

- **BRM 400** (18/04/2026): 28.9 km/h sur 399 km / 3 798 D+, NP 194 W, IF 0.64.
  Validation moteur jour unique.
- **BikingMan X Morocco 2024**: 913.8 km / ~9 552 m D+ lissé, 61h45 total,
  41h36 moving / 20h09 non-moving, 22.0 km/h moving avg, 87% paved,
  71 km rough absorbés sans incident épaule majeur. **Validation ultra
  longue distance, durabilité multi-jour, ET tolérance épaule sur 70 km
  d'exposition rough étalée**. Source principale de la calibration speed-by-grade
  pour Corse.
- **Graaalps** (DNF juillet 2025): 13.3 km/h sur 222 km / 5 485 D+, terrain
  50%+ rough, épaule cassée pendant le bloc nuit à 2 483 m. Validation des
  limites posturales sur rough soutenu + concentré + technique.
- **Lecture comparative**: Corse se situe entre Morocco/BRM et Graaalps. Même
  ordre de D+ que Morocco mais sur deux fois moins de distance (D+/km
  multiplié par 2). Même nombre de km rough que Morocco mais **deux fois plus
  concentrés** (14 km continu sur Sequence C vs étalé sur 913 km au Maroc),
  et très loin de la densité VTT de Graaalps. Le risque structurel clé reste
  Sequence C km 440-462: c'est le seul segment de la course qui a la
  signature "Graaalps" (rough + steep + tard dans la course).
