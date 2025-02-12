import { NextRequest, NextResponse } from 'next/server';

// GET request handler
export async function GET(req: NextRequest) {
    const pythonResponse = await fetch('http://api:8000/initial_scrape', {
        method: 'GET',
        headers: {
            "Content-Type": "application/json",
            // "Access-Control-Allow-Credentials": "true",
            // "Access-Control-Allow-Origin": "*"
        },
    });

    // Check if the response from the Python backend was successful
    if (!pythonResponse.ok) {
        throw new Error(`Failed to connect to Python endpoint: ${pythonResponse.statusText}`);
    }

    // Parse the response from the Python backend
    const result = await pythonResponse.json();
    
    // Return the response back to the client
    return NextResponse.json(result, { status: 200 });
}