"""
ai_backend.py - single pluggable entry point for every AI feature in this
framework (locator healing, RCA-on-failure, scenario->code generation).

Pick backend via environment variable AI_BACKEND, so nothing is hard-coded
and no secret ever lives in source:

    AI_BACKEND=gemini      GEMINI_API_KEY=...      (default, free tier ok)
    AI_BACKEND=anthropic   ANTHROPIC_API_KEY=...
    AI_BACKEND=ollama      (no key - needs local Ollama server running)
    AI_BACKEND=openrouter  OPENROUTER_API_KEY=...   (has free models)
    AI_BACKEND=nvidia      NVIDIA_API_KEY=...       (build.nvidia.com hosted models)

These can be set once in a .env file at the repo root (same folder as
this repo's src/ and scripts/ folders) instead of typing $env:... every
terminal session - see _load_dotenv() below for the exact file it looks
for and where.

Usage (from anywhere in the framework):

    from src.common.utilities.ai_backend import ask_ai
    reply = ask_ai("You are a Playwright locator-fixing assistant.", user_prompt)

Every call is wrapped so a network/key failure NEVER crashes a test run -
it logs and returns None, and callers must treat None as "AI unavailable,
skip this step, continue normally".
"""
from __future__ import annotations

import os
import logging
from pathlib import Path

logger = logging.getLogger("ai_backend")


def _load_dotenv() -> None:
    """Reads a .env file (KEY=VALUE per line, # comments allowed) and loads
    it into os.environ - values already set in the real environment are
    never overwritten. No external dependency (python-dotenv) required,
    just a plain-text file. Looked up at the repo root: this file lives
    at <repo_root>/src/common/utilities/ai_backend.py, so the repo root
    is 3 parents up."""
    repo_root = Path(__file__).resolve().parents[3]
    env_path = repo_root / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


_load_dotenv()

BACKEND = os.environ.get("AI_BACKEND", "gemini").lower()
TIMEOUT_SECONDS = int(os.environ.get("AI_TIMEOUT_SECONDS", "30"))


def _ask_gemini(system_prompt: str, user_prompt: str, cache_prefix: str | None = None) -> str | None:
    # Gemini implicit caching applies automatically server-side for
    # repeated content, so cache_prefix isn't sent as a separate block
    # here (unlike Anthropic's explicit cache_control) - just fold it
    # back into the prompt so nothing is silently dropped.
    if cache_prefix:
        user_prompt = cache_prefix + "\n" + user_prompt
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        logger.error("google-genai not installed. Run: pip install google-genai --break-system-packages")
        return None
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY not set. export GEMINI_API_KEY=<your key>")
        return None
    client = genai.Client(api_key=api_key)
    try:
        response = client.models.generate_content(
            model=os.environ.get("GEMINI_MODEL", "gemini-2.0-flash"),
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                http_options=types.HttpOptions(timeout=TIMEOUT_SECONDS * 1000),
            ),
        )
        return response.text
    except Exception as exc:
        logger.error(f"Gemini call failed: {exc}")
        return None


