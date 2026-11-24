# Mérite ou héritage : L'excellence scolaire est-elle une illusion ?
Le mouvement lycéen de 2026

Ce projet est parti d'un événement d'actualité. À partir du 21 septembre 2026, des lycéens ont lancé un mouvement de blocage de leurs établissements, parti du lycée Saint-Exupéry à Créteil (Val-de-Marne), puis étendu à de nombreux lycées d'Île-de-France et à d'autres villes (Marseille, Lille, Rennes, Strasbourg…). Début octobre, plusieurs centaines de lycées étaient perturbés ou bloqués, et les journées de manifestation ont rassemblé des dizaines, voire des centaines de milliers de personnes selon les décomptes.

Ce que dénoncent les élèves est très concret : ce sont leurs conditions d'études.
Un point nous a particulièrement frappés : les élèves insistent sur le fait que ces conditions ne sont pas les mêmes d'un lycée à l'autre. Les conditions d'études des lycées de banlieue sont décrites comme très éloignées de celles de certains établissements des grandes métropoles. Autrement dit, le mouvement ne parle pas seulement de moyens, il parle d'inégalités entre les lycées.

Nous avons donc voulu dépasser le ressenti des étudiants et les débats médiatiques. Nous avons essayé de monter notre propre étude sur la différence entre lycée public, où les élèves étudient dans de moins bonnes conditions, et les lycées privées qui ont plus de moyen.

Nous avons commencé par étudier les inégalités dans la France entière entre les lycées privés et publics. Ensuite, nos résultats nous ont poussé a nous intéresser a l'Ile de France. La même région où le mouvement lycéen est né. L'Île-de-France concentre à quelques dizaines de kilomètres d'écart certains des lycées les plus favorisés et les plus sélectifs de France, et certains des départements les plus pauvres. Elle est donc le meilleur terrain pour observer ces inégalités.
Aller au-delà des palmarès. Les classements de lycées publiés par la presse reposent sur le taux de réussite ou de mentions, qui reflètent en grande partie le recrutement social. Nous voulions distinguer ce qui relève de l'IPS (indice de position sociale) des élèves et de ce qui relève de l'établissement lui-même (valeur ajoutée). 

Nous nous sommes donc posées la question suivante : Comment l'origine sociale des élèves, mesurée par l'IPS, une moyenne entre l'indice attribué à la catégorie socio-professionelle des deux parents, pèse-t-elle sur la réussite au baccalauréat dans les lycées généraux et technologiques, et comment ces inégalités se transmettent-elles du niveau national au niveau de l'Ile de France?

Les trois sources que nous avons utilisés sont des données ouvertes, importées directement depuis leur URL dans le notebook :
df_ips : Indice de Position Sociale (IPS) de chaque lycée, par année trouvé sur	data.education.gouv.fr : (fr-en-ips_lycees)
df_res	Indicateurs de résultat des lycées généraux et technologiques (réussite, mentions, taux d'accès, valeur ajoutée…) trouvé aussi sur	data.education.gouv.fr (fr-en-indicateurs-de-resultat-des-lycees-gt_v2)
df_carte :	Contours géographiques des départements	ADEME (geo-contours-departements)

L'IPS (indice de position sociale) résume le niveau social et culturel des familles des élèves d'un établissement : plus il est élevé, plus le public est favorisé.

Pour répondre a notre problématique, nous avons crée de nouvelles variables plus faciles a analyser
ecart_selectivite	
Taux de réussite − taux d'accès de la seconde au bac. Plus il est grand, plus le lycée « perd » d'élèves en route
taux_TB	Part des mentions Très Bien parmi les présents en voie générale
quartile_IPS	Classement des lycées en 4 groupes selon leur IPS (Q1 = les moins favorisés, Q4 = les plus favorisés)
taux_mentions_seconde_approx	Approximation du taux de mentions rapporté aux élèves entrés en seconde
ecart moyen	Moyenne de cinq écarts public − privé (IPS, réussite, mentions, accès, TB), utilisée pour classer les régions

Lors de l'analyse, nous avons effectué plusieurs choix importants : 
Le taux de réussite seul ne suffit pas : il dépasse 95 % dans la grande majorité des lycées. Nous nous appuyons donc surtout sur le taux de mentions et sur le taux de mentions Très Bien, qui reflètent mieux l'accès aux filières sélectives post-bac.
La valeur ajoutée (calculée par la DEPP) permet de comparer ce qu'un lycée obtient à ce qu'on pouvait attendre au vu du profil de ses élèves.
L'écart-type de l'IPS mesure la mixité sociale interne d'un lycée.
Le notebook se structure de la manière suivante :
l'import et le nettoyage données : décompte des valeurs manquantes, jointure, création des variables.
L'étude sur la France entière : public vs privé sous contrat, ainsi que la comparaison des régions.
Le focus sur l'Île-de-France, au niveau des départements et des arrondissements parisiens.

Enfin nous avons aussi réalisé un site web local grâce à la librairie streamlit de python. Celui ci permet de tracer une carte, de la france ou d'une région en particulier, pour une année déterminée, avec différents paramètres comme l'IPS, le taux de réussite au bac etc. Le site consiste en un code python nommé app_cartes.py structuré simplement : la récupération des données et leur organisation en un tableau avec les données géogtraphiques, la fonction qui permet de tracer la ou les carte.s, et enfin la structure du site avec les différents boutons qui permettent à l'utilisateur de créer les cartes voulues. Pour le lancer il faut ouvrir un terminal python dans un environnement qui contient bien les différents requirements (différentes bibliothèques téléchargées, cf le fichier requirements.txt) puis exécuter le code dans ce terminal et lui donner la commande "streamlit run app_cartes.py".
