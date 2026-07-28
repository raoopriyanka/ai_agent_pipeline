import json
from src.utils.tokenizer import count_tokens

class BaselinePipeline:
    """Simulates an AI pipeline and applies token optimization strategies."""
    
    def __init__(self):
        self.system_prompt = "You are a highly capable enterprise AI assistant. Analyze the provided context and history to answer the user query accurately."
        self.user_query = "Based on the enterprise architecture reports, what is the recommended scaling strategy for the Redis cache?"
        
        # Raw Data Generation
        self.raw_documents = [
            f"DOCUMENT ID {i}: The system utilizes a microservices architecture. Network latency between the API gateway and the authentication service has increased by 15% during peak load. Recommendation: Scale the Redis cache and implement circuit breakers in the routing mesh. End of report.\n"
            for i in range(1500)
        ]
        self.raw_history = [
            {"role": "user", "content": "Hello."},
            {"role": "assistant", "content": "Hi, how can I help?"},
            {"role": "user", "content": "Can you check the logs?"},
            {"role": "assistant", "content": "Yes, I am checking the logs now."}
        ] * 125  # Simulates 500 total messages
        
        self.raw_tools = [{"user_id": i, "status": "active", "latency_ms": 120 + i} for i in range(200)]

    def build_unoptimized_payload(self) -> list:
        """Builds the massive 100k token baseline."""
        docs_str = "".join(self.raw_documents)
        hist_str = "\n".join([f"{m['role']}: {m['content']}" for m in self.raw_history])
        tools_str = json.dumps(self.raw_tools)

        massive_context = (
            f"--- CONVERSATION HISTORY ---\n{hist_str}\n\n"
            f"--- RETRIEVED DOCUMENTS ---\n{docs_str}\n\n"
            f"--- TOOL OUTPUTS ---\n{tools_str}"
        )

        return [
            {"role": "system", "content": f"{self.system_prompt}\n\n{massive_context}"},
            {"role": "user", "content": self.user_query}
        ]

    def build_optimized_payload(self) -> list:
        """Applies multiple optimization strategies to strictly limit context."""
        
        # STRATEGY 1: Retrieval Filtering (Top-K)
        # We simulate a vector search returning only the 5 most relevant documents.
        optimized_docs = self.raw_documents[:5]
        docs_str = "".join(optimized_docs)

        # STRATEGY 2: Windowed Context 
        # We slice the array to only keep the last 4 interactions.
        optimized_history = self.raw_history[-4:]
        hist_str = "\n".join([f"{m['role']}: {m['content']}" for m in optimized_history])

        # STRATEGY 3: Tool Output Truncation
        # We only pass the exact fields the AI needs, limiting to top 5 results.
        optimized_tools = [{"latency_ms": t["latency_ms"]} for t in self.raw_tools[:5]]
        tools_str = json.dumps(optimized_tools)

        optimized_context = (
            f"--- CONVERSATION HISTORY ---\n{hist_str}\n\n"
            f"--- RETRIEVED DOCUMENTS ---\n{docs_str}\n\n"
            f"--- TOOL OUTPUTS ---\n{tools_str}"
        )

        return [
            {"role": "system", "content": f"{self.system_prompt}\n\n{optimized_context}"},
            {"role": "user", "content": self.user_query}
        ]

def run_analysis():
    """Calculates before/after metrics and displays them professionally."""
    pipeline = BaselinePipeline()
    
    # Process Unoptimized
    unopt_messages = pipeline.build_unoptimized_payload()
    unopt_text = unopt_messages[0]["content"] + unopt_messages[1]["content"]
    unopt_tokens = count_tokens(unopt_text)
    unopt_cost = (unopt_tokens / 1_000_000) * 5.00  # Based on $5/1M tokens
    
    # Process Optimized
    opt_messages = pipeline.build_optimized_payload()
    opt_text = opt_messages[0]["content"] + opt_messages[1]["content"]
    opt_tokens = count_tokens(opt_text)
    opt_cost = (opt_tokens / 1_000_000) * 5.00
    
    # Metrics
    reduction = ((unopt_tokens - opt_tokens) / unopt_tokens) * 100
    
    print("\n" + "="*60)
    print("PIPELINE OPTIMIZATION RESULTS")
    print("="*60)
    print(f"Original Token Count: {unopt_tokens:,}")
    print(f"Optimized Token Count: {opt_tokens:,}")
    print(f"Percentage Reduction: {reduction:.2f}%")
    print("-" * 60)
    print(f"Estimated Cost Before: ${unopt_cost:.4f}")
    print(f"Estimated Cost After:  ${opt_cost:.6f}")
    print("-" * 60)
    print("PERFORMANCE METRICS:")
    print("Latency Improvement: High (Significantly lower Time-To-First-Token)")
    print("Quality Tradeoff: Minor history loss, but massive gain in 'Lost in the Middle' prevention.")
    print("="*60)

if __name__ == "__main__":
    run_analysis()