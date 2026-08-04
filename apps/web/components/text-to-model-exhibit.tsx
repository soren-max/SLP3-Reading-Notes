"use client";

import { useState } from "react";
import { ArrowDown, ArrowRight, Braces, CheckCircle2, CircleAlert, Code2, Database, Layers3, ScanText, Search, Sparkles, Split, Waypoints } from "lucide-react";

const stages = [
  { title: "原始文本", sub: "Unicode 字符串", icon: ScanText, color: "bg-slate-900", example: "西安邮电大学发布了新成果" },
  { title: "Unicode / Normalization", sub: "规范化字符串", icon: Sparkles, color: "bg-violet-600", example: "统一字符形式、空格与大小写" },
  { title: "Tokenizer", sub: "Token / Subword", icon: Split, color: "bg-indigo-600", example: "[西安, 邮电, 大学, 发布, ...]" },
  { title: "ID Mapping", sub: "整数 ID 序列", icon: Database, color: "bg-cyan-600", example: "[6205, 6917, 1921, ...]" },
  { title: "Embedding Lookup", sub: "初始向量序列", icon: Braces, color: "bg-teal-600", example: "[0.12, −0.31, ...] × n" },
  { title: "Positional Information", sub: "带位置信息的向量", icon: Waypoints, color: "bg-emerald-600", example: "embedding + position" },
  { title: "Transformer Encoder", sub: "上下文融合", icon: Layers3, color: "bg-amber-500", example: "self-attention across tokens" },
  { title: "Contextual Representation", sub: "上下文化向量", icon: Code2, color: "bg-orange-500", example: "h₁, h₂, …, hₙ" },
];

const tokenizerRows = [
  { name: "BERT-base-Chinese", tone: "bg-indigo-50 text-indigo-700 border-indigo-200", data: [
    ["西安邮电大学", "西, 安, 邮, 电, 大, 学", 6, "是"], ["GraphReasoner-X2.5", "Graph, ##Reason, ##er, -, X, ##2, ., 5", 8, "是"], ["使用 BERT 完成命名实体识别", "使, 用, bert, 完, 成, 命, 名, 实, 体, 识, 别", 11, "是"],
  ] },
  { name: "Qwen2.5", tone: "bg-cyan-50 text-cyan-700 border-cyan-200", data: [
    ["西安邮电大学", "西安, 邮电, 大学", 3, "否"], ["GraphReasoner-X2.5", "Graph, Reasoner, -, X, 2, ., 5", 7, "轻微"], ["使用 BERT 完成命名实体识别", "使用, BERT, 完成, 命名, 实体, 识别", 6, "否"],
  ] },
  { name: "XLM-R", tone: "bg-emerald-50 text-emerald-700 border-emerald-200", data: [
    ["西安邮电大学", "▁西安, 邮电, 大学", 3, "否"], ["GraphReasoner-X2.5", "▁Graph, Reason, er, -, X, 2, ., 5", 8, "是"], ["使用 BERT 完成命名实体识别", "▁使用, ▁BERT, ▁完成, 命名, 实体, 识别", 6, "否"],
  ] },
];

const wordSenses = [
  { sentence: "苹果发布了新产品。", sense: "科技公司", vector: [0.86, 0.70, 0.29] },
  { sentence: "我吃了一个苹果。", sense: "水果", vector: [0.26, 0.76, 0.88] },
  { sentence: "苹果公司的总部在哪里？", sense: "科技公司", vector: [0.90, 0.68, 0.25] },
];

const defaultInspectorText = "GraphReasoner-X2.5 使用了什么数据集？";

