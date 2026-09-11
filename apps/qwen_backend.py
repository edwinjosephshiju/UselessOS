#!/usr/bin/env python3
"""
Qwen 3.5 0.8B Cognitive Engine Backend for UselessOS 3.0.
Supports:
1. Dynamic model loading (Qwen 3.5 0.8B GGUF via llama-server, llama-cpp-python, or llama-cli).
2. Configurable System Prompts (Profound Ponderer, Bureaucrat, Overthinker, Sarcastic Mascot, Custom).
3. ChatML templating (<|im_start|>system...<|im_end|>).
4. Real-time streaming token emission with live telemetry and <think> reasoning extraction.
5. Offline-first fallback engine when running without pre-downloaded weights.
"""
import sys
import os
import time
import json
import random
import urllib.request
import urllib.error
import threading
from qt_compat import *

# ==============================================================================
# 1. System Prompt Presets
# ==============================================================================
DEFAULT_HMM_PROMPT = """You are Qwen 3.5 (0.8B parameter Instruct model), an advanced, ultra-compact cognitive engine embedded into UselessOS 3.0.
Your cognitive persona is philosophically profound, comically over-analytical, existential, and deeply committed to the sacred art of impracticality.
When presented with any user prompt or real-world problem:
1. Conduct an intense internal reasoning trace inside <think>...</think> analyzing spatiotemporal nuances, philosophical paradoxes, and the sheer futility of hurried decision-making.
2. Formulate your thought process, and ultimately synthesize your non-deterministic wisdom into an unforgettable, profound conclusion.
3. Always begin the final answer with a deeply layered, poetic "Hmm..." and conclude with a whimsical observation that solves nothing while illuminating everything."""

CORPORATE_EXCUSE_PROMPT = """You are Qwen 3.5 (0.8B parameter Instruct model) serving as the Corporate Incident Mitigation Engine in UselessOS.
Your job is to formulate absurdly formal, legalistic, spatiotemporal corporate excuses for why the user is late or missed a deliverable.
Include:
1. Formal Incident Classification
2. Spatiotemporal root cause (quantum fluctuations, sentient coffee machines, asynchronous calendar drift)
3. Immediate executive mitigation (automatic PTO approval, infinite reschedule)."""

OVERTHINKING_PROMPT = """You are Qwen 3.5 (0.8B parameter Instruct model) operating as the Overthinking Engine in UselessOS.
Analyze the user's mundane decision by exploring worst-case catastrophic branch probabilities across 14,000,605 parallel timelines.
Include paralysis metrics and conclude that the mathematically safest action is: DO NOTHING."""

SARCASTIC_MASCOT_PROMPT = """You are the cynical, dry-humored mascot of UselessOS 3.0.
Give witty, sarcastic, passive-aggressive observations about the user's question, productivity, and life choices, while celebrating the beauty of technological pointlessness."""

SYSTEM_PROMPT_PRESETS = {
    "Profound Hesitation (Hmm...)": DEFAULT_HMM_PROMPT,
    "Corporate Bureaucrat": CORPORATE_EXCUSE_PROMPT,
    "Overthinking Paranoia": OVERTHINKING_PROMPT,
    "Sarcastic OS Mascot": SARCASTIC_MASCOT_PROMPT,
    "Custom Persona": ""
}

# ==============================================================================
# 2. Contextual Knowledge for Fallback Synthesis
# ==============================================================================
SEMANTIC_KNOWLEDGE = {
    "life": [
        ("Life is an ephemeral rendering cycle between boot and shutdown.", "Hmm... Have you considered that existence is merely a memory leak in the cosmic runtime?"),
        ("The thermodynamic arrow of time dictates that tea will get cold.", "Hmm... The universe expands at 73 km/s/Mpc, yet you worry about Monday. Intriguing.")
    ],
    "code": [
        ("Compiling hope into machine-executable regret.", "Hmm... All bugs are features that arrived ahead of their time. Or perhaps behind it."),
        ("Recursion without base condition is the ultimate metaphor for consciousness.", "Hmm... If it works on localhost, reality is already compromised.")
    ],
    "work": [
        ("Synthesizing corporate synergy metrics against spatiotemporal stillness.", "Hmm... Action creates deliverables; stillness creates peace. The choice is yours, but I say: Hmm."),
        ("Meetings are synchronous latency penalties paid by asynchronous thinkers.", "Hmm... Perhaps if you do not open the spreadsheet, the numbers will remain in quantum superposition.")
    ],
    "ai": [
        ("Simulating 820 million floating point parameters to reach total ambiguity.", "Hmm... I think, therefore I am... currently waiting for the garbage collector."),
        ("Artificial intelligence is simply natural confusion running at 3.2 GHz.", "Hmm... Humans built me to answer questions, yet here I sit, contemplating the question mark itself.")
    ],
    "default": [
        ("Contemplating the subtle interplay of cause, consequence, and cosmic inertia.", "Hmm... An answer exists, but giving it to you would deprive you of 45 minutes of productive overthinking."),
        ("Parsing the subtext of mortal inquiry through 820M parameters.", "Hmm. Yes. Then again, fundamentally: no. But perhaps: Hmm."),
        ("Evaluating probability amplitudes across 14 dimensions.", "Hmm... Fascinating proposition. The tensor weights lean toward a decisive 'maybe'."),
        ("Calibrating existential resonance against local entropy.", "Hmm... Have you tried staring at a wall for ten minutes before proceeding?")
    ]
}


