import getUser from "@/app/lib/getUserPosts"
import getUserPosts from "@/app/lib/getUserPosts"
import getAllUsers from "@/app/lib/getAllUsers"
import { Suspense } from "react";
import UserPosts from "./components/UserPosts";
import type { Metadata } from "next";

type Params = {
    params: {
        userId: string
    }
}

export async function generateMetadata({params: { userId } }: Params) {
    const userData: Promise<User> = getUser(userId);
    const user: User = await userData

    if (!user.name) {
        return {
            title: 'User not found',
            description: 'The user you requested does not exist.'
        }
    }

    return {
        title: user.name,
        description: `This is the page of ${user.name}`
    }
}

export default async function UserPage({params: {userId}}: Params, props: User[]) {
    
    console.log("CHECK PROPS!!! ", props);

    console.log("PARAMS USER ID: ", userId)
    
    const userData: Promise<User> = getUser(userId);
    const usersPostsData: Promise<User[]> = getAllUsers();
    // const theUser = (await userData).filter((user: any) => user.id === userId && user)
    const userPostsData: Promise<Post[]> = getUserPosts(userId)
    // console.log("USER DATA? ", userData);
    const user = await userData;
    console.log("HEY USER POSTS!!! ", userData);
    console.log("THE USER: ", userData);
    return (
        <>
        <h1>TEST</h1>
            <h1>{user.name}</h1>
            <div>
                <br />
                <Suspense fallback={<h2>Loading...</h2>}>
                    <UserPosts promise={userPostsData} />
                </Suspense>
            </div>
        </>
    )
}

export async function generateStaticParams() {
    const usersData: Promise<User[]> = getAllUsers()
    const users = await usersData

    console.log("USERS: ", users);

    return users.map(user => ({
        userId: user.id.toString()
    }))
}

