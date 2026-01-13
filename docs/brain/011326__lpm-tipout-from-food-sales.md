TITLE
LPM TIPOUT CALCULATION — FOOD SALES BASED (MANDATORY)

STATUS
CANONICAL

DATE ADDED
2025-01-13 (mmddyy filename: 011326)

SOURCE
Jon — direct instruction

PURPOSE
Define the new tipout calculation method for LPM where tipouts are computed as percentages of food sales rather than being stated explicitly in the audio recording. This changes both the verbal input format and the calculation logic.

DEFINITIONS
- Food sales: The dollar amount of food sold by a server during a shift (distinct from tips earned).
- Tipout: The portion of earnings paid to support staff (utility, bussers, expos).
- Utility: Solo or dual support role handling multiple responsibilities; receives 5% of food sales.
- Busser/Runner: Support staff clearing tables and running food; receives 4% of food sales.
- Expo: Support staff expediting orders; receives 1% of food sales.

CORE ASSERTIONS
- Tipouts are calculated from food sales, not stated explicitly in the recording.
- Jon will provide: server name, total tips (before tipout), and food sales for each server.
- The system calculates tipouts by applying percentage rates to total shift food sales.
- Detail blocks must show individual food sales and the tipout calculation.

NON-NEGOTIABLE CONSTRAINTS
- Utility tipout rate: 5% of total food sales.
- Busser/Runner tipout rate: 4% of total food sales.
- Expo tipout rate: 1% of total food sales.
- These rates are fixed unless explicitly changed by Jon.

ALLOWED BEHAVIORS
- Calculate tipouts from food sales using the defined percentages.
- Split tipouts evenly among multiple support staff in the same role.
- Split tipouts by hours when support staff are in a tip pool (like servers).
- Show each server's individual food sales in detail blocks.
- Show the tipout calculation formula in detail blocks.

DISALLOWED BEHAVIORS
- Using explicitly stated tipout amounts from the recording (old format).
- Calculating tipouts without food sales data.
- Omitting food sales from detail blocks.
- Applying different tipout percentages without explicit instruction.

DECISION TESTS
- Does the recording include food sales for each server? If yes, use this new calculation method.
- Are there multiple support staff in the same role? If yes, split the tipout evenly (or by hours if tip pool).
- Is the tipout rate unclear? If yes, use: Utility 5%, Busser 4%, Expo 1%.

ENFORCEMENT & OVERRIDES
- This rule overrides the previous method of using explicitly stated tipout amounts.
- Food sales-based calculation is mandatory when food sales are provided.
- If food sales are not provided, ask Jon for clarification.

VERBAL INPUT FORMAT (NEW)
Jon will say:
1. Support staff declaration: "Expo was [name], busser was [name]" or "Utility was [name]"
2. For each server: "[Name], tips $[amount], food sales $[amount]"

Example:
"Support staff: Expo was Atticus, bussers were John and Ryan.
Austin Kelley, tips $487.17, food sales $1,271.00.
Brooke Neal, tips $320.57, food sales $1,046.00."

CALCULATION METHOD
1. Sum all servers' food sales for the shift = Total Food Sales
2. Calculate tipouts:
   - Utility tipout = Total Food Sales × 0.05
   - Busser tipout = Total Food Sales × 0.04
   - Expo tipout = Total Food Sales × 0.01
3. Subtract total tipouts from total tips to get pool amount
4. Distribute pool to servers (evenly or by hours)
5. Distribute tipouts to support staff (evenly or by hours)

DETAIL BLOCK FORMAT (NEW)
Each detail block must show:
1. Each server's tips and food sales on separate lines
2. Total food sales for the shift
3. Tipout calculation with formula: "Role X% ($Total) = $Amount"
4. Pool calculation and distribution
5. Final amounts for servers
6. Final amounts for support staff

Example:
[
  "Austin Kelley tips $487.17, food sales $1,271.00",
  "Brooke Neal tips $320.57, food sales $1,046.00",
  "Total food sales: $2,317.00",
  "Tipouts: Busser 4% ($2,317.00) = $92.68, Expo 1% ($2,317.00) = $23.17",
  "Pool after tipout: $807.74 − $115.85 = $691.89 ÷ 2 = $345.95 each",
  "Austin Kelley $345.95, Brooke Neal $345.95",
  "Expo: Atticus Usseglio $23.17",
  "Bussers: John Neal $46.34, Ryan Alexander $46.34"
]

SUPPORT STAFF SPLIT RULES
- Multiple bussers: Split 4% evenly, or by hours if in tip pool
- Multiple expos: Split 1% evenly
- Multiple utility: Split 5% evenly, or by hours if in tip pool
- Single support staff: Receives full percentage amount

EDGE CASES & AMBIGUITIES
- If Jon provides explicit tipout amounts instead of food sales, ask for clarification.
- If support staff hours are mentioned, use hourly split instead of even split.
- If a role is not present (e.g., no expo), that percentage is not deducted.

OPERATIONAL IMPACT
- Changes the verbal input format Jon uses when recording.
- Changes how tipouts are calculated in the parsing phase.
- Changes the detail block format to include food sales and calculation formulas.
- Does NOT change the approval JSON schema or output formats.

CODE REVIEW CHECKLIST
- Is the tipout calculated from food sales using correct percentages?
- Are all servers' individual food sales shown in detail blocks?
- Is the tipout formula shown (e.g., "Busser 4% ($2,317.00) = $92.68")?
- Are support staff splits calculated correctly (even or by hours)?

FAILURE MODES
- Using old explicit tipout amounts when food sales are provided.
- Applying wrong percentage rates.
- Omitting food sales from detail blocks.
- Not splitting support staff tipouts correctly.

CHANGELOG
- v1.0 (2025-01-13): Initial rule — tipouts calculated from food sales.

CANONICAL SOURCE LANGUAGE
From here on out, after I explain the support staff situation, I will say each servers' name, then I will say their total tip amount (before tipout), then I will say each servers' food sales. Use this information to calculate final numbers: Utility employees make 5% of food sales as their tipout; bussers/runners make 4% of food sales as their tipout; expos make 1% of food sales as their tipout. This calculation needs to be represented in the detailed math portion of the tip report. Bussers/utility can also have various hours in a busser/utility tip pool, just like the servers. Multiple utility staff split the 5% evenly. Detail blocks should show each server's individual food sales and show how the tipouts were calculated from it.
