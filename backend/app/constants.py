import uuid

DEFAULT_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")

# ── Book processing ───────────────────────────────────────────
# Number of pages converted per vision batch during chapter parsing.
BATCH_SIZE = 3

# ── KP animation (Manim pipeline) ─────────────────────────────
# KPs with difficulty strictly below this threshold are skipped — trivial
# facts don't benefit enough from a visual to justify the render cost.
ILLUSTRATION_MIN_DIFFICULTY = 2
# Concurrent Manim renders per chapter. CPU + FFmpeg bound; raising above 2
# on a laptop saturates cores and *slows* total throughput.
ILLUSTRATION_CONCURRENCY = 2
# "low" | "medium" | "high". High = 1080p60, ~45–90s per render.
ILLUSTRATION_QUALITY = "high"

# ── Tutor ──────────────────────────────────────────────────────
# Learner-profile blob is prepended to every tutor system prompt; cap it
# so the cached system block stays bounded.
MAX_LEARNER_PROFILE_CHARS = 2000
# How many most-recent messages are fed back into each streamed turn.
HISTORY_WINDOW = 6
