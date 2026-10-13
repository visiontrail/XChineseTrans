import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {Film} from './Film';
import {T} from './motion';
registerRoot(()=> <Composition id="RouteAroundFailure" component={Film} durationInFrames={T.durationFrames} fps={T.fps} width={T.width} height={T.height}/>);
