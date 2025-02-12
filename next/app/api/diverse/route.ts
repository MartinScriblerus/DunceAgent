import { getQdrantClient, parseResult } from "../../utils/qDrantHelpers";
import { NextRequest, NextResponse } from "next/server";

// No cache when deployed to Vercel
// https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config#dynamic
export const dynamic = "force-dynamic";

export async function POST(request: NextRequest | Request) {
  // NOTE: REQUESTS TO THIS ROUTE HAVE BEEN DISABLED AT
  // context/data-context.jsx#L119-L128
  const client = getQdrantClient();

  const { target, context } = await request.json();

  const qdrantCollectionName: string | any = process.env.QDRANT_COLLECTION_NAME;

  let response: any = await client.retrieve(qdrantCollectionName, {
    ids: [target],
    with_vector: true,
  });

  let reversedVector = response[0].vector.map((x: number) => -x);

  response = await client.discoverPoints(qdrantCollectionName, {
    limit: 1,
    context,
    target: reversedVector,
    with_vector: true,
    with_payload: true,
  });

  const itemA: any = response[0];

  reversedVector = itemA.vector.map((x: number) => -x);

  response = await client.discoverPoints(qdrantCollectionName, {
    context,
    limit: 1,
    target: reversedVector,
    filter: {
      must_not: [{ has_id: [itemA.id] }],
    },
    with_payload: true,
  });

  const results = [parseResult(response[0]), parseResult(itemA)];
  return NextResponse.json(results);
}