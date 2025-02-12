export async function fetchScrapeData() {
    const res = await fetch("/api/scrape", {
        method: "GET",
        // body: JSON.stringify({
        //     "dbName": JSON.stringify(name)
        // }),
        headers: {
            "Content-Type": "application/json",
        }
        });
        console.log("ANY SCRAPE RESPONSE? ", res);
        const createDbResponse = await res.json();
        console.log("CREATE SCRAPE RESPO! ", createDbResponse);
        return createDbResponse;
  }