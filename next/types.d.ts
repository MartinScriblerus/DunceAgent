type Post = {
    "userId": number | string,
    "id": number | string,
    "title": string,
    "body": string,
}

type User = {
    map(arg0: (user: User) => { userId: number }): unknown
    "id": number,
    "name": string,
    "username": string,
    "email": string,
    "address": {
        "street": string,
        "suite": string,
        "city": string,
        "zipcode": string,
        "geo": {
            "lat": string,
            "lng": string
        }
    },
    "phone": string,
    "website": string,
    "company": {
        "name": string,
        "catchPhrase": string,
        "bs": string
    }
}