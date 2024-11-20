import subprocess
import sys

port = 8000

if len(sys.argv) >= 2:
    try:
        port = int(sys.argv[1])
    except ValueError:
        print(f"Invalid port: {sys.argv[1]}")
        sys.exit(1)

INTERPRETER = sys.executable
COMMAND = f'{INTERPRETER} -m gunicorn --reload --timeout 1 --bind 0.0.0.0:{port} "app:create_app()"'

p = subprocess.Popen(
    COMMAND,
    shell=True,
    stdin=sys.stdin,
    stdout=sys.stdout,
    stderr=sys.stderr,
    text=True,
    bufsize=1,
    universal_newlines=True,
)

p.wait()
