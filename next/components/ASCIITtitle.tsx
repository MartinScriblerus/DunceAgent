import React, { useEffect, useRef, useState } from 'react';
import "../app/globals.css"

const ScribotASCII = () => {

  const textStyle = {
    color: '#5C9E9A',
    fontFamily: 'monospace',
    whiteSpace: 'pre',
    fontSize: '16px',         
    lineHeight: '.88',         
    display: 'inline-block', 
    overflow: 'auto',      
  };



  return (
    <div className="w-full h-full" style={textStyle}>
      {String.raw`                   
___________________________________                             
           ===      *        |
          //         | _  _ / /  
          \    __ __ |/ \/ \ |     
            \ /  |  || O  O  |
____________//\__|  ||\_/\_/ |
      `}
    </div>
  );
};

export default ScribotASCII;