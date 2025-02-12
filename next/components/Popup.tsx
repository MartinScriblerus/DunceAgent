import React from 'react';

type Position = {
    x: number;
    y: number;
}

type PopupProps = {
    content: React.ReactNode;
    position: Position;
}

const Popup = ({ content, position }: PopupProps) => {
  if (!content) return null;

  return (
    <div
      style={{
        position: 'absolute',
        top: position.y,
        left: position.x,
        backgroundColor: 'white',
        border: '1px solid #ccc',
        padding: '5px',
        borderRadius: '4px',
        pointerEvents: 'none', // Prevent the popup from interfering with mouse events
      }}
    >
      {content}
    </div>
  );
};

export default Popup;