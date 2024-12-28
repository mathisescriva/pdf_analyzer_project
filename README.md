# Analyseur de Documents Financiers

## Aperçu
Ce projet est un outil sophistiqué d'analyse de documents financiers qui utilise le modèle Mistral-7B LLM pour extraire des informations structurées à partir de documents financiers tels que les KID PRIIPs (Documents d'Informations Clés). Le système traite le texte en entrée et génère une sortie JSON standardisée contenant les informations financières clés, les dates, les facteurs de risque et les scénarios de performance. Le système intègre également un processus de validation robuste pour garantir la qualité et la cohérence des données extraites.

## Fonctionnalités

### 1. Traitement des Documents
- Traitement de différents types de documents financiers
- Extraction d'informations structurées au format JSON standardisé
- Gestion de multiples formats et structures de documents

### 2. Extraction d'Informations
Le système extrait les informations suivantes :
- **Métadonnées du Document**
  - Type et catégorie du document
  - Classification réglementaire
  - Objectif et portée

- **Détails du Produit**
  - Numéro ISIN
  - Nom du produit
  - Niveaux et conditions de protection
  - Informations sur la devise
  - Actifs sous-jacents et codes Bloomberg

- **Dates Clés**
  - Date d'émission
  - Dates de remboursement
  - Dates d'évaluation
  - Date de production du document

- **Informations sur les Risques**
  - Évaluation du niveau de risque
  - Facteurs de risque et avertissements
  - Horizon d'investissement
  - Mécanismes de protection

- **Informations sur les Entités**
  - Détails de l'émetteur
  - Informations sur le garant
  - Autorité réglementaire
  - Détails du fabricant

- **Scénarios de Performance**
  - Valeurs du scénario de stress
  - Données du scénario défavorable
  - Projections du scénario modéré
  - Calculs du scénario favorable
  - Valeurs initiales et finales
  - Taux de rendement annuel

- **Structure des Coûts**
  - Coûts totaux
  - Impact sur le rendement
  - Composition des coûts

### 3. Configuration du Modèle
- Utilisation du modèle Mistral-7B-Instruct-v0.2
- Fenêtre de contexte configurable (actuellement 4096 tokens)
- Taille de lot et nombre de threads ajustables
- Paramètre de température pour la cohérence des sorties

### 4. Système de Validation
- **Extraction Intelligente** : Utilisation du modèle Mistral-7B pour une compréhension approfondie des documents financiers
- **Sortie Structurée** : Génération de JSON suivant un schéma standardisé
- **Validation Avancée** :
  - Vérification de la structure et du format des données
  - Validation des formats spécifiques (ISIN, dates, pourcentages)
  - Système de scoring de qualité des documents
  - Mode de validation souple permettant la sauvegarde avec avertissements
  - Feedback détaillé sur les erreurs et suggestions d'amélioration
- **Configuration Centralisée** : Gestion des paramètres via un fichier de configuration JSON unique

## Structure du Projet
```
tests_llm/
├── configs/
│   ├── config.json        # Configuration générale (modèle, validation, etc.)
│   └── json_schema.json   # Schéma de validation JSON
├── inputs/
│   └── vlm_output.txt     # Fichier d'entrée avec le texte extrait
├── outputs/
│   └── example_output.json # Résultat de l'analyse au format JSON
├── src/
│   ├── llm_test_options.py   # Script principal d'analyse
│   ├── validation_advanced.py # Système de validation
│   └── exceptions.py         # Gestion des erreurs personnalisée
└── models/
    └── mistral-7b-instruct-v0.2.Q8_0.gguf  # Modèle LLM
```

## Configuration

Le fichier `config.json` centralise tous les paramètres du système :
- Configuration du modèle LLM (chemin, paramètres)
- Règles de validation
- Seuils de qualité
- Paramètres de logging

## Validation des Données

Le système de validation assure la qualité des données extraites :
1. **Validation Structurelle** : Vérifie la présence et le format des champs requis
2. **Validation Sémantique** : Contrôle la cohérence des données (dates, montants, etc.)
3. **Scoring de Qualité** : Calcul d'un score global basé sur différents critères
4. **Mode Souple** : Permet la sauvegarde des documents même avec des avertissements si le score minimal est atteint
5. **Feedback Détaillé** : Fournit des messages d'erreur précis et des suggestions d'amélioration

## Entrée/Sortie

### Format d'Entrée
Le système accepte des entrées texte de documents financiers, contenant typiquement :
- Descriptions des produits
- Évaluations des risques
- Scénarios de performance
- Informations sur les coûts
- Informations réglementaires

### Format de Sortie
Génère une sortie JSON structurée avec :
- Formats de date standardisés (AAAA-MM-JJ)
- Valeurs numériques sans symboles de devise
- Pourcentages convertis en format décimal
- Valeurs nulles pour les informations manquantes
- Structure de données hiérarchique

## Utilisation

1. Placez votre texte de document d'entrée dans `inputs/vlm_output.txt`
2. Exécutez le script principal :
```bash
python src/llm_test_options.py
```
3. Trouvez la sortie traitée dans `outputs/example_output.json`

## Détails Techniques

### Dépendances
- llama-cpp-python
- torch
- transformers
- json
- logging

### Paramètres du Modèle
- Fenêtre de Contexte : 4096 tokens
- Threads : 4
- Taille de Lot : 8
- Température : 0.1

## Considérations de Performance
- Utilisation de la mémoire optimisée pour Apple Silicon (MPS)
- Nombre de threads configurable pour la performance
- Taille de lot ajustable pour différentes longueurs de documents
- Gestion des erreurs pour les limites de tokens

## Améliorations Futures
- Support du traitement par lots de plusieurs documents
- Amélioration de la gestion des erreurs et de la validation
- Support de types de documents supplémentaires
- Amélioration de la précision d'extraction
- Extension du schéma JSON pour des informations plus détaillées
- Couverture des tests unitaires
- Optimisations de performance

## Contribution
Les contributions sont les bienvenues ! N'hésitez pas à soumettre des pull requests ou à créer des issues pour les bugs et les demandes de fonctionnalités.

## Licence
[Spécifiez votre licence ici]
