"""Throwaway check that openJiuwen rails behave the way the PVL needs.

Answers four questions on the real baseline agent:
  1. Do the hooks fire on every message, and in what order?
  2. Does rail state carry over between messages?
  3. Can a rail add text to the prompt that the model actually follows (and remove it again)?
  4. Can a rail register a tool that the model calls?

Run from the repo root:  C:/Users/A2306101770/venvs/pvl/Scripts/python experiments/hook_test.py
"""
import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
logging.disable(logging.CRITICAL)

from openjiuwen.core.foundation.tool import tool
from openjiuwen.core.single_agent.prompts.builder import PromptSection
from openjiuwen.core.single_agent.rail.base import AgentRail

from pvl.agent import SYSTEM_PROMPT, build_agent

SECTION = "hook_test_injection"


class HookTestRail(AgentRail):
    priority = 90

    def __init__(self):
        self.turn = 0          # state that should survive between messages
        self.events = []       # hooks fired during the current message
        self.inject = False
        self.tool_calls = 0

    def init(self, agent):
        rail = self

        @tool(name="count_turns", description="Return how many user messages there have been so far in this chat.")
        def count_turns() -> str:
            rail.tool_calls += 1
            return str(rail.turn)

        agent.ability_manager.add_ability(count_turns.card, count_turns)
        self.agent = agent

    async def before_invoke(self, ctx):
        self.turn += 1
        self.events = ["before_invoke"]

    async def on_user_message(self, ctx):
        self.events.append(f"on_user_message(parts={len(ctx.inputs.parts)})")

    async def before_model_call(self, ctx):
        self.events.append("before_model_call")
        if self.inject:
            self.agent.prompt_builder.add_section(PromptSection(
                name=SECTION,
                content={"cn": "In your next reply, mention the word 'pineapple' exactly once.",
                         "en": "In your next reply, mention the word 'pineapple' exactly once."},
                priority=200,
            ))
        system = self.agent.prompt_builder.build()
        self.events.append(f"(system prompt: base={'yes' if SYSTEM_PROMPT[:30] in system else 'NO'}, "
                           f"injection={'yes' if SECTION and 'pineapple' in system else 'no'})")

    async def after_model_call(self, ctx):
        self.events.append("after_model_call")
        self.agent.prompt_builder.remove_section(SECTION)

    async def before_tool_call(self, ctx):
        self.events.append("before_tool_call")

    async def after_invoke(self, ctx):
        self.events.append("after_invoke")


async def main():
    sys.stdout.reconfigure(encoding="utf-8")
    agent = build_agent()
    rail = HookTestRail()
    await agent.register_rail(rail)

    script = [
        ("Hi, I'm Ray.", False),
        ("Suggest a snack in one line.", True),
        ("Use the count_turns tool and tell me the number.", False),
        ("Suggest a drink in one line.", False),
    ]
    for query, inject in script:
        rail.inject = inject
        result = await agent.invoke({"query": query, "conversation_id": "hooktest"})
        reply = str(result.get("output")).strip().replace("\n", " ")
        print(f"\n[turn {rail.turn}] you> {query}" + ("   (injecting 'pineapple')" if inject else ""))
        print(f"  hooks: {' -> '.join(rail.events)}")
        print(f"  bot> {reply[:160]}")
        print(f"  mentions pineapple: {'pineapple' in reply.lower()}   tool calls so far: {rail.tool_calls}")


if __name__ == "__main__":
    asyncio.run(main())
