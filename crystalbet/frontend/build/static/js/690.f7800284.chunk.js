"use strict";(self.webpackChunkcrystalbet=self.webpackChunkcrystalbet||[]).push([[690],{4690:(e,s,l)=>{l.r(s),l.d(s,{default:()=>r});var t=l(5043),c=l(8729),n=l(2188),a=l(9443),i=l(579);const o=e=>{let{liveBets:s}=e;return 0===s.length?(0,i.jsx)("div",{children:"No live bets available"}):(0,i.jsx)("div",{className:"grid grid-cols-1 gap-4",children:s.map((e=>(0,i.jsxs)("div",{className:"p-4 bg-white shadow rounded",children:[(0,i.jsx)("h3",{className:"text-xl font-bold",children:e.match}),(0,i.jsxs)("p",{children:["Odds: ",e.odds]}),(0,i.jsxs)("p",{children:["Stake: ",e.stake]})]},e.id)))})};var d=l(8224);const r=()=>{const{loading:e}=(0,t.useContext)(c.c),{liveBets:s,loading:l,setLiveBets:r,fetchLiveBets:x}=(0,t.useContext)(n.d);return(0,t.useEffect)((()=>{x();const e=new WebSocket("ws://localhost:8000/ws/live");return e.onmessage=e=>{const s=JSON.parse(e.data);r(s)},e.onclose=()=>{console.log("WebSocket connection closed")},()=>{e.close()}}),[x,r]),e||l?(0,i.jsx)("div",{children:"Loading..."}):(0,i.jsxs)("div",{className:"min-h-screen flex flex-col bg-gray-100",children:[(0,i.jsx)(a.A,{}),(0,i.jsx)("main",{className:"flex-1 container mx-auto p-4",children:(0,i.jsxs)("section",{className:"mb-8",children:[(0,i.jsx)("h2",{className:"text-2xl font-bold mb-4",children:"Live Bets"}),(0,i.jsx)(o,{liveBets:s})]})}),(0,i.jsx)(d.A,{})]})}}}]);
//# sourceMappingURL=690.f7800284.chunk.js.map