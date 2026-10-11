# Phase 4 UI review

Actual Next.js pages and FastAPI guards were exercised with synthetic identities and in-memory records. Screenshots use the application's real stylesheet and fonts. They are local integration evidence, not deployed screenshots.

| Surface                                              | Captures                                                                                                                                                       |
| ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Persisted English public submission                  | [Public success](screenshots/public-success.png)                                                                                                               |
| Dutch public form                                    | [1440](screenshots/public-nl-1440.png), [1024](screenshots/public-nl-1024.png), [768](screenshots/public-nl-768.png), [390](screenshots/public-nl-390.png)     |
| Board and mobile stage view                          | [1440](screenshots/demo-board-1440.png), [1024](screenshots/demo-board-1024.png), [768](screenshots/demo-board-768.png), [390](screenshots/demo-board-390.png) |
| Persisted assignment/schedule/follow-up/note/history | [Detail](screenshots/demo-detail.png)                                                                                                                          |
| URL-restored server-paginated list                   | [List](screenshots/demo-list.png)                                                                                                                              |

The implementation layout is public introduction/form/receipt; staff header/view controls/filter grid followed by independently loaded stage columns or server table; and detail contact/workflow panels followed by separate notes/activity pages. Each write opens the shared ActionDialog. On mobile, the board shows the selected stage and uses the same accessible Move to stage control. Scheduling explicitly labels UTC time and records the contact timezone. Preferred contact text is shown separately.

The route regression waits for responsive frame transitions and verifies main-content bounds as well as document overflow. A transient screenshot captured during the 300 ms frame transition is not counted as mobile acceptance. Portable browser fixtures cover lost-response retry, version conflicts, read-only controls and stale refresh errors separately.
