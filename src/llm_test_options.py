import logging
import json
import llama_cpp
from typing import Dict, Any, List
from dataclasses import dataclass
import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.validation_advanced import validate_document

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_config() -> Dict[str, Any]:
    """Charge la configuration depuis config.json."""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'configs', 'config.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Erreur lors du chargement de la configuration: {str(e)}")
        raise

@dataclass
class LLMConfig:
    """Configuration pour le modèle LLM."""
    max_retries: int = 3
    temperature: float = 0.1
    max_tokens: int = 1000

def read_vlm_output(file_path: str) -> str:
    """Lit le contenu du fichier VLM."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            logger.info(f"Fichier {file_path} lu avec succès")
            return content
    except Exception as e:
        logger.error(f"Erreur lors de la lecture du fichier: {str(e)}")
        return ""

def save_json_output(data: Dict[str, Any], output_file: str) -> None:
    """Sauvegarde les données au format JSON après validation."""
    try:
        # Validation avancée
        validation_result = validate_document(data)
        
        # Affichage des résultats de validation
        logger.info(f"\nScore de qualité du document : {validation_result.score:.2%}")
        
        # Si le score est supérieur à 0, on considère que c'est valide
        if validation_result.score > 0:
            # Sauvegarde du JSON
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logger.info(f"Résultats sauvegardés dans {output_file}")
            
            # Affichage du feedback
            if validation_result.feedback:
                logger.info("\nFeedback de validation:")
                for fb in validation_result.feedback:
                    logger.info(f"- {fb}")
        else:
            logger.warning("Document invalide - score trop bas")
            
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde du JSON: {str(e)}")

def load_json_schema(schema_file: str) -> Dict[str, Any]:
    """Charge le schéma JSON depuis un fichier."""
    try:
        with open(schema_file, 'r', encoding='utf-8') as file:
            schema = json.load(file)
            logger.info(f"Schéma JSON chargé depuis {schema_file}")
            return schema
    except Exception as e:
        logger.error(f"Erreur lors du chargement du schéma JSON: {str(e)}")
        return {}

def main():
    try:
        # Chargement de la configuration
        config = load_config()
        model_config = config["model"]
        
        # Initialisation du modèle LLM
        llm = llama_cpp.Llama(
            model_path=model_config["path"],
            n_ctx=model_config["max_length"],
            n_threads=8,
            n_gpu_layers=1
        )
        
        # Lecture du fichier d'entrée
        input_path = os.path.join(project_root, "inputs", "vlm_output.txt")
        vlm_output = read_vlm_output(input_path)
        if not vlm_output:
            logger.error("Impossible de lire le fichier d'entrée")
            return

        # Chargement du schéma JSON
        schema_path = os.path.join(project_root, "configs", "json_schema.json")
        json_structure = load_json_schema(schema_path)
        if not json_structure:
            logger.error("Impossible de charger le schéma JSON")
            return
        
        # Préparation du prompt
        prompt = f"""[INST] You are a financial document analyzer. Extract information from the document below into the specified JSON format.

Rules:
1. Return ONLY the JSON object, no other text
2. The JSON must exactly match the provided structure
3. ALL dates must be in YYYY-MM-DD format
4. ALL percentages must be converted to decimals (e.g., -18.9% -> -0.189)
5. ALL monetary values should be numbers without currency symbols
6. Risk levels should be "Low" (1-2), "Medium" (3-4), or "High" (5-7)
7. If a value is not found in the document, use null
8. Arrays (factors, warnings) must not be empty if information exists
9. For risk factors, include:
   - Investment horizon (e.g., "5 year investment horizon")
   - Risk level description
   - Any other relevant risk information
10. For performance scenarios:
    - 'initial' should be the investment amount
    - 'final' should be the "what you might get back" amount
    - Convert all percentages to decimals

Document to analyze:
{vlm_output}

Required JSON structure:
{json.dumps(json_structure, indent=2)}
[/INST]"""
        
        # Génération de la réponse
        response = llm(
            prompt,
            max_tokens=model_config["max_tokens"],
            temperature=model_config["temperature"],
            stop=["```"],
            echo=False
        )

        response_text = response["choices"][0]["text"]

        # Extraction et validation du JSON
        start_idx = response_text.find("{")
        end_idx = response_text.rfind("}") + 1
        
        if start_idx != -1 and end_idx != -1:
            json_str = response_text[start_idx:end_idx]
            result = json.loads(json_str)
            save_json_output(result, "outputs/example_output.json")
            logger.info("Traitement terminé avec succès")
        else:
            logger.error("Aucun JSON valide trouvé dans la réponse")

    except Exception as e:
        logger.error(f"Erreur lors du traitement : {str(e)}")

if __name__ == "__main__":
    main()
