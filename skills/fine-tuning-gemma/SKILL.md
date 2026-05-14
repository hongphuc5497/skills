---
name: fine-tuning-gemma
description: "Fine-tune Gemma models via Unsloth on macOS — dataset prep, training, evaluation. Currently configured for Gemma 4 E4B 4-bit on M2 Pro 32GB GPU."
license: MIT
metadata:
  version: 1.0.0
  category: tailored
  author: hongphuc5497
---

# Fine-Tuning Gemma Models

Fine-tune Gemma models with Unsloth on Apple Silicon.

## When to Use

Use when the user wants to fine-tune, train, or evaluate a Gemma model. Trigger on phrases like "fine-tune", "train a model", "run training", "check training results".

## Environment

- **Hardware**: M2 Pro 32GB (Metal GPU)
- **Stack**: Unsloth via `unsloth` package
- **Python**: 3.11.6 (via pyenv)
- **Dataset**: Wiki-based QMD semantic search, ~294 examples
- **Env var**: `AGX_RELAX_CDM_CTXSTORE_TIMEOUT=1` (Metal performance fix)

## Current Configuration

```
Model: Gemma 4 E4B 4-bit
Adapter: adapters/gemma-4-wiki/0000100 (best val loss: 2.744)
Training: 294 examples, ~12 min/run on GPU
Eval: 46-example benchmark, 96% clean
```

## Instructions

### Dataset Prep

1. Source data from Obsidian wiki at `~/Documents/knowledge-base-wiki/`
2. Use QMD files with semantic search (lex+vec, threshold 0.88-0.93)
3. RAG pipeline at `_fine-tuning/rag_pipeline.py` handles score fallback at 0.7

### Training

1. Set env: `export AGX_RELAX_CDM_CTXSTORE_TIMEOUT=1`
2. Activate pyenv: `pyenv local 3.11.6` or `pyenv shell 3.11.6`
3. Run training script
4. Check adapters directory for checkpoints
5. Evaluate on benchmark (46 examples)

### Evaluation

- Best val loss < 3.0 is good target
- Best checkpoint is the one with lowest val loss (not necessarily latest)
- Evaluate against the 46-example benchmark

## References

- Unsloth docs for macOS MPS support
- Wiki RAG pipeline: `_fine-tuning/rag_pipeline.py`
