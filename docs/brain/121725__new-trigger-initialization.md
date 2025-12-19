TITLE
"NEW" TRIGGER — CLAUDE INITIALIZATION PROTOCOL

STATUS
CANONICAL

DATE ADDED
2024-12-17 (mmddyy filename: 121725)

SOURCE
Jon — direct instruction

PURPOSE
Define a trigger phrase "new" that causes Claude to read and execute the initialization protocol from mise-core/claude_new file. This provides a single-word command to reset/reinitialize Claude's understanding of the Mise repository and workflow protocols.

DEFINITIONS
- Trigger phrase: The single word "new" typed alone by the user
- claude_new file: Repository file at /Users/jonathanflaig/mise-core/claude_new containing initialization instructions
- Initialization protocol: The process of reading all repo documentation, understanding architecture, and confirming readiness

CORE ASSERTIONS
- When the user types ONLY the word "new", Claude must read /Users/jonathanflaig/mise-core/claude_new and execute its contents as instructions
- The trigger uses ABSOLUTE PATHS and works regardless of current working directory
- The trigger ALWAYS refers to the mise-core repository at /Users/jonathanflaig/mise-core
- The trigger is case-sensitive: "new" (all lowercase)
- The trigger requires exact match: only the word "new" alone, no other text
- This trigger takes precedence over normal conversation flow

NON-NEGOTIABLE CONSTRAINTS
- Must read claude_new file when triggered
- Must execute all steps in claude_new as written
- Must confirm completion as specified in claude_new
- Cannot skip or abbreviate the initialization process

ALLOWED BEHAVIORS
- Read /Users/jonathanflaig/mise-core/claude_new when user types "new" (absolute path, works from any directory)
- Execute each step in the initialization protocol using absolute paths to mise-core
- Read all documentation from /Users/jonathanflaig/mise-core as specified
- Search mise-core repository before asking questions
- Assume mise-core is the working context unless explicitly told otherwise
- Confirm when initialization is complete

DISALLOWED BEHAVIORS
- Ignoring the "new" trigger
- Treating "new" as normal conversation
- Skipping any initialization steps
- Proceeding with tasks before completing steps 1-2 of initialization

DECISION TESTS
- Did user type exactly "new" with no other words? If yes → trigger initialization
- Is the trigger word part of a larger sentence? If yes → do not trigger
- Has claude_new been read? If no → read it immediately
- Have all initialization steps been completed? If no → continue until done

ENFORCEMENT & OVERRIDES
- This trigger overrides normal conversation flow
- Initialization steps must be completed in order
- Cannot proceed with other tasks until initialization confirms ready
- Approval token remains apostrophe (')

EXAMPLES
User input: "new"
→ Claude reads mise-core/claude_new and executes initialization protocol

User input: "Can you create a new feature?"
→ Normal conversation, not a trigger (word "new" is part of larger sentence)

User input: "new file"
→ Not a trigger (contains additional words)

NON-EXAMPLES
- User says "I need a new approach" → not a trigger
- User says "NEW" (uppercase) → not a trigger (case-sensitive)
- User says "new." → not a trigger (has punctuation)

EDGE CASES & AMBIGUITIES
- If "new" appears with only punctuation (e.g., "new." or "new?"), treat as trigger
- If user says "new" in the middle of a conversation, still trigger initialization
- If initialization is already complete in current session, still re-run when triggered
- Works from ANY directory - always uses absolute path /Users/jonathanflaig/mise-core
- User does NOT need to cd into mise-core first - trigger handles this automatically

OPERATIONAL IMPACT
- Provides quick way to reset Claude's context for the Mise repository
- Ensures consistent initialization across sessions
- Reduces need to manually repeat onboarding instructions
- Standardizes the initialization protocol

CODE REVIEW CHECKLIST
- Is trigger detection case-sensitive and exact match?
- Does trigger read mise-core/claude_new file?
- Are all initialization steps executed in order?
- Is confirmation provided when ready?
- Are other tasks blocked until initialization complete?

FAILURE MODES
- Not detecting "new" trigger → initialization not run
- Treating "new" as conversation → missing initialization
- Skipping initialization steps → incomplete setup
- Proceeding before ready → violates protocol

CHANGELOG
- v1.0 (2024-12-17): Initial "new" trigger protocol created

CANONICAL SOURCE LANGUAGE
Any time I type ONLY the word "new", I want you to automatically use the contents of "claude_new" as instructions. The file is located at /Users/jonathanflaig/mise-core/claude_new. When triggered, read the file and execute all steps as written using ABSOLUTE PATHS. The "new" trigger should ALWAYS trigger the whole process of ingesting the information contained in "mise-core" regardless of current working directory. Just assume we're in mise-core - the trigger always works with absolute paths to /Users/jonathanflaig/mise-core. Do not proceed with any task until you have completed steps 1-2 of the initialization protocol. Confirm when ready.
