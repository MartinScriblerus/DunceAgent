export const getVectorDb = async (name: string) => {
    let response = null;
        // const createVectorDb = async (dbName: string) => {
        // console.log("Hit function");
    try {
        const res = await fetch("/api/createvectordb", {
        method: "POST",
        body: JSON.stringify({
            "dbName": JSON.stringify(name)
        }),
        headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Origin": "*"
        }
        });
        console.log("ANY RESPONSE? ", res);
        const createDbResponse = await res.json();
        console.log("CREATE RESPO! ", createDbResponse);
        return createDbResponse;
    } catch (err) {
        console.error("There was a problem with the fetch operation:", err);
    }
    // }
    // try {
    //     Promise.resolve(createVectorDb(name)).then((response: any) => {
    //         response.json();
    //     }).then((data: any) => {
    //         console.log("RESPONSE FROM PYTHON! ", data);
    //         response = data;
    //     });
    // } catch (err) {
    //     console.log("error: ", err);
    // }
    return (response);
};