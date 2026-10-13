import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {createServer} from 'node:http';
import {readFile, readdir, mkdir, writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {createHash} from 'node:crypto';

const directory = path.dirname(fileURLToPath(import.meta.url));
const frontend = path.resolve(directory,'../../crusource-crm-frontend');
const require = createRequire(path.join(frontend,'package.json'));
const {build} = require('esbuild');
const postcss = require('postcss');
const tailwind = require('@tailwindcss/postcss');
const {chromium} = require('playwright');
const output = path.join(directory,'screenshots');
await mkdir(output,{recursive:true});

// Replace domain effects only; shell, sidebar, header and platform pages stay real.
const emptyNames = ['GlobalModalManager','TrialExpiryBanner','TrialExpiredLockout','OnboardingTopBar','OnboardingChecklistDrawer','SpotlightTourOverlay','FeedbackPulseToast','LoopAISidePanel','FloatingImportProgress','DeleteProgress','GlobalSearchModal','NotificationDropdown','HeaderImportStatus'];
const effectHooks = {
  useSSEListener: 'export const useSSEListener=()=>{};',
  useBilling: 'export const useBillingSubscriptionQuery=()=>({data:{is_trial_expired:false}});',
  useMyPermissions: 'export const useMyPermissions=()=>({isSuperAdmin:false,permissions:{is_admin:true,is_super_admin:false,modules:{},fields:{},teamspace:{}}});',
  useCurrentUser: 'export const useCurrentUser=()=>({user:{id:"customer-fixture",name:"Example Customer",email:"customer@example.test",role:"admin"}});',
  usePendingRequestCounts: '',
  useTeamspaceQueries: 'export const usePendingRequestCounts=()=>({data:{total_pending:0}});',
  useOrganization: 'export const useOrganization=()=>({organization:{name:"Example Workspace"}});',
  useInboxQueries: 'export const useInboxReplyCountQuery=()=>({data:{count:0}});',
};
const stubs = [];
const bundle = await build({stdin:{contents:await readFile(path.join(directory,'ui-fixture.tsx'),'utf8'),resolveDir:frontend,loader:'tsx'},outfile:'fixture.js',bundle:true,write:false,platform:'browser',format:'iife',tsconfig:path.join(frontend,'tsconfig.json'),define:{'process.env':'{"NODE_ENV":"development"}'},plugins:[{
  name:'phase0-offline-effects',setup(build){
    build.onResolve({filter:/.*/},args=>{
      const name = path.basename(args.path).replace(/\.tsx?$/,'');
      if(emptyNames.includes(name)||Object.hasOwn(effectHooks,name)) return {path:name,namespace:'phase0-stub'};
    });
    build.onLoad({filter:/.*/,namespace:'phase0-stub'},args=>{
      stubs.push(args.path);
      return {contents:effectHooks[args.path] ?? `export const ${args.path}=()=>null;`,loader:'js'};
    });
  }
}],loader:{'.css':'local-css'}});
let css = (await postcss([tailwind({base:frontend})]).process(await readFile(path.join(frontend,'src/app/globals.css'),'utf8'),{from:path.join(frontend,'src/app/globals.css')})).css;
css += '\n' + bundle.outputFiles.filter(f=>f.path.endsWith('.css')).map(f=>f.text).join('\n');
// Resolve the cached Next font by its declared family, rather than guessing a file.
const chunks = path.join(frontend,'.next/static/chunks');
let fontName;
for(const entry of await readdir(chunks)){
  if(!entry.endsWith('.css')) continue;
  const content = await readFile(path.join(chunks,entry),'utf8');
  for(const face of content.matchAll(/@font-face\s*\{[^}]+\}/g)){
    if(/Instrument[_ ]Sans/i.test(face[0]) && /unicode-range:U\+(?:\?\?|0-FF|0000-00FF)/i.test(face[0])){
      fontName = face[0].match(/([^/"')]+\.woff2)/)?.[1];
      if(fontName) break;
    }
  }
  if(fontName) break;
}
assert.ok(fontName,'Build cache must contain the installed Instrument Sans latin font. Run the normal frontend build first.');
const font = await readFile(path.join(frontend,'.next/static/media',fontName));
css += '\n@font-face{font-family:"Phase0 Instrument Sans";font-style:normal;font-weight:100 900;font-display:block;src:url("/fixture-font.woff2") format("woff2")} :root{--font-sans:"Phase0 Instrument Sans",sans-serif}';
const script = bundle.outputFiles.find(f=>!f.path.endsWith('.css')).text;
const loopIcon = await readFile(path.join(frontend,'public/images/loop-ai.webp'));
const server = createServer((request,response)=>{
  const resources = {'/fixture.js':['text/javascript',script],'/fixture.css':['text/css',css],'/fixture-font.woff2':['font/woff2',font],'/images/loop-ai.webp':['image/webp',loopIcon]};
  const resource = resources[request.url] ?? ['text/html','<!doctype html><html lang="en"><head><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="/fixture.css"></head><body><div id="root"></div><script src="/fixture.js"></script></body></html>'];
  response.setHeader('Content-Type',resource[0]);response.end(resource[1]);
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
let browser;
const captures=[];
const externalRequests=[];
try {
  browser=await chromium.launch({channel:process.platform==='win32'?'msedge':undefined,headless:true});
  const context=await browser.newContext({locale:'en-US',timezoneId:'UTC',reducedMotion:'reduce',deviceScaleFactor:1});
  await context.route('**/*',route=>{
    const url=new URL(route.request().url());
    if(url.hostname!=='127.0.0.1'){externalRequests.push(url.origin);return route.abort();}
    if(url.pathname.startsWith('/api/')||url.pathname.startsWith('/public/')) throw new Error('Unstubbed application request: '+url.pathname);
    return route.continue();
  });
  const routes = ['dashboard/reference','superadmin/dashboard','superadmin/organizations','superadmin/access','superadmin/login','superadmin/login-history','superadmin/feedback','superadmin/trial-extensions'];
  for(const [width,height] of [[1440,1000],[768,1000],[390,844]]){
    for(const route of routes){
      const page=await context.newPage();const errors=[];
      page.on('pageerror',error=>errors.push(error.message));
      await page.setViewportSize({width,height});
      await page.goto(`http://127.0.0.1:${server.address().port}/${route}`,{waitUntil:'networkidle'});
      await page.evaluate(()=>document.fonts.ready);
      assert.ok(await page.evaluate(()=>document.fonts.check('16px "Phase0 Instrument Sans"')));
      assert.equal(errors.length,0,`${route}: ${errors.join('; ')}`);
      await page.locator('h1').first().waitFor();
      assert.equal(await page.locator('img').evaluateAll(images=>images.filter(image=>!image.complete||image.naturalWidth===0).length),0,'Reference images must load');
      const metrics=await page.evaluate(()=>({font:getComputedStyle(document.body).fontFamily,viewport:innerWidth,documentWidth:document.documentElement.scrollWidth,sidebarWidth:document.querySelector('aside')?.getBoundingClientRect().width ?? null,heading:document.querySelector('h1')?.textContent}));
      const filename=route.replaceAll('/','-')+'-'+width+'.png';
      await page.screenshot({path:path.join(output,filename),fullPage:true,animations:'disabled'});
      captures.push({file:filename,route,width,height,...metrics});
      if(route==='dashboard/reference'&&width===1440){
        await page.goto(`http://127.0.0.1:${server.address().port}/${route}?collapsed=true`,{waitUntil:'networkidle'});
        await page.screenshot({path:path.join(output,'dashboard-reference-collapsed-1440.png'),fullPage:true,animations:'disabled'});
        captures.push({file:'dashboard-reference-collapsed-1440.png',route,width,height,sidebarWidth:await page.locator('aside').evaluate(e=>e.getBoundingClientRect().width)});
      }
      await page.close();
    }
  }
  const report={status:'offline presentation baseline; not full Next.js route/auth/e2e proof',browser:browser.version(),locale:'en-US',timezone:'UTC',fontFile:fontName,fontSha256:createHash('sha256').update(font).digest('hex'),disabledCrmEffects:[...new Set(stubs)].sort(),blockedExternalOrigins:[...new Set(externalRequests)],captures};
  await writeFile(path.join(directory,'ui-captures.json'),JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify({captures:captures.length,browser:report.browser,externalOrigins:report.blockedExternalOrigins}));
} finally {await browser?.close();await new Promise(resolve=>server.close(resolve));}
