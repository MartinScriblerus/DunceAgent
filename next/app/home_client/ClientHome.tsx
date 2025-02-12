"use client";

import { ChatWindow } from "@/components/ChatWindow";
import ShowVectorDbs from "@/components/ShowVectorDbs";
import Image from "next/image";
import useCustomInput from "@/hooks/useCustomInput";
import { FormEventHandler, useEffect, useState, useContext, useRef } from "react";
import { getVectorDb } from "../../app/utils/getVectorDb";
import AsciiAnimation from "./asciiAnimation";
import { useSession } from "next-auth/react";
import { usePathname } from 'next/navigation';
import { useRouter } from 'next/navigation';
import { RiTa } from "rita";

import { 
  fetchPeriBathousScrapeData, 
  fetchPopeSecondScrapeData,
  fetchDunciadScrapeData, 
  fetchPopeLettersScrapeData, 
  fetchScriblerianCollaboratorsScrapeData, 
  fetchPopeMajorWorksScrapeData, 
  fetchScriblerianCollaboratorsSecondScrapeData, 
  fetchDramaticScriblerianCollaboratorsScrapeData,
  fetchIliadScrapeData
} from "../utils/fetchScrapeMethods";
import ScrapedDataLayout from "./ScrapedDataLayout";
import { init } from "next/dist/compiled/webpack/webpack";
import type { InferGetServerSidePropsType, GetServerSideProps } from 'next'
import { Props } from "next/script";
import D3Canvas from "../visualizations/d3Canvas";
import {CURRENT_LEVELS, MUTED_TEAL} from "../utils/constants"
import { Navbar } from "@/components/Navbar";
import MainTextArea from "@/components/MainTextArea";
// import { fetchScrapeData } from "../utils/fetchScrapeData";
import "../globals.css"
import { extendPeriBathous, scrapeDunciadAndMajorPope, scrapePeriBathous, scrapePopeIliad, scrapePopeSecondLetters, scrapeSwiftMajorMiscellaniesDramaticData } from "../utils/adminScrapeMethods";
import { time } from "console";
import CheckboxList from "@/components/Checkboxes";
import ScribotASCII from "@/components/ASCIITtitle";

