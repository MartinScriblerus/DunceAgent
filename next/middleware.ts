import {withAuth} from 'next-auth/middleware';
import { NextRequest, NextResponse } from "next/server";

export default withAuth({
    secret: process.env.SECRET,
  });

export function middleware() {
    // retrieve the current response
    const res = NextResponse.next()
    //   const { pathname } = req.nextUrl; 

    //   const token = req.cookies.get('token'); // Check for an auth token

    //   if (pathname.startsWith('/dashboard')) {
        // Redirect to login page if not authenticated
        // if (!token) {
        //     const loginUrl = new URL('/login', req.url);
        //     return NextResponse.redirect(loginUrl);
        // }
    //   }

    // add the CORS headers to the response
    res.headers.append('Access-Control-Allow-Credentials', "true")
    res.headers.append('Access-Control-Allow-Origin', '*') // replace this your actual origin
    res.headers.append('Access-Control-Allow-Methods', 'GET,DELETE,PATCH,POST,PUT')
    res.headers.append(
        'Access-Control-Allow-Headers',
        'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
    )
    return res
}
// export const config = {matcher:['/private/']};
export const config = {
    matcher: ['/private/'],
};
// /** @type {import('next').NextConfig} */
// const nextConfig = {
//     async headers() {
//         return [
//             {
//                 // matching all API routes
//                 // source: "/api/:path*",
//                 source: "/*",
//                 headers: [
//                     { key: "Access-Control-Allow-Credentials", value: "true" },
//                     { key: "Access-Control-Allow-Origin", value: "*" }, // replace this your actual origin
//                     { key: "Access-Control-Allow-Methods", value: "GET,DELETE,PATCH,POST,PUT" },
//                     { key: "Access-Control-Allow-Headers", value: "X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version" },
//                 ]
//             }
//         ]
//     }
// }
// module.exports = nextConfig