const fs=require('fs'),vm=require('vm'),path=require('path');
const root=__dirname,window={};
const scripts=['data.js','data-en.js','translation-fixes.js','data-tw.js','religion.js','religion-tw.js','figures.js','figures-tw.js','i18n.js','i18n-tw.js','reading.js','reading-tw.js','guides.js','guides-tw.js','curriculum.js','curriculum-tw.js','study-i18n.js','study-i18n-tw.js','story-addons.js','story-addons-tw.js'];
for(const f of scripts)vm.runInNewContext(fs.readFileSync(path.join(root,f),'utf8'),{window},{filename:f});
const figures=[...window.FIGURES_EAST,...window.FIGURES_WEST,...window.FIGURES_WORLD];
const myths=[...window.MYTHS,window.CHRISTIANITY_CN].map(m=>({...m,stories:[...m.stories,...(window.STORY_ADDONS[m.id]||[])]}));
const output={myths,figures,reading:window.READING,guides:window.GUIDES,curriculum:window.CURRICULUM,ui:{...window.UI_CN,...window.STUDY_UI_CN}};
fs.writeFileSync(path.join(root,'site-data.json'),JSON.stringify(output));
console.log(JSON.stringify({traditions:myths.length,figures:figures.length,stories:myths.reduce((n,m)=>n+m.stories.length,0),simplified:window.UI_CN.faithFigures,traditional:window.UI_TW.faithFigures},null,2));
