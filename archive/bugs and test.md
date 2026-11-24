##### **Initial Changes:**

~~in the imports feature of all the modules, if items gets rejected for any case, for example lets say a data is rejected because it has missing data, and that data is  a mandatory, we have to allow the rejected data to be downloaded as a separate csv and excel, so that they can fill that data and re-upload it. it will be easy for the user this way right.~~



~~in leads, on Kanban view, we show the status also in the cell, where it hides the name. So remoe that status inside the cells~~



~~in the imports module, have a button for Map using AI, where AI will study the colomsna dn rows of the incoming data, it will have knolodge of the CRM filds, So it will automatically map those fileds, so that no data is missied.~~



~~have a separate tour and description for AI capabilities in the CRM~~



~~in the reports section, admin profile can see all the reports that are created by manager and standard profile, that is good. in a team, if a standard profile creates a report, and the reporting manager cannot see that reports that was created by the standardprofile.~~



~~redesign the tour, make is short and useful of the user, current it just highlights the section name, but not visually showing the UI, this is mainly in the AI tour. remove the starts in the settings of the tour, it gives a AI feel.~~



~~remove the superadmin implementation in the crm application, its a dead code right, we have a central super admin now~~



~~reports section saved views and filter UI refactor, reports section, duplicate export in the table. import of report section has to have UI refactor.~~



##### TO-DO:



workflow automation and dynamic custom fields and mandatory fields



website connection



in the login page, we should have captcha, MFA using authenticator



in leads converted tracking is needed, because most data from other crm has that ID, so we will also get and use accordingly.



Use the slug url somewhere, initial idea is to use them in the share a doc, others has to be brainstormed and used.



"eye" button on the respective modules and functions, on-click, the knowledge base opens and guides the user.



while importing, we have to give them the option to split and assign, I was thinking of the print function, where based on the page number, I can skip few page and then take print, in the excel sheet, we have the cell number right, can we use that, because lets say I am importing 7k data, I was to split and assign it while importing, what are my options to do it. in the imports of all the modules, we have to as them a option to add the import to private or public (team visiliablity).



documents section is completely private and even the manager cannot see it.



teamspace in the profiles and permissions has to have a UI refactor



teamspace filters refactor.



from lead bulk convert to deal, ask value for each deal.



remove the "Export selected" duplicate in deals section.



##### **Review meet in 14/11/26:**



**Info:** AIR - is lead gen tool the internal team uses



**Changes and Bugs:**



~~the add user buton is brought down, just like the task section.~~



~~the delete functions in the users section, the delete button should not be aviliable for person avobe the role herichy~~



~~I cannot invite users higher than my role and hirechy~~



~~request a export in the module level~~



~~the favicon is not shown in the safiry browser~~



~~the lead progress is not shown in the timeline, and the status is not shown in the list view~~



~~if I do some activity in the google products, it should show the activity in the crm, sunc both the ways.~~



~~first date in the meets, calls~~

#### 

~~sow, op (statement of work, purpchase of work)~~



~~leads table size and height has been changed, make it similar to that on prod. and in Kanban view, we ask permission to stage back, but in the detail drawer, if I give previous stage, it just does it without asking for confirmation or warning.~~



~~duplicate contacts are allowed, check that, on lead import also, the contact exasit in crm, yet it import lead.~~



stop or pause email campigne. how to add email alises, so that the actual domain is not flagged as spam.

