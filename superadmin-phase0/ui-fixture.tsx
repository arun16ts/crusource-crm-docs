// Offline presentation baseline: actual shells/pages, deterministic service data.
// Ancillary CRM effects are disabled by capture-ui.mjs; no production identity.
import React from 'react';
import {createRoot} from 'react-dom/client';
import {QueryClient, QueryClientProvider} from '@tanstack/react-query';
import {Provider} from 'react-redux';
import {NextIntlClientProvider} from 'next-intl';
import {AppRouterContext} from 'next/dist/shared/lib/app-router-context.shared-runtime';
import {PathnameContext, SearchParamsContext} from 'next/dist/shared/lib/hooks-client-context.shared-runtime';
import messages from './src/i18n/locales/en.json';
import {store} from './src/store/store';
import {setSidebarCollapsed} from './src/store/slices/uiSlice';
import {DashboardShell} from './src/components/layout/DashboardShell';
import {AdminPageHeader} from './src/components/admin/shared/AdminPageHeader';
import {Building2} from 'lucide-react';
import SuperAdminLayout from './src/app/superadmin/layout';
import Overview from './src/app/superadmin/dashboard/page';
import Organizations from './src/app/superadmin/organizations/page';
import Feedback from './src/app/superadmin/feedback/page';
import Trials from './src/app/superadmin/trial-extensions/page';
import Logins from './src/app/superadmin/login-history/page';
import {PlatformEntry} from './src/components/superadmin/auth/PlatformEntry';
import {PlatformAccessManagement} from './src/components/superadmin/auth/PlatformAccessManagement';
import {platformHttpClient} from './src/lib/api/platformHttpClient';

const now = '2026-10-09T09:00:00Z';
const org = {id:'org-fixture',name:'Example Workspace',slug:'example-workspace',org_code:'EXAMPLE',subscription_status:'trial',is_active:true,owner_id:'customer-fixture',member_count:6,created_at:now};
const page = (items) => ({items,total:items.length,limit:20,offset:0});
const requests = [{id:'request-fixture',email:'staff@example.test',name:'Example Staff',reason:'Customer support',status:'pending',delivery_status:'not_sent',created_at:now}];
const operators = [{id:'owner-fixture',name:'Example Owner',email:'owner@example.test',is_owner:true,active:true}];
const stats = {total_logins_all_time:42,total_logins_today:3,total_logins_7d:12,total_logins_30d:30,successful_logins_30d:28,failed_logins_30d:2,failure_rate_percentage:6.7,unique_active_users_30d:6,top_organizations:[{org_id:org.id,org_name:org.name,login_count:30}],method_breakdown:{email:30},device_breakdown:{desktop:30}};
const logins = [{id:'login-fixture',org_id:org.id,org_name:org.name,org_slug:org.slug,user_id:'customer-fixture',user_name:'Example Customer',attempted_email:'customer@example.test',login_method:'email',status:'success',failure_reason:null,ip_address:'192.0.2.10',user_agent_raw:null,device_type:'desktop',browser:'Edge',os:'Windows',session_id:null,created_at:now}];
platformHttpClient.get = async (url) => {
  const endpoint = url.split('?')[0];
  if(endpoint === '/superadmin/auth/me') return {...operators[0],csrf_token:'synthetic-csrf'};
  if(endpoint === '/superadmin/auth/requests') return requests;
  if(endpoint === '/superadmin/auth/operators') return operators;
  if(endpoint === '/superadmin/dashboard/kpis') return {total_organizations:4,active_organizations:3,total_users:24,active_users:20,users_by_role:{admin:4,sales_rep:20},subscription_breakdown:{trial:2,active:2},new_orgs_30d:1,new_users_30d:6,total_feedback:1,avg_feedback_rating:4,feedback_30d:1,total_deals:12,total_pipeline_value:24000,total_leads:48,total_contacts:36,total_accounts:8,total_tasks:20,total_meetings:4,total_campaigns:2,total_audit_logs:42,auth_provider_breakdown:{email:20,google:4}};
  if(endpoint === '/superadmin/organizations') return page([org]);
  if(endpoint === '/superadmin/feedback/stats') return {total_count:1,average_rating:4,five_star_count:0,four_star_count:1,three_star_count:0,two_star_count:0,one_star_count:0,category_counts:{suggestion:1}};
  if(endpoint === '/superadmin/feedback') return page([{id:'feedback-fixture',rating:4,category:'suggestion',tags:['navigation'],content:'A shared layout would make navigation more consistent.',trigger_source:'manual',client_metadata:null,user_id:'customer-fixture',user_name:'Example Customer',user_email:'customer@example.test',org_id:org.id,org_name:org.name,created_at:now}]);
  if(endpoint === '/superadmin/trial-extensions') return {...page([]),pending_count:0};
  if(endpoint === '/superadmin/login-history/stats') return stats;
  if(endpoint === '/superadmin/login-history/organizations') return [{id:org.id,name:org.name}];
  if(endpoint === '/superadmin/login-history') return page(logins);
  throw new Error('Unmapped fixture GET: ' + endpoint);
};
const pathname = location.pathname;
const collapsed = new URLSearchParams(location.search).get('collapsed') === 'true';
localStorage.setItem('crusource_sidebar_collapsed',String(collapsed));
store.dispatch(setSidebarCollapsed(collapsed));
const router = {push(){},replace(){},back(){},forward(){},refresh(){},prefetch:async()=>{}};
const client = new QueryClient({defaultOptions:{queries:{retry:false},mutations:{retry:false}}});

function CrmReference() {
  // Actual shell/header/sidebar and heading. Sample body illustrates shared tokens;
  // it is deliberately not represented as a shipped CRM feature page.
  return <DashboardShell><div className="p-6 space-y-5 overflow-auto"><AdminPageHeader title="Workspace reference" subtitle="Synthetic data · current CRM presentation components" icon={Building2} breadcrumbs={['Admin','Workspace']} /><div className="rounded-xl border border-outline overflow-hidden"><table className="w-full text-sm text-left"><thead className="bg-background text-on-surface-variant"><tr><th className="p-4">Workspace</th><th className="p-4">Members</th><th className="p-4">Status</th></tr></thead><tbody><tr><td className="p-4">Example Workspace</td><td className="p-4">6</td><td className="p-4">Active</td></tr></tbody></table></div></div></DashboardShell>;
}
const screens = {'/superadmin/dashboard':<Overview/>,'/superadmin/organizations':<Organizations/>,'/superadmin/feedback':<Feedback/>,'/superadmin/trial-extensions':<Trials/>,'/superadmin/login-history':<Logins/>,'/superadmin/access':<PlatformAccessManagement/>,'/superadmin/login':<PlatformEntry mode="login"/>};
createRoot(document.getElementById('root')).render(<NextIntlClientProvider locale="en" timeZone="UTC" messages={messages}><Provider store={store}><QueryClientProvider client={client}><AppRouterContext.Provider value={router}><PathnameContext.Provider value={pathname}><SearchParamsContext.Provider value={new URLSearchParams(location.search)}>{pathname.startsWith('/dashboard') ? <CrmReference/> : <SuperAdminLayout>{screens[pathname]}</SuperAdminLayout>}</SearchParamsContext.Provider></PathnameContext.Provider></AppRouterContext.Provider></QueryClientProvider></Provider></NextIntlClientProvider>);
