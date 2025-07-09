import asyncio
import os
import sys

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add project root to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

try:
    from ml_eval.agents.rl.agent import LLMRLAgent
except ImportError:
    print(
        "Error: Could not import LLMRLAgent. Make sure you're running from the correct directory."
    )
    sys.exit(1)

# Config with LLM enabled
config = {
    "llm": {
        "enabled": True,
        "provider": "openai",
        "provider_config": {
            "api_key": os.getenv("OPENAI_API_KEY", "your-openai-api-key-here"),
            "model": "gpt-4o-mini",  # Cheapest and fast model
            "max_tokens": 1000,
        },
    },
    "rl_agent": {
        "learning_rate": 0.01,
        "exploration_rate": 0.1,
        "safety_constraints": {},
        "compliance_requirements": {},
        "experience_replay_size": 10,
    },
}


# Sample system state
def get_state():
    return {
        "cpu_usage": 0.7,
        "memory_usage": 0.6,
        "response_time": 450,
        "error_rate": 0.005,
    }


# Simple mock environment step function
def mock_env_step(state, action):  # noqa: ARG001
    # For demo: next_state is random, reward is +1 if action is not fallback, else 0, done after 5 steps
    import random

    next_state = {
        "cpu_usage": random.uniform(0.5, 0.9),
        "memory_usage": random.uniform(0.5, 0.9),
        "response_time": random.randint(400, 600),
        "error_rate": random.uniform(0.001, 0.01),
    }
    reward = 1.0 if action.get("decision_type") == "llm_rl_policy" else 0.0
    done = False  # The RL loop will handle max_steps
    info = {}
    return next_state, reward, done, info


async def main():
    print("Testing LLM-based RL Agent with RL loop and policy learning...")
    print(f"API Key loaded: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")

    agent = LLMRLAgent(config)

    # Run multiple episodes to build experience
    for episode in range(3):
        print(f"\n--- Episode {episode + 1} ---")
        initial_state = get_state()
        total_reward = await agent.run_episode(
            initial_state, mock_env_step, max_steps=5
        )
        print(f"Episode {episode + 1} total reward: {total_reward}")

        # Show policy insights if available
        policy_insights = agent.get_policy_insights()
        if policy_insights:
            print(f"Policy insights: {policy_insights}")

    print("\n--- Final Results ---")
    print(f"Total episodes completed: {agent.episodes_completed}")
    print(f"Total cumulative reward: {agent.total_reward}")
    print(f"Experience buffer size: {len(agent.experience_buffer)}")
    print(f"Learning progress: {agent.get_learning_progress()}")


if __name__ == "__main__":
    asyncio.run(main())
