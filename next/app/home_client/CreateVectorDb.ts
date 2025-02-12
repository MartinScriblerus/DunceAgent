// import ShowVectorDbs from '@/components/ShowVectorDbs';
// import { useState } from 'react';

// type GetVectorDbProps = {
//     createVectorDb: any;
// }

// const getVectorDb = (props: GetVectorDbProps) => {
//     const {createVectorDb} = props;
//     let response = null;
//     try {
//         Promise.resolve(createVectorDb).then((response: any) => {
//             response.json();
//         }).then((data: any) => {
//             console.log("RESPONSE FROM PYTHON! ", data);
//             response = data;
//         });
//     } catch (err) {
//         console.log("error: ", err);
//     }


//   return (response);
// };

// export default GetVectorDb;