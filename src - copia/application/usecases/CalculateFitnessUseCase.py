from src.domain.entities.IndividualType import IndividualType

class CalculateFitnessUseCase:
    _weight_1: int = 0
    _weight_2: int = 0
    _weight_3: int = 0
    _weight_4: int = 0
    _weight_5: int = 0
    
    def __init__(self):
        pass
    
    def execute(self, individual: IndividualType) -> int:
        """
        Calculate the fitness score of an individual based on its properties.
        
        :param individual: An instance of IndividualType containing the properties to evaluate.
        :return: The calculated fitness score as an integer.
        """
        # Example calculation logic (to be replaced with actual logic)
        score = 0
        
        # Calculate total irrigation
        score += individual.totalIrrigation
        
        # Calculate nutritional value
        score += individual.totalNutritionalValue
        
        # Calculate compatibility
        score += individual.compatibility
        
        # Calculate care time (inverted, lower is better)
        score -= individual.careTime
        
        # Set the fitness score
        individual.fitnessScore = score
        
        return individual.fitnessScore