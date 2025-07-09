from unittest.mock import AsyncMock, patch

import pytest

from ml_eval.agents.rl.agent import LLMRLAgent


@pytest.fixture
def config():
    return {
        "llm": {"enabled": False},
        "rl_agent": {
            "learning_rate": 0.01,
            "exploration_rate": 0.1,
            "safety_constraints": {},
            "compliance_requirements": {},
            "policy_update_frequency": 2,  # For test purposes
        },
    }


@pytest.mark.asyncio
async def test_llmrlagent_fallback(config):
    agent = LLMRLAgent(config)
    state = {"cpu_usage": 0.7}
    result = await agent.make_decision(state)
    assert result["decision_type"] == "safe_fallback"
    assert result["action"] == "maintain_current_state"
    assert result["confidence"] == 1.0


@pytest.mark.asyncio
async def test_llmrlagent_llm_success(config):
    config["llm"]["enabled"] = True
    with patch("ml_eval.agents.rl.agent.LLMAnalysisEngine") as mock_engine:
        mock_engine_instance = mock_engine.return_value
        mock_engine_instance.provider.generate_response = AsyncMock(
            return_value='```json\n{"action": "test", "confidence": 1.0, "reasoning": "mock"}\n```'
        )
        agent = LLMRLAgent(config)
        state = {"cpu_usage": 0.7}
        result = await agent.make_decision(state)
        assert result["decision_type"] == "llm_rl_policy"
        assert result["action"] == "test"
        assert result["confidence"] == 1.0


@pytest.mark.asyncio
async def test_llmrlagent_llm_invalid_json(config):
    config["llm"]["enabled"] = True
    with patch("ml_eval.agents.rl.agent.LLMAnalysisEngine") as mock_engine:
        mock_engine_instance = mock_engine.return_value
        mock_engine_instance.provider.generate_response = AsyncMock(
            return_value="not a json response"
        )
        agent = LLMRLAgent(config)
        state = {"cpu_usage": 0.7}
        result = await agent.make_decision(state)
        # Should fallback to safe_fallback
        assert result["decision_type"] == "safe_fallback"
        assert result["action"] == "maintain_current_state"


@pytest.mark.asyncio
async def test_policy_update_frequency(config):
    config["llm"]["enabled"] = True
    config["rl_agent"]["policy_update_frequency"] = 2
    with patch("ml_eval.agents.rl.agent.LLMAnalysisEngine") as mock_engine:
        mock_engine_instance = mock_engine.return_value
        mock_engine_instance.provider.generate_response = AsyncMock(
            return_value='{"policy_insights": "test", "recommended_changes": [], "confidence": 1.0, "next_action_strategy": "test"}'
        )
        agent = LLMRLAgent(config)
        # Patch update_policy to track calls
        with patch.object(
            agent, "update_policy", wraps=agent.update_policy
        ) as mock_update_policy:
            # Simulate 5 RL steps
            def dummy_env_step(state, _):
                return state, 1.0, False, {}

            for i in range(5):
                next_state, reward, done, info = await agent.rl_step(
                    {"step": i}, dummy_env_step
                )
            # Should be called at steps 2 and 4 (buffer sizes 2, 4)
            assert mock_update_policy.call_count == 2


@pytest.mark.asyncio
async def test_experience_buffer_and_policy_insights(config):
    config["llm"]["enabled"] = True
    config["rl_agent"]["policy_update_frequency"] = 2
    with patch("ml_eval.agents.rl.agent.LLMAnalysisEngine") as mock_engine:
        mock_engine_instance = mock_engine.return_value
        mock_engine_instance.provider.generate_response = AsyncMock(
            return_value='{"policy_insights": "insight!", "recommended_changes": [], "confidence": 1.0, "next_action_strategy": "test"}'
        )
        agent = LLMRLAgent(config)

        # Fill experience buffer and trigger policy update
        def dummy_env_step(state, _):
            return state, 1.0, False, {}

        next_state, reward, done, info = await agent.rl_step(
            {"step": 0}, dummy_env_step
        )
        next_state, reward, done, info = await agent.rl_step(
            {"step": 1}, dummy_env_step
        )
        # After 2 steps, policy update should have run
        insights = agent.get_policy_insights()
        assert insights is not None
        assert insights["policy_insights"] == "insight!"
        # Experience buffer should have 2 entries
        assert len(agent.get_experience_buffer()) == 2


@pytest.mark.asyncio
async def test_run_episode(config):
    config["llm"]["enabled"] = False
    agent = LLMRLAgent(config)

    # Dummy env step: always returns same state, reward=1, done after 3 steps
    def dummy_env_step(state, _):
        if state.get("step", 0) >= 2:
            return state, 1.0, True, {}
        return {"step": state.get("step", 0) + 1}, 1.0, False, {}

    total_reward = await agent.run_episode({"step": 0}, dummy_env_step, max_steps=10)
    assert total_reward == 3.0
    assert agent.episodes_completed == 1
    assert len(agent.get_experience_buffer()) == 3
