import React, { useRef, useEffect, useState } from 'react';
import * as d3 from 'd3';
import Popup from '../../components/Popup'; // Import the Popup component
import { NODE_COLORS_CORAL_PINK, NODE_COLORS_CYAN, NODE_COLORS_LIME_GREEN, RICH_LAVENDER, SOFT_BLUE } from '../utils/constants';

type GraphProps = {
  nodes: any,
  updatedNodesLength: number,
}

const GraphWithPopup = (props: GraphProps) => {
  const {nodes, updatedNodesLength} = props;
  const svgRef = useRef(null);
  const [popup, setPopup] = useState<any>({ content: '', position: { x: 0, y: 0 } });
  const [minX, setMinX] = useState<number>(0);
  const [maxX, setMaxX] = useState<number>(0);
  const [minY, setMinY] = useState<number>(0);
  const [maxY, setMaxY] = useState<number>(0);
  const [width, setWidth] = useState<number>(
    window.innerWidth
  );
  const [height, setHeight] = useState<number>(window.innerHeight);

  if (!nodes) {
    alert("NO NODES");
    return;
  }

  const getEdges: any = []

  Object.values(nodes).length > 0 && Object.values(nodes).map((node:any) => {

    if (node.type === "line") {

    }    

    if (node.type === "person") {
      const relevantWorks = nodes.filter((n:any)=>n.type === "work").filter((n:any) => n.data && n.data.authors.map((i:any) => i.name).includes(node.label))
      relevantWorks.map((work: any) => {
        getEdges.push({ source: node.id, target: work.id, type: "work_to_section" })
      })
    }

    if (node.type === "work") {
      const relevantSections = nodes.filter((n:any)=>n.type === "section").filter((n:any) => n.data && n.data.work.includes(node.label))
      relevantSections.map((section: any) => {
        getEdges.push({ source: node.id, target: section.id, type: "work_to_section" })
      })
    }

    if (node.type === "section") {
      const relevantLines = nodes.filter((n:any)=>n.type === "line").filter((n:any) => n.data && n.data.section.includes(node.label))
      relevantLines.map((line: any) => {
        getEdges.push({ source: node.id, target: line.id, type: "section_to_line" })
      })
    }
  })

  const data: any = {
    nodes: Array.from(nodes),
    edges: getEdges,
  };


  useEffect(() => {   
    const svg: any = d3.select(svgRef.current)
    const padding = 2;
    const xValues = data.nodes.map((node:any) => node.x && node.x);
    const yValues = data.nodes.map((node:any) => node.y && node.y);
    const minXTemp = Math.min(...xValues) - padding;
    const maxXTemp = Math.max(...xValues) + padding;
    const minYTemp = Math.min(...yValues) - padding;
    const maxYTemp = Math.max(...yValues) + padding;
    if (minXTemp && minXTemp > 0) {
      setMaxX(maxXTemp);
    }
    if (minYTemp && minYTemp > 0) {
      setMaxY(maxYTemp);
    }
    if (maxXTemp && maxXTemp > 0) {
      setMinX(minXTemp);
    }
    if (maxYTemp && maxYTemp > 0) {
      setMinY(minYTemp);
    }
    // Calculate width and height for viewBox
    const widthTemp = maxX - minX;
    const heightTemp = maxY - minY;
    if (widthTemp) {
      setWidth(widthTemp);
    }
    if (heightTemp) {
      setHeight(heightTemp);
    }
    
    svg.call(
      d3.zoom()
        .scaleExtent([0.5, 2]) // Limits on zoom
        .on("zoom", (event) => {
          svg.selectAll("g").attr("transform", event.transform);
        })
    );

    // Create the simulation
    const simulation: any = d3.forceSimulation(data.nodes)
      .force('link', d3.forceLink().id((d:any) => d.id).distance(100))
      .force("charge", d3.forceManyBody().strength(-100))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("x", d3.forceX().strength(0.0025).x(width / 2))
      .force("y", d3.forceY().strength(0.0025).y(height / 2))
      .force("collide", d3.forceCollide(50));

    // Create links
    const link = svg.append('g')
      .attr('class', 'links')
      .selectAll('line')
      .data(data.edges)
      .enter().append('line')
      .attr('stroke', 'gray');

    // Create nodes
    const node = svg.append('g')
      .attr('class', 'nodes')
      .selectAll('circle')
      .data(data.nodes)
      .enter().append('circle')
      .attr('r', 8)
      .attr('fill', (d: any) => d.type === 'person' ? `${NODE_COLORS_CORAL_PINK}` : d.type === 'work' ? `${NODE_COLORS_CYAN}` : d.type === 'section' ? `${NODE_COLORS_LIME_GREEN}` : d.type === 'line' ? "blue" :`${"#ffffff"}`)
      .on('mouseover', (event: any, d: any) => {
        setPopup({ content: d.info, position: { x: event.pageX, y: event.pageY } });
      })
      .on('mouseout', () => {
        setPopup({ content: '', position: { x: 0, y: 0 } });
      })
      .on('click', (event: any, d: any) => {
        console.log("CONSOLE LOG CLICK** ", d, event)
      });

    // Update simulation on tick
    simulation
      .nodes(data.nodes)
      .on('tick', () => {
        link
          .attr('x1', (d: any) => d.source.x)
          .attr('y1', (d: any) => d.source.y)
          .attr('x2', (d: any) => d.target.x)
          .attr('y2', (d: any) => d.target.y);
        node
          .attr('cx', (d: any) => d.x)
          .attr('cy', (d: any) => d.y);
      });
    console.log("heyo simulation: ", data);
    simulation.force('link').links(data.edges);
  }, []);

  
  return (
    <>
      <svg 
        // style={{overflow: "scroll"}}
        width={width}
        height={height}
        className=" z-100" 
        ref={svgRef}
      >
      </svg>
      <Popup content={popup.content} position={popup.position} />
    </>
  );
};

export default GraphWithPopup;