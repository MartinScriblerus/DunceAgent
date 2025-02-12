import { signIn } from "next-auth/react";
import { SetStateAction } from "react";
export const handleSubmit = async (e: React.FormEvent<HTMLFormElement>, formData: any, setIsLogged: React.Dispatch<SetStateAction<boolean>>, setInvalidUser: React.Dispatch<SetStateAction<boolean>>, setIsPassInvalid: React.Dispatch<SetStateAction<boolean>>) => {
    e.preventDefault();

    try {
        const res = await signIn('credentials', {
            email: formData.email,
            password: formData.password,
            redirect: false,
        });

        if (res?.error === 'Invalid password') {
            setIsPassInvalid(true);
        } else if (res?.error === 'Invalid user') {
            setInvalidUser(true)
        } 
        // else {
        //     setIsLogged(true);
        // }

    } catch (error) {
        console.log('signIn had an error', error)
    }
};
