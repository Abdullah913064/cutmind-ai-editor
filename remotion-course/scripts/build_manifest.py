#!/usr/bin/env python3
from pathlib import Path
import json, re
ROOT=Path(__file__).resolve().parents[1]
from course_content import make_scenes
SCENES=make_scenes()

VISUAL_KEYS = {
  1: [('sealed box','box'),('boxes','three-boxes'),('ticket','tickets'),('cricket bat','bat'),('placeholder','variable'),('divide','divide'),('unknown','variable')],
  2: [('jersey','jerseys'),('coefficient','expression-parts'),('constant','expression-parts'),('variable','expression-parts')],
  3: [('taxi','taxi'),('bill','bill'),('t-shirt','shirts'),('delivery','delivery'),('per item','rate'),('per kilometre','rate')],
  4: [('apples and oranges','fruit-mixed'),('apples','fruit'),('oranges','fruit-mixed'),('like terms','like-terms'),('combine','combine')],
  5: [('weighing scale','scale'),('scale','scale'),('balance','scale'),('subtract','balance-operation'),('inverse','inverse')],
  6: [('teams','teams'),('balls','teams'),('cone','teams'),('bracket','brackets'),('distribut','distribute'),('multiplies every','distribute')],
  7: [('budget','fraction'),('split equally','fraction'),('fraction','fraction'),('denominator','fraction'),('shirts','shirts'),('division','fraction')],
  8: [('word problem','words-to-math'),('translat','words-to-math'),('ali','money'),('money','money'),('match fees','fees'),('travel cost','fees')],
  9: [('jersey','cost-graph'),('straight line','graph'),('y = mx + b','graph-labels'),('slope','graph-labels'),('rate of change','graph-labels'),('intercept','graph-labels')],
 10: [('cricket','cricket'),('shop','shop'),('delivery charge','shop'),('represent','workflow'),('simplify','workflow'),('solve','workflow'),('check','workflow')],
}

def normalize_spaces(s): return re.sub(r'\s+',' ',s).strip()

def split_long_piece(piece,max_words=18):
    piece=normalize_spaces(piece)
    if not piece: return []
    words=piece.split()
    if len(words)<=max_words: return [piece]
    sub=re.split(r'(?<=[,;:])\s+',piece)
    if len(sub)>1:
        out=[]; buf=[]; n=0
        for p in sub:
            w=len(p.split())
            if buf and n+w>max_words:
                out.append(normalize_spaces(' '.join(buf))); buf=[p]; n=w
            else: buf.append(p); n+=w
        if buf: out.append(normalize_spaces(' '.join(buf)))
        if all(len(x.split())<=max_words*1.4 for x in out): return out
    out=[]; start=0
    while start<len(words):
        end=min(len(words),start+max_words)
        if end<len(words):
            lo=max(start+7,end-5); best=None
            for j in range(end,lo-1,-1):
                if words[j-1].lower().strip(',') in {'and','but','so','then','because','while','before','after','if'}:
                    best=j-1; break
            if best and best>start+5: end=best
        out.append(' '.join(words[start:end])); start=end
    return out

def split_chunks(text):
    sents=re.split(r'(?<=[.!?])\s+',normalize_spaces(text)); out=[]
    for s in sents: out.extend(split_long_piece(s,18))
    return [x for x in out if x]

def visual_for(text,module,kind):
    low=text.lower()
    if kind=='practice':
        if 'now compare your work' in low or 'if your answer was different' in low or 'finally, explain' in low: return 'answer'
        if 'pause the video' in low or 'twenty seconds' in low: return 'practice'
        if 'your turn' in low: return 'practice'
    if 'common error' in low or 'common mistake' in low or 'mistake' in low or 'wrong' in low: return 'mistake'
    for needle,key in VISUAL_KEYS.get(module,[]):
        if needle in low: return key
    if any(sym in text for sym in [' = ',' + ',' - ',' ÷ ',' × ','→']) or re.search(r'\b\d+[a-zA-Z]\b',text): return 'equation'
    if 'rule' in low: return 'rule'
    if 'example' in low: return 'example'
    if 'question' in low or '?' in text: return 'questions'
    if 'check' in low: return 'check'
    return {'chapter':'chapter','intuition':'concept','rule':'rule','steps':'steps','compare':'compare','practice':'practice'}.get(kind,'concept')

def tts_text(text):
    t=text.replace('₹',' rupees ').replace('÷',' divided by ').replace('×',' times ').replace('→',' then ').replace('²',' squared ')
    t=re.sub(r'(?<=\w)=(?=\w)',' equals ',t)
    t=re.sub(r'\s*=\s*',' equals ',t)
    t=re.sub(r'\s*\+\s*',' plus ',t)
    t=re.sub(r'\s+-\s+',' minus ',t)
    t=re.sub(r'([A-Za-z0-9])/(\d+)',r'\1 divided by \2',t)
    return normalize_spaces(t)

def make_estimated_manifest():
    out=[]; absolute=0.0
    for sc in SCENES:
        chunks=split_chunks(sc['narration'])
        answer_idx=next((i for i,c in enumerate(chunks) if c.lower().startswith('now compare your work')),None)
        speech_words=sum(max(1,len(c.split())) for c in chunks)
        silence=20.0 if sc['kind']=='practice' and answer_idx is not None else 0.0
        total=max(sc['durationEstimate'],silence+5); speech_dur=max(1,total-silence)
        segs=[]; local=0.0
        for i,c in enumerate(chunks):
            if answer_idx is not None and i==answer_idx:
                segs.append({'start':round(local,3),'end':round(local+20,3),'text':'','tts':'','visual':'countdown','silent':True}); local+=20
            w=max(1,len(c.split())); dur=speech_dur*w/speech_words; v=visual_for(c,sc['module'],sc['kind'])
            segs.append({'start':round(local,3),'end':round(local+dur,3),'text':c,'tts':tts_text(c),'visual':v}); local+=dur
        if segs: segs[-1]['end']=round(total,3)
        out.append({'id':sc['id'],'module':sc['module'],'kind':sc['kind'],'title':sc['title'],'label':sc['label'],'concept':sc['concept'],'analogy':sc['analogy'],'rule':sc['rule'],'example':sc['example'],'steps':sc['steps'],'example2':sc['example2'],'mistake':sc['mistake'],'practice':sc['practice'],'answer':sc['answer'],'start':round(absolute,3),'duration':round(total,3),'audio':f'audio/scene_{sc["id"]:02d}.wav','segments':segs})
        absolute+=total
    return out

manifest=make_estimated_manifest(); js=json.dumps(manifest,ensure_ascii=False,indent=2)
(ROOT/'src/generatedManifest.ts').write_text("// AUTO-GENERATED fallback timing. scripts/generate_audio.py replaces durations with measured Kokoro audio timings.\nimport type {SceneSpec} from './types';\n"+f"export const scenes: SceneSpec[] = {js} as SceneSpec[];\n"+"export const TOTAL_DURATION = scenes.reduce((m,s)=>Math.max(m,s.start+s.duration),0);\n",encoding='utf-8')
print(f'Wrote {len(manifest)} scenes, estimated duration {sum(s["duration"] for s in manifest)/60:.2f} min')
print('segments',sum(len(s['segments']) for s in manifest))
