"""Semantic similarity and entity-identity counterexamples.

Install once: pip install sentence-transformers torch
The exact scores vary with the embedding model and version; inspect the ranking
and the semantic-vs-identity distinction rather than a fixed threshold.
"""

from __future__ import annotations

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

PAIRS = [
    ("如何减少大模型幻觉？", "怎样避免语言模型编造事实？", "是", "不涉及"),
    ("如何减少大模型幻觉？", "西安今天气温很高。", "否", "不涉及"),
    ("苹果公司", "微软公司", "是", "否"),
    ("苹果发布了新款手机。", "我吃了一个苹果。", "部分相关", "否"),
]


def similarity(model: SentenceTransformer, left: str, right: str) -> float:
    vectors = model.encode([left, right], convert_to_tensor=True, normalize_embeddings=True)
    return float(cos_sim(vectors[0], vectors[1]))


def main() -> None:
    model = SentenceTransformer(MODEL_NAME)
    print("| 文本对 | Cosine Similarity | 是否语义相关 | 是否同一实体 |")
    print("|---|---:|---|---|")
    for left, right, semantic, same_entity in PAIRS:
        score = similarity(model, left, right)
        print(f"| {left} / {right} | {score:.3f} | {semantic} | {same_entity} |")

    print("\n观察：预期 sim(减少幻觉, 避免编造事实) > sim(减少幻觉, 西安气温)。")
    print("结论：Semantic Similarity ≠ Entity Identity。苹果公司和微软公司可以在语义空间接近，因为二者都是科技公司；这不能证明它们链接到同一知识库实体。")


if __name__ == "__main__":
    main()