def _ask_anthropic(system_prompt: str, user_prompt: str, cache_prefix: str | None = None) -> str | None:
    """cache_prefix (optional): a big chunk of the prompt that is BYTE-FOR-
    BYTE IDENTICAL across many calls in the same session (e.g. this
    framework's reference conventions / base_page.py text - same on every
    module/bank/action you generate). Sent as its own content block with
    Anthropic prompt caching turned on, so the 2nd+ call in a session pays
    only ~10% of that block's input-token cost instead of the full price
    every single time. The system prompt itself is ALSO marked cacheable
    below since SYSTEM_PROMPT in generate_scenario.py is one constant
    string reused for every call regardless of cache_prefix.

    SELF-HEALING: identifies the SPECIFIC Anthropic error (not just a raw
    exception string) and auto-recovers from the ones that have a safe,
    unambiguous fix - a wrong/retired model name, a request that turns
    out too big for max_tokens, or an SDK too old to understand
    cache_control - by adjusting and retrying WITHIN this same call,
    never silently on the ones that need the person to actually do
    something (bad key, no network) - those get one clear, specific
    diagnosis instead of a generic 'call failed' string."""
    try:
        import anthropic
    except ImportError:
        logger.error("anthropic package not installed. Run: pip install \"anthropic>=0.40.0,<1.0.0\" --break-system-packages")
        return None
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error("ANTHROPIC_API_KEY not set - add it to your .env file or set it in the environment.")
        return None
    client = anthropic.Anthropic(api_key=api_key, timeout=TIMEOUT_SECONDS)

    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    max_tokens = int(os.environ.get("ANTHROPIC_MAX_TOKENS", "16000"))
    use_cache = bool(cache_prefix)

    # Known-good current models to fall back through, in order, if the
    # configured one 404s (renamed/retired) - never includes anything
    # older/deprecated, only today's current self-serve model lineup.
    FALLBACK_MODELS = ["claude-sonnet-5", "claude-opus-5", "claude-haiku-4-5-20251001"]
    tried_models: list[str] = []

    def _build_kwargs(use_model: str, use_cache_blocks: bool, tokens: int) -> dict:
        if use_cache_blocks:
            content = [
                {"type": "text", "text": cache_prefix, "cache_control": {"type": "ephemeral"}},
                {"type": "text", "text": user_prompt},
            ]
            system = [{"type": "text", "text": system_prompt, "cache_control": {"type": "ephemeral"}}]
        else:
            content = (cache_prefix + "\n" + user_prompt) if (cache_prefix and not use_cache_blocks) else user_prompt
            system = system_prompt
        return dict(model=use_model, max_tokens=tokens, system=system,
                    messages=[{"role": "user", "content": content}])

    def _classify_and_log(exc: Exception) -> str:
        """Returns one of: 'model_not_found', 'cache_unsupported',
        'too_many_tokens', 'auth', 'connection', 'rate_limit', 'other' -
        and logs a specific, actionable message for whichever it is."""
        msg = str(exc).lower()
        status = getattr(exc, "status_code", None)
        if isinstance(exc, getattr(anthropic, "NotFoundError", ())) or status == 404 or "model:" in msg and "not_found" in msg:
            return "model_not_found"
        if isinstance(exc, getattr(anthropic, "AuthenticationError", ())) or status == 401:
            logger.error("Anthropic AUTHENTICATION ERROR (401) - ANTHROPIC_API_KEY is missing, wrong, or "
                        "revoked. Generate a fresh key at https://console.anthropic.com/settings/keys "
                        "and update your .env - this cannot be auto-fixed.")
            return "auth"
        if isinstance(exc, getattr(anthropic, "APIConnectionError", ())) or "connection" in msg or "timed out" in msg:
            logger.error("Anthropic CONNECTION ERROR - could not reach api.anthropic.com. If you're on a "
                        "company network, check a proxy/firewall isn't blocking it (corporate VPN/proxy "
                        "often needs HTTPS_PROXY set) - this cannot be auto-fixed from here.")
            return "connection"
        if isinstance(exc, getattr(anthropic, "RateLimitError", ())) or status == 429:
            logger.info("Anthropic RATE LIMIT (429) hit - ask_ai's own retry/backoff will try again shortly.")
            return "rate_limit"
        if status == 529 or "overloaded" in msg:
            logger.info("Anthropic OVERLOADED (529) - the service is at capacity - ask_ai's retry/backoff "
                        "will try again shortly.")
            return "rate_limit"
        if "cache_control" in msg or ("cache" in msg and "unsupported" in msg):
            return "cache_unsupported"
        if "max_tokens" in msg and ("exceed" in msg or "too large" in msg or "greater than" in msg):
            return "too_many_tokens"
        logger.error(f"Anthropic call failed (unrecognized error type): {exc}")
        return "other"

    current_model = model
    current_cache = use_cache
    current_tokens = max_tokens
    for _ in range(4):  # at most: original + model-fallback + cache-fallback + token-fallback
        try:
            response = client.messages.create(**_build_kwargs(current_model, current_cache, current_tokens))
            return "".join(b.text for b in response.content if b.type == "text")
        except Exception as exc:  # noqa: BLE001 - must classify every possible SDK exception shape
            kind = _classify_and_log(exc)

            if kind == "model_not_found":
                tried_models.append(current_model)
                next_model = next((m for m in FALLBACK_MODELS if m not in tried_models), None)
                if next_model:
                    logger.error(f"Anthropic MODEL NOT FOUND: '{current_model}' - it may be renamed/retired. "
                                f"Auto-falling back to '{next_model}' for this call. Update ANTHROPIC_MODEL "
                                f"in your .env to stop seeing this message.")
                    current_model = next_model
                    continue
                logger.error(f"Anthropic MODEL NOT FOUND and no fallback model worked either "
                            f"(tried: {tried_models}) - this cannot be auto-fixed further.")
                return None

            if kind == "cache_unsupported" and current_cache:
                logger.error("Anthropic SDK/account rejected cache_control - retrying this call WITHOUT "
                            "prompt caching (you lose the token discount for this call, but it still runs; "
                            "`pip install --upgrade \"anthropic>=0.40.0,<1.0.0\"` to restore caching).")
                current_cache = False
                continue

            if kind == "too_many_tokens" and current_tokens > 4096:
                new_tokens = max(4096, current_tokens // 2)
                logger.error(f"Anthropic rejected max_tokens={current_tokens} - retrying with {new_tokens} "
                            f"(lower ANTHROPIC_MAX_TOKENS in your .env to avoid this retry every time).")
                current_tokens = new_tokens
                continue

            # auth / connection / rate_limit / other: not auto-fixable here -
            # already logged above with a specific diagnosis.
            return None
    return None


def _ask_ollama(system_prompt: str, user_prompt: str, cache_prefix: str | None = None) -> str | None:
    # No prompt-caching support in local Ollama - fold cache_prefix back
    # into the prompt so it's still sent, just not discounted.
    if cache_prefix:
        user_prompt = cache_prefix + "\n" + user_prompt
    try:
        import requests
    except ImportError:
        logger.error("requests not installed.")
        return None
    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    model = os.environ.get("OLLAMA_MODEL", "qwen2.5-coder:7b")
    try:
        resp = requests.post(
            f"{host}/api/chat",
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "stream": False,
            },
            timeout=TIMEOUT_SECONDS,
        )
        resp.raise_for_status()
        return resp.json()["message"]["content"]
    except Exception as exc:
        logger.error(f"Ollama call failed (is `ollama serve` running at {host}?): {exc}")
        return None


