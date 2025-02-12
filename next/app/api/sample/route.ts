import { getQdrantClient, parseResult } from "@/app/utils/qDrantHelpers";
import { NextResponse } from "next/server";

// https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config#dynamic
export const dynamic = "force-dynamic";

export async function GET(request: any) {
  const client = getQdrantClient();

  const pointsCount = (await client.count(process.env.QDRANT_COLLECTION_NAME as string))
    .count;

  const itemId = Math.floor(Math.random() * pointsCount);

  const response = await client.retrieve(process.env.QDRANT_COLLECTION_NAME as string, {
    ids: [itemId],
    with_payload: true,
    with_vector: false,
  });

  return NextResponse.json(parseResult(response[0]));
}