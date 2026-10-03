/* Dump the deck's resolved SVG diagrams to art.json, so the page and the deck
   cannot drift apart visually. Run: node extract-art.js */
const fs=require("fs"),path=require("path"),vm=require("vm");
const html=fs.readFileSync(path.join(__dirname,"..","session-console","index.html"),"utf8");
const js=html.split("<script>")[1].split("</script>")[0];
const node={innerHTML:"",textContent:"",style:{},classList:{add(){},remove(){},toggle(){}},
  insertAdjacentHTML(){},querySelector:()=>null,querySelectorAll:()=>[],offsetWidth:0};
const ctx={console,setInterval(){},clearInterval(){},setTimeout(){},clearTimeout(){},
  requestAnimationFrame(){},addEventListener(){},Date,Math,JSON,
  URL:{createObjectURL:()=>""},Blob:class{},
  document:{querySelector:()=>node,querySelectorAll:()=>[],createElement:()=>({...node}),
            body:node,fullscreenElement:null,documentElement:node},
  window:{open:()=>null}};
ctx.window=Object.assign(ctx.window,ctx); ctx.globalThis=ctx;
vm.createContext(ctx);
vm.runInContext(js+"\nglobalThis.__ART=ART;",ctx);
fs.writeFileSync(path.join(__dirname,"art.json"),JSON.stringify(ctx.__ART,null,1));
console.log("wrote art.json:",Object.keys(ctx.__ART).join(", "));
