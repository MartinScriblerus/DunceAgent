import { fetchDramaticScriblerianCollaboratorsScrapeData, fetchDunciadScrapeData, fetchIliadScrapeData, fetchPeriBathousExtendData, fetchPeriBathousScrapeData, fetchPopeLettersScrapeData, fetchPopeMajorWorksScrapeData, fetchPopeSecondScrapeData, fetchScriblerianCollaboratorsScrapeData, fetchScriblerianCollaboratorsSecondScrapeData } from "./fetchScrapeMethods";

  const getPopeIliadData = async() => {
    try {
      const iliadScrapeResult: any = await fetchIliadScrapeData();
      return iliadScrapeResult;
    } catch (err) {
      console.log("ERR ", err);
      return null;
    }
  }

  const getPopeLettersData = async() => {
    try {
      const popeLettersScrapeResult: any = await fetchPopeLettersScrapeData();
      return popeLettersScrapeResult
    } catch (err) {
      console.log("ERR in letters scrape: ", err);
      return null;
    }
  }

  const getDunciadData = async() => {
        try {
          const dunciadScrapeResult: any = await fetchDunciadScrapeData();
          return dunciadScrapeResult
        } catch (err) {
          console.log("ERR ", err);
          return null;
        }
  }

  const getPopeMajorWorksData = async() => {
    try {
      const popeMajorWorksScrapeResult: any = await fetchPopeMajorWorksScrapeData();
      return popeMajorWorksScrapeResult
    } catch (err) {
      console.log("ERR MAJOR WORKS", err);
      return null;
    }
  }

  const getScriblerianScrapeData = async() => {
    try {
      const scriblerianScrapeResult: any = await fetchScriblerianCollaboratorsScrapeData();
      return scriblerianScrapeResult
    } catch (err) {
      console.log("ERR Scrib Scrape", err);
      return null;
    }
  }

  const getDramaticScriblerianScrapeData = async() => {
    try {
      const scriblerianScrapeResult: any = await fetchDramaticScriblerianCollaboratorsScrapeData();
      return scriblerianScrapeResult
    } catch (err) {
      console.log("ERR Scrib Scrape", err);
      return null;
    } 
  }

  const getPopeSecondScrapeData = async() => {
    // e.preventDefault();
    try {
      const popeSecondScrapeResult: any = await fetchPopeSecondScrapeData();
      return popeSecondScrapeResult
    } catch (err) {
      console.log("ERR POPE SECOND ", err);
      return null;
    }
  }

  const getScriblerianSecondScrapeData = async() => {
    try {
      const scriblerianSecondScrapeResults: any = fetchScriblerianCollaboratorsSecondScrapeData();
      return scriblerianSecondScrapeResults
    } catch (err) {
      console.log("ERR Scriblerian Second Scrape", err);
      return null;
    }
}

////////////////////////////////////////////////////////////////////////////////////////////////



export const scrapePeriBathous = async () => {
    try {
        const [data1] = await Promise.all(
          [
            fetchPeriBathousScrapeData(),
          ]
        )
        const d1 = await data1;
        return d1;
    } catch (err) {
        console.log("error in initial peri bathous scrape");
    };
};

export const extendPeriBathous = async (textArray: string[]) => {
  try {    
    const [extendedPeriBathousData] = await Promise.all(
      [
        fetchPeriBathousExtendData(textArray)
      ]
    )
    const d1Extended = await extendedPeriBathousData;
    return d1Extended;
  } catch (err) {
    console.log("error in extending peri bathous: ", err);
  }
}

export const scrapeDunciadAndMajorPope = () => {
    const concurrentFetch = async() => {
        try {
            const [data1, data2] = await Promise.all(
                [
                  getDunciadData(),  // Get the Dunciad data
                  getPopeMajorWorksData(),
                ]
            )
            const d1 = await data1;
            const d2 = await data2;
            // setDunciadData(d1);
            // setMajorPopeData(d2);
            // setPeriBathousData(d1);
            return {d1, d2};
        } catch (err) {
            console.log("error in initial pope major scrape");
        };
    };
    concurrentFetch;
};

export const scrapeSwiftMajorMiscellaniesDramaticData = () => {
    const concurrentFetch = async() => {
        try {
            const [ data5, data6, data8 ] = await Promise.all(
                [
                getScriblerianScrapeData(),
                getScriblerianSecondScrapeData(),
                getDramaticScriblerianScrapeData(),
                ]
            )
            const d5 = await data5;
            const d6 = await data6;
            const d8 = await data8;
            return {d5, d6, d8}
        } catch (err) {
            console.log("error in initial swift major Scrib collab scrape");
        };
    };
    concurrentFetch;
};

export const scrapePopeSecondLetters = () => {
    const concurrentFetch = async() => {
        try {
            const [ data4, data7] = await Promise.all(
                [
                  getPopeSecondScrapeData(),
                  getPopeLettersData(),
                ]
              )
              const d4 = await data4;
              const d7 = await data7;
              return {d4, d7}      
        } catch (err) {
            console.log("error in initial pope second letters scrape");
        }
    };
    concurrentFetch;
};

export const scrapePopeIliad = () => {
    const concurrentFetch = async() => {
        try {
            const [ data9 ] = await Promise.all(
                [
                  getPopeIliadData(),  // Get the Iliad data
                ]
              )   
              const d9 = await data9;
              return d9;
        } catch (err) {
            console.log("error in initial pope iliad scrape");
        }
    };
    concurrentFetch;
};