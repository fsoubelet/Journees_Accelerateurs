# Démonstration Xsuite [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fsoubelet/Journees_Accelerateurs/HEAD)

Ce dépôt contient des notebooks démontrant l'interface d'[Xsuite](https://xsuite.readthedocs.io/en/latest/), utilisé pour des simulations de dynamique des faisceaux en accélérateurs de particules.
Il est conçu comme complément à ma présentation aux [Journées Accélérateurs 2025](https://indico.ijclab.in2p3.fr/event/11661/), et les exemples sont basés sur divers tutoriels Xsuite donnés par le passé.

Les notebooks peuvent être exécutés directement dans le navigateur via [Binder](https://mybinder.org/), en cliquant sur le badge ci-dessus.

## Notebooks

Cette démonstration est basée sur la maille de PIMMS (voir : [CERN-PS-99-010-DI](https://cds.cern.ch/record/385378/)).

Les notebooks suivants seront présentés en direct :

- [`00_maille.ipynb`](00_maille.ipynb) : Présentation de l'interface d'Xsuite en concevant depuis zéro la maille de PIMMS.
- [`01_optique.ipynb`](01_optique.ipynb) : Calcul des fonctions optiques, puis leur optimisation via les quadripôles et sextupôles pour l'extraction de faisceau via une résonance du troisième ordre dans la section droite.
- [`02_impedance.ipynb`](02_impedance.ipynb) : Démonstration du tracking de particules et mitigation d'une instabilté due à l'impédance de la cavité RF.

Les notebooks suivants ne seront pas présentés et sont fournis comme matériel supplémentaire :

- [`03_characterisation_espace_phase.ipynb`](extras/03_characterisation_espace_phase.ipynb) : Caractérisation de l'espace des phases en excitant la résonance du troisième ordre pour extraction.
- [`04_optimisation_topologie.ipynb`](extras/04_optimisation_topologie.ipynb) : Optimisation de la topologie de l'espace des phases proche de la résonance du troisième ordre pour faciliter l'extraction.
- [`05_extraction_lente.ipynb`](extras/05_extraction_lente.ipynb) : Simulation d'extraction lente du faisceau via tracking, et optimisation d'une excitation pour extraire le faisceau.
- [`06_formats.ipynb`](extras/06_formats.ipynb) : Aperçu des différents formats supportés par Xsuite.

<details> <summary><b>Rendu pages statiques</b></summary>

Un rendu HTML des notebooks est disponible en ligne via l'espace GitHub Pages de ce dépôt.
Les notebooks post-exécution sont accessibles aux liens suivants :

- [00_maille.ipynb](https://fsoubelet.github.io/Journees_Accelerateurs/00_maille.html)
- [01_optique.ipynb](https://fsoubelet.github.io/Journees_Accelerateurs/01_optique.html)
- [02_impedance.ipynb](https://fsoubelet.github.io/Journees_Accelerateurs/02_impedance.html)
- [03_characterisation_espace_phase.ipynb](https://fsoubelet.github.io/Journees_Accelerateurs/03_characterisation_espace_phase.html)
- [04_optimisation_topologie.ipynb](https://fsoubelet.github.io/Journees_Accelerateurs/04_optimisation_topologie.html)
- [05_extraction_lente.ipynb](https://fsoubelet.github.io/Journees_Accelerateurs/05_extraction_lente.html)
- [06_formats.ipynb](https://fsoubelet.github.io/Journees_Accelerateurs/06_formats.html)

</details>

## Licence

Ce dépôt est sous licence [MIT](LICENSE).
