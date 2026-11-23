"""Genera la pista instrumental (alegre y suave, sin letra) y los efectos (whoosh + pops).

Todo se sintetiza con numpy: no hay muestras ni música de terceros.
Salida: audio/musica.wav y audio/sfx.wav (48 kHz, estéreo, 27 s).
"""
import json
import sys
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SR = 48000
DUR = 27.0
BPM = 104
BEAT = 60 / BPM
BAR = 4 * BEAT
N = int(SR * DUR)
rng = np.random.default_rng(7)


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def add(buf, sig, t0, gain=1.0, pan=0.0):
    i0 = int(t0 * SR)
    if i0 >= len(buf):
        return
    sig = sig[: len(buf) - i0]
    l = np.cos((pan + 1) * np.pi / 4)
    r = np.sin((pan + 1) * np.pi / 4)
    buf[i0 : i0 + len(sig), 0] += sig * gain * l * 1.414
    buf[i0 : i0 + len(sig), 1] += sig * gain * r * 1.414


def lowpass(x, cutoff):
    # filtro de un polo, cutoff puede ser escalar o array
    a = np.exp(-2 * np.pi * np.asarray(cutoff) / SR)
    y = np.zeros_like(x)
    prev = 0.0
    if np.ndim(a) == 0:
        b = 1 - a
        for i in range(len(x)):
            prev = b * x[i] + a * prev
            y[i] = prev
    else:
        for i in range(len(x)):
            prev = (1 - a[i]) * x[i] + a[i] * prev
            y[i] = prev
    return y


def pluck(f, dur=0.5):
    t = np.arange(int(SR * dur)) / SR
    s = (np.sin(2 * np.pi * f * t) * np.exp(-t * 7)
         + 0.35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 11)
         + 0.12 * np.sin(2 * np.pi * 3 * f * t) * np.exp(-t * 16))
    att = np.minimum(1, t / 0.004)
    return s * att


def pad(freqs, dur):
    t = np.arange(int(SR * dur)) / SR
    s = np.zeros_like(t)
    for f in freqs:
        for det in (0.9985, 1.0015):
            ff = f * det
            s += np.sin(2 * np.pi * ff * t) + 0.4 * np.sin(2 * np.pi * 2 * ff * t) + 0.15 * np.sin(2 * np.pi * 3 * ff * t)
    env = np.minimum(1, t / 0.35) * np.minimum(1, (dur - t) / 0.4)
    return s * env / (len(freqs) * 2)


def bass(f, dur):
    t = np.arange(int(SR * dur)) / SR
    s = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)
    env = np.minimum(1, t / 0.01) * np.exp(-t * 2.2)
    return s * env


def kick():
    t = np.arange(int(SR * 0.3)) / SR
    f = 50 + 90 * np.exp(-t * 30)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 14)


def shaker():
    n = int(SR * 0.06)
    t = np.arange(n) / SR
    x = rng.standard_normal(n)
    x = x - lowpass(x, 5000)  # paso alto
    return x * np.exp(-t * 70)


def clap():
    n = int(SR * 0.2)
    t = np.arange(n) / SR
    x = rng.standard_normal(n)
    x = lowpass(x, 3500) - lowpass(x, 900)
    return x * np.exp(-t * 22)


def music():
    buf = np.zeros((N, 2))
    prog = [  # (acorde, bajo)
        ([60, 64, 67], 48),  # C
        ([59, 62, 67], 43),  # G
        ([57, 60, 64], 45),  # Am
        ([57, 60, 65], 41),  # F
    ]
    arp = [0, 2, 1, 2, 3, 2, 1, 2]
    k, sh, cl = kick(), shaker(), clap()
    nbars = int(np.ceil(DUR / BAR))
    for b in range(nbars):
        chord, root = prog[b % 4]
        t0 = b * BAR
        add(buf, pad([midi(n) for n in chord], BAR + 0.3), t0, 0.10)
        add(buf, bass(midi(root), BEAT * 2), t0, 0.22)
        add(buf, bass(midi(root), BEAT * 2), t0 + 2 * BEAT, 0.18)
        tones = chord + [chord[0] + 12]
        for i, idx in enumerate(arp):
            n = tones[idx] + 12
            add(buf, pluck(midi(n)), t0 + i * BEAT / 2, 0.10, pan=-0.3 if i % 2 else 0.3)
        for beat in range(4):
            tb = t0 + beat * BEAT
            add(buf, k, tb, 0.35)
            add(buf, sh, tb + BEAT / 2, 0.05, pan=0.4)
            add(buf, sh, tb + BEAT / 4, 0.025, pan=-0.4)
            if beat in (1, 3):
                add(buf, cl, tb, 0.10)
    t = np.arange(N) / SR
    fade = np.minimum(1, t / 0.15) * np.minimum(1, (DUR - t) / 1.2)
    buf *= fade[:, None]
    return buf


def whoosh(dur=0.7):
    n = int(SR * dur)
    t = np.arange(n) / SR
    x = rng.standard_normal(n)
    sweep = 400 + 5000 * np.sin(np.pi * t / dur) ** 2
    y = lowpass(x, sweep) - lowpass(x, sweep * 0.25)
    env = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 2
    return y * env / (np.abs(y).max() + 1e-9)


def pop(f0=650, f1=1100):
    t = np.arange(int(SR * 0.09)) / SR
    f = f0 + (f1 - f0) * t / 0.09
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 40)


def sfx():
    buf = np.zeros((N, 2))
    w = whoosh()
    for tb in (3.0, 6.0, 12.0, 19.0, 24.0):  # cambios de escena
        add(buf, w, tb - 0.35, 0.5)
    for tp in (0.15, 0.3, 0.45, 0.6, 0.75, 0.9,  # cajas cayendo
               9.9, 10.15, 10.4, 10.65,          # chips de lo que incluye
               13.2, 14.6, 15.8, 17.4,           # pasos para cotizar + sello
               19.6, 21.5, 22.2,                 # chat + fecha
               24.5, 25.0):                      # cierre
        add(buf, pop(), tp, 0.18)
    return buf


def write_wav(path, buf):
    buf = buf / max(1.0, np.abs(buf).max() / 0.89)
    data = (np.clip(buf, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes(data.tobytes())


if __name__ == "__main__":
    out = ROOT / "audio"
    out.mkdir(exist_ok=True)
    write_wav(out / "musica.wav", music())
    write_wav(out / "sfx.wav", sfx())
    print("ok", out)
