import jwt from 'jsonwebtoken';
const secretKey = 'createAGenericToken';
const fakeUser = {  
    email: "test@test.com",
    password: "test",
  };

export const authenticate = async (credentials: {
    email: string;
    password: string;
}) => {
    const { email, password } = credentials;
    
    if (email === fakeUser.email && password === fakeUser.password) {
        const accessToken = jwt.sign({email:email}, secretKey, {expiresIn:'1h'})
        return {
            status: 202,
            token: accessToken,
            email: fakeUser.email,
        };
    } else if (email === fakeUser.email && password !== fakeUser.password) {
        return {
            status: 404,
            error: "invalid_password",
        };
    } else {
        return {
            status: 404,
            error: "invalid_user",
        };
    }
};