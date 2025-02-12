import NextAuth from "next-auth/next";
import type { User } from 'next-auth';
import type { AuthOptions } from "next-auth";
import CredentialsProvider from 'next-auth/providers/credentials';
import { authenticate } from "@/services/authenticate";
import GoogleProvider from 'next-auth/providers/google';
import GithubProvider from 'next-auth/providers/github';

// console.log("sanity: ", process.env.NEXTAUTH_SECRET)

const googlelientId = process.env.GOOGLE_CLIENT_ID as string;
const googleClientSecret = process.env.GOOGLE_CLIENT_ID as string;
const githubClientId = process.env.GITHUB_CLIENT_ID as string;
const githubClientSecret = process.env.GITHUB_CLIENT_SECRET as string;

const authOptions: AuthOptions = {
    providers: [
        GoogleProvider({
            clientId: googlelientId,
            clientSecret: googleClientSecret,
        }),
        GithubProvider({
            clientId: githubClientId,
            clientSecret: githubClientSecret,
        }),
        CredentialsProvider({
            name: 'credentials',
            credentials: {
                email: {
                    name: 'email',
                    label: 'email',
                    type: 'email',
                    placeholder: 'Email'
                },
                password: {
                    name: 'password',
                    label: 'password',
                    type: 'password',
                    placeholder: 'Password'
                }
            },
            async authorize(
                credentials: Record<"email" | "password", string> | undefined,
                req: any
            ): Promise<User | null> {
                if (typeof credentials !== "undefined") {
                    const res: any = await authenticate({
                        email: credentials.email,
                        password: credentials.password,
                    });

                    if (typeof res !== "undefined") {
                        if (res.error === "invalid_password") {
                            throw new Error("Invalid password");
                        } else if (res.error === "invalid_user") {
                            throw new Error("Invalid user");
                        } else {
                            return { ...res };
                        }
                    } else {
                        throw new Error("Unknown error");
                    }
                } else {
                    throw new Error("Missing credentials");
                }
            },
        })
    ],
    session: { strategy: 'jwt' },
    secret: process.env.NEXTAUTH_SECRET,

    callbacks: {
        async jwt({ token, user, account }: any) {
            if (user && account) {
                return { ...token, ...user };
            }
            return token
        },
        async session({ session, token }) {
            session.user = token;
            return session;
        },
        
        async redirect({ url, baseUrl }: { url: string; baseUrl: string }) {
            console.log("Redirecting to " + baseUrl + "/private");
            // Redirect users to the dashboard or a default page after sign-in
            if (url.startsWith(baseUrl)) {
                return baseUrl + "/private";
            }
            return baseUrl;
        }
    },
    pages: {
        signIn: '/login',
        signOut: '/logout',
    }
};

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };