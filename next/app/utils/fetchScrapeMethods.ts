export async function fetchPopeLettersScrapeData() {

    let response = null;
    try {
        const res = await fetch("/api/scrapePopeLetters", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        });
        // console.log("HEYA THIS RES POPE LETTERS: ", res);
        // return res;
        // const data = await streamToString(res.body);
        // console.log("HEYA/WHUUU? THIS RE POPE LETTERS: ", JSON.parse(data));
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }
        const data = await res.json();
        return data;
    } catch (err) {
        console.error("There was a problem with the Pope's letters fetch operation:", err);
    }
    return (response)
}

async function streamToString(stream: any) {
    const chunks = [];
    for await (const chunk of stream) {
        chunks.push(chunk);
    }
        return Buffer.concat(chunks).toString('utf8');
    } 

export async function fetchPopeSecondScrapeData() {
    let response = null;
    try {
        const res = await fetch("/api/scrapePopeSecond", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        });

        const data = await streamToString(res.body);
        return data;
    } catch (err) {
        console.error("There was a problem with the Scrib Collab Second fetch operation:", err);
    }
    return (response);
}

export async function fetchScriblerianCollaboratorsSecondScrapeData() {
    let response = null;
    try {
        const res = await fetch("/api/scrapeScriblerianCollaboratorsSecond", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        });

        const data = await streamToString(res.body);
        return data;
    } catch (err) {
        console.error("There was a problem with the Scriblerian Collaborators fetch operation:", err);
    }
    return (response);
}

export async function fetchDunciadScrapeData() {
    let response = null;
    try {
        const res = await fetch("/api/scrapeDunciad", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        });
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }
        const data = await res.json();
        return data; 
    } catch (err) {
        console.error("There was a problem with the Dunciad fetch operation:", err);
    }
    return (response);
}

export async function fetchIliadScrapeData() {
    let response = null;
    try {
        const res = await fetch("/api/scrapeIliad", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        });
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }
        const data = await res.json();
        return data; 
    } catch (err) {
        console.error("There was a problem with the Iliad fetch operation:", err);
    }
    return (response);
}

export async function fetchPeriBathousScrapeData() {
    let response = null;
    try {
        const res = await fetch("/api/scrapePeriBathous", {
            method: "GET",
            signal: AbortSignal.timeout(120000),
            headers: {
                "Content-Type": "application/json",
            }
        });
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }
        const data = await res.json();
        return data; 
        // const data = await streamToString(res.body);
        // return data;
    } catch (err) {
        console.error("There was a problem with the Peri Bathous fetch operation:", err);
    } 
}

export async function fetchPeriBathousExtendData(textArray: string[]) {
    let response = null;
    try {
        const res = await fetch("/api/extendPeriBathous", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify([{'data':textArray}])
        });
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }
        const data = await res.json();
        return data; 
    } catch (err) {
        console.error("There was a problem with the Peri Bathous extend fetch operation:", err);
    } 
    return (response);
}

export async function fetchPopeMajorWorksScrapeData() {
    try {
        const res = await fetch("/api/scrapeMajorWorks", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        });
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }
        const data = await res.json();
        return data; 
    } catch (err) { 
        console.error("There was a problem with the Major Works fetch operation:", err);
    }
}

export async function fetchScriblerianCollaboratorsScrapeData() {
    let response = null;
    try {
        const res = await fetch("/api/scrapeScriblerianCollaborators", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        });

        const data = await streamToString(res.body);
        return data;
    } catch (err) {
        console.error("There was a problem with the Scriblerian Collaborators fetch operation:", err);
    }
    return (response);
}

export async function fetchDramaticScriblerianCollaboratorsScrapeData() {
    let response = null;
    try {
        const res = await fetch("/api/scrapeDramaticScriblerianCollaborators", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        });

        const data = await streamToString(res.body);
        return data;
    } catch (err) {
        console.error("There was a problem with the Scriblerian Collaborators fetch operation:", err);
    }
    return (response);
}