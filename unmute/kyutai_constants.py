import os
from pathlib import Path

from unmute.websocket_utils import http_to_ws

HEADERS = {"kyutai-api-key": "public_token"}

# The defaults are already ws://, but make the env vars support http:// and https://
STT_SERVER = http_to_ws(os.environ.get("KYUTAI_STT_URL", "ws://localhost:8090"))
TTS_SERVER = http_to_ws(os.environ.get("KYUTAI_TTS_URL", "ws://localhost:8089"))
LLM_SERVER = os.environ.get("KYUTAI_LLM_URL", "http://localhost:8091")
KYUTAI_LLM_MODEL = os.environ.get("KYUTAI_LLM_MODEL")
KYUTAI_LLM_API_KEY = os.environ.get("KYUTAI_LLM_API_KEY")
# On OpenRouter, send tool requests only to providers that support every
# parameter we pass (tools, tool_choice). Without it, some Llama providers
# return the tool call as plain text instead of a real call. Set to 0 to allow
# any provider. Ignored for non-OpenRouter servers.
LLM_REQUIRE_TOOL_PROVIDERS = os.environ.get("LLM_REQUIRE_TOOL_PROVIDERS", "1").lower() not in (
    "0",
    "false",
    "no",
)
# Among those providers, prefer the quickest to answer ("latency"), or
# "throughput" / "price". Empty leaves OpenRouter's default load balancing.
# Every tool call costs two model round trips, so this is most of the wait.
LLM_PROVIDER_SORT = os.environ.get("LLM_PROVIDER_SORT", "latency").strip()
# OpenRouter providers never to use, comma-separated, e.g. "Groq" if one keeps
# rejecting the model's tool calls. Empty uses them all.
LLM_PROVIDER_IGNORE = [
    p.strip() for p in os.environ.get("LLM_PROVIDER_IGNORE", "").split(",") if p.strip()
]
# Speak a stock phrase ("One moment...") when the model calls a tool without a
# lead-in. Off by default: the TTS voices text about 2 s behind what it has
# been sent, so a short phrase followed by silence isn't spoken until the
# answer after the tool arrives, and then comes out glued to it.
TOOL_FILLER_ENABLED = os.environ.get("TOOL_FILLER_ENABLED", "0").lower() in ("1", "true", "yes")

# --- Tool calling (fork addition) ---
# The fork holds NO business logic and NO third-party secrets: it only knows
# where the voice-ai-agent backend lives and the key to authenticate with it.
# See 00-TOOL-CONTRACT.md §1. TOOL_API_BASE_URL must NOT end in a slash.
TOOL_API_BASE_URL = os.environ.get("TOOL_API_BASE_URL", "http://localhost:8081").rstrip(
    "/"
)
TOOL_API_KEY = os.environ.get("TOOL_API_KEY")
# Hard per-tool client-side timeout, seconds (contract §1 fast path).
TOOL_TIMEOUT_S = float(os.environ.get("TOOL_TIMEOUT_S", "3.0"))
# Client tools make a round trip over the session's WebSocket and may hit a CRM
# (a room check, saving requests), so they get longer than a local lookup.
CLIENT_TOOL_TIMEOUT_S = float(os.environ.get("CLIENT_TOOL_TIMEOUT_S", "10.0"))
# Bound the pause-act-resume loop so a misbehaving model cannot spiral.
MAX_TOOL_ITERATIONS = int(os.environ.get("MAX_TOOL_ITERATIONS", "3"))
# Offer ONLY the local, in-process smoke-test tool (no backend needed). Use this
# to demo the pipeline end-to-end before the voice-ai-agent routes exist.
TOOL_SMOKE_TEST = os.environ.get("TOOL_SMOKE_TEST", "").lower() in ("1", "true", "yes")
VOICE_CLONING_SERVER = os.environ.get(
    "KYUTAI_VOICE_CLONING_URL", "http://localhost:8092"
)
# If None, a dict-based cache will be used instead of Redis
REDIS_SERVER = os.environ.get("KYUTAI_REDIS_URL")

SPEECH_TO_TEXT_PATH = "/api/asr-streaming"
TEXT_TO_SPEECH_PATH = "/api/tts_streaming"

repo_root = Path(__file__).parents[1]
VOICE_DONATION_DIR = Path(
    os.environ.get("KYUTAI_VOICE_DONATION_DIR", repo_root / "voices" / "donation")
)

# If None, recordings will not be saved
_recordings_dir = os.environ.get("KYUTAI_RECORDINGS_DIR")
RECORDINGS_DIR = Path(_recordings_dir) if _recordings_dir else None

# Also checked on the frontend, see constant of the same name
MAX_VOICE_FILE_SIZE_MB = 4


SAMPLE_RATE = 24000
SAMPLES_PER_FRAME = 1920
FRAME_TIME_SEC = SAMPLES_PER_FRAME / SAMPLE_RATE  # 0.08
# TODO: make it so that we can read this from the ASR server?
STT_DELAY_SEC = 0.5
