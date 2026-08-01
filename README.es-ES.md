

# qwen-voice (Habilidad de Agente)

Objetivo: Agregar **comprensión de voz + respuesta por voz** a los chats de agentes.

Destacados:
- ASR: voz → texto (marcas de tiempo aproximadas opcionales mediante segmentación)
- TTS: texto → voz (voz predeterminada: Cherry)
- Clonación de voz: una muestra de voz → tu voz personalizada → respuestas por voz

Funciona muy bien en **Clawdbot** (y en otros alojamientos de agentes que admiten Habilidades de Agente).

## Instalación (Habilidad de Agente)

```bash
npx skills add ada20204/qwen-voice
```

## Requisitos

Sistema:
- ffmpeg

Python:
- Python 3.10+
- Recomendado: `uv` (o cualquier venv + pip)

## Variables de entorno

Requeridas:
- `DASHSCOPE_API_KEY`

### Origen de lectura de variables de entorno

Los scripts admiten **ambas opciones**:
1) **Nivel de usuario** (recomendado): `~/.config/qwen-voice/.env`
2) **Nivel de proyecto** (desarrollo/pruebas): `./.qwen-voice/.env`

Precedencia: primero nivel de usuario, luego nivel de proyecto.

> Importante: Intencionalmente ignoramos las variables de entorno del sistema. Solo se utilizan archivos `.env`.

### Configuración (recomendada)

Copia el directorio de plantilla en tu configuración de usuario:

```bash
cp -r .qwen-voice ~/.config/qwen-voice
cp ~/.config/qwen-voice/.env.example ~/.config/qwen-voice/.env
# edita ~/.config/qwen-voice/.env
```

### Configuración (local al proyecto, opcional)

```bash
cp .qwen-voice/.env.example .qwen-voice/.env
# edita .qwen-voice/.env
```

## Comandos rápidos

ASR (sin marcas de tiempo):
```bash
python3 scripts/qwen_asr.py --in /path/to/audio.ogg
```

ASR (con marcas de tiempo aproximadas):
```bash
python3 scripts/qwen_asr.py --in /path/to/audio.ogg --timestamps --chunk-sec 3
```

TTS (voz predefinida):
```bash
python3 scripts/qwen_tts.py --text '你好，我是 Pi。' --voice Cherry --out /tmp/out.ogg
```

Clonación de voz (crear perfil una vez, reutilizar):
```bash
python3 scripts/qwen_voice_clone.py --in ./sample.ogg --name george --out ./george.voice.json
python3 scripts/qwen_tts.py --text '你好，我是 George。' --voice-profile ./george.voice.json --out /tmp/out.ogg
```

## Notas / advertencias

- Las marcas de tiempo son **basadas en segmentos**, no alineación a nivel de palabra.
- Las entradas se convierten a **WAV mono de 16k** antes del ASR.
- La salida `.ogg` es Opus (compatible con notas de voz de Telegram).

## Estructura del repositorio

- `SKILL.md` + `scripts/` son el punto de entrada de la Habilidad de Agente (descubrimiento estándar)
- `.qwen-voice/` directorio de plantilla de entorno (copiar a `~/.config/qwen-voice/`)
