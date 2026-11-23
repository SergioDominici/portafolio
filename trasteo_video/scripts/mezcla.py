"""Mezcla audio + video y exporta H.264/AAC normalizado a -14 LUFS (dos pasadas de loudnorm).

Uso:
  python3 scripts/mezcla.py sinvoz               -> final/trasteo_sin_voz.mp4 (música + efectos)
  python3 scripts/mezcla.py final audio/voz.mp3  -> final/trasteo_final.mp4 (voz + música con ducking + efectos)
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VIDEO = ROOT / "clips" / "escenas.mp4"
MUSIC = ROOT / "audio" / "musica.wav"
SFX = ROOT / "audio" / "sfx.wav"
TARGET = "I=-14:TP=-1.5:LRA=11"


def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def graph(voice):
    if not voice:
        # sin voz: la música va al frente
        return "[1:a]volume=0.9[m];[2:a]volume=0.8[s];[m][s]amix=inputs=2:normalize=0[mix]"
    # con voz: la voz entra 0.3 s tarde; la música baja (sidechain) cuando habla
    return (
        "[3:a]aresample=48000,aformat=channel_layouts=stereo,adelay=300|300,"
        "highpass=f=80,acompressor=threshold=0.1:ratio=3:attack=5:release=120,volume=1.6,asplit=2[v][key];"
        "[1:a]volume=0.55[m];"
        "[m][key]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=350:makeup=1[md];"
        "[2:a]volume=0.6[s];"
        "[v][md][s]amix=inputs=3:normalize=0[mix]"
    )


def main():
    mode = sys.argv[1]
    voice = Path(sys.argv[2]) if mode == "final" else None
    out = ROOT / "final" / ("trasteo_final.mp4" if voice else "trasteo_sin_voz.mp4")
    ins = ["-i", str(VIDEO), "-i", str(MUSIC), "-i", str(SFX)] + (["-i", str(voice)] if voice else [])
    g = graph(voice)
    # pasada 1: medir
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats"] + ins + [
        "-filter_complex", g + f";[mix]loudnorm={TARGET}:print_format=json[o]",
        "-map", "[o]", "-t", "27", "-f", "null", "-"], capture_output=True, text=True)
    m = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr).group(0))
    ln = (f"loudnorm={TARGET}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    # pasada 2: exportar
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"] + ins + [
        "-filter_complex", g + f";[mix]{ln},aresample=48000[o]",
        "-map", "0:v", "-map", "[o]", "-t", "27",
        "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(out)])
    print("ok", out)


if __name__ == "__main__":
    main()
