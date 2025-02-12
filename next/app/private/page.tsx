// "use client";
import Home from '../page';
import SessionProviderWrapper from '@/components/SessionProviderWrapper';

export default function Private(){
    // const [isExpert, setIsExpert] = useState<boolean>(true)
    // const dialogueManager = useRef<any>({
    //     "isExpert": isExpert
    // });
    return(
        <>
        <nav className="p-8 w-full h-full bg-extreme-neon px-5 py-3 ">
            <div className="text-black flex items-center justify-end gap-2">
                <SessionProviderWrapper>
                    <Home  /> 
                </SessionProviderWrapper>
            </div>
        </nav>
            {/* <h1 className="text-white text-4xl text-center">Hello from private router</h1> */}
        </>
    )
}