import { NextRequest, NextResponse } from 'next/server';

// GET request handler
export async function GET(req: NextRequest) {
    try {
        const pythonResponse = await fetch('http://api:8000/extend_peri_bathous', {
            method: 'GET',
            headers: {
                "Content-Type": "application/json"
            }
        });
        if (!pythonResponse.ok) {
            throw new Error(`Failed to connect to Python endpoint: ${pythonResponse.statusText}`);
        }
        const result = await pythonResponse.json();
        return NextResponse.json(result, { status: 200 });
    } catch (err) {
        return NextResponse.json({ error: err || 'Internal Server Error' }, { status: 500 });
    }
}
export async function POST(req: NextRequest) {
    try {
        const body = await req.json();
        const pythonResponse = await fetch('http://api:8000/extend_peri_bathous', {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        });
        if (!pythonResponse.ok) {
            throw new Error(`Failed to connect to Python endpoint: ${pythonResponse.statusText}`);
        }
        const result = await pythonResponse.json();
        return NextResponse.json(result, { status: 200 });
    } catch (err) {
        return NextResponse.json({ error: err || 'Internal Server Error' }, { status: 500 });
    }
}