import uvicorn
import sys
import os
from pathlib import Path

# Add the 'src' directory to the Python path
src_path = str(Path(__file__).parent / "src")

# Insert it for the current process
sys.path.insert(0, src_path)

# Set PYTHONPATH so that uvicorn's reload workers can also find 'app'
os.environ["PYTHONPATH"] = src_path + os.pathsep + os.environ.get("PYTHONPATH", "")

if __name__ == "__main__":
    # Run the fast api server using string reference for reload to work
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
