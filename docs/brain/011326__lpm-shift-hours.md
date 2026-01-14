TITLE
LPM SHIFT HOURS — DST-BASED SCHEDULE (MANDATORY)

STATUS
CANONICAL

DATE ADDED
2025-01-13 (mmddyy filename: 011326)

SOURCE
Jon — direct instruction with schedule image

PURPOSE
Define standard shift hours for Papa Surf Burger Bar, based on daylight savings time. This allows automatic calculation of PM shift lengths without requiring explicit hours in every recording.

DEFINITIONS
- AM shift: Morning/lunch shift, always 10:00AM–4:30PM (6.5 hours). This NEVER changes.
- PM shift: Evening shift, 4:30PM–close. Close time varies by day and DST status.
- DST (Daylight Savings Time): Early March through early November.
- Standard Time: Early November through early March.

DAYLIGHT SAVINGS SCHEDULE RULE
Papa Surf hours are dependent on daylight savings time:
- The **Monday following the start of daylight savings**, we switch to DST (summer) hours.
- The **Monday after daylight savings time ends**, we switch back to Standard (offseason) hours.

This means the actual DST transition (Sunday) does not immediately change hours — the change takes effect the following Monday.

DST TRANSITION DATES (Reference)
- DST starts: 2nd Sunday in March → Switch to DST hours on Monday
- DST ends: 1st Sunday in November → Switch to Standard hours on Monday

CORE ASSERTIONS
- AM shift is ALWAYS 6.5 hours (10:00AM–4:30PM). No exceptions.
- PM shift length varies based on day of week and DST status.
- Schedule changes happen on Monday, not on the DST transition day itself.

AM SHIFT HOURS (FIXED)
| Start | End | Duration |
|-------|-----|----------|
| 10:00AM | 4:30PM | 6.5 hours |

This NEVER changes regardless of day or season.

PM SHIFT HOURS — DST (Early March → Early November)
| Day | Open | Close | PM Shift Duration |
|-----|------|-------|-------------------|
| Sunday | 11:00AM | 9:00PM | 4.5 hours |
| Monday | 11:00AM | 9:00PM | 4.5 hours |
| Tuesday | 11:00AM | 9:00PM | 4.5 hours |
| Wednesday | 11:00AM | 9:00PM | 4.5 hours |
| Thursday | 11:00AM | 9:00PM | 4.5 hours |
| Friday | 11:00AM | 10:00PM | 5.5 hours |
| Saturday | 11:00AM | 10:00PM | 5.5 hours |

PM SHIFT HOURS — STANDARD (Early November → Early March)
| Day | Open | Close | PM Shift Duration |
|-----|------|-------|-------------------|
| Sunday | 11:00AM | 8:00PM | 3.5 hours |
| Monday | 11:00AM | 8:00PM | 3.5 hours |
| Tuesday | 11:00AM | 8:00PM | 3.5 hours |
| Wednesday | 11:00AM | 8:00PM | 3.5 hours |
| Thursday | 11:00AM | 8:00PM | 3.5 hours |
| Friday | 11:00AM | 9:00PM | 4.5 hours |
| Saturday | 11:00AM | 9:00PM | 4.5 hours |

RESTAURANT HOURS VS SHIFT HOURS
- Restaurant opens at 11:00AM (customers)
- Shifts start at 10:00AM (staff prep/setup)
- PM shift starts at 4:30PM (handoff from AM)
- Close time = end of PM shift

NON-NEGOTIABLE CONSTRAINTS
- AM shift duration is fixed at 6.5 hours.
- PM shift starts at 4:30PM always.
- Schedule changes only on Mondays following DST transitions.
- These hours apply unless Jon explicitly states different hours in the recording.

ALLOWED BEHAVIORS
- Auto-calculate expected shift hours based on date and day of week.
- Use these hours for tip pool splits when hours are not explicitly stated.
- Flag when stated hours differ significantly from expected hours.

DISALLOWED BEHAVIORS
- Assuming PM hours without checking DST status and day of week.
- Changing AM shift duration for any reason.
- Applying DST hours on the transition Sunday itself.

DECISION TESTS
- Is the date after the Monday following DST start (March)? If yes, use DST hours.
- Is the date after the Monday following DST end (November)? If yes, use Standard hours.
- Is this a Friday or Saturday? If yes, use the later close time.

EXAMPLES
- Pay period Jan 5–11, 2026: Standard time (November–March), so Sun–Thu close at 8PM, Fri–Sat close at 9PM.
- Pay period July 6–12, 2026: DST (March–November), so Sun–Thu close at 9PM, Fri–Sat close at 10PM.
- March 9, 2026 (DST starts on Sunday): Still use Standard hours. Switch to DST hours on Monday March 10.

EDGE CASES & AMBIGUITIES
- If Jon states explicit hours in the recording, use those instead of defaults.
- If a shift ends early (slow night), Jon will mention it.
- If someone works a partial shift, Jon will state their hours.

OPERATIONAL IMPACT
- Enables automatic PM shift hour calculation.
- Reduces need to state hours in every recording.
- Provides baseline for detecting anomalies (e.g., "Kevin worked 2 hours" on a 4.5-hour shift).

CHANGELOG
- v1.0 (2025-01-13): Initial shift hours documentation with DST-based schedule.

CANONICAL SOURCE LANGUAGE
AM shift: 10AM - 4:30PM. This NEVER changes. PM shift: 4:30PM-close (changes based on the day AND based on the time of the year). Our hours are dependent on daylight savings time. The Monday following the start of daylight savings, we will start staying open later. The Monday after daylight savings time ends, we will go back to our offseason hours.
