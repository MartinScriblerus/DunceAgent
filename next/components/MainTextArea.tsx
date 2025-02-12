import { BLACK_TEXT, DARK_GRAY, EDGE_COLORS_SOFT_GRAY, INTERACTIVE_TEXT_COLOR, LIGHT_GRAY, MUTED_TEAL } from '@/app/utils/constants';
import React from 'react';

const MainTextArea = () => {
    return (
        <div style={{background: `${LIGHT_GRAY}`}} className={`z-10 absolute top-2 left-8 p-2 flex flex-col h-36 w-3/5 rounded`}>
                            <h1 style={{color:`${BLACK_TEXT}`}} className="mb-2 text-4xl font-extrabold leading-none tracking-tight md:text-5xl lg:text-6xl">HELLO</h1>
            <span className="flex w-full h-full">
                <p style={{color:`${DARK_GRAY}`}} className="text-2xl font-extrabold">HELLO</p>
                <p style={{color:`${INTERACTIVE_TEXT_COLOR}`}} className="text-2xl font-extrabold">HELLO</p>
            </span>
            <span className="flex w-full h-full">
                <p style={{color:`${BLACK_TEXT}`}} className="text-1xl font-bold">HELLO</p>
                <p style={{color:`${BLACK_TEXT}`}} className="text-1xl">Hello</p>
            </span>
        </div>
    )
}
export default MainTextArea;