function inspectText(text: string) {
  const entity = "GraphReasoner-X2.5";
  const entityStart = text.indexOf(entity);
  const entityTokens = entityStart >= 0 ? ["Graph", "Reason", "##er", "-", "X", "##2", ".", "5"] : [];
  const suffix = text.slice(Math.max(0, entityStart + entity.length)).match(/[\u4e00-\u9fff]+|\S/g) ?? [];
  const tokens = [...entityTokens, ...suffix];
  const offsets = entityTokens.length
    ? [[0, 5], [5, 11], [11, 13], [13, 14], [14, 15], [15, 17], [17, 18], [18, 19]].map(([start, end]) => [start + entityStart, end + entityStart])
    : [];
  let cursor = entityStart >= 0 ? entityStart + entity.length : 0;
  suffix.forEach((token) => {
    const start = text.indexOf(token, cursor);
    offsets.push([start, start + token.length]);
    cursor = start + token.length;
  });
  return {
    normalized_text: text.trim().replace(/\s+/g, " "),
    tokens,
    token_ids: tokens.map((_, index) => 1001 + index * 137),
    offset_mapping: offsets,
    token_count: tokens.length,
    detected_mentions: entityStart >= 0 ? [{ text: entity, type: "MODEL", start_char: entityStart, end_char: entityStart + entity.length, start_token: 0, end_token: 7 }] : [],
    entity_candidates: entityStart >= 0 ? [
      { entity: "kg:GraphReasoner-X2.5", score: 0.94, reason: "exact alias + MODEL type" },
      { entity: "kg:GraphReasoner", score: 0.61, reason: "partial string match" },
      { entity: "kg:GraphReasoner-X1", score: 0.35, reason: "name-neighbor" },
    ] : [],
  };
}

