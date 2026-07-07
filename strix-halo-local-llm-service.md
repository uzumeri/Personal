# Strix Halo (Ryzen AI Max+ 395, 128 GB) as a Local LLM Service

A working plan for turning the Strix Halo box into an always-on inference server that
your other machines — including this VS Code / Claude Code setup — can call over the LAN.

*Written 2026-07-06. Local-LLM tooling moves fast; re-check version numbers before you commit.*

---

## 1. What you actually have (and what it means)

| Spec | Value | Consequence |
|---|---|---|
| APU | Ryzen AI Max+ 395 (16× Zen 5) | Strong CPU, but the iGPU/NPU do the LLM work |
| iGPU | Radeon 8060S, RDNA 3.5, `gfx1151` | This is what llama.cpp/ROCm/Vulkan target |
| NPU | XDNA 2, ~50 TOPS | Used by AMD's Lemonade for *prefill* only |
| Memory | 128 GB LPDDR5X-8000, **unified** | The whole reason this box is interesting |
| Bandwidth | ~256 GB/s | **The real bottleneck** — governs tokens/sec |

**The one mental model that matters:** this machine is *capacity-rich but bandwidth-poor*.

- A discrete 4090 has ~1000 GB/s but only 24 GB. It's fast on small models, can't hold big ones.
- Strix Halo has ¼ the bandwidth but **5×+ the usable VRAM**. It runs models a 4090 physically
  cannot load — 70B dense, or 100B+ MoE — just at a gentler token rate.

**Practical implication:** favor **Mixture-of-Experts (MoE)** models. Token-generation speed
scales with *active* parameters, not total. A 120B MoE with ~5B active parameters runs *far*
faster here than a dense 70B, because only the active experts stream through memory each token.
This is the sweet spot for the hardware.

---

## 2. Decision: OS and server stack

Two axes to decide. My recommendations in **bold**.

**OS:**
- **Linux (Ubuntu 24.04 / Fedora 42)** — best ROCm support, best memory-allocation control,
  best for a headless always-on service. **Recommended for the server role.**
- Windows — fine if this box is also your daily driver; Lemonade and LM Studio both run natively.
  You lose some ROCm maturity and the fine-grained GTT memory tricks.

**Server (pick one to start; you can run more than one on different ports later):**

| Stack | Best for | API | Notes |
|---|---|---|---|
| **Lemonade Server** | AMD-native, NPU+iGPU | OpenAI-compatible | AMD's own; splits prefill→NPU, decode→iGPU. Bundles Whisper/SD/TTS too. |
| **Ollama** | Easiest, lowest friction | OpenAI-compatible (`/v1`) + native | Great model management; Vulkan/ROCm backends. **Start here.** |
| **llama.cpp server** | Max speed & tuning | OpenAI-compatible | Vulkan (RADV) build is currently the fastest path on `gfx1151`. |
| LM Studio | GUI + one-click server | OpenAI-compatible | Nice for exploring; less ideal as a headless daemon. |

**My suggested path:** start with **Ollama** (up and serving in 15 minutes), then add
**llama.cpp Vulkan** or **Lemonade** once you want more speed or NPU-assisted prefill.

Community benchmarks on this exact chip: **RADV Vulkan generally beats ROCm HIP** on `gfx1151`
for token generation, and is much easier to install (just Mesa drivers). ROCm is worth it mainly
for specific kernels/tooling that require it.

---

## 3. Critical prerequisite: give the iGPU its memory

Out of the box, firmware hands only ~16–32 GB to the iGPU. To load big models you must raise that.

1. **BIOS/UEFI:** set **UMA Frame Buffer Size** (a.k.a. VRAM / GART) as high as it allows —
   often 64–96 GB. Some vendors label it "Dedicated VRAM" or hide it under an "Advanced" menu.
2. **Linux extra headroom (GTT):** the amdgpu driver can lend *system* RAM to the GPU on top of
   the BIOS reservation via GTT. Kernel params like:
   ```
   amdgpu.gttsize=98304    # ~96 GB in MiB
   ttm.pages_limit=...      # match, in 4K pages
   ```
   let you reach ~110 GB GPU-visible on a 128 GB box while leaving RAM for the OS.
3. **ROCm gotcha:** if a tool refuses to see `gfx1151`, export
   `HSA_OVERRIDE_GFX_VERSION=11.5.1` so ROCm treats it as a supported target.

Rule of thumb for a 128 GB box: reserve ~16–24 GB for the OS, give the rest to the GPU.

---

## 4. Quickstart — Ollama serving on the LAN

On the Strix Halo machine:

```bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Expose to the LAN (default binds to localhost only)
#   Linux service: add to the systemd unit or /etc/systemd/system/ollama.service.d/override.conf
#   Environment="OLLAMA_HOST=0.0.0.0:11434"
#   Environment="OLLAMA_KEEP_ALIVE=30m"        # keep model warm between requests
#   Environment="OLLAMA_MAX_LOADED_MODELS=2"

sudo systemctl restart ollama

# Pull a model that fits and flies on this hardware
ollama pull qwen3:30b            # dense-ish coder, ~100 t/s reported on gfx1151 Vulkan
ollama pull gpt-oss:120b         # MoE, ~50 t/s despite size — the capacity payoff
```

Test from **another** machine on the LAN:

```bash
curl http://STRIX-HOST:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen3:30b","messages":[{"role":"user","content":"ping"}]}'
```

If that returns text, you have a private OpenAI-compatible endpoint at
`http://STRIX-HOST:11434/v1`. Everything downstream just points at that URL.

---

## 5. Reach it securely from your other machines

You use several machines across macOS and Windows. Two options:

- **LAN only:** bind to `0.0.0.0`, then firewall the port to your subnet. Simple, but nothing
  outside the house can reach it.
- **Tailscale (recommended):** install Tailscale on the Strix box and every client. You get a
  stable private IP (e.g. `100.x.y.z`) that works from anywhere, encrypted, without opening any
  router ports. Then bind Ollama to the Tailscale IP and point every client at
  `http://strix.your-tailnet.ts.net:11434/v1`. This fits your multi-machine, dual-OS setup cleanly.

Add a bearer token / reverse proxy (Caddy or nginx) in front if you ever expose it more widely —
Ollama/llama.cpp have no auth of their own.

---

## 6. Wiring it into VS Code and your dev tools

All of these speak the OpenAI-compatible endpoint from §4.

### Continue.dev (best general local-model extension)
`~/.continue/config.json` (or the newer YAML):
```json
{
  "models": [{
    "title": "Strix qwen3-30b",
    "provider": "openai",
    "model": "qwen3:30b",
    "apiBase": "http://strix.your-tailnet.ts.net:11434/v1",
    "apiKey": "unused"
  }]
}
```
Gives you chat + autocomplete + edit, all local.

### Cline (agentic coding in VS Code)
Settings → API Provider → **OpenAI Compatible** (or **Ollama**) → Base URL = your endpoint.
Good for local agentic edits when you don't want to spend cloud tokens.

### GitHub Copilot (BYOK)
Recent Copilot Chat supports local/Ollama models — add the endpoint under its model picker.
Useful if you already live in Copilot.

### Claude Code (this tool) — the interesting one
Claude Code talks the **Anthropic** API, not OpenAI, so it can't hit Ollama directly. Bridge it:

