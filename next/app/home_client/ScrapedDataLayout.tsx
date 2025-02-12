import React from 'react';

interface ScraperInitProps {
    getPopeData: (e:any) => void,
    buttonLabel: string,  // Button Label for the Scrape Data Button
}

const ScrapeDataLayout = (props: ScraperInitProps) => {   
    const {getPopeData, buttonLabel} = props;
    return (
        // <div >
        <button 
            className="flex-auto bg-blue-500 w-[200px] hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
            onClick={(e:any) => getPopeData(e)}
        >
        {buttonLabel}
        </button>
        // </div>
    )
};
export default ScrapeDataLayout;