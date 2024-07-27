import React from "react";

export default function Badges({text,type}){
    return(
        <>
            <div className={type == "Main"? "rounded-lg bg-green-400 text-black":"text-white bg-green-600 rounded-sm"}>
                {text}
            </div>
        </>
    )
}