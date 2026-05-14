---
name: wiki-rag-pipeline
description: "RAG pipeline for Obsidian wiki — QMD semantic search, score fallback context assembly. Supports wiki queries and knowledge distillation (LLM Wiki pattern)."
license: MIT
metadata:
  version: 1.0.0
  author: hongphuc5497
---

# Wiki RAG Pipeline

RAG pipeline for the Obsidian knowledge-base wiki.

## When to Use

Use when querying, searching, or ingesting content into the Obsidian wiki. Trigger on phrases like "search the wiki", "query the knowledge base", "RAG", "ingest into wiki", "find in wiki".

## Project Location

```bash
~/Documents/knowledge-base-wiki/
```

## Architecture

- **Source**: QMD (Obsidian) files with YAML frontmatter
- **Search**: Semantic search with lex+vec hybrid, threshold 0.88-0.93
- **Fallback**: Score-based at 0.7 threshold
- **Pipeline**: `_fine-tuning/rag_pipeline.py`
- **Pattern**: LLM Wiki — distill knowledge into interlinked markdown

## Instructions

### Querying the Wiki

1. Use semantic search with appropriate threshold
2. Start at 0.88 threshold, fall back to 0.7 if no results
3. Lexical + vector hybrid gives best results
4. Rerank top-5 results by relevance

### Ingesting Content

1. Place QMD files in appropriate directory
2. Ensure YAML frontmatter with tags
3. Run rebuild: `cd ~/Documents/knowledge-base-wiki && ...`
4. Verify with a sample query

### Pipeline Components

- `_fine-tuning/rag_pipeline.py` — Main RAG pipeline with score fallback
- Semantic search params: lex+vec, threshold configurable

## Conventions

- Tags follow the tag taxonomy (see tag-taxonomy skill)
- Notes follow LLM Wiki pattern
- Each note has YAML frontmatter with title, tags, date
