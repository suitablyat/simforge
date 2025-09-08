import json
import tempfile
import pathlib
import subprocess
import time

from .settings import settings

class SimcError(RuntimeError):
    ...

def resolve_simc_bin(channel: str | None) -> pathlib.Path:
    """
    Wählt das passende simc-Binary je nach Channel.
    Reihenfolge:
      1) SIMC_BIN (harte ENV-Override) -> ignoriert Channel komplett
      2) nightly/latest -> settings.simc_bin_nightly
      3) weekly -> settings.simc_bin_weekly (Fallback: nightly, falls weekly fehlt)
    """
    # 1) harter Override
    if settings.simc_bin:
        p = pathlib.Path(settings.simc_bin)
        if not p.exists():
            raise SimcError(f"SIMC_BIN override not found at: {p}")
        return p

    # 2) Channel-Logik
    c = (channel or settings.simc_default_channel or "latest").lower()
    if c in ("latest", "nightly"):
        p = pathlib.Path(settings.simc_bin_nightly)
    elif c == "weekly":
        p = pathlib.Path(settings.simc_bin_weekly)
        if not p.exists():
            # Fallback, falls weekly noch nicht eingebaut/gebaut wurde
            p = pathlib.Path(settings.simc_bin_nightly)
    else:
        raise SimcError(f"Unknown simc channel '{channel}'. Use: latest|nightly|weekly")

    if not p.exists():
        raise SimcError(f"simc binary not found at {p}")
    return p

def run_simc(simc_input: str, channel: str | None = None) -> dict:
    """
    Führt SimulationCraft aus.
    - schreibt Input in eine temp-Datei
    - bevorzugt JSON-Ausgabe via 'json2=<file>'
    - loggt stdout/stderr in /app/logs (konfigurierbar)
    """
    bin_path = resolve_simc_bin(channel)

    # Log-Dateien anlegen
    log_dir = pathlib.Path(settings.simc_log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d-%H%M%S")
    ch = (channel or settings.simc_default_channel or "latest").lower()
    base = log_dir / f"simc_{ch}_{ts}"
    stdout_log = base.with_suffix(".out.log")
    stderr_log = base.with_suffix(".err.log")

    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        in_file = td / "input.simc"
        out_file = td / "result.json"
        in_file.write_text(simc_input, encoding="utf-8")

        cmd = [
            str(bin_path),
            f"input={in_file}",
            f"json2={out_file}",
            f"threads={settings.simc_threads}",
        ]

        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=settings.simc_timeout_sec,
                check=False,
            )
        except subprocess.TimeoutExpired as e:
            raise SimcError(f"simc timeout after {settings.simc_timeout_sec}s (channel={ch})") from e

        # Logs persistieren
        stdout_log.write_text(proc.stdout or "", encoding="utf-8")
        stderr_log.write_text(proc.stderr or "", encoding="utf-8")

        if proc.returncode != 0:
            raise SimcError(f"simc failed (exit {proc.returncode}) — see {stderr_log}")

        if out_file.exists():
            try:
                return json.loads(out_file.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                # Fallback: stdout als JSON versuchen
                pass

        if proc.stdout:
            try:
                return json.loads(proc.stdout)
            except Exception:
                return {"stdout": proc.stdout}

        raise SimcError("simc produced no output")
