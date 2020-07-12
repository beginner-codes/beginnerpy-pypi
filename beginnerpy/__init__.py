from typing import Optional
import colorama
import json
import pathlib
import time
import toml
import urllib.request


colorama.init()


def _get_expected_version() -> Optional[str]:
    resp = urllib.request.urlopen("https://beginnerpy.com/challenges/pip-version", timeout=1)
    data = json.loads(resp.read())
    return data.get("version") if isinstance(data, dict) else None


def _check_versions(expected_version: str):
    pyproject = toml.load(pathlib.Path(__file__).parent.parent / "pyproject.toml")
    current_version = pyproject.get("tool", {}).get("poetry", {}).get("version")
    message = ""
    if not current_version:
        message = (
            f"Please update the BeginnerPy package\n\n"
            f"pip install beginnerpy --upgrade"
        )
    elif current_version != expected_version:
        message = (
            f"Please update the BeginnerPy package\n"
            f"Your version is {current_version}\n"
            f"The latest version is {expected_version}\n\n"
            f"pip install beginnerpy --upgrade"
        )

    if message:
        style = f"{colorama.Fore.RED}{colorama.Back.WHITE}{colorama.Style.BRIGHT}"
        out = [f"{style}{' ' * 80}"]
        for line in message.split("\n"):
            out.append(line.center(80))
        out.append(" " * 80)
        out.append(" " * 80 + colorama.Style.RESET_ALL)
        print(f"{colorama.Style.RESET_ALL}\n{style}".join(out), flush=True)

        print(f"{colorama.Fore.BLACK}{colorama.Back.YELLOW}Running tests in 5", end="", flush=True)
        for i in range(5, -1, -1):
            print(f"\b{i}", end="", flush=True)
            time.sleep(1)
        print(colorama.Style.RESET_ALL, flush=True)


_check_versions(_get_expected_version())
