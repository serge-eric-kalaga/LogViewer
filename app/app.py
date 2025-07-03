from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
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


if __name__ == "__main__":
    import uvicorn

    # Load environment variables from .env file
    dotenv.load_dotenv()

    # Run the FastAPI app
    uvicorn.run("app:app", host="0.0.0.0", port=80, reload=True)
