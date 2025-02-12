export default async function getUserPosts(userId: string) {
    const res = await fetch(`https://jsonplaceholder.typicode.com/posts?userId=${userId}`, 
        // {cache: 'force-cache'} // SSG
        // { next: { revalidate: 60}}
        {cache: 'no-store'} // SSP
    )

    if (!res.ok) throw new Error('failed to fetch user');

    return res.json();
}