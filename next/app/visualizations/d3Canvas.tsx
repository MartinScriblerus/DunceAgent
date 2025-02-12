import { useEffect, useRef, useState } from "react";
import "../globals.css";
import { EDGE_COLORS_DEEP_PURPLE, NODE_COLORS_CORAL_PINK } from "../utils/constants";
import * as d3 from 'd3';
import GraphWithPopup from "./GraphWithPopups";
import MainTextArea from "@/components/MainTextArea";

interface ScrapeDataProps {
    periBathousData: any;
    majorPopeData: any;
    secondaryPopeData: any;
    scribMiscellaniesData: any;
    dunciadData: any;
    scriblerianDramaticData: any;
    popeIliadData: any;
    swiftMajorData: any;
    scriblerianMiscellaniesData: any;
    popeLettersData: any;
    nodes: any;
    updatedNodesLength: number;
}

const D3Canvas = (props: ScrapeDataProps) => {
    const {
        periBathousData,
        majorPopeData,
        secondaryPopeData,
        scribMiscellaniesData,
        dunciadData,
        scriblerianDramaticData,
        popeIliadData,
        swiftMajorData,
        scriblerianMiscellaniesData,
        popeLettersData,
        nodes,
        updatedNodesLength
    } = props;

    const canvasRef = useRef(null);

    const resizeCanvas = () => {
      const canvas: any = canvasRef.current;
      if (canvas) {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        draw(); // Call your drawing function here
      }
    };
  
    const draw = () => {
      const canvas: any = canvasRef.current;
      const context = canvas.getContext('2d');
      // Example drawing: clear canvas and fill with a color
      context.clearRect(0, 0, canvas.width, canvas.height);
      context.fillStyle = '#1E1E2F';
      context.fillRect(0, 0, canvas.width, canvas.height);
      // Add your custom drawing logic here
    };
  
    useEffect(() => {
      if (scriblerianDramaticData)
          console.log("SECONDARY DRAMATIC DATA: ", JSON.parse(scriblerianDramaticData)); console
    }, [scriblerianDramaticData]);

    useEffect(() => {
      if (popeIliadData)
          console.log("POPE ILIAD DATA: ", popeIliadData);
    }, [popeIliadData]);

    useEffect(() => {
      if (scribMiscellaniesData)
          console.log("SCRIB MISCELLANIES DATA: ", JSON.parse(scribMiscellaniesData));
    }, [scribMiscellaniesData]);

    useEffect(() => {
      if (swiftMajorData)
          console.log("SWIFT MAJOR DATA: ", JSON.parse(swiftMajorData));
    }, [swiftMajorData]);

    useEffect(() => {
      resizeCanvas();
      window.addEventListener('resize', resizeCanvas);
      return () => {
        window.removeEventListener('resize', resizeCanvas);
      };
    }, []);

    useEffect(() => {
        if (scriblerianMiscellaniesData)
            console.log("SCRIBLERIAN MISCELLANIES DATA: ", JSON.parse(scriblerianMiscellaniesData));
    },[scriblerianMiscellaniesData]);

    useEffect(() => {
      if (popeLettersData)
          console.log("POPE LETTERS DATA: ", popeLettersData);
    },[popeLettersData]);

    useEffect(() => {
        if (periBathousData) 
            console.log("PERI BATHOUS DATA: ", periBathousData);
    }, [periBathousData]);

    useEffect(() => {
      if (dunciadData)
          console.log("DUNCIAD DATA: ", dunciadData);
  }, [dunciadData]);

    useEffect(() => {
      if (majorPopeData) {
        if (majorPopeData.pope_major_works && majorPopeData.pope_major_works.length > 0 && majorPopeData.pope_major_works[1]) {
          majorPopeData.pope_major_works[1].sort((a: any, b: any) => 
            a.chapter_number - b.chapter_number);
        }
        console.log("MAJOR POPE DATAz: ", majorPopeData);
      } 
    }, [majorPopeData]);
  
    useEffect(() => {
      if (secondaryPopeData)
          console.log("SECONDARY POPE DATA: ", JSON.parse(secondaryPopeData));
    }, [secondaryPopeData]);


    useEffect(() => {
      console.log("UPDATED NOD LEN ", updatedNodesLength)
    }, [updatedNodesLength])

    useEffect(() => {
      console.log("### WHAT ARE FUCKING NODES???? ", nodes)
    },[nodes])

    return (
      <>
        <canvas 
            ref={canvasRef}
            style={{width: window.innerWidth, height:window.innerHeight}}
            className="fixed z-negative top-0 bottom-0 left-0 w-full h-full"
        >
        </canvas>
        {/* <>{updatedNodesLength}</> */}
        {updatedNodesLength > 0
        ? 
        <GraphWithPopup nodes={nodes} updatedNodesLength={updatedNodesLength} />
        :
        <></>
        }
      </>
    )
}
export default D3Canvas;