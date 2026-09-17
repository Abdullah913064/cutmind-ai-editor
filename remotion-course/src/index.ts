import React from 'react';
import {Composition, registerRoot} from 'remotion';
import {AlgebraCourse, ChapterCourse, getChapterDuration, getTotalDuration} from './Course';

const FPS=30;
const WIDTH=1920;
const HEIGHT=1080;

const Root:React.FC=()=> <>
  <Composition id="AlgebraCourse" component={AlgebraCourse} durationInFrames={Math.ceil(getTotalDuration()*FPS)} fps={FPS} width={WIDTH} height={HEIGHT} defaultProps={{audioEnabled:true}}/>
  {Array.from({length:10},(_,i)=>i+1).map((chapter)=><Composition
    key={chapter}
    id={`Chapter${String(chapter).padStart(2,'0')}`}
    component={ChapterCourse}
    durationInFrames={Math.ceil(getChapterDuration(chapter)*FPS)}
    fps={FPS}
    width={WIDTH}
    height={HEIGHT}
    defaultProps={{chapter,audioEnabled:true}}
  />)}
</>;

registerRoot(Root);
