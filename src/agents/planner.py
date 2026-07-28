import json
import random
import time
from src.agents.base_agent import BaseAgent
from src.agents.validator import ValidatorAgent

class PlannerAgent(BaseAgent):
    """Responsible for breaking down the user query into logical steps."""
    
    def __init__(self):
        super().__init__(name="PlannerAgent")
        self.validator = ValidatorAgent()
        self.max_retries = 3

    def process(self, task: str) -> dict:
        self.logger.info(f"Received planning task: '{task}'")
        
        messages = [
            {"role": "system", "content": "You are a planning agent. Output ONLY valid JSON containing a 'steps' array of strings. Do not include markdown formatting like ```json."},
            {"role": "user", "content": task}
        ]
        
        # ---------------------------------------------------------
        # THE FIX: Implementing a robust retry loop
        # ---------------------------------------------------------
        for attempt in range(1, self.max_retries + 1):
            try:
                self.logger.info(f"Attempt {attempt}/{self.max_retries} to generate plan...")
                
                # RE-INJECTING THE CHAOS MONKEY FOR TESTING
                # (We leave this in to prove the retry mechanism actually catches it)
                failure_type = random.choice(["timeout", "malformed_json", "success"])
                
                if failure_type == "timeout":
                    self.logger.warning("Simulated Timeout occurred.")
                    time.sleep(1)
                    raise TimeoutError("The LLM API took too long.")
                
                raw_response = self.llm.chat(messages)
                
                if failure_type == "malformed_json":
                    self.logger.warning("Simulated hallucination occurred.")
                    raw_response = raw_response[:-3] 
                
                # Parse and Validate
                parsed_data = json.loads(raw_response)
                self.validator.validate_planner_output(parsed_data)
                
                self.logger.info("Successfully generated and validated plan.")
                return parsed_data
                
            except (json.JSONDecodeError, ValueError, KeyError, TypeError, TimeoutError) as e:
                self.logger.error(f"Attempt {attempt} failed: {str(e)}")
                if attempt == self.max_retries:
                    self.logger.critical("Max retries reached. Failing the pipeline.")
                    raise RuntimeError(f"Planner failed after {self.max_retries} attempts.") from e
                
                # Exponential backoff (waiting before trying again)
                sleep_time = 2 ** attempt
                self.logger.info(f"Retrying in {sleep_time} seconds...\n")
                time.sleep(sleep_time)

# Manual test execution block
if __name__ == "__main__":
    planner = PlannerAgent()
    print("Running robust planner with automatic retries...")
    try:
        result = planner.process("Analyze the database for latency issues.")
        print("\nFinal Output:", json.dumps(result, indent=2))
    except RuntimeError as e:
        print("\nPipeline failed entirely:", e)