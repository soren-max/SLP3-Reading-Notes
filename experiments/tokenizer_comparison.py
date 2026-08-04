"""Compare how tokenizers segment entity-heavy text.

Install once: pip install transformers sentencepiece torch
The token IDs are printed only to inspect each tokenizer's own vocabulary. They
must not be numerically compared across tokenizers.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from transformers import AutoTokenizer


TEXTS = [
    "西安邮电大学",
    "GraphReasoner-X2.5",
    "使用 BERT 完成命名实体识别",
    "Qwen3-32B",
    "ERR_CONNECTION_RESET",
    "Retrieval-Augmented Generation",
]


@dataclass(frozen=True)
class TokenizerSpec:
    name: str
    model_id: str


TOKENIZERS = [
    TokenizerSpec("BERT-base-Chinese", "bert-base-chinese"),
    TokenizerSpec("Qwen2.5", "Qwen/Qwen2.5-0.5B-Instruct"),
    TokenizerSpec("XLM-R", "xlm-roberta-base"),
]


def is_fragmented(tokens: list[str], text: str) -> str:
    """A transparent heuristic for a learning demo, not a tokenizer metric."""
    if len(tokens) >= 7 or (len(text) >= 6 and len(tokens) >= len(text) * 0.65):
        return "是"
    if len(tokens) >= 5:
        return "轻微"
    return "否"


def inspect(spec: TokenizerSpec) -> list[dict[str, object]]:
    tokenizer = AutoTokenizer.from_pretrained(spec.model_id, trust_remote_code=False)
    rows = []
    for text in TEXTS:
        encoded = tokenizer(text, add_special_tokens=False)
        token_ids = encoded["input_ids"]
        tokens = tokenizer.convert_ids_to_tokens(token_ids)
        rows.append(
            {
                "tokenizer": spec.name,
                "text": text,
                "tokens": tokens,
                "token_ids": token_ids,
                "token_count": len(tokens),
                "severely_fragmented": is_fragmented(tokens, text),
            }
        )
    return rows


def main() -> None:
    all_rows: list[dict[str, object]] = []
    for spec in TOKENIZERS:
        print(f"\n## {spec.name} ({spec.model_id})")
        rows = inspect(spec)
        all_rows.extend(rows)
        for row in rows:
            print(json.dumps(row, ensure_ascii=False))

    with open("tokenizer_comparison_results.json", "w", encoding="utf-8") as f:
        json.dump(all_rows, f, ensure_ascii=False, indent=2)

    print("\n结论：实体切得越碎，序列越长，实体信息分散到更多位置；NER 标签对齐和实体向量聚合都更困难，并会占用更多上下文预算。")


if __name__ == "__main__":
    main()
