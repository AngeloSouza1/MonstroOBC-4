def createMonster(name, element, health, skills):
    if not isinstance(name, str) or not name.strip():
        raise ValueError("O nome do monstro deve ser uma string válida.")
    
    if element not in ['fogo', 'água', 'terra', 'ar']:
        raise ValueError("O elemento deve ser 'fogo', 'água', 'terra' ou 'ar'.")
    
    if not (50 <= health <= 200):
        raise ValueError("Os pontos de vida devem estar entre 50 e 200.")
    
    if not isinstance(skills, list) or len(skills) > 3 or not all(isinstance(skill, str) for skill in skills):
        raise ValueError("As habilidades devem ser uma lista de até 3 strings.")

    return {
        "name": name,
        "element": element,
        "health": health,
        "skills": skills
    }