def _ask_openrouter(system_prompt: str, user_prompt: str, cache_prefix: str | None = None) -> str | None:
    """OpenRouter - a single API that proxies many models, including
    several genuinely free ones (no billing required). Good fallback when
    Gemini is hitting quota/timeout limits, since it's a completely
    separate provider/quota. Uses the OpenAI-compatible SDK pointed at
    OpenRouter's base_url, exactly as OpenRouter's own docs show.
    cache_prefix: no explicit caching support through this proxy path -
    folded back into the prompt so it's still sent."""
    if cache_prefix:
        user_prompt = cache_prefix + "\n" + user_prompt
    try:
        from openai import OpenAI
    except ImportError:
        logger.error("openai package not installed. Run: pip install openai --break-system-packages")
        return None
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        logger.error("OPENROUTER_API_KEY not set. Get a free key at https://openrouter.ai/keys")
        return None
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key, timeout=TIMEOUT_SECONDS)
    try:
        response = client.chat.completions.create(
            model=os.environ.get("OPENROUTER_MODEL", "nvidia/nemotron-3-super-120b-a12b:free"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        # DEFENSIVE: some free/overloaded models return HTTP 200 with
        # choices=null or an empty list instead of raising an error (e.g.
        # rate-limited, content-filtered, or the provider behind
        # OpenRouter having an internal hiccup) - response.choices[0]
        # on that would raise a confusing "'NoneType' object is not
        # subscriptable" with no hint of the real cause. Check first and
        # give a clear, actionable message instead.
        if not response or not getattr(response, "choices", None):
            error_detail = getattr(response, "error", None) or getattr(response, "model_extra", None)
            logger.error(
                f"OpenRouter returned no choices (response.choices was empty/null) - this usually "
                f"means the free model is overloaded/rate-limited or the prompt was too large for "
                f"it, not a real exception. Raw response detail: {error_detail}. Try again in a "
                f"moment, or switch OPENROUTER_MODEL to a different (possibly paid) model."
            )
            return None
        return response.choices[0].message.content
    except Exception as exc:
        logger.error(f"OpenRouter call failed: {exc}")
        return None


def _ask_nvidia(system_prompt: str, user_prompt: str, cache_prefix: str | None = None) -> str | None:
    """NVIDIA's own hosted model API (build.nvidia.com / NIM) - a
    DIFFERENT provider and quota from both Anthropic and OpenRouter, so
    it's a genuine third option for AI_BACKEND or AI_FALLBACK_BACKEND,
    not just another route to the same underlying models. Also
    OpenAI-compatible, so the same SDK pattern as OpenRouter applies -
    only the base_url, API key, and default model differ.
    cache_prefix: no explicit caching support through this API - folded
    back into the prompt so it's still sent."""
    if cache_prefix:
        user_prompt = cache_prefix + "\n" + user_prompt
    try:
        from openai import OpenAI
    except ImportError:
        logger.error("openai package not installed. Run: pip install openai --break-system-packages")
        return None
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        logger.error("NVIDIA_API_KEY not set. Get a key at https://build.nvidia.com")
        return None
    client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=api_key, timeout=TIMEOUT_SECONDS)
    try:
        response = client.chat.completions.create(
            model=os.environ.get("NVIDIA_MODEL", "nvidia/llama-3.1-nemotron-70b-instruct"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        # DEFENSIVE: same reasoning as _ask_openrouter above - an
        # overloaded/rate-limited model can return HTTP 200 with
        # choices=null instead of a real error.
        if not response or not getattr(response, "choices", None):
            logger.error(
                f"NVIDIA API returned no choices (response.choices was empty/null) - this usually "
                f"means the model is overloaded/rate-limited or the prompt was too large for it, "
                f"not a real exception. Try again in a moment, or switch NVIDIA_MODEL."
            )
            return None
        return response.choices[0].message.content
    except Exception as exc:
        logger.error(f"NVIDIA API call failed: {exc}")
        return None


_BACKENDS = {
    "gemini": _ask_gemini,
    "anthropic": _ask_anthropic,
    "ollama": _ask_ollama,
    "openrouter": _ask_openrouter,
    "nvidia": _ask_nvidia,
}


def ask_ai_vision(system_prompt: str, user_prompt: str, image_paths) -> str | None:
    """Like ask_ai(), but also sends one or more images - this is what
    lets code be generated straight from SCREENSHOTS instead of a live
    browser scan, for when Playwright automation (login/navigation/DOM
    scan) keeps failing - just screenshot the listing page and the Add
    form yourself in your own already-working browser and hand those
    over instead. image_paths can be a single path (str) or a list of
    paths (e.g. [listing_screenshot, add_form_screenshot]).

    Supports Anthropic and Gemini (both multimodal); other backends
    return None so callers can treat vision as unavailable rather than
    crash. Best-effort: any failure (bad image path, network, no key)
    returns None."""
    if isinstance(image_paths, str):
        image_paths = [image_paths]

    if BACKEND == "anthropic":
        try:
            import anthropic
        except ImportError:
            logger.error("anthropic package not installed. Run: pip install \"anthropic>=0.40.0,<1.0.0\" --break-system-packages")
            return None
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            logger.error("ANTHROPIC_API_KEY not set.")
            return None

        import base64
        content = []
        for img_path in image_paths:
            try:
                with open(img_path, "rb") as f:
                    image_bytes = f.read()
            except Exception as exc:
                logger.error(f"Could not read image at {img_path}: {exc}")
                return None
            ext = str(img_path).lower().rsplit(".", 1)[-1]
            media_type = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
                          "webp": "image/webp"}.get(ext, "image/png")
            content.append({
                "type": "image",
                "source": {"type": "base64", "media_type": media_type,
                          "data": base64.b64encode(image_bytes).decode("utf-8")},
            })
        content.append({"type": "text", "text": user_prompt})

        client = anthropic.Anthropic(api_key=api_key, timeout=TIMEOUT_SECONDS)
        try:
            response = client.messages.create(
                model=os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5"),
                max_tokens=int(os.environ.get("ANTHROPIC_MAX_TOKENS", "16000")),
                system=system_prompt,
                messages=[{"role": "user", "content": content}],
            )
            return "".join(b.text for b in response.content if b.type == "text")
        except Exception as exc:
            logger.error(f"Anthropic vision call failed: {exc}")
            return None

    if BACKEND != "gemini":
        logger.info(f"ask_ai_vision: AI_BACKEND='{BACKEND}' doesn't support images here yet - skipping.")
        return None
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        logger.error("google-genai not installed - run: pip install google-genai --break-system-packages")
        return None
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY not set.")
        return None

    parts = []
    for img_path in image_paths:
        try:
            with open(img_path, "rb") as f:
                image_bytes = f.read()
        except Exception as exc:
            logger.error(f"Could not read image at {img_path}: {exc}")
            return None
        parts.append(types.Part.from_bytes(data=image_bytes, mime_type="image/png"))
    parts.append(user_prompt)

    client = genai.Client(api_key=api_key)
    try:
        response = client.models.generate_content(
            model=os.environ.get("GEMINI_MODEL", "gemini-2.0-flash"),
            contents=parts,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                http_options=types.HttpOptions(timeout=TIMEOUT_SECONDS * 1000),
            ),
        )
        return response.text
    except Exception as exc:
        logger.error(f"Gemini vision call failed: {exc}")
        return None



def ask_ai(system_prompt: str, user_prompt: str, cache_prefix: str | None = None) -> str | None:
    """Returns the model's text reply, or None if the AI call could not be
    completed for any reason. Callers must handle None gracefully - AI is
    always a best-effort assist layer, never a hard dependency of the run.

    cache_prefix (optional): a chunk of the prompt that's IDENTICAL across
    many calls in the same run (e.g. this framework's reference/base_page
    conventions - same text regardless of which module/bank/action is
    being generated). On the Anthropic backend this is sent as its own
    prompt-cache-marked block, so the 2nd+ call in a session is billed at
    a fraction of that block's token cost. Other backends fold it back
    into the prompt (no discount, but nothing is lost).

    Retries the PRIMARY backend up to 3 times with exponential backoff
    (2s, 4s, 8s) on transient errors (rate limit / demand spike / timeout
    signatures like 429, 503, 504, DEADLINE_EXCEEDED, RESOURCE_EXHAUSTED)
    before giving up on it - a busy model often succeeds on the very next
    attempt a few seconds later.

    If AI_FALLBACK_BACKEND is set (e.g. AI_FALLBACK_BACKEND=openrouter)
    and the primary backend still fails after its retries, automatically
    tries the fallback backend once - useful when one provider (e.g. a
    newly-released, high-demand Gemini model) is spiking, since a
    completely different provider has its own separate capacity/quota."""
    import time

    TRANSIENT_MARKERS = ("429", "503", "504", "deadline_exceeded", "resource_exhausted",
                        "unavailable", "overloaded", "rate limit")

    REQUIRED_KEY_ENV = {
        "gemini": "GEMINI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "openrouter": "OPENROUTER_API_KEY",
        "nvidia": "NVIDIA_API_KEY",
        # "ollama" needs no key - a local server, not an API key
    }

    def _try_backend(backend_name: str) -> str | None:
        fn = _BACKENDS.get(backend_name)
        if fn is None:
            logger.error(f"Unknown AI_BACKEND '{backend_name}'. Choose one of: {list(_BACKENDS)}")
            return None
        required_env = REQUIRED_KEY_ENV.get(backend_name)
        if required_env and not os.environ.get(required_env):
            logger.error(f"{required_env} not set for backend '{backend_name}' - skipping retries, "
                        f"this won't succeed until the key is set.")
            return None
        delay = 2
        for attempt in range(1, 4):
            result = fn(system_prompt, user_prompt, cache_prefix)
            if result:
                return result
            # fn() already logged the specific error via logger.error(); we
            # can't inspect the exception text here without changing every
            # backend's signature, so just retry a fixed few times on any
            # failure - cheap, and only 3 short waits worst case.
            if attempt < 3:
                logger.info(f"{backend_name} call failed (attempt {attempt}/3) - "
                           f"retrying in {delay}s...")
                time.sleep(delay)
                delay *= 2
        return None

    result = _try_backend(BACKEND)
    if result:
        return result

    fallback = os.environ.get("AI_FALLBACK_BACKEND")
    if fallback and fallback.lower() != BACKEND:
        logger.info(f"Primary backend '{BACKEND}' failed after retries - "
                   f"trying fallback backend '{fallback}'...")
        result = _try_backend(fallback.lower())
        if result:
            return result

    return None
