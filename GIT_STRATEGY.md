# GIT_STRATEGY.md

## Rôles
- **Développeur** : Implémente les fonctionnalités, rédige les tests, et effectue les revues de code.  
- **Reviwer** : Supervise l'intégrité du projet, prend des décisions sur la stratégie de branchement et gère les merges/rebases.  

## Conventions de nommage
- **Branches** :
  - `feature/nom_de_fonctionnalité` : Pour une nouvelle fonctionnalité.
  - `hotfix/nom_du_bug_urgent` : Pour des corrections urgentes en production.
  - `release/nom_version` : Pour préparer une nouvelle version.
- **Commits** :
  - Utilisez le format `type: message`
  - Types : `feat` pour une fonctionnalité, `fix` pour une correction de bug, `docs` pour les modifications de documentation, `style` pour les modifications de style sans changement fonctionnel, `test` pour les ajouts/modifications de tests.

## Règles de merge/rebase
- **Merge** : Ne jamais utiliser `git merge` pour fusionner directement dans la branche `main` sans revues. Utilisez des Pull Requests (PR) pour toute fusion dans `main`.