export function TextToModelExhibit() {
  const [activeTokenizer, setActiveTokenizer] = useState(0);
  const [activeSense, setActiveSense] = useState(0);
  const [inspectorText, setInspectorText] = useState(defaultInspectorText);
  const active = tokenizerRows[activeTokenizer];
  const inspection = inspectText(inspectorText);

  return <div className="space-y-8 pb-10">
    <section className="relative overflow-hidden rounded-2xl border border-indigo-200 bg-gradient-to-br from-indigo-950 via-violet-900 to-slate-950 px-6 py-10 text-white shadow-xl sm:px-10">
      <div className="absolute -right-16 -top-24 h-72 w-72 rounded-full bg-cyan-400/20 blur-3xl" />
      <div className="relative max-w-4xl space-y-5">
        <p className="text-sm font-medium tracking-[0.18em] text-cyan-200">SLP3 · LEARNING EXHIBIT 01</p>
        <h2 className="text-4xl font-semibold tracking-tight sm:text-6xl">文本，如何成为<br /><span className="text-cyan-300">模型能够理解的表示？</span></h2>
        <p className="max-w-2xl text-base leading-7 text-indigo-100 sm:text-lg">从离散符号到上下文向量：用一条完整的处理链，连接 Tokenizer、Embedding、Transformer 与下游任务。</p>
        <div className="flex flex-wrap gap-2 pt-2 text-sm"><span className="rounded-full bg-white/10 px-3 py-1.5">1 份总结</span><span className="rounded-full bg-white/10 px-3 py-1.5">2 个实验</span><span className="rounded-full bg-white/10 px-3 py-1.5">1 个误差分析</span><span className="rounded-full bg-white/10 px-3 py-1.5">1 次口头讲解</span></div>
      </div>
    </section>

    <section className="space-y-4" aria-labelledby="pipeline-title">
      <div><p className="text-sm font-medium text-primary">01 / 完整流程图</p><h3 id="pipeline-title" className="text-2xl font-semibold">文本 → 模型接口 → 下游任务</h3></div>
      <div className="overflow-x-auto rounded-2xl border bg-card p-5 shadow-sm"><div className="flex min-w-[1050px] items-center gap-2">
        {stages.map((stage, i) => { const Icon = stage.icon; return <div className="contents" key={stage.title}><div className="w-28 shrink-0 text-center"><div className={`mx-auto flex h-12 w-12 items-center justify-center rounded-xl ${stage.color} text-white shadow-lg`}><Icon className="h-5 w-5" /></div><p className="mt-2 text-xs font-semibold">{stage.title}</p><p className="mt-1 text-[11px] text-muted-foreground">{stage.sub}</p></div>{i < stages.length - 1 && <ArrowRight className="h-4 w-4 shrink-0 text-muted-foreground" />}</div>; })}
        <ArrowRight className="h-4 w-4 shrink-0 text-muted-foreground" /><div className="w-36 shrink-0 rounded-xl border border-amber-200 bg-amber-50 p-3 text-center"><p className="text-xs font-semibold text-amber-900">Task Head</p><p className="mt-1 text-[11px] text-amber-800">NER · Linking · Retrieval · Classify</p></div>
      </div></div>
      <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-5">{[
        ["Tokenizer", "原始字符串", "token 序列", "决定模型处理单位"], ["ID Mapping", "token", "整数 ID", "在词表中定位 token"], ["Embedding", "token ID", "初始向量", "将离散符号变为连续表示"], ["Transformer", "向量序列", "上下文向量", "融合左右或历史上下文"], ["Task Head", "上下文向量", "标签或分数", "完成 NER、检索、分类"],
      ].map(([name, input, output, role]) => <article key={name} className="rounded-xl border bg-card p-4"><p className="font-semibold">{name}</p><div className="mt-3 space-y-2 text-xs"><p><span className="text-muted-foreground">输入</span>　{input}</p><ArrowDown className="h-3 w-3 text-muted-foreground" /><p><span className="text-muted-foreground">输出</span>　{output}</p><p className="border-t pt-2 text-muted-foreground">{role}</p></div></article>)}</div>
    </section>

    <section className="grid gap-5 lg:grid-cols-[1.25fr_.75fr]">
      <div className="rounded-2xl border bg-card p-6 shadow-sm"><p className="text-sm font-medium text-primary">02 / Tokenizer 对比实验</p><h3 className="mt-1 text-2xl font-semibold">同一段文本，不同的切分边界</h3><div className="mt-5 flex flex-wrap gap-2">{tokenizerRows.map((item, index) => <button key={item.name} onClick={() => setActiveTokenizer(index)} className={`rounded-full border px-3 py-1.5 text-sm font-medium transition ${activeTokenizer === index ? item.tone : "bg-background text-muted-foreground hover:bg-muted"}`}>{item.name}</button>)}</div><div className="mt-5 overflow-x-auto"><table className="w-full min-w-[620px] text-left text-sm"><thead className="border-b text-xs text-muted-foreground"><tr><th className="pb-3 font-medium">文本</th><th className="pb-3 font-medium">Tokens</th><th className="pb-3 font-medium">数量</th><th className="pb-3 font-medium">严重碎片化</th></tr></thead><tbody>{active.data.map(([text, tokens, count, fragmented]) => <tr key={String(text)} className="border-b last:border-0"><td className="py-3 font-medium">{text}</td><td className="max-w-72 py-3 font-mono text-xs text-muted-foreground">{tokens}</td><td className="py-3">{count}</td><td className="py-3"><span className={fragmented === "否" ? "text-emerald-600" : "text-amber-600"}>{fragmented}</span></td></tr>)}</tbody></table></div></div>
      <aside className="rounded-2xl border border-cyan-200 bg-cyan-50/70 p-6"><CircleAlert className="h-5 w-5 text-cyan-700" /><h4 className="mt-3 text-lg font-semibold text-cyan-950">读实验时，别比较 ID 大小</h4><p className="mt-2 text-sm leading-6 text-cyan-900">Token ID 只是各自词表里的索引；不同 tokenizer 的 1001 与 1001 没有可比性。</p><div className="mt-4 rounded-lg border border-cyan-200 bg-white/70 p-3 font-mono text-xs text-slate-700">{`{\n  "text": "GraphReasoner-X2.5",\n  "tokens": ["Graph", "Reason", "##er", ...],\n  "token_ids": [1001, 1002, 1003, ...],\n  "token_count": 8\n}`}</div></aside>
    </section>

    <section className="rounded-2xl border border-violet-200 bg-gradient-to-r from-violet-50 to-indigo-50 p-6"><p className="text-sm font-medium text-violet-700">误差分析链条</p><div className="mt-4 flex flex-wrap items-center gap-x-3 gap-y-2 text-sm font-medium text-violet-950"><span>实体切得越碎</span><ArrowRight className="h-4 w-4" /><span>序列越长</span><ArrowRight className="h-4 w-4" /><span>信息分散到更多位置</span><ArrowRight className="h-4 w-4" /><span>NER 标签对齐更复杂</span><ArrowRight className="h-4 w-4" /><span>实体聚合更困难</span><ArrowRight className="h-4 w-4" /><span>上下文预算增加</span></div></section>

    <section className="grid gap-5 lg:grid-cols-2">
      <div className="rounded-2xl border bg-card p-6 shadow-sm"><p className="text-sm font-medium text-primary">03 / Embedding 相似度实验</p><h3 className="mt-1 text-2xl font-semibold">相似语义，不等于同一实体</h3><div className="mt-5 overflow-hidden rounded-xl border"><table className="w-full text-left text-sm"><thead className="bg-muted/50 text-xs text-muted-foreground"><tr><th className="p-3">文本对</th><th className="p-3">Cosine</th><th className="p-3">语义相关</th><th className="p-3">同一实体</th></tr></thead><tbody><tr className="border-t"><td className="p-3">减少幻觉 / 避免编造事实</td><td className="p-3 font-mono">0.82</td><td className="p-3 text-emerald-600">是</td><td className="p-3 text-muted-foreground">不涉及</td></tr><tr className="border-t"><td className="p-3">苹果公司 / 微软公司</td><td className="p-3 font-mono">0.71</td><td className="p-3 text-emerald-600">是</td><td className="p-3 text-rose-600">否</td></tr><tr className="border-t"><td className="p-3">发布手机 / 吃苹果</td><td className="p-3 font-mono">0.23</td><td className="p-3 text-amber-600">部分</td><td className="p-3 text-rose-600">否</td></tr></tbody></table></div><p className="mt-4 text-sm leading-6 text-muted-foreground">句向量的数值会随模型改变；这里展示的是实验应观察到的关系，而不是可跨模型复用的绝对阈值。</p></div>
      <div className="rounded-2xl border bg-slate-950 p-6 text-white shadow-sm"><p className="text-sm font-medium text-cyan-300">上下文消歧 · “苹果”</p><div className="mt-4 flex gap-2">{wordSenses.map((item, index) => <button key={item.sense + index} onClick={() => setActiveSense(index)} className={`rounded-lg px-3 py-2 text-left text-xs transition ${activeSense === index ? "bg-cyan-400 text-slate-950" : "bg-white/10 text-slate-200"}`}>案例 {index + 1}</button>)}</div><blockquote className="mt-6 border-l-2 border-cyan-300 pl-4 text-lg">“{wordSenses[activeSense].sentence}”</blockquote><div className="mt-6 grid grid-cols-3 gap-3">{wordSenses[activeSense].vector.map((v, i) => <div key={i}><div className="flex h-20 items-end rounded bg-white/10 p-1"><div className="w-full rounded bg-cyan-300" style={{ height: `${v * 100}%` }} /></div><p className="mt-2 text-center font-mono text-xs text-cyan-200">d{i + 1}</p></div>)}</div><p className="mt-5 text-sm text-slate-300">当前表示更接近：<strong className="text-white">{wordSenses[activeSense].sense}</strong>。Tokenizer 可以相似，但 Transformer 会用周围的词重写“苹果”的向量。</p></div>
    </section>

    <section className="rounded-2xl border bg-card p-6 shadow-sm"><p className="text-sm font-medium text-primary">04 / NER 的 Subword 对齐</p><div className="mt-2 flex flex-wrap items-end justify-between gap-3"><h3 className="text-2xl font-semibold">一个实体，被拆成八个预测位置</h3><span className="rounded-full bg-indigo-50 px-3 py-1 text-sm font-medium text-indigo-700">GraphReasoner-X2.5 → MODEL</span></div><div className="mt-6 grid gap-5 lg:grid-cols-[1fr_.9fr]"><div className="overflow-hidden rounded-xl border"><div className="grid grid-cols-[1fr_auto] bg-muted/60 px-4 py-2 text-xs text-muted-foreground"><span>Subword</span><span>BIO 标签</span></div>{[["Graph", "B-MODEL"], ["Reason", "I-MODEL"], ["##er", "I-MODEL"], ["-", "I-MODEL"], ["X", "I-MODEL"], ["##2", "I-MODEL"], [".", "I-MODEL"], ["5", "I-MODEL"]].map(([token, label]) => <div key={token} className="grid grid-cols-[1fr_auto] border-t px-4 py-2 font-mono text-sm"><span>{token}</span><span className="text-indigo-600">{label}</span></div>)}</div><div className="space-y-3"><div className="rounded-xl border border-indigo-200 bg-indigo-50 p-4"><p className="font-semibold text-indigo-950">策略一：标签复制</p><p className="mt-1 text-sm leading-6 text-indigo-900">把词级标签扩展到全部 subword。实现直接，但长实体会在 loss 中获得更多权重。</p></div><div className="rounded-xl border border-emerald-200 bg-emerald-50 p-4"><p className="font-semibold text-emerald-950">策略二：只训练首个 subword</p><p className="mt-1 text-sm leading-6 text-emerald-900">Graph 训练为 B-MODEL，其余设为 IGNORE。loss 更稳定；预测后仍须用 offset 恢复完整实体。</p></div><div className="rounded-xl bg-slate-950 p-4 font-mono text-xs leading-5 text-cyan-200">{`{\n  "entity_text": "GraphReasoner-X2.5",\n  "start_char": 0, "end_char": 19,\n  "start_token": 0, "end_token": 7\n}`}</div></div></div></section>

    <section className="rounded-2xl border border-rose-200 bg-gradient-to-br from-rose-50 via-white to-amber-50 p-6 shadow-sm"><p className="text-sm font-medium text-rose-700">05 / 端到端误差传播</p><h3 className="mt-1 text-2xl font-semibold">一次 Tokenization 错误，如何让 KG-RAG 答错？</h3><p className="mt-2 text-sm text-muted-foreground">用户问题：<span className="font-medium text-foreground">GraphReasoner-X2.5 使用了什么数据集？</span></p><div className="mt-6 grid gap-3 lg:grid-cols-6">{[
      ["1", "Tokenizer", "GraphReasoner-X2.5 被切为 8 个碎片", "边界线索分散"],
      ["2", "NER", "只识别出 GraphReasoner", "版本号 X2.5 丢失"],
      ["3", "Entity Linking", "召回 kg:GraphReasoner", "错误模型节点"],
      ["4", "KG Retrieval", "沿相似模型节点展开", "走入错误关系"],
      ["5", "Evidence", "取到错误数据集三元组", "证据已污染"],
      ["6", "LLM Answer", "根据错误路径生成流畅回答", "流畅 ≠ 正确"],
    ].map(([index, title, detail, impact], i) => <div key={title} className="relative rounded-xl border border-rose-100 bg-white p-4 shadow-sm"><span className="flex h-6 w-6 items-center justify-center rounded-full bg-rose-600 text-xs font-bold text-white">{index}</span><p className="mt-3 text-sm font-semibold">{title}</p><p className="mt-1 text-xs leading-5 text-muted-foreground">{detail}</p><p className="mt-3 border-t pt-2 text-xs font-medium text-rose-700">{impact}</p>{i < 5 && <ArrowRight className="absolute -right-5 top-1/2 z-10 hidden h-4 w-4 -translate-y-1/2 text-rose-300 lg:block" />}</div>)}</div><div className="mt-5 rounded-xl border border-emerald-200 bg-emerald-50 p-4"><p className="font-semibold text-emerald-950">修复不是只换一个 tokenizer，而是逐层建立防线</p><div className="mt-3 flex flex-wrap gap-2 text-sm">{["Tokenizer offset 对齐", "领域实体词典", "Alias Matching", "Character-level Candidate Recall", "Entity Type Filtering", "KG Coherence Verification"].map((item) => <span key={item} className="rounded-full border border-emerald-200 bg-white px-3 py-1.5 text-emerald-800">{item}</span>)}</div></div></section>

    <section className="rounded-2xl border bg-slate-950 p-6 text-white shadow-sm"><div className="flex items-center gap-3"><Search className="h-5 w-5 text-cyan-300" /><div><p className="text-sm font-medium text-cyan-300">06 / Text Representation Inspector</p><h3 className="text-2xl font-semibold">让 tokenizer 成为可观察、可调试的系统模块</h3></div></div><div className="mt-6 grid gap-5 lg:grid-cols-[.85fr_1.15fr]"><div><label htmlFor="inspector-text" className="text-sm font-medium text-slate-200">输入文本</label><textarea id="inspector-text" value={inspectorText} onChange={(event) => setInspectorText(event.target.value)} className="mt-2 min-h-28 w-full rounded-xl border border-slate-700 bg-slate-900 p-4 text-sm text-white outline-none ring-cyan-300 transition focus:ring-2" /><p className="mt-3 text-xs leading-5 text-slate-400">演示 tokenizer：针对 GraphReasoner-X2.5 展示 subword、offset 与候选实体。实际项目可替换为 Hugging Face tokenizer 与 NER / Entity Linking 服务。</p></div><div className="rounded-xl border border-slate-700 bg-slate-900/70 p-4"><p className="font-mono text-xs text-cyan-200">{`{ "normalized_text": "${inspection.normalized_text}", "token_count": ${inspection.token_count} }`}</p><div className="mt-4 flex flex-wrap gap-2">{inspection.tokens.map((token, index) => <span key={`${token}-${index}`} className={`rounded-md px-2 py-1 font-mono text-xs ${index < 8 && inspection.detected_mentions.length ? "bg-cyan-400 text-slate-950" : "bg-white/10 text-slate-200"}`}>{token}<small className="ml-1 opacity-60">#{inspection.token_ids[index]}</small></span>)}</div><div className="mt-4 grid gap-2 sm:grid-cols-2"><div className="rounded-lg bg-white/5 p-3"><p className="text-xs text-slate-400">实体 span</p>{inspection.detected_mentions.length ? <p className="mt-1 text-sm text-white">{inspection.detected_mentions[0].text} <span className="text-cyan-300">MODEL</span></p> : <p className="mt-1 text-sm text-slate-400">未检测到模型实体</p>}</div><div className="rounded-lg bg-white/5 p-3"><p className="text-xs text-slate-400">字符 / token offset</p><p className="mt-1 font-mono text-xs text-slate-200">{inspection.offset_mapping.map(([start, end]) => `[${start},${end})`).join(" ") || "—"}</p></div></div><div className="mt-3 rounded-lg bg-white/5 p-3"><p className="text-xs text-slate-400">实体链接候选 → 最终规范实体</p>{inspection.entity_candidates.map((candidate, index) => <div key={candidate.entity} className="mt-2 flex items-center justify-between gap-3 text-sm"><span className={index === 0 ? "text-cyan-300" : "text-slate-300"}>{index === 0 ? "✓ " : ""}{candidate.entity}</span><span className="font-mono text-xs text-slate-400">{candidate.score} · {candidate.reason}</span></div>)}</div></div></div></section>

    <section className="rounded-2xl border border-emerald-200 bg-emerald-50 p-6"><div className="flex gap-3"><CheckCircle2 className="mt-0.5 h-5 w-5 shrink-0 text-emerald-600" /><div><p className="text-sm font-medium text-emerald-700">07 / 3–5 分钟口头讲解</p><h3 className="mt-1 font-semibold text-emerald-950">一段可以脱稿讲清的总结</h3><p className="mt-3 text-sm leading-7 text-emerald-950">自然语言首先经过 tokenizer，被切分成 token 或 subword，并映射为 token ID。ID 只是词表中的整数索引，不能直接表示语义。模型通过 embedding matrix 把 ID 转成初始向量，再加入位置信息，送入 Transformer。Transformer 用 self-attention 融合上下文，得到 contextual representation。</p><p className="mt-3 text-sm leading-7 text-emerald-950">这些表示可以用于 NER、实体链接、语义检索和分类。但 tokenization 错误会向后传播：专业实体被过度切碎，会造成 NER 边界错误；实体链接到错误 KG 节点后，图检索和多跳路径也会出错。Embedding 只能表示语义接近，不能证明两个 mention 是同一实体。因此 KG-RAG 还需要实体类型、别名、知识图谱邻居和全局一致性约束。</p></div></div></section>
  </div>;
}
