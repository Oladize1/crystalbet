import React from "react";
import Badges from "./Badges";

export default function Macthes(){
    return(
        <>
            <section>
                <h1>Norvegia - Eliteserien</h1>
                <div className="flex space-x-3">
                    <Badges text={"2nd Half"} type={"Main"}/>
                    <Badges text={"TV"} type={"Sub"}/>
                </div>
                <div className="w-100 justify-between">
                    <div>
                        <p className="text-white">West Ham United</p>
                        <p className="text-white">Chelsea FC</p>
                    </div>
                    <div>
                        <p className="text-white">2</p>
                        <p className="text-white">0</p>
                    </div>
                </div>
            </section>
        </>
    )
}