export default function HomeClient() {

  const [dbNames, setDbNames] = useState<string[]>([]);
  const [dbNameInput, setDbNameInput] = useState<string>("");
  const [dbIsLoading, setDbIsLoading] = useState<boolean>(false);
  const { data: session } = useSession();
  // const [isLogged, setIsLogged] = useState(!!session);
  const [isLogged, setIsLogged] = useState(false);

  const nodes: any = {
    nodes: [
      { id: 'Pope', info: 'Pope Information', data: {
        id: 'Peri Bathous', info: 'Peri Bathous Information', data: {}
      } },
      { id: 'Swift', info: 'Swift Information', data: {} },
      { id: 'Gay', info: 'Gay Information', data: {} },
      { id: 'Arbuthnot', info: 'Arbuthnot Information', data: {} },
      { id: 'Parnell', info: 'Parnell Information', data: {} },
    ],
  }

  const [periBathousData, setPeriBathousData] = useState<any[]>();
  const [dunciadData, setDunciadData] = useState<any[]>();
  const [majorPopeData, setMajorPopeData] = useState<any[]>();
  const [secondaryPopeData, setSecondaryPopeData] = useState<any[]>();
  const [swiftMajorData, setSwiftMajorData] = useState<any[]>();
  const [scriblerianDramaticData, setScriblerianDramaticData] = useState<any[]>();
  const [scriblerianMiscellaniesData, setScriblerianMiscellaniesData] = useState<any[]>();
  const [popeIliadData, setPopeIliadData] = useState<any[]>(); 
  const [popeLettersData, setPopeLettersData] = useState<any[]>();
  const [selectedNodesData, setSelectedNodesData] = useState<any>();

  const [modalOpen, setModalOpen] = useState<boolean>(false);
  const [modalOpenCount, setModalOpenCount] = useState<number>(0);
  const [modalIsOpen, setModalIsOpen] = useState<boolean>(false);
  const [updatedNodesLength, setUpdatedNodesLength] = useState<number>(0);
  const [allGenericNodes, setAllGenericNodes] = useState<GenericNode[]>([]);
  const [currentLevel, setCurrentLevel] = useState<string>("");

  // Ontology / Nodes
  const persons = useRef<Person[]>([]);
  const [selectedPerson, setSelectedPerson] = useState<Person | null>(null);
  const works = useRef<Work[]>([]);
  const [selectedWork, setSelectedWork] = useState<Work | null>(null);
  const [isScraperMode, setIsScraperMode] = useState<boolean>(true);
  const sections = useRef<Section[]>([]);
  
  const [selectedItems, setSelectedItems] = useState<string[]>(["Persons", "Works", "Sections", "Lines"])

  const [selectedSection, setSelectedSection] = useState<Section | null>(null);
  const lines = useRef<Line[]>([]);
  const [selectedLine, setSelectedLine] = useState<Line | null>(null);

  const router = useRouter();
  // const getPopeData = async() => {
  //   try {
  //     const periBathousScrapeResult: any = await fetchPeriBathousScrapeData();
  //     return periBathousScrapeResult;
  //   } catch (err) {
  //     console.log("ERR ", err);
  //     return null;
  //   }
  // }

  // const getPopeIliadData = async() => {
  //   try {
  //     const iliadScrapeResult: any = await fetchIliadScrapeData();
  //     return iliadScrapeResult;
  //   } catch (err) {
  //     console.log("ERR ", err);
  //     return null;
  //   }
  // }

  // const getPopeLettersData = async() => {
  //   try {
  //     const popeLettersScrapeResult: any = await fetchPopeLettersScrapeData();
  //     return popeLettersScrapeResult
  //   } catch (err) {
  //     console.log("ERR in letters scrape: ", err);
  //     return null;
  //   }
  // }

  // const getDunciadData = async() => {
  //       try {
  //         const dunciadScrapeResult: any = await fetchDunciadScrapeData();
  //         return dunciadScrapeResult
  //       } catch (err) {
  //         console.log("ERR ", err);
  //         return null;
  //       }
  // }

  // const getPopeMajorWorksData = async() => {
  //   try {
  //     const popeMajorWorksScrapeResult: any = await fetchPopeMajorWorksScrapeData();
  //     return popeMajorWorksScrapeResult
  //   } catch (err) {
  //     console.log("ERR MAJOR WORKS", err);
  //     return null;
  //   }
  // }

  // const getScriblerianScrapeData = async() => {
  //   try {
  //     const scriblerianScrapeResult: any = await fetchScriblerianCollaboratorsScrapeData();
  //     return scriblerianScrapeResult
  //   } catch (err) {
  //     console.log("ERR Scrib Scrape", err);
  //     return null;
  //   }
  // }

  // const getDramaticScriblerianScrapeData = async() => {
  //   try {
  //     const scriblerianScrapeResult: any = await fetchDramaticScriblerianCollaboratorsScrapeData();
  //     return scriblerianScrapeResult
  //   } catch (err) {
  //     console.log("ERR Scrib Scrape", err);
  //     return null;
  //   } 
  // }

  // const getPopeSecondScrapeData = async() => {
  //   // e.preventDefault();
  //   try {
  //     const popeSecondScrapeResult: any = await fetchPopeSecondScrapeData();
  //     return popeSecondScrapeResult
  //   } catch (err) {
  //     console.log("ERR POPE SECOND ", err);
  //     return null;
  //   }
  // }

  // const getScriblerianSecondScrapeData = async() => {
  //   try {
  //     const scriblerianSecondScrapeResults: any = fetchScriblerianCollaboratorsSecondScrapeData();
  //     return scriblerianSecondScrapeResults
  //   } catch (err) {
  //     console.log("ERR Scriblerian Second Scrape", err);
  //     return null;
  //   }
  // }



  // useEffect(() => {
  //   const concurrentFetch = async() => {
  //     console.log("IN ILIAD TOO..... " )
  //     try {
  //       const [ data9 ] = await Promise.all(
  //         [
  //           getPopeIliadData(),  // Get the Iliad data
  //         ]
  //       )   
  //       const d9 = await data9;
  //       setPopeIliadData(d9);
  //       console.log("POPE ILIAD DATA????: ", popeIliadData);
  //     } catch (error) {
  //       console.error("Error in concurrent scrape: ", error);
  //     }
  //   };
  //   concurrentFetch();
  //   return () => {
  //     // cleanup logic, if necessary
  //   };
  // }, [popeLettersData]);

  // useEffect(() => {
  //   const concurrentFetch = async() => {
  //      console.log("HERE NOW HERE NOW ALL GOOD HERE")
  //     try {
  //       const [ data4, data7] = await Promise.all(
  //         [
  //           getPopeSecondScrapeData(),
  //           getPopeLettersData(),
  //           // getPopeIliadData(),  // Get the Iliad data
  //         ]
  //       )
  //       const d4 = await data4;
  //       const d7 = await data7;      
  //       // const d9 = await data9;
  //       setSecondaryPopeData(d4);
  //       // setPopeIliadData(d9);
  //       setPopeLettersData(d7);
  //       console.log("HERE STILL... ", popeLettersData);
  //       return;
  //     } catch (error) {
  //       console.error("Error in concurrent scrape: ", error);
  //     }
  //   };
  //   concurrentFetch();
  //   return () => {
  //     // cleanup logic, if necessary
  //   };
  // }, [scriblerianDramaticData]);

  // useEffect(() => {
  //   const concurrentFetch = async() => {
  //     try {
  //       const [ data5, data6, data8 ] = await Promise.all(
  //         [
  //           getScriblerianScrapeData(),
  //           getScriblerianSecondScrapeData(),
  //           getDramaticScriblerianScrapeData(),
  //         ]
  //       )
  //       const d5 = await data5;
  //       const d6 = await data6;
  //       const d8 = await data8;
  //       setSwiftMajorData(d5);
  //       setScriblerianMiscellaniesData(d6);
  //       setScriblerianDramaticData(d8);
    
  //     } catch (error) {
  //       console.error("Error in concurrent scrape: ", error);
  //     }
  //   };
  //   concurrentFetch();
  //   return () => {
  //     // cleanup logic, if necessary
  //   };
  // }, [majorPopeData]);

  useEffect(() => {
    setCurrentLevel(CURRENT_LEVELS[3]);
  }, []);

  useEffect(() => {
    console.log("hello");
    // const timeout = setTimeout(() => {
    //   // if (!session) router.push('/login');
    // }, 4000);
    return () => {
      // clearTimeout(timeout);
    }

  }, [isLogged]);

  useEffect(() => {
    console.log("WHAT IS SESSION??? ", session);
    if (!!session && !isLogged) {
      setIsLogged(true);
    }
  },[session]);
  
  const handleDbSubmit = (e: FormEventHandler<HTMLFormElement> | any) => {
    e?.preventDefault();
    //parsing & checking steps here...
    console.log("WTF EVENT: ", e);

    const name: string | "" | undefined | null = e.target[0].value;
    if (name && dbNames.indexOf(name) !== -1) { 
      return;
    }
    if (name && name.length > 0 && isLogged) {
        const result = getVectorDb(name);
        console.log("REZ ", result);
        setDbNames([...dbNames, name]);
        return result;
    }
  };

  let handleDbInputChange = (msg: string | any) => {
    console.log("HEYA DBNAME: ", msg.target.value);
    if (msg && msg.target) {
      console.log("CHECK E ", msg);
      setDbNameInput(msg.target.value);
    }
  }

  const dbPlaceholder = "Name a new vector storage space...";
  const CreateDbFormInput = useCustomInput({
    handleFormInputChange: handleDbInputChange, 
    handleFormSubmit: handleDbSubmit, 
    formInput: dbNameInput,
    setFormInput: setDbNameInput,
    formIsLoading: dbIsLoading,
    setFormIsLoading: setDbIsLoading,
    formPlaceholder: dbPlaceholder,
    }
  );

  const InfoCard = (
    <div className="p-4 md:p-8 rounded bg-[#25252d] w-full max-h-[85%] overflow-hidden">
    </div>
  );
  const pathname = usePathname();



  const toggleModal = (e: any) => {
    const modal: any = document.getElementById('modal');
    console.log("modal ***? ", modal);
    if (modal.classList.contains("hidden")) {
      modal.classList.remove('hidden');
      modal.children[0].classList.remove('slide-out');
      modal.style.zIndex = 1;
      
      setModalOpen(true);
    } else {
      setTimeout(() => {
        modal.classList.add('hidden');
        modal.style.zIndex = -1;
        setModalOpen(false);
      }, 100); // Match duration with the CSS transition duration
    }
  };

  useEffect(() => {
    if (modalIsOpen) {
      window.addEventListener("click", (e: any) => {
        console.log("YO! ", e.target);
        if (!e.target.includes("modal")){
          toggleModal(e);
        }
      });
      return () => {
        window.removeEventListener("click", (e: any) => {});
      }
    }
  }, [modalIsOpen])

  const updateGraphWithData = (data: any) => {
    alert("shit bad")
    console.log("GOT THIS!!! ", data);
  };

  const updateGraphWithGenericNodes = (persons: Person[], works: Work[], sections: Section[], lines: Line[]) => {
    alert("YOOO good")
    console.log("FUGGGG works: ", works, sections, persons)
    const generalNodes = {
      persons: persons,
      works: works,
      sections: sections,
      lines: lines,
    };

    const genericNodes: GenericNode[] = [];

    console.log("BADAFUCKINBOOM =>>>>>>>  ", generalNodes);
    let currentId = 0;
    generalNodes.persons.map((person: any) => {
      currentId = currentId + 1;
      const newNode: GenericNode = {
        id: currentId.toString(),
        type: 'person',
        label: person.name,
        info: `Explore ${person.name}`,
        data: person
      }
      genericNodes.push(newNode);
    });
    generalNodes.works.map((work: any) => {
      currentId = currentId + 1;
      const newNode: GenericNode = {
        id: currentId.toString(),
        type: 'work',
        label: work.title,
        info: `Explore ${work.title}`,
        data: work
      }
      genericNodes.push(newNode);
    });
    generalNodes.sections.map((section: any) => {
      currentId = currentId + 1;
      const newNode: GenericNode = {
        id: currentId.toString(),
        type: 'section',
        label: section.title,
        info: `${section.title}`,
        data: section
      }
      genericNodes.push(newNode);
    });
    generalNodes.lines.map((line: any) => {
      currentId = currentId + 1;
      const newNode: GenericNode = {
        id: currentId.toString(),
        type: 'line',
        label: line.text,
        info: `${line.text}`,
        data: line
      }
      genericNodes.push(newNode);
    });
    console.log("FUCK YA! ", genericNodes)
    setAllGenericNodes(genericNodes);
    setSelectedNodesData(genericNodes);
  }

  const clearSelectedNodesData = () => {
    // setSelectedNodesData([]);
  };

  const addToSelectedNodesData = (paramKey: any, paramVal: any, isDataProp: boolean) => {
    alert("FUCK!")
    if (isDataProp) {
      const nodesToPush = allGenericNodes.filter((n: any) => 
        (n['data'][paramKey] === paramVal) && 
        (selectedNodesData.map((i:any)=>i.id).indexOf(n.id) === -1)
      );
      // setSelectedNodesData([...selectedNodesData, ...nodesToPush])
    } else {
      const nodesToPush = allGenericNodes.filter((n: any) => 
        (n['data'][paramKey] === paramVal) && 
        (selectedNodesData.map((i:any)=>i.id).indexOf(n.id) === -1)
      );
      // nodesToPush && 
      // nodesToPush.length > 0 && 
      // setSelectedNodesData([...selectedNodesData, ...nodesToPush])
    }
  };

  const filterSelectedNodesData = (paramKey: any, paramVal: any, isDataProp: boolean) => {
    if (isDataProp) {
      const nodesAfterFilter = allGenericNodes.filter((n: any) => 
        (n['data'][paramKey] === paramVal)
      );
      // setSelectedNodesData(nodesAfterFilter);
    } else {
      const nodesAfterFilter = allGenericNodes.filter((n: any) => 
        (n[paramKey] === paramVal)
      )
      // setSelectedNodesData(nodesAfterFilter);
    }
  };

  const scrapePeriBathousHelper = async (e: any) => {
    e.preventDefault();
    console.log("in scraper");
    toggleModal(e);
    let getPeriBathousData: any;
    let getExtendPeriBathousData;
    
    try {
      getPeriBathousData = await scrapePeriBathous();
    } catch (err) {
      console.log("error scraping periBathous: ", err);
    }
    // console.log("HEY HEY HEY CHECK THIS: ", await getPeriBathousData.length && getPeriBathousData.map((i:any)=>i));
    
    // Get Person / Author for ontology
    const authors: Person[] = [
      {
        name: "Alexander Pope",
        works: [],
        associations: ["Scriblerus Club", "Tory", "Catholic", "Poet"]
      },
      {
        name: "Martinus Scriblerus",
        works: [],
        associations: ["Scriblerus Club", "Pseudonym"]
      }
    ];
    authors.map(i => i.name && i).forEach((author: any) => {
      if (!persons.current.map(i=>i.name).includes(author.name)) {
        persons.current.push(author)
      }
    });

    if (!isScraperMode && getPeriBathousData && getPeriBathousData.length > 0 ) {
      setPeriBathousData((getPeriBathousData.peri_bathous).map((i:any) => i));
    }

    const objects = getPeriBathousData.peri_bathous[0].map((i:any)=>JSON.parse(JSON.stringify(i)));
    let sectionsArr: any = []; 
    objects.map((o:any) => {
      if (o.type === "section") {
        sectionsArr.push(`${o.data.chapter_number} - ${o.data.subtitle}`)
      }
    })

    const chaptNums: any = sectionsArr.map((i:any) => i.split(" - ")[0]);
    const subTitles: any = sectionsArr.map((i:any) => i.split(" - ")[1]);
 
    
    console.log("fucking subtitles ", subTitles)
    await subTitles.map((chapt:any, idx:number) => {
      sectionsArr.push(`${chapt} - ${subTitles[idx]}`)
    });

    const work: Work = {
      title: "ΠΕΡΙ ΒΑΘΟΎΣ: OR, OF THE ART OF SINKING IN POETRY",
      authors: authors,
      criticalIntro: [],
      sections: sectionsArr,
      genres: ["Prose", "Parody", "Satire", "Criticism"]
    };
    if(!works.current.map(i=>i.title).includes(work.title)) {
      works.current.push(work)
    }

    let section: Section = {
      title: "",
      lines: [],
      work: "",
      authors: [],
      isSecondary: false,
      speakers: [],
      addressees: []
    };

    let line: Line = {
      id: "",
      text: "",
      tokenizedText: [],
      section: "",
      authors: [],
      work: "",
      annotation: [],
      posData: [],
      stresses: [],
      phonemes: [],
      speaker: "",
      addressees: [],
      mentions: [],
      sentiment: {
        score: 0.0,
        label: "",
      },
    }

    const analyzableData = isScraperMode 
      ? 
      await getPeriBathousData && Object.values(getPeriBathousData.peri_bathous).length && Object.values(getPeriBathousData.peri_bathous).map((i:any) => i[0])
      : 
        await getPeriBathousData && Object.values(getPeriBathousData.peri_bathous).length && Object.values(getPeriBathousData.peri_bathous).map((i:any) => i[0] && i[0])
    
    if (!isScraperMode) {
      console.log("&&&& ", analyzableData)
      if (!isScraperMode) {
        console.log("WHAT THE FLYING FUCK: ", getPeriBathousData.peri_bathous)
      }

      ////////////////////////////////////////////////////////////////////////////////////////////////
      // THIS RETURN MODIFIES THE WHOLE TYPE/ROLE/PURPOSE OF ANALYZABLE DATA... rework a new endpoint for huggingface scrapes 
      setPeriBathousData(analyzableData);
      
      setSelectedNodesData(analyzableData);
      // updateGraphWithGenericNodes(
      //   persons.current,
      //   works.current,
      //   sections.current,
      //   lines.current
      // )
      ////////////////////////////////////////////////////////////////////////////////////////////////
      return;
    } else {
      setPeriBathousData(analyzableData);
      
      setSelectedNodesData(analyzableData);
    }
    let getMentions: any = [];
    console.log("ummm??? ",  await getPeriBathousData && Object.values(getPeriBathousData.peri_bathous).length && Object.values(getPeriBathousData.peri_bathous).map((i:any) => i[0]));
    console.log("GOSH ", analyzableData)
    analyzableData.map(async(dat: any, idx: number) => {
      console.log("DAT: ", dat);
      const data = dat.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "");
      if (!data) {
        
      }
      const ritaData: any = RiTa.analyze(data.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, ""));
      console.log("RITA DATA: ", ritaData);

      section = {
        // title: `${getPeriBathousData.peri_bathous[0][idx]['chapter_number']} - ${getPeriBathousData.peri_bathous[0][idx]['subtitle']}`.trim(),
        title: isScraperMode ? `${getPeriBathousData.peri_bathous[0][idx]['chapter_number']} - ${getPeriBathousData.peri_bathous[0][idx]['subtitle']}`.trim() : `${getPeriBathousData.peri_bathous[idx]['chapter_number']} - ${getPeriBathousData.peri_bathous[idx]['subtitle']}`.trim(),
        isSecondary: false,
        lines: [],
        work: "ΠΕΡΙ ΒΑΘΟΎΣ: OR, OF THE ART OF SINKING IN POETRY",
        speakers: ["Martinus Scriblerus"],
        authors: ["Alexander Pope", "Martinus Scriblerus"],
        addressees: ["English Writers", "English Critics", "Scriblerus Club"]
      };

      sections.current.push(section)      
      const pos_arr = ritaData.pos.split(" ");
      const tokenizedText = ritaData.tokens.split(" ");
      const stresses = ritaData.stresses.split(" "); 
      const phonemes = ritaData.phones.split(" ");

      pos_arr.map((pos: any, idx: number) => {
        console.log("POS SHOULD BE A STRING --> ", pos);
        if (pos === "NNS" || pos === "NNP" || pos === "NN" || pos === "NNPS" ) {
          getMentions.push(tokenizedText[idx]) 
        }
      })
 
      line = {
        id: getPeriBathousData.peri_bathous[0][idx]["id"],
        text: data,
        tokenizedText: tokenizedText,
        section: section.title,
        authors: persons.current.map(i=>i.name),
        work: "ΠΕΡΙ ΒΑΘΟΎΣ: OR, OF THE ART OF SINKING IN POETRY",
        annotation: getPeriBathousData.peri_bathous[0][idx]["annotation"],
        posData: pos_arr,
        stresses: stresses,
        phonemes: phonemes,
        speaker: "Martinus Scriblerus",
        addressees: [],
        mentions: getMentions,
        sentiment: {
          score: 0.0,
          label: "",
        },
      }
      if (!section.lines.includes(line.id)) {
        const getSect: any = sections.current.find((s: any) => s.title === section.title)
        console.log("heya get sect: ", getSect);
        getSect.lines.push(line.id)
      }

      // clear getMentions array for the next line
      getMentions = [];
      if (!lines.current.map((l:any) => l.id).includes(line.id)) lines.current.push(line);
      
      
      getPeriBathousData.peri_bathous[0].map((i:any)=>{
        if (JSON.parse(JSON.stringify(i)).data && JSON.parse(JSON.stringify(i)).data.works) {
          works.current.push(JSON.parse(JSON.stringify(i)).data['work']);
        }
      })
    });

    updateGraphWithData(getPeriBathousData.peri_bathous)

    try {
      getExtendPeriBathousData = await extendPeriBathous(analyzableData);
      console.log("GET EXTEND PERI BATHOUS DATA: ", getExtendPeriBathousData);
      getExtendPeriBathousData.map((sentimentDatum: any, idx: number) => {
        if (sentimentDatum) lines.current[idx].sentiment = sentimentDatum;
      })
    } catch (err) {
      console.log("error extending periBathous: ", err);
    }
  };

  const scrapeDunciadAndMajorPopeHelper = (e: any) => {
    e.preventDefault();
    console.log("in scraper");
    try {
      const getDunciadData = scrapeDunciadAndMajorPope();
      return console.log("HEY Dunciad and Major Pope DATA: ", getDunciadData);
    } catch (err) {
      console.log("error scraping dunciad: ", err);
    }
  };

  const scrapeSwiftMajorMiscellaniesDramaticDataHelper = async (e: any) => {
    e.preventDefault();
    console.log("in scraper");
    try {
      const getCollaboratorsMajor = await scrapeSwiftMajorMiscellaniesDramaticData();
      return console.log("HEY Scriblerian DATA: ", getCollaboratorsMajor);
    } catch (err) {
      console.log("error scraping scriblerian: ", err);
    }
  };

  const scrapePopeSecondLettersHelper = async (e:any) => {
    e.preventDefault();
    console.log("in scraper");
    try {
      const getPopeSecondData = await scrapePopeSecondLetters();
      return console.log("HEY Pope Second DATA: ", getPopeSecondData);
    } catch (err) {
      console.log("error scraping pope second: ", err);
    }
  };

  const scrapePopeIliadHelper = async (e: any) => {
    e.preventDefault();
    console.log("in scraper");
    try {
      const getPopeIliadData = await scrapePopeIliad();
      return console.log("HEY Pope Iliad DATA: ", getPopeIliadData);
    } catch (err) {
      console.log("error scraping pope iliad: ", err);
    }
  }

  useEffect(() => {
    console.log("SELECTED ITEMS: ", selectedItems);
  }, [selectedItems]);

  const handleCheckboxChange = (item: any) => {
    setSelectedItems((prevSelectedItems: any) =>
      prevSelectedItems.includes(item)
        ? prevSelectedItems.filter((i:any) => i !== item)
        : [...prevSelectedItems, item]
    );
  };

  useEffect(() => {
    if (periBathousData && periBathousData.length > 0)
        console.log("PERI BAT NODES LEN: ", periBathousData.length);
        setUpdatedNodesLength(periBathousData && periBathousData.length ? periBathousData.length : 0);
  }, [periBathousData]);
  
  const Checkboxes = () => { 
    return (
      <CheckboxList 
        handleCheckboxChange={handleCheckboxChange}
        items={selectedItems}
      />
    )
  }

  return (
    <div className="color-#fffff position-relative w-full" style={{height: '100vh', alignSelf: "stretch"}}>
      {/* {isLogged && InfoCard ? */}
      {
        isLogged && InfoCard 
        ?
        <>
          <Navbar 
            isLogged={isLogged} 
            toggleModal={toggleModal}
            Checkboxes={Checkboxes}
            handleCheckboxChange={handleCheckboxChange}
            selectedItems={selectedItems}
            currentLevel={currentLevel}
            selectedNodesData={selectedNodesData}
            setSelectedNodesData={setSelectedNodesData}
          />
          
          <D3Canvas 
            periBathousData={periBathousData}
            majorPopeData={majorPopeData}
            secondaryPopeData={secondaryPopeData}
            scribMiscellaniesData={scriblerianMiscellaniesData}
            dunciadData={dunciadData}
            scriblerianDramaticData={scriblerianDramaticData}
            popeIliadData={popeIliadData}
            swiftMajorData={swiftMajorData}
            scriblerianMiscellaniesData={scriblerianMiscellaniesData}
            popeLettersData={popeLettersData}
            nodes={selectedNodesData}
            updatedNodesLength={updatedNodesLength}
          />
            {
              selectedNodesData && (
              <ScribotASCII />
              )
            }

            {
              periBathousData && periBathousData.length > 0 
                ?
                  (<MainTextArea/>) 
                : 
                  <></>
            }
          
        <div id="modal" className="z-negative bg-[#25252d] transform transition-transform duration-100 top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 h-4/5 absolute w-1/2 inset-0 flex items-center justify-center hidden">
        <button
          style={{background: `${MUTED_TEAL}`}}
          className={`absolute mt-12 top-0 left-12 z-200 w-200px hover:bg-mutedTeal text-white font-bold py-2 px-4 rounded`}
          onClick={(e:any) => toggleModal(e)}
        > {`Back`} </button>
        <button
          style={{background: `${MUTED_TEAL}`}}
          className={`absolute mt-12 top-0 right-12 z-200 w-200px hover:bg-mutedTeal text-white font-bold py-2 px-4 rounded`}
          onClick={(e:any) => setModalOpenCount(modalOpenCount + 1)}
        > {`Next`} </button>

        {
          modalOpenCount % 2 !== 0
          ? 
            <div className="bg-black w-half scroll text-white m-8 p-6 rounded-lg shadow-lg">
              <h2 className="text-xl w-full font-bold mb-12">Vector Database</h2>
              <div className="flex w-full  z-1 items-left justify-left bg-black bg-opacity-25 text-white">
                <div className="text-lg w-full  z-1">
                  {CreateDbFormInput}
                  </div>
              </div>
              <ShowVectorDbs dbNames={dbNames} />
            </div>
          :
            <div className="bg-transparent m-8 flex flex-col z-0 relative w-half text-white m-8 p-6 rounded-lg shadow-lg">
              <button 
                style={{background: `${MUTED_TEAL}`}}
                className={`mt-4 top-0 z-200 w-200px hover:bg-mutedTeal text-white font-bold py-2 px-4 rounded`}
                onClick={(e:any) => scrapePeriBathousHelper(e)}
              >Peri Bathous</button>

              <button 
                style={{background: `${MUTED_TEAL}`}}
                className={`mt-4 top-0 z-200 w-200px hover:bg-mutedTeal text-white font-bold py-2 px-4 rounded`}
                onClick={(e:any) => scrapeDunciadAndMajorPopeHelper(e)}
              >Pope Major Works</button>

              <button 
                style={{background: `${MUTED_TEAL}`}}
                className={`mt-4 top-0 z-200 w-200px hover:bg-mutedTeal text-white font-bold py-2 px-4 rounded`}
                onClick={(e:any) => scrapeSwiftMajorMiscellaniesDramaticDataHelper(e)}
              >Swift Major Works</button>

              <button 
                style={{background: `${MUTED_TEAL}`}}
                className={`mt-4 top-0 z-200 w-200px hover:bg-mutedTeal text-white font-bold py-2 px-4 rounded`}
                onClick={(e:any) => scrapePopeSecondLettersHelper(e)}
              >Pope Essays and Letters</button>

              <button 
                style={{background: `${MUTED_TEAL}`}}
                className={`mt-4 top-0 z-200 w-200px hover:bg-mutedTeal text-white font-bold py-2 px-4 rounded`}
                onClick={(e:any) => scrapePopeIliadHelper(e)}
              >Pope's Iliad</button>
              
            </div>
          }
        </div>








          {/* <ChatWindow
            endpoint="api/chat"
            emoji="🏴‍☠️"
            titleText="Patchy the Chatty Pirate"
            placeholder="I'm an LLM pretending to be a pirate! Ask me about the pirate life!"
            emptyStateComponent={InfoCard}
          ></ChatWindow> */}
        </>
        :
          <h3 className="center text-slate-300">You've been logged out. Please log back in!</h3>
      }
    </div>
  );
}
