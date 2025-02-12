import React, { useEffect, useState } from 'react';
import styles from './AsciiAnimation.module.css';

const AsciiAnimation: React.FC = () => {
  const [asciiArt, setAsciiArt] = useState<string[]>([]);
  const chars = ['#', '*', '@', '&', '%', '+', 'o'];

  // Generate random ASCII pattern
  const generateAscii = () => {
    const rows = 20; // Set the number of rows for the animation
    const cols = 60; // Set the number of columns for the animation
    let art = [];
    
    for (let i = 0; i < rows; i++) {
      let row = '';
      for (let j = 0; j < cols; j++) {
        row += chars[Math.floor(Math.random() * chars.length)];
      }
      art.push(row);
    }
    return art;
  };

  // useEffect(() => {
  //   const interval = setInterval(() => {
  //     setAsciiArt(generateAscii());
  //   }, 1000); // Update every 100ms for fluid animation
  //   return () => clearInterval(interval);
  // }, []);

  return (
    <div className={styles.asciiContainer}>
      {/* {asciiArt.map((line, index) => (
        <pre key={index} className={styles.asciiLine}>
          {line}
        </pre>
      ))} */}
    </div>
  );
};

export default AsciiAnimation;