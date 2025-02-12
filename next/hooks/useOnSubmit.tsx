import { signIn } from "next-auth/react";
import { SetStateAction } from "react";

const onSubmit = async (e: React.FormEvent<HTMLFormElement>, formData: { password: string; email: string; }, setIsPassInvalid: React.Dispatch<SetStateAction<boolean>>, setInvalidUser: React.Dispatch<SetStateAction<boolean>>) => {
    e.preventDefault();

    try {
        const res = await signIn('credentials', {
            email: formData.email,
            password: formData.password,
            redirect: false,
        });

        if (res?.error === 'Invalid password') {
            setIsPassInvalid(true);
            return false;
        } else if (res?.error === 'Invalid user') {
            setInvalidUser(true);
            return false;
        } else {
            return true;
        }
    } catch (error) {
        console.log('signIn had an error', error)
    }
};
export default onSubmit;
