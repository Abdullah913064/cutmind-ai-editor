export type SceneKind = 'chapter'|'intuition'|'rule'|'steps'|'compare'|'practice';
export type VisualKey =
  | 'chapter' | 'concept' | 'rule' | 'steps' | 'compare' | 'practice' | 'answer' | 'countdown'
  | 'box' | 'three-boxes' | 'tickets' | 'bat' | 'variable' | 'divide'
  | 'jerseys' | 'expression-parts' | 'bill' | 'taxi' | 'shirts' | 'delivery' | 'rate'
  | 'fruit' | 'fruit-mixed' | 'like-terms' | 'combine' | 'scale' | 'balance-operation' | 'inverse'
  | 'teams' | 'brackets' | 'distribute' | 'fraction' | 'words-to-math' | 'money' | 'fees'
  | 'cost-graph' | 'graph' | 'graph-labels' | 'cricket' | 'shop' | 'workflow'
  | 'equation' | 'example' | 'questions' | 'check' | 'mistake';

export type SegmentSpec = {
  start: number;
  end: number;
  text: string;
  tts?: string;
  visual: VisualKey;
  silent?: boolean;
};

export type SceneSpec = {
  id: number;
  module: number;
  kind: SceneKind;
  title: string;
  label: string;
  concept: string;
  analogy: string;
  rule: string;
  example: string;
  steps: string[];
  example2: string;
  mistake: string;
  practice: string;
  answer: string;
  start: number;
  duration: number;
  audio: string;
  segments: SegmentSpec[];
};
