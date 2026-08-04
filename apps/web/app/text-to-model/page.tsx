import type { Metadata } from "next";

import { TextToModelExhibit } from "@/components/text-to-model-exhibit";

export const metadata: Metadata = {
  title: "文本—模型接口 | SLP3 Reading Notes",
  description: "Tokenizer、Embedding、Transformer 与 NER 对齐的交互式学习展出。",
};

export default function TextToModelPage() {
  return <TextToModelExhibit />;
}
