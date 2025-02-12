import { getQdrantClient, parseResult } from "../../utils/qDrantHelpers";
import { NextRequest, NextResponse } from "next/server";

// No cache when deployed to Vercel
// https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config#dynamic
export const dynamic = "force-dynamic";

export async function POST(request: NextRequest | Request) {
  const client = getQdrantClient();

  const { context, limit } = await request.json();

  const response = await client.discoverPoints(
    process.env.QDRANT_COLLECTION_NAME as string,
    {
      limit,
      context,
      with_payload: true,
    },
  );

  const results = response.map(parseResult);
  return NextResponse.json(results);
}