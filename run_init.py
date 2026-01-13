import subprocess
import sys


def run_script():
    try:
        result = subprocess.run(
            [sys.executable, "src/db/init_referees_coaches.py"],
            capture_output=True,
            text=True,
            check=True,
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")


if __name__ == "__main__":
    run_script()
