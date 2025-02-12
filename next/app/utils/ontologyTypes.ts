type Person = {
    name: string;
    works: string[];
    associations: string[];
}

type Work = {
    title: string;
    authors?: Person[];
    criticalIntro?:Section[];
    sections?: string[];
    genres?: string[];
}

type Section = {
    title: string;
    lines: any[];
    work: string;
    authors: string[];
    isSecondary: boolean;
    speakers: string[];
    addressees: string[];
}

type Line = {
    id: string;
    text: string;
    tokenizedText: string[];
    section: string;
    work: string;
    authors: string[];
    annotation: string[];
    posData: string[];
    stresses: string[];
    phonemes: string[];
    speaker: string;
    addressees: string[];
    mentions: string[];
    sentiment: {
        score: number;
        label: string;
    }
}

type GenericNode = {
    id: string;
    type: string;
    label: string;
    info: string;
    data: Line | Section | Work | Person | any;
}