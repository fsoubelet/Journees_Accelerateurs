# Démonstration Xsuite

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fsoubelet/Journees_Accelerateurs/HEAD)

Ce dépôt contient des notebooks démontrant l'interface d'[Xsuite](https://xsuite.readthedocs.io/en/latest/), utilisé pour des simulations de dynamique des faisceaux en accélérateurs de particules.
Il est conçu comme complément à ma présentation aux [Journées Accélérateurs 2025](https://indico.ijclab.in2p3.fr/event/11661/).

Les notebooks peuvent être exécutés directement dans le navigateur via [Binder](https://mybinder.org/), en cliquant sur le badge ci-dessus.

## Notebooks

Cette démonstration est basée sur la maille de PIMMS (voir : [CERN-PS-99-010-DI](https://cds.cern.ch/record/385378/)).

Les notebooks suivants seront présentés en direct :

- [`00_maille.ipynb`](00_maille.ipynb) : Présentation de l'interface d'Xsuite en re concevant la maille de PIMMS.
- [`01_optique.ipynb`](01_optique.ipynb) : Calcul des fonctions optiques, puis leur optimisation via les quadripôles et sextupôles pour l'extraction de faisceau via une résonance du troisième ordre dans la section droite.
- [`02_impedance.ipynb`](02_impedance.ipynb) : Démonstration du tracking de particules et mitigation d'une instabilté due à l'impédance de la cavité RF.

Les notebooks suivants ne seront pas présentés et sont fournis comme matériel supplémentaire :

- [`03_formats.ipynb`](extra/03_formats.ipynb) : Aperçu des différents formats d'entrée et de sortie supportés par Xsuite.
- [`04_espace_phases.ipynb`](extra/04_espace_phase.ipynb) : Charactérisation de l'espace des phases et préparation des conditions pour l'extraction lente du faisceau.
- [`05_extraction.ipynb`](extra/05_extraction.ipynb) : Simulation d'extraction lente du faisceau via tracking.

## Licence

Ce dépôt est sous licence [MIT](LICENSE).