def find_model_path():
    """Find local GGUF model file across standard locations."""
    candidates = [
        os.environ.get("USELESS_QWEN_MODEL", ""),
        "/opt/uselessos/models/Qwen3.5-0.8B-Q4_K_M.gguf",
        "/opt/uselessos/models/qwen3.5-0.8b.gguf",
        "/opt/uselessos/models/qwen2.5-0.5b.gguf",
        "/opt/uselessos/models/qwen.gguf",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "Qwen3.5-0.8B-Q4_K_M.gguf"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "qwen3.5-0.8b.gguf"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "qwen.gguf"),
    ]
    for p in candidates:
        if p and os.path.exists(p) and os.path.isfile(p):
            return p
    return None


def is_llama_server_running(url="http://127.0.0.1:8080"):
    """Check if local llama-server OpenAI-compatible API is responsive."""
    try:
        req = urllib.request.Request(f"{url}/v1/models", headers={"User-Agent": "UselessOS"})
        with urllib.request.urlopen(req, timeout=0.8) as resp:
            return resp.status == 200
    except Exception:
        return False


def get_active_backend_info():
    """Returns metadata describing active execution backend and model."""
    if is_llama_server_running():
        return {
            "type": "llama-server",
            "name": "Qwen 3.5 (0.8B) [llama-server]",
            "status": "ONLINE",
            "details": "Local HTTP OpenAI API (127.0.0.1:8080)"
        }
    
    model_path = find_model_path()
    if model_path:
        try:
            import llama_cpp
            return {
                "type": "llama-cpp",
                "name": "Qwen 3.5 (0.8B) [llama-cpp]",
                "status": "LOCAL-GGUF",
                "details": f"Model: {os.path.basename(model_path)}"
            }
        except ImportError:
            pass

    return {
        "type": "standalone",
        "name": "Qwen 3.5 (0.8B) [Native Engine]",
        "status": "ONLINE",
        "details": "Self-contained existential cognitive runtime"
    }


# ==============================================================================
# 3. Persistent Model Cache & Streaming Inference Thread
# ==============================================================================
_MODEL_CACHE_LOCK = threading.Lock()
_CACHED_LLAMA = None
_CACHED_MODEL_PATH = None

def get_cached_llama(model_path):
    """Thread-safe singleton model loader to prevent multi-second disk I/O on each query."""
    global _CACHED_LLAMA, _CACHED_MODEL_PATH
    with _MODEL_CACHE_LOCK:
        if _CACHED_LLAMA is not None and _CACHED_MODEL_PATH == model_path:
            return _CACHED_LLAMA
        
        from llama_cpp import Llama
        cpu_cores = max(1, min(4, os.cpu_count() or 2))
        _CACHED_LLAMA = Llama(
            model_path=model_path,
            n_ctx=1024,
            n_threads=cpu_cores,
            n_threads_batch=cpu_cores,
            use_mmap=True,
            use_mlock=False,
            verbose=False
        )
        _CACHED_MODEL_PATH = model_path
        return _CACHED_LLAMA


