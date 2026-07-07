def get_roadmap() -> list[dict]:
    return [
        {
            "phase": "阶段一：LLM 基础",
            "goal": "建立大语言模型基础概念和训练范式的阅读框架。",
            "steps": ["Tokenization", "Embedding", "Neural Networks", "LLM", "Transformer", "Post-training"],
        },
        {
            "phase": "阶段二：RAG 与检索增强",
            "goal": "从检索模型进入 RAG、KG-RAG 和 GraphRAG 的证据组织问题。",
            "steps": ["Retrieval-based Models", "Dense Retrieval", "RAG", "KG-RAG", "GraphRAG"],
        },
        {
            "phase": "阶段三：知识图谱构建",
            "goal": "掌握从文本抽取实体、关系、事件和指代链的关键模块。",
            "steps": ["NER", "Relation Extraction", "Event Extraction", "Semantic Role Labeling", "Coreference Resolution", "Entity Linking"],
        },
        {
            "phase": "阶段四：大模型推理实践",
            "goal": "把问题理解、子图检索、证据路径和 LLM 推理串成实验流程。",
            "steps": ["Question", "Entity Recognition", "Subgraph Retrieval", "Evidence Path Construction", "LLM Reasoning", "Answer with Evidence"],
        },
    ]
