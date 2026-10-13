import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {Film} from './Film';
registerRoot(()=> <Composition id='SteeringWithoutTurning' component={Film} durationInFrames={2160} fps={60} width={1920} height={1080}/>);
