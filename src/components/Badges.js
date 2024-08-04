import React from "react";

export default function Badges({text,type}){
    return(
        <>
            <div className={`ml-2 text-sm ${type === "Main"? "rounded-lg bg-primary text-black px-4 my-2":"text-white my-2 bg-primary rounded-sm"}`}>
                {text}
            </div>
        </>
    )
}