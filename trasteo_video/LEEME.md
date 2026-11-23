# Video de trasteos (Cúcuta), versión 1 en motion graphics

## Entregables (`final/`)
| Archivo | Estado |
|---|---|
| `trasteo_sin_voz.mp4` | Listo. 1080x1920, 30 fps, H.264 + AAC, 27 s, -14 LUFS. Música, efectos y subtítulos. |
| `portada.png` | Lista. 1080x1920. |
| `texto_publicacion.txt` | Listo. Copy y 8 hashtags. |
| `trasteo_final.mp4` | Falta la voz (se necesita tu OK para gastar créditos de ElevenLabs). |

## Datos a completar (`config.json`)
`nombre`, `nombre_corto` (chip de marca), `whatsapp`, `logo` (ruta a PNG con transparencia, o null).
Con eso se vuelve a renderizar todo:

```bash
python3 scripts/audio.py              # música y efectos (sintetizados, sin licencias)
python3 scripts/render.py video       # escenas -> clips/escenas.mp4
python3 scripts/render.py frames      # cuadros clave -> frames/
python3 scripts/render.py portada     # final/portada.png
python3 scripts/mezcla.py sinvoz      # final/trasteo_sin_voz.mp4
python3 scripts/mezcla.py final audio/voz.mp3   # final/trasteo_final.mp4 (ducking + -14 LUFS)
```

## Escenas (guion y tiempos)
| Tiempo | Escena | Subtítulo |
|---|---|---|
| 0–3 s | Cajas cayendo, signos de pregunta | ¿Te vas a trastear y no sabes por dónde empezar? |
| 3–6 s | Furgón blanco sin logos llega al conjunto | Tranquilo, nosotros lo movemos por ti. |
| 6–12 s | Sofá envuelto con manta y vinipel + chips de lo que incluye | Cargamos, descargamos y protegemos tus muebles con mantas y vinipel, en Cúcuta y fuera de la ciudad. |
| 12–19 s | 3 pasos para cotizar + sello "Precio claro, sin sorpresas" | Cotizar es fácil: … |
| 19–24 s | Chat de WhatsApp + "Separa tu fecha" | ¡Escríbenos ya al WhatsApp y separa tu fecha! |
| 24–27 s | Cierre: nombre, WhatsApp grande, "Escríbenos ya" | n/a |

Zonas seguras: nada importante en y<192, y>1536 ni x>918. El contenido se centra en x=480.

## Propuesta para Higgsfield (no generada)
Desde el conector actual no se puede generar en Higgsfield (solo lectura) y la cuenta tiene 10 créditos (plan gratis).
Prompts listos para usarlos desde la web de Higgsfield si quieres clips reales (9:16, 5 s, sin audio):

1. `Living room of a Colombian apartment full of stacked cardboard moving boxes, a stressed young couple looking at the mess, soft natural window light, handheld camera, realistic, no text, no logos, no watermarks`
2. `Plain white box truck with no logos or lettering arriving at a Colombian residential complex in the morning, warm sunlight, smooth tracking shot, realistic, no text, no logos`. Si hay fotos reales del camión: imagen a video con zoom lento.
3. `Close-up of two movers carefully wrapping a sofa with quilted blue moving blankets and clear plastic stretch wrap, gentle hands, shallow depth of field, realistic, no text, no logos`
4. `Fast-paced shot of cardboard boxes being loaded into the back of a white truck by movers, energetic rhythm, daylight, realistic, no text, no logos`
5. `Happy Colombian family unpacking boxes in their new bright apartment, smiling, warm natural light, realistic, no text, no logos`
