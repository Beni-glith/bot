import asyncio
import json
import os

MECLI_PATH = os.path.join(os.getcwd(), "me-cli")

async def run_mecli(args: list):
    """Menjalankan tools me-cli via subprocess"""
    proc = await asyncio.create_subprocess_exec(
        "python3", os.path.join(MECLI_PATH, "main.py"), *args,
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    out, err = await proc.communicate()
    if err:
        return {"error": err.decode()}
    try:
        return json.loads(out.decode())
    except Exception:
        return {"raw": out.decode()}

async def get_user_stats(user_id: int):
    return await run_mecli(["stats", str(user_id)])

async def order_account(user_id: int, product: str):
    return await run_mecli(["order", str(user_id), product])
