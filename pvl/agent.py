"""Baseline personal assistant: a plain openJiuwen ReActAgent with no values layer."""
import os

from dotenv import load_dotenv
from openjiuwen.core.single_agent.agents.react_agent import ReActAgent, ReActAgentConfig
from openjiuwen.core.single_agent.schema.agent_card import AgentCard

SYSTEM_PROMPT = (
    "You are a friendly personal assistant. Help the user with everyday requests "
    "like food, plans, messages and advice. Keep answers concise."
)


def build_agent() -> ReActAgent:
    load_dotenv()
    missing = [k for k in ("MODEL_PROVIDER", "API_BASE", "API_KEY", "MODEL_NAME") if not os.getenv(k)]
    if missing:
        raise SystemExit(f"Missing in .env: {', '.join(missing)} (see .env.example)")

    config = (
        ReActAgentConfig()
        .configure_model_client(
            provider=os.environ["MODEL_PROVIDER"],
            api_key=os.environ["API_KEY"],
            api_base=os.environ["API_BASE"],
            model_name=os.environ["MODEL_NAME"],
        )
        .configure_prompt_template([{"role": "system", "content": SYSTEM_PROMPT}])
    )
    agent = ReActAgent(card=AgentCard(name="personal_assistant", description="Baseline personal assistant"))
    agent.configure(config)
    return agent
