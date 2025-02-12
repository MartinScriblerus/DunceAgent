"use client";

import { usePathname } from 'next/navigation';
import { useSession } from "next-auth/react";
import { useEffect, useState } from 'react'; // Add this line
import { MUTED_TEAL } from '@/app/utils/constants';

type NavProps = {
  isLogged: boolean;
  toggleModal: (e:any) => void;
  Checkboxes: any;
  handleCheckboxChange: (e:any) => void;
  selectedItems: any[];
  currentLevel: string;
  setSelectedNodesData: (d:any) => void;
  selectedNodesData: any[];
}

export function Navbar({isLogged, toggleModal, Checkboxes, handleCheckboxChange, selectedItems, setSelectedNodesData, selectedNodesData}: NavProps) {
  const { data: session } = useSession();
  const [showChatOptions, setShowChatOptions] = useState<boolean>(false);
  // const [isLogged, setIsLogged] = useState(!!session);
  // const [isLogged, setIsLogged] = useState(false);

  useEffect(() => {
    console.log("is logged? ", isLogged);
    console.log("WHAT IS SESSION DATA? ", !!session);
    // if (!!session) {
    //   setIsLogged(true);
    // } else {
    //   setIsLogged(false);
    // }
  },[isLogged]);

  const toggleChatOptions = () => {
    setShowChatOptions(!showChatOptions);
  };

  const pathname = usePathname();

  console.log("HEYO DATAAAAAA ", selectedNodesData);

  return (
    <nav className="mb-1 flex flex-col absolute right-0 z-10">
      
    {
      !selectedNodesData || selectedNodesData.length <= 0
      ?
      <>  
        <button 
          style={{color: `${MUTED_TEAL}`, background: `transparent`}}
          className={`top-0 mr-4 z-200 w-200px hover:bg-mutedTeal text-white font-bold py-1 px-1 rounded`}
          onClick={(e:any) => toggleModal(e)}
        >
          Vectors
        </button>
        <button
          style={{color: `${MUTED_TEAL}`, background: `transparent`}}
          className={`mt-1 top-0 mr-4 z-200 w-200px hover:bg-mutedTeal text-white font-bold py-2 px-2 rounded`}
          onClick={() => toggleChatOptions()}
        >
          Chat
        </button>
        {/* {isLogged  */}
        {isLogged && showChatOptions &&
        <>
          {/* <a className="mr-4" onClick={signOut}>Sign Out</a>
          <span className="text-gray-600">Welcome, {session.user.name}</span> */}
          <a className={`mr-4 hover:bg-gray-700/50 ${pathname === "/" ? "text-white border-b" : "text-gray-600"}`} href="/">Chat</a>
          <a className={`mr-4 hover:bg-gray-700/50 ${pathname === "/structured_output" ? "text-white border-b" : "text-gray-600"}`} href="/structured_output">Structured Output</a>
          <a className={`mr-4 hover:bg-gray-700/50 ${pathname === "/agents" ? "text-white border-b" : "text-gray-600"}`} href="/agents">Agents</a>
          <a className={`mr-4 hover:bg-gray-700/50 ${pathname === "/retrieval" ? "text-white border-b" : "text-gray-600"}`} href="/retrieval">Retrieval</a>
          <a className={`mr-4 hover:bg-gray-700/50 ${pathname === "/retrieval_agents" ? "text-white border-b" : "text-gray-600"}`} href="/retrieval_agents">Retrieval Agents</a>
          <a className={`mr-4 hover:bg-gray-700/50 ${pathname === "/ai_sdk" ? "text-white border-b" : "text-gray-600"}`} href="/ai_sdk">LangChain x AI SDK</a>
        </>}
      </>
      :
      <Checkboxes
        handleCheckboxChange={handleCheckboxChange}
        items={selectedItems}
      />
    }
    </nav>
  );
}

