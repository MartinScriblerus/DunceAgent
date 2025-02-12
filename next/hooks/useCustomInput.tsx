"use client";

import React, { Dispatch, FormEventHandler, SetStateAction, useState } from "react";

type formInputProps = {
    handleFormInputChange: (name: string) => void,
    handleFormSubmit: (dbName: FormEventHandler<HTMLFormElement>) => void,
    formInput:string,
    setFormInput: Dispatch<SetStateAction<string>>
    formIsLoading: boolean,
    setFormIsLoading: Dispatch<SetStateAction<boolean>>,
    formPlaceholder: string,
}


const FormInput = (props: formInputProps) => {
    const { formInput, handleFormInputChange, handleFormSubmit, formPlaceholder } = props;
    return (
    <div className="w-full" key="editor1">
        <form  onSubmit={(e:any) => handleFormSubmit(e)} className="flex w-full flex-col">
            <div className="flex w-full">
            {/* {intemediateStepsToggle} */}

                <div className="flex w-full mt-4">
                    <input
                        className="grow w-full p-4 rounded"
                        value={formInput}
                        placeholder={formPlaceholder}
                        onChange={(e: any) => handleFormInputChange(e)}
                        // onLoading={formIsLoading}
                    />
                </div>
            </div>
        </form>
    </div>
    )
}
export default FormInput;