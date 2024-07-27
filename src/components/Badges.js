import React from "react";

export default function Badges({text,type}){
    return(
        <>
            <div className={`ml-2 text-sm ${type === "Main"? "rounded-lg bg-green-400 text-black px-4 my-2":"text-white my-2 bg-green-600 rounded-sm"}`}>
                {text}
            </div>
        </>
    )
}