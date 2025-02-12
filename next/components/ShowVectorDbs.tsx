import React from 'react';

interface ShowVectorDbsProps {
    dbNames: string[],
}

const ShowVectorDbs = (props: ShowVectorDbsProps) => {
    const { dbNames } = props;
    return (
        <>
        {
            dbNames.map((name, idx) => 
                <button 
                    className='
                        text-slate-300
                        bg-blue-500 
                        hover:bg-blue-700 
                        font-bold 
                        py-2 px-4 
                        m-2
                        height-48
                        rounded
                    '
                    key={`vector_db_name_${name}_${idx}`} 
                    id={`vector_db_btn_${name}`}
                >
                    {name}
                </button>
            )}
        </>
    )
}
export default ShowVectorDbs;