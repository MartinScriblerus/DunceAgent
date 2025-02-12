import { NextRequest, NextResponse } from 'next/server';

// GET request handler
export async function GET(req: NextRequest) {
    try {
        const pythonResponse = await fetch('http://api:8000/scrape_pope_letters', {
            method: 'GET',
            headers: {
                "Content-Type": "application/json"
            }
        });
        
        if (!pythonResponse.ok) {
            throw new Error(`Failed to connect to Python endpoint: ${pythonResponse.statusText}`);
        }
        const result = await pythonResponse.json();

        console.log("LETTERS && RESULT IS ", result);
        return NextResponse.json(result, { status: 200 });
    } catch (err) {
        return NextResponse.json({ error: err || 'Internal Server Error' }, { status: 500 });
    }
}