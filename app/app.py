import asyncio
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
import dotenv
import os

app = FastAPI(
    title="Log Viewer API",
    description="An API to view and manage log files.",
    version="1.0.0",
)

templates = Jinja2Templates(directory="./templates")

app.mount("/app/logs", StaticFiles(directory="./logs"), name="Logs Files")

# Get environment variables
LOGS_EXTENSIONS = os.getenv("LOGS_EXTENSIONS", ".log,.txt").split(",")
LOGS_DIRECTORY = os.getenv("LOGS_DIRECTORY", "./logs")

# Create the app logs directory if it doesn't exist
if not os.path.exists("./logs"):
    os.makedirs("./logs", exist_ok=True)


def get_logs_files():
    """
    Get a list of log files in the specified directory with the specified extensions.
    """
    if not os.path.exists("./logs"):
        print("Logs directory 'logs' does not exist.")
        return []

    files = []
    for root, _, filenames in os.walk("./logs"):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in LOGS_EXTENSIONS):
                files.append(os.path.join(root, filename))

    # Sort files by modification time, newest first
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return files


@app.get("/")
async def logs(request: Request):
    log_files = get_logs_files()
    return templates.TemplateResponse(
        "index.html", {"request": request, "log_files": log_files}
    )


def tail_file(file_path: str, n: int):
    """Efficiently get last n lines of a file (like Unix tail)"""
    with open(file_path, "rb") as f:
        # Go to the end of file
        f.seek(0, os.SEEK_END)
        file_size = f.tell()

        block_size = 1024
        lines = []
        remaining_bytes = file_size

        while len(lines) < n + 1 and remaining_bytes > 0:
            if remaining_bytes - block_size > 0:
                # Seek back one block
                f.seek(max(0, file_size - block_size), os.SEEK_SET)
                blocks = [f.read(block_size)]
            else:
                # File too small, read from start
                f.seek(0, os.SEEK_SET)
                blocks = [f.read(remaining_bytes)]

            remaining_bytes -= block_size
            lines_found = blocks[0].count(b"\n")
            lines.extend(blocks[0].splitlines(keepends=True))
            if len(lines) >= n + 1:
                break

        return lines[-n:]


@app.get("/stream")
async def stream_log(file: str = None, lines: int = 100):
    if file is None:
        file_path = os.path.join("logs", "app.log")
    else:
        file = os.path.basename(file.replace("..", ""))
        file_path = os.path.join("logs", file)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    async def generate():
        try:
            # Get ONLY the last N lines
            last_lines = tail_file(file_path, lines)
            for line in last_lines:
                yield line.decode("utf-8", errors="replace")
        except Exception as e:
            yield f"ERROR: {str(e)}\n"

    return StreamingResponse(
        generate(),
        media_type="text/plain",
        headers={"X-Content-Type-Options": "nosniff"},
    )
