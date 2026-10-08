import asyncio
import runpod

from app.agent.manus import Manus


async def run_openmanus(prompt: str):
    agent = await Manus.create()

    try:
        result = await agent.run(prompt)
        return result
    finally:
        await agent.cleanup()


def handler(job):
    job_input = job.get("input", {})
    prompt = job_input.get("prompt")

    if not prompt:
        return {
            "error": "Missing prompt. Send input.prompt."
        }

    try:
        result = asyncio.run(run_openmanus(prompt))

        return {
            "status": "completed",
            "result": result
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


runpod.serverless.start({
    "handler": handler
})
