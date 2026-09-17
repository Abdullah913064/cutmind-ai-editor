import React from 'react';
import {AbsoluteFill, Sequence, staticFile, useVideoConfig} from 'remotion';
import {Audio} from '@remotion/media';
import {scenes} from './generatedManifest';
import {SemanticScene} from './Scene';
import type {SceneSpec} from './types';

const withOffsets=(input:SceneSpec[])=>{
  let cursor=0;
  return input.map((scene)=>{
    const offset=cursor;
    cursor+=scene.duration;
    return {scene,offset};
  });
};

const Timeline:React.FC<{input:SceneSpec[]; audioEnabled?:boolean}>=({input,audioEnabled=true})=>{
  const {fps}=useVideoConfig();
  const timed=withOffsets(input);
  return <AbsoluteFill style={{backgroundColor:'#07111f'}}>
    {timed.map(({scene,offset})=>{
      const from=Math.round(offset*fps);
      const durationInFrames=Math.max(1,Math.round(scene.duration*fps));
      return <Sequence key={scene.id} from={from} durationInFrames={durationInFrames} layout="absolute-fill">
        <SemanticScene scene={scene}/>
        {audioEnabled ? <Audio src={staticFile(scene.audio)} volume={0.96}/> : null}
      </Sequence>;
    })}
  </AbsoluteFill>;
};

export const AlgebraCourse:React.FC<{audioEnabled?:boolean}>=({audioEnabled=true})=><Timeline input={scenes} audioEnabled={audioEnabled}/>;
export const ChapterCourse:React.FC<{chapter:number; audioEnabled?:boolean}>=({chapter,audioEnabled=true})=><Timeline input={scenes.filter((s)=>s.module===chapter)} audioEnabled={audioEnabled}/>;

export const getChapterDuration=(chapter:number)=>scenes.filter((s)=>s.module===chapter).reduce((a,s)=>a+s.duration,0);
export const getTotalDuration=()=>scenes.reduce((a,s)=>a+s.duration,0);
