import { NextRequest, NextResponse } from 'next/server';

// POST request handler
export async function POST(req: NextRequest) {
    try {
        // Parse the incoming request body
        const data = await req.json();
        console.log("CHECK DATA BEFORE SEND: ", data);
        // Send the request to the Python endpoint
        const pythonResponse = await fetch('http://api:8000/createvectordb', {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Origin": "*"
            },
            body: JSON.stringify(data),
        });

        // Check if the response from the Python backend was successful
        if (!pythonResponse.ok) {
            throw new Error(`Failed to connect to Python endpoint: ${pythonResponse.statusText}`);
        }

        // Parse the response from the Python backend
        const result = await pythonResponse.json();
        console.log("RESULT!@ ", result)
        // Return the response back to the client
        return NextResponse.json(result, { status: 200 });
    } catch (error) {
        console.error('Error forwarding request to Python endpoint:', error);
        return NextResponse.json({ error: 'Failed to connect to Python endpoint' }, { status: 500 });
    }
}