```bash
pip install "litellm[proxy]"
# litellm config maps an Anthropic-shaped route to your local OpenAI endpoint
litellm --config litellm.yaml --port 4000
```
`litellm.yaml`:
```yaml
model_list:
  - model_name: claude-3-5-sonnet-20241022   # a name Claude Code will send
    litellm_params:
      model: openai/qwen3:30b
      api_base: http://strix.your-tailnet.ts.net:11434/v1
      api_key: unused
```
Then run Claude Code against the proxy:
```bash
export ANTHROPIC_BASE_URL=http://localhost:4000
export ANTHROPIC_AUTH_TOKEN=anything
claude
```
**Reality check:** a local 30B won't match Opus 4.8 on hard agentic work — you'll feel the drop
on multi-file reasoning and tool use. Best uses for the local route: offline work, bulk/cheap
throwaway tasks, privacy-sensitive code, and burning zero cloud budget on low-stakes edits.
Keep cloud Claude for the heavy lifting; treat local as the daily-driver-when-it's-good-enough tier.
(You're on the Max flat-rate plan, so the motive here is offline/privacy, not saving tokens.)

### Anything else
Open WebUI (a nice browser chat front-end for the household), n8n, scripts using the `openai`
Python/JS SDK — all take a `base_url` override and Just Work against the same endpoint.

---

## 7. Model shortlist for 128 GB

Prioritize MoE for speed; keep a strong dense model around for quality.

| Model | Type | Why it fits this box |
|---|---|---|
| **gpt-oss-120B** | MoE (~5B active) | Big-model quality, ~50 t/s — the headline capability |
| **Qwen3-Coder 30B** | dense/coder | ~100 t/s on Vulkan; excellent daily coding driver |
| **Qwen3.5 35B-A3B** | MoE (3B active) | ~55 t/s, fast general assistant |
| **Llama 3.3 70B** | dense | Q4/Q5 fits; slower (~4–6 t/s) but strong reasoning when you can wait |
| Whisper / Kokoro / SD | multimodal | Lemonade bundles these — one box for STT/TTS/image too |

Quantization: **Q4_K_M** is the usual sweet spot (quality vs. footprint). Go Q5/Q6 for a favorite
model if it still fits and you want a little more fidelity.

---

## 8. Realistic performance expectations

- **Dense 70B, Q4:** ~4–6 tok/s. Usable for batch/async, not snappy interactive chat.
- **30B dense coder, Vulkan:** ~100 tok/s reported. Genuinely pleasant interactive coding.
- **100–120B MoE, Q4:** ~40–55 tok/s. The "how is this even running on one APU" moment.
- **Prompt processing (prefill):** the weak spot on long contexts — this is exactly what
  Lemonade offloads to the NPU to cut time-to-first-token on big prompts.

If interactive speed disappoints, in order: (1) confirm you're on the **Vulkan/RADV** backend,
(2) confirm the model is fully on the **iGPU** (not spilling to CPU), (3) drop to a **MoE** model,
(4) lower quantization, (5) shorten context window.

---

## 9. Suggested rollout

1. **Today:** Ollama on Linux, BIOS VRAM maxed, bind to Tailscale, pull `qwen3:30b`.
   Point Continue.dev at it from this VS Code. Confirm end-to-end.
2. **This week:** add `gpt-oss:120b`; feel the capacity advantage. Set `OLLAMA_KEEP_ALIVE` so
   the model stays warm.
3. **When you want more:** build **llama.cpp Vulkan** for top speed, or install **Lemonade** to
   pull the NPU into prefill and get the bundled Whisper/TTS/SD server for the household.
4. **Optional:** stand up the **LiteLLM** bridge so Claude Code can fall back to the local model
   for offline / low-stakes work.

---

## Sources

- [Strix Halo local LLM guide (Ollama, llama.cpp Vulkan/RADV, ROCm)](https://github.com/hogeheer499-commits/strix-halo-guide)
- [Ryzen AI Max+ 395 for Local LLMs in 2026 — 128 GB, 100 t/s on 30B](https://runaihome.com/blog/ryzen-ai-max-395-strix-halo-local-llm-2026/)
- [Framework Strix Halo LLM setup — BIOS, kernel, ROCm, llama.cpp](https://github.com/Gygeek/Framework-strix-halo-llm-setup)
- [AMD: run large LLMs on a Ryzen AI Max+ cluster](https://www.amd.com/en/developer/resources/technical-articles/2026/how-to-run-a-one-trillion-parameter-llm-locally-an-amd.html)
- [Lemonade SDK (GitHub)](https://github.com/lemonade-sdk/lemonade)
- [AMD: Ryzen AI and Radeon LLMs with Lemonade](https://www.amd.com/en/developer/resources/technical-articles/2025/ryzen-ai-radeon-llms-with-lemonade.html)
- [Lemonade local AI server — GPU + NPU inference guide (2026)](https://runaihome.com/blog/amd-lemonade-local-llm-server-npu-gpu-guide-2026/)
- [Strix Halo + Ollama performance guide](https://hyperion-consulting.io/en/insights/amd-strix-halo-llm-guide-ollama-lmstudio-llamacpp-ubuntu-24)
