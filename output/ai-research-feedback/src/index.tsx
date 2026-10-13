import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {Film} from './Film';
import T from '../public/timeline.json';
registerRoot(()=> <Composition id="AIResearchFeedback" component={Film} durationInFrames={T.duration_frames} fps={T.fps} width={T.width} height={T.height}/>);