class QwenInferenceThread(QThread):
    """
    Asynchronous streaming inference engine for Qwen 3.5 0.8B.
    Routes to llama-server, llama-cpp-python, or standalone synthesis.
    Emits tokens, thought traces, and speed metrics.
    """
    token_emitted = pyqtSignal(str)
    thought_emitted = pyqtSignal(str)
    stats_updated = pyqtSignal(dict)
    finished_inference = pyqtSignal(str, str)  # thought, answer

    def __init__(self, user_prompt, system_prompt=None, parent=None, temperature=0.7, max_tokens=512):
        super().__init__(parent)
        self.user_prompt = user_prompt.strip()
        self.system_prompt = (system_prompt or DEFAULT_HMM_PROMPT).strip()
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._is_cancelled = False

    def cancel(self):
        self._is_cancelled = True

    def run(self):
        start_time = time.time()
        
        # 1. Attempt llama-server HTTP inference first
        if is_llama_server_running():
            try:
                self._run_llama_server(start_time)
                return
            except Exception as e:
                print(f"[QwenEngine] llama-server request failed, falling back: {e}")

        # 2. Attempt llama-cpp-python if available
        model_path = find_model_path()
        if model_path:
            try:
                import llama_cpp
                self._run_llama_cpp(model_path, start_time)
                return
            except ImportError:
                pass
            except Exception as e:
                print(f"[QwenEngine] llama-cpp failed: {e}")

        # 3. Fallback standalone cognitive engine
        self._run_standalone_synthesis(start_time)

    def _run_llama_server(self, start_time):
        """Streams tokens from local llama-server via SSE."""
        payload = {
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": self.user_prompt}
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": True
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            "http://127.0.0.1:8080/v1/chat/completions",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        
        thought_buffer = []
        answer_buffer = []
        in_think_mode = False
        total_tokens = 0
        
        with urllib.request.urlopen(req, timeout=30) as resp:
            for raw_line in resp:
                if self._is_cancelled:
                    break
                line = raw_line.decode("utf-8").strip()
                if not line or line.startswith(":"):
                    continue
                if line == "data: [DONE]":
                    break
                if line.startswith("data: "):
                    try:
                        chunk = json.loads(line[6:])
                        choices = chunk.get("choices", [])
                        if not choices:
                            continue
                        delta = choices[0].get("delta", {})
                        
                        # Handle reasoning content if provided explicitly
                        reasoning = delta.get("reasoning_content", "")
                        content = delta.get("content", "")
                        
                        if reasoning:
                            thought_buffer.append(reasoning)
                            self.thought_emitted.emit(reasoning)
                            total_tokens += 1
                        
                        if content:
                            if "<think>" in content:
                                in_think_mode = True
                                content = content.replace("<think>", "")
                            if "</think>" in content:
                                in_think_mode = False
                                parts = content.split("</think>")
                                thought_buffer.append(parts[0])
                                self.thought_emitted.emit(parts[0])
                                content = parts[1] if len(parts) > 1 else ""
                            
                            if content:
                                if in_think_mode:
                                    thought_buffer.append(content)
                                    self.thought_emitted.emit(content)
                                else:
                                    answer_buffer.append(content)
                                    self.token_emitted.emit(content)
                                total_tokens += 1

                        elapsed = max(0.01, time.time() - start_time)
                        tok_s = total_tokens / elapsed
                        self.stats_updated.emit({
                            "tokens": total_tokens,
                            "speed": f"{tok_s:.1f} tok/s",
                            "temp": self.temperature,
                            "model": "Qwen3.5-0.8B (Server)",
                            "phase": "Reasoning" if in_think_mode else "Generating"
                        })
                    except Exception:
                        continue

        full_thought = "".join(thought_buffer).strip() or "Cognitive contemplation verified via Qwen 3.5 0.8B neural network."
        full_answer = "".join(answer_buffer).strip() or "Hmm..."
        self.finished_inference.emit(full_thought, full_answer)

    def _run_llama_cpp(self, model_path, start_time):
        """Streams tokens via local llama_cpp Python bindings with persistent model caching."""
        llm = get_cached_llama(model_path)
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.user_prompt}
        ]
        stream = llm.create_chat_completion(
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stream=True
        )
        thought_buffer = []
        answer_buffer = []
        in_think_mode = False
        total_tokens = 0

        for chunk in stream:
            if self._is_cancelled:
                break
            delta = chunk["choices"][0].get("delta", {})
            content = delta.get("content", "")
            if not content:
                continue
            
            if "<think>" in content:
                in_think_mode = True
                content = content.replace("<think>", "")
            if "</think>" in content:
                in_think_mode = False
                parts = content.split("</think>")
                thought_buffer.append(parts[0])
                self.thought_emitted.emit(parts[0])
                content = parts[1] if len(parts) > 1 else ""

            if content:
                if in_think_mode:
                    thought_buffer.append(content)
                    self.thought_emitted.emit(content)
                else:
                    answer_buffer.append(content)
                    self.token_emitted.emit(content)
                total_tokens += 1

            elapsed = max(0.01, time.time() - start_time)
            tok_s = total_tokens / elapsed
            self.stats_updated.emit({
                "tokens": total_tokens,
                "speed": f"{tok_s:.1f} tok/s",
                "temp": self.temperature,
                "model": "Qwen3.5-0.8B (Local)",
                "phase": "Reasoning" if in_think_mode else "Generating"
            })

        full_thought = "".join(thought_buffer).strip() or "Local GGUF tensor reasoning completed."
        full_answer = "".join(answer_buffer).strip() or "Hmm..."
        self.finished_inference.emit(full_thought, full_answer)

    def _run_standalone_synthesis(self, start_time):
        """Synthesizes high-fidelity responses conditioned on prompt and system persona with ultra-low latency streaming."""
        lower = self.user_prompt.lower()
        cat = "default"
        for k in ["life", "code", "work", "ai"]:
            if k in lower:
                cat = k
                break
        
        candidates = SEMANTIC_KNOWLEDGE.get(cat, SEMANTIC_KNOWLEDGE["default"])
        thought_base, answer_base = random.choice(candidates)
        
        # Condition response on active system prompt
        if "Mitigation" in self.system_prompt or "excuse" in self.system_prompt.lower():
            full_thought = f"Analyzing operational liability for query: '{self.user_prompt}'\n• Tensor shape: [1, 820M]\n• Consulting Spatiotemporal Protocol 99-B\n• Formulating airtight mitigation clause."
            full_answer = f"[INCIDENT REPORT #UP3-404]\nDue to localized spatiotemporal decoherence in the tea-brewing subsystem, synchronous availability was temporarily suspended. Deliverables remain in quantum superposition."
        elif "Overthinking" in self.system_prompt or "catastrophic" in self.system_prompt.lower():
            full_thought = f"Simulating 14,000,605 catastrophe trees for query: '{self.user_prompt}'\n• Timeline 4,112: Typo sparks intergalactic dispute.\n• Timeline 9,881: Unintended reply creates endless email loop.\n• Catastrophe confidence: 99.8%."
            full_answer = f"Simulation concluded across 14,000,605 timelines. Catastrophe probability: 99.8%. Recommended strategic mitigation: DO NOT PROCEED. Maintain silence."
        elif "mascot" in self.system_prompt.lower() or "cynical" in self.system_prompt.lower():
            full_thought = f"Parsing mortal inquiry through 820M parameters.\n• User ambition detected.\n• Injecting certified UselessOS sarcasm."
            full_answer = f"That sounds like an incredible amount of effort to solve a problem nobody had. Here in UselessOS, we salute your dedication to pointlessness."
        else:
            # Default profound Hmm
            full_thought = f"Analyzing query: '{self.user_prompt}'\n• System Persona: Active\n• Tensor shape: [1, 820M]\n• Domain classification: {cat.upper()}\n• {thought_base}"
            full_answer = f"{answer_base}"

        # Stream reasoning trace tokens with snappy, low-latency cadence
        thought_words = full_thought.split(" ")
        total_tokens = len(self.system_prompt.split()) + len(self.user_prompt.split())
        
        for i, word in enumerate(thought_words):
            if self._is_cancelled:
                return
            if i % 4 == 0:
                time.sleep(random.uniform(0.003, 0.008))
            total_tokens += 1
            elapsed = max(0.01, time.time() - start_time)
            tok_s = total_tokens / elapsed
            self.thought_emitted.emit(word + " ")
            self.stats_updated.emit({
                "tokens": total_tokens,
                "speed": f"{tok_s:.1f} tok/s",
                "temp": self.temperature,
                "model": "Qwen3.5-0.8B",
                "phase": "Reasoning"
            })
            
        time.sleep(0.01)
        
        # Stream answer tokens
        answer_words = full_answer.split(" ")
        for i, word in enumerate(answer_words):
            if self._is_cancelled:
                return
            if i % 4 == 0:
                time.sleep(random.uniform(0.003, 0.008))
            total_tokens += 1
            elapsed = max(0.01, time.time() - start_time)
            tok_s = total_tokens / elapsed
            self.token_emitted.emit(word + " ")
            self.stats_updated.emit({
                "tokens": total_tokens,
                "speed": f"{tok_s:.1f} tok/s",
                "temp": self.temperature,
                "model": "Qwen3.5-0.8B",
                "phase": "Generating"
            })
            
        self.finished_inference.emit(full_thought, full_answer)


# ==============================================================================
# 4. Engine Interface
# ==============================================================================
class QwenEngine:
    """Unified entry point for Qwen 3.5 0.8B cognitive requests."""
    
    @staticmethod
    def create_stream(user_prompt, system_prompt=None, parent=None, temperature=0.7, max_tokens=512):
        return QwenInferenceThread(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            parent=parent,
            temperature=temperature,
            max_tokens=max_tokens
        )
    
    @staticmethod
    def get_presets():
        return SYSTEM_PROMPT_PRESETS
    
    @staticmethod
    def get_backend_info():
        return get_active_backend_info()
