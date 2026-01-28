#!/usr/bin/env python3
"""Process payroll transcript using transrouter payroll agent."""

from transrouter.src.agents.payroll_agent import PayrollAgent
import json

# Read the transcript
with open('/Users/jonathanflaig/mise-core/payroll_agent/LPM/011226_011826.txt', 'r') as f:
    transcript = f.read()

# Initialize agent and parse
agent = PayrollAgent()
result = agent.parse_transcript(
    transcript=transcript,
    pay_period_hint='2026-01-12 to 2026-01-18',
    shift_code=''
)

# Print the full result
print("="*80)
print("FULL RESULT")
print("="*80)
print(json.dumps(result, indent=2))
print("\n")

# Extract and display approval_json
if 'approval_json' in result:
    approval_json = result['approval_json']

    print("="*80)
    print("WEEKLY TOTALS BY EMPLOYEE")
    print("="*80)

    # Calculate totals by employee
    employee_totals = {}

    for shift in approval_json.get('shifts', []):
        for staff_type in ['servers', 'support_staff']:
            for person in shift.get(staff_type, []):
                name = person.get('name', 'Unknown')
                tips = float(person.get('tips', 0))

                if name not in employee_totals:
                    employee_totals[name] = {
                        'tips': 0.0,
                        'shifts': 0
                    }

                employee_totals[name]['tips'] += tips
                employee_totals[name]['shifts'] += 1

    # Print totals sorted by employee name
    for name in sorted(employee_totals.keys()):
        totals = employee_totals[name]
        print(f"{name:20s} - {totals['shifts']:2d} shifts - ${totals['tips']:8.2f}")

    print("\n")
    print("="*80)
    print("FULL APPROVAL JSON")
    print("="*80)
    print(json.dumps(approval_json, indent=2))
else:
    print("ERROR: No approval_json found in result")
