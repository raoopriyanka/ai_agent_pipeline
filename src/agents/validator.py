from src.agents.base_agent import BaseAgent

class ValidatorAgent(BaseAgent):
    """Validates the output structures of other agents to prevent pipeline collapse."""
    
    def __init__(self):
        super().__init__(name="ValidatorAgent")

    def validate_planner_output(self, data: dict) -> bool:
        """
        Ensures the planner output is a dictionary containing a 'steps' list.
        """
        self.logger.debug("Validating planner output schema...")
        
        if not isinstance(data, dict):
            self.logger.error("Validation failed: Output is not a dictionary.")
            raise ValueError("Output must be a JSON object.")
            
        if "steps" not in data:
            self.logger.error("Validation failed: Missing 'steps' key.")
            raise KeyError("Output JSON must contain a 'steps' key.")
            
        if not isinstance(data["steps"], list):
            self.logger.error("Validation failed: 'steps' is not a list.")
            raise TypeError("The 'steps' value must be an array.")
            
        if len(data["steps"]) == 0:
            self.logger.warning("Validation flagged an empty steps array.")
            
        self.logger.info("Validation passed successfully.")
        return True