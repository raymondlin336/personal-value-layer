"""Chat with the baseline agent in the terminal. Type 'quit' to exit."""
import asyncio

from pvl.agent import build_agent


async def main() -> None:
    agent = build_agent()
    print("Baseline assistant ready. Type 'quit' to exit.\n")
    while True:
        query = input("you> ").strip()
        if query.lower() in {"quit", "exit"}:
            break
        if not query:
            continue
        result = await agent.invoke({"query": query, "conversation_id": "demo"})
        print(f"bot> {result.get('output')}\n")


if __name__ == "__main__":
    asyncio.run(main())
