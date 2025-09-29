import asyncio
import websockets
import logging
from pathlib import Path
from typing import List

# Конфигурация истории
HISTORY_FILE = Path(__file__).parent / "chat_history.txt"
MAX_HISTORY = 10

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Множество для хранения активных WebSocket-подключений
connected_clients = set()

import functools
import asyncio
from pathlib import Path

history_lock = asyncio.Lock()
HISTORY_FILE = Path(__file__).parent / "chat_history.txt"

def _sync_append_line(path: Path, line: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    safe_line = line.replace("\r", " ").replace("\n", " ")
    with open(path, "a", encoding="utf-8") as f:
        f.write(safe_line + "\n")

def _sync_read_lines(path: Path):
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [ln.rstrip("\n") for ln in f]

async def _run_in_thread(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    pfunc = functools.partial(func, *args, **kwargs)
    return await loop.run_in_executor(None, pfunc)

async def save_message(message: str):
    async with history_lock:
        await _run_in_thread(_sync_append_line, HISTORY_FILE, message)

async def load_history(n: int):
    lines = await _run_in_thread(_sync_read_lines, HISTORY_FILE)
    return lines[-n:] if lines else []

async def handle_connection(websocket: websockets.WebSocketServerProtocol):
    """
    Логика при новом подключении:
      1) добавить в connected_clients
      2) отправить последние MAX_HISTORY сообщений только этому клиенту
      3) принимать сообщения: сохранять и транслировать
    """
    connected_clients.add(websocket)
    logger.info(f"New connection: {websocket.remote_address}")

    try:
        # Отправляем историю новому клиенту
        history = await load_history(MAX_HISTORY)
        if history:
            logger.info(f"Sending {len(history)} history messages to {websocket.remote_address}")
            for msg in history:
                try:
                    await websocket.send(msg)
                except Exception as e:
                    logger.warning(f"Failed to send history to {websocket.remote_address}: {e}")
                    break

        # Обработка входящих сообщений от этого клиента
        async for message in websocket:
            logger.info(f"Received from {websocket.remote_address}: {message}")
            # Сохраняем (не блокирует event loop)
            await save_message(message)
            # Транслируем всем клиентам
            await broadcast(message)

    except websockets.exceptions.ConnectionClosed as e:
        logger.info(f"Connection closed by {websocket.remote_address}: {e}")
    except Exception as e:
        logger.exception(f"Error handling {websocket.remote_address}: {e}")
    finally:
        if websocket in connected_clients:
            connected_clients.remove(websocket)
        logger.info(f"Client {websocket.remote_address} disconnected")
async def broadcast(message):
    """
    Транслирует полученное сообщение всем подключенным клиентам.
    """
    if connected_clients:
        # Отправляем сообщение всем клиентам, используя asyncio.gather
        await asyncio.gather(*(client.send(message) for client in connected_clients))

async def main():
    # Запуск WebSocket-сервера на localhost:8765
    server = await websockets.serve(handle_connection, "localhost", 8765) # websockets.serve(handle_connection, "0.0.0.0", 8765)
    logger.info("WebSocket сервер запущен на ws://localhost:8765")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())


# pip install websockets
# Запуск сервера: python .\serve\main.py &
# Запуск клиента: cd client/ && python -m http.server 8000 &