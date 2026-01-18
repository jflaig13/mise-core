# Investor Question Bank
## 150 Questions with Responses & Explanations

---

# MARKET & OPPORTUNITY

## 1. "What's your TAM, SAM, and SOM?"

**Response:** "TAM is $7.2B — the US restaurant management software market. SAM is $800M — independent restaurants with 10-100 employees. SOM is $8M — restaurants in Texas using voice/mobile-first tools. We're starting hyperlocal and expanding."

**Why this works:** TAM = Total Addressable Market (everyone who could theoretically buy). SAM = Serviceable Addressable Market (the segment you can realistically reach). SOM = Serviceable Obtainable Market (what you can actually capture in 2-3 years). Investors want to see you understand the difference.

---

## 2. "Why now? What's changed that makes this the right time?"

**Response:** "Three things: AI transcription hit 95%+ accuracy in 2024, labor costs are at historic highs forcing automation, and restaurant managers are finally smartphone-native. Five years ago, voice-to-payroll wasn't technically possible. Five years from now, someone else will have done it."

**Why this works:** "Why now" tests whether you understand market timing. Many good ideas fail because they're too early or too late. Show the tailwinds.

---

## 3. "How do you know restaurants will pay for this?"

**Response:** "Because Papa Surf already is. We're deployed, processing real payroll weekly. The manager saves 3+ hours per week. At $20/hour loaded cost, that's $3,000/year in time savings for a tool that'll cost $1,200/year."

**Why this works:** Willingness to pay is proven by actual payment, not surveys. Having one paying customer beats 100 "I would definitely pay for that" responses.

---

## 4. "What happens if OpenAI/Google builds this?"

**Response:** "They'll build horizontal tools, not vertical solutions. Google won't build tip pooling logic for Texas restaurants. Our moat is domain expertise — knowing that a 'utility' replaces expo+busser at 5%, that PM shifts have variable closing times, that managers say 'COVID' when they mean 'Coben.' That's thousands of micro-decisions big tech won't make."

**Why this works:** Platform risk is real. Your answer should show why your vertical depth protects you from horizontal players.

---

## 5. "Who's your ideal customer profile?"

**Response:** "Independent full-service restaurants, 15-40 employees, $1-5M revenue, Texas-based, owner-operated. They're big enough to have payroll pain, small enough to not afford a full-time bookkeeper, and the owner is hands-on enough to adopt new tools."

**Why this works:** ICP (Ideal Customer Profile) shows you know who to target. Vague answers like "restaurants" signal you haven't done the work.

---

## 6. "What's your unfair advantage?"

**Response:** "I ran restaurant ops for years. I know the pain viscerally — not from interviews, from living it. Plus I built the entire product myself, so our burn rate is near zero. We can iterate faster than any VC-backed competitor burning $200k/month on engineers."

**Why this works:** Unfair advantages are things competitors can't easily copy: proprietary data, unique relationships, founder expertise, or structural cost advantages.

---

## 7. "How big can this get?"

**Response:** "Base case: $5M ARR serving 2,500 restaurants in Texas. Bull case: We expand to all restaurant back-office ops — scheduling, inventory, forecasting — and become the Toast for independent restaurants. That's a $100M+ outcome."

**Why this works:** Investors need to see a path to a return that matters for their portfolio. A $5M exit doesn't move the needle for most funds.

---

## 8. "What's your go-to-market strategy?"

**Response:** "Land and expand in Texas first. Direct sales to owner-operators through restaurant associations and local networking. Once we have 50 customers, we add a self-serve trial. Our CAC should be under $500 because the product demos itself in 60 seconds."

**Why this works:** GTM (Go-to-Market) shows how you'll acquire customers. Investors want to see a realistic, capital-efficient plan — not "we'll go viral."

---

## 9. "What are the barriers to entry?"

**Response:** "Low technical barriers, high domain barriers. Anyone can build transcription + math. But knowing how tip pooling actually works, handling partial tipouts, integrating with restaurant workflows — that's years of embedded knowledge."

**Why this works:** Barriers to entry protect your business from competition. Be honest if they're low technically, but show where the real moat is.

---

## 10. "What trends could kill this business?"

**Response:** "If restaurants eliminate tipping entirely — which some are trying — tip calculation becomes irrelevant. Also, if major POS systems build native voice features. We mitigate by expanding beyond tips into full back-office operations."

**Why this works:** This tests self-awareness. Investors respect founders who understand existential risks and have mitigation plans.

---

# PRODUCT & TECHNOLOGY

## 11. "Walk me through the technical architecture."

**Response:** "Mobile web app (FastAPI + Jinja2), audio hits our transrouter which uses OpenAI Whisper for transcription, then Claude parses the transcript into structured payroll data. Results go to Google Sheets for approval. All deployed on Google Cloud Run, scales to zero when idle."

**Why this works:** Shows you actually built it and understand your stack. Red flag if a "technical founder" can't explain their own architecture.

---

## 12. "What's your tech debt situation?"

**Response:** "Moderate and intentional. We hardcode some business logic that should be configurable, and our test coverage is around 40%. But we're pre-product-market-fit — speed matters more than perfection right now. I track debt in the codebase and will address it post-funding."

**Why this works:** Tech debt is normal. Investors worry if you either deny having any (naive) or have so much you can't ship features (paralyzed).

---

## 13. "How accurate is the transcription?"

**Response:** "Whisper gets us 95%+ accuracy on clear audio. The real work is downstream — normalizing 'COVID' to 'Coben,' handling partial tipouts, calculating pools. We've built correction logic that catches most errors before they hit payroll."

**Why this works:** AI accuracy questions test whether you understand failure modes and have built safeguards.

---

## 14. "What happens when it gets something wrong?"

**Response:** "Every submission goes through an approval screen. The manager sees the parsed data, can edit any field, and confirms before it hits payroll. We're augmenting the manager, not replacing their judgment."

**Why this works:** Human-in-the-loop design shows maturity. Investors are wary of AI that runs unsupervised on critical workflows.

---

## 15. "Can this scale to thousands of restaurants?"

**Response:** "Architecturally, yes — Cloud Run auto-scales, costs are per-request. The scaling challenge is human: onboarding, support, and customizing for each restaurant's quirks. That's where the $150k goes — building the ops infrastructure for scale."

**Why this works:** Technical scale is rarely the bottleneck. Operational scale is. Show you understand both.

---

## 16. "What's your data strategy?"

**Response:** "Every transcript, every correction, every approval becomes training data. Over time we build the largest corpus of restaurant payroll voice data in existence. That's a moat no competitor can buy."

**Why this works:** Data moats compound. Investors love businesses that get smarter with each customer.

---

## 17. "How do you handle PII and compliance?"

**Response:** "Minimal PII — we process first names and dollar amounts, no SSNs or bank info. We're not a payroll processor; we feed data to their existing payroll system. That said, we'll need to add SOC 2 compliance as we scale to enterprise customers."

**Why this works:** Compliance gets expensive. Show you understand where you sit on the risk spectrum.

---

## 18. "What's your product roadmap?"

**Response:** "Next 6 months: multi-restaurant support, scheduling integration, inventory voice reports. Next 18 months: full back-office suite — we become the operating system for independent restaurants."

**Why this works:** Roadmaps show vision. But be careful not to promise features that distract from current traction.

---

## 19. "How defensible is the AI component?"

**Response:** "The AI itself isn't defensible — we use commodity models. The defensibility is in the training data, the correction logic, and the domain-specific prompt engineering. We have 50+ pages of business rules Claude uses to parse transcripts correctly."

**Why this works:** AI wrappers aren't defensible. AI + proprietary data + domain logic can be.

---

## 20. "What would you build with unlimited engineering resources?"

**Response:** "A real-time labor optimizer that listens to ambient restaurant audio, detects busyness, and suggests shift adjustments on the fly. That's science fiction today, but it's where voice-first restaurant ops goes."

**Why this works:** Tests vision and ambition. Also reveals if you'd waste money on shiny things vs. high-impact features.

---

# BUSINESS MODEL & FINANCIALS

## 21. "What's your pricing model?"

**Response:** "We're targeting $99/month per restaurant, flat rate. Simple, predictable, easy to sell. As we add modules — scheduling, inventory — we'll move to $199/month for the full suite."

**Why this works:** Pricing should be simple and defensible. Per-seat models are harder for SMBs; flat rate reduces friction.

---

## 22. "What are your unit economics?"

**Response:** "CAC target is $500, LTV target is $2,400 at 24-month retention. LTV:CAC of ~5:1. Right now we're at one paying customer so these are projections, but the retention thesis is strong because switching costs are high once we're embedded in their workflow."

**Why this works:** LTV:CAC ratio shows business viability. 3:1 is minimum; 5:1+ is excellent. Be honest if you're projecting vs. measured.

---

## 23. "What's your burn rate?"

**Response:** "Under $2,000/month — just API costs and hosting. I don't take a salary. This $150k gives us 18+ months of runway, or 12 months if I take a modest salary to focus full-time."

**Why this works:** Low burn = more runway = less dilution = investor loves this. Capital efficiency is a feature.

---

## 24. "How will you spend the $150k?"

**Response:** "70% on go-to-market: sales, marketing, conference booths. 20% on product: contractor help for mobile app polish. 10% buffer. I'm not hiring a team — I'm proving the sales motion works before scaling headcount."

**Why this works:** Use of funds shows priorities. Investors worry about founders who want to hire before proving product-market fit.

---

## 25. "What's your runway with this raise?"

**Response:** "18 months at current burn. 12 months if I take a $50k salary. That's enough time to hit $20k MRR and raise a proper seed round at a much higher valuation."

**Why this works:** Runway = cash / burn rate. Investors want 12-18 months minimum. Less means you'll be fundraising again immediately.

---

## 26. "When will you be profitable?"

**Response:** "At 50 restaurants paying $99/month, we hit $60k ARR and break-even on operating costs. That's achievable in 12 months. Full profitability including my salary happens around 100 restaurants."

**Why this works:** Path to profitability shows sustainability. Even if you plan to raise more, showing you could survive without it is powerful.

---

## 27. "What's your revenue today?"

**Response:** "Effectively zero — we're deployed at Papa Surf but haven't turned on billing yet. This raise is to build the billing infrastructure and sign paying customers."

**Why this works:** Pre-revenue is fine at this stage. Own it and explain why you're confident revenue will follow deployment.

---

## 28. "What are your key metrics?"

**Response:** "Restaurants deployed, shifties processed per week, transcription accuracy, manager time saved. Revenue will be the north star once we turn on billing, but right now it's about proving the product works at multiple locations."

**Why this works:** Metrics show what you're optimizing for. At pre-revenue, usage metrics matter. Post-revenue, it's MRR and churn.

---

## 29. "What's your churn assumption?"

**Response:** "We're targeting under 5% monthly, which is strong for SMB SaaS. Restaurant software typically sees 3-7% monthly churn. Our advantage is daily usage — we're embedded in their workflow, not a quarterly report they forget about."

**Why this works:** SMB churn is notoriously high. Show you understand the challenge and have a stickiness strategy.

---

## 30. "What valuation are you seeking and why?"

**Response:** "$3M pre-money. We're pre-revenue but product-complete with a live deployment. Comparable pre-seed restaurant tech companies raised at $2-4M. I'm open to discussing if you see it differently."

**Why this works:** Valuation is negotiable. Anchor confidently but show flexibility. Justifying with comps is stronger than "I think it's worth X."

---

# TEAM & EXECUTION

## 31. "Why are you the right person to build this?"

**Response:** "I ran restaurant operations for years — I've done the payroll calculations by hand hundreds of times. Then I taught myself to code and built this entire platform solo. I'm the rare founder who understands both the problem and can build the solution."

**Why this works:** Founder-market fit is critical. Investors bet on people who have unfair insight into the problem.

---

## 32. "What's your co-founder situation?"

**Response:** "Austin is my equity partner — he owns 40% — but he's not operationally involved day-to-day. I'm the sole full-time founder. I'll hire as we scale, but right now the product needs one obsessed person, not a committee."

**Why this works:** Solo founders are riskier but not dealbreakers. Show you have support (equity partners, advisors) without the co-founder title.

---

## 33. "What's your biggest weakness as a founder?"

**Response:** "Sales. I'm a builder by nature — I'd rather add features than cold-call restaurants. That's why this raise focuses on GTM: I need to force myself into sales mode, and potentially hire sales help."

**Why this works:** Self-awareness matters. A weakness + mitigation plan is better than "I don't have weaknesses."

---

## 34. "Have you started a company before?"

**Response:** "Not a venture-backed startup. I've run freelance consulting and restaurant operations. I've also experienced the downside — I got burned in a commercial real estate deal — which taught me the importance of protective structures."

**Why this works:** First-time founders are common. Frame past experience as relevant learning, even if it wasn't a startup.

---

## 35. "How do you handle disagreement?"

**Response:** "I listen fully, ask clarifying questions, then make a decision. I don't need consensus, but I do need to understand opposing views. With investors specifically, I'll always hear your advice — what I do with it is my call as CEO."

**Why this works:** This probes coachability vs. stubbornness. Investors want founders who listen but aren't pushovers.

---

## 36. "What will you do if this doesn't work?"

**Response:** "Learn from it and try again. Probably something else in restaurant tech — I know the space. Or maybe apply my coding skills to a different vertical. Failure isn't the end; quitting the game is."

**Why this works:** Resilience matters. Founders who would be destroyed by failure are risky. Those who see it as tuition are more likely to eventually succeed.

---

## 37. "How do you prioritize your time?"

**Response:** "Right now: 60% product, 40% customer conversations. Post-funding: 30% product, 70% sales and GTM. The build phase is ending; the sell phase is starting."

**Why this works:** Time allocation reveals priorities. Post-funding founders should skew toward distribution.

---

## 38. "What's your unfair recruiting advantage?"

**Response:** "I don't need to recruit yet — I built this solo. When I do hire, my advantage is equity + mission. Restaurant industry people love the idea of fixing a broken system. I'll hire operators who became coders, like me."

**Why this works:** Recruiting is a top challenge. Having a thesis on who you'll hire and why they'll join is important.

---

## 39. "How do you make decisions under uncertainty?"

**Response:** "Bias toward action with reversible decisions, careful deliberation on irreversible ones. Picking a database? Just pick one and move. Signing an exclusive contract? Sleep on it."

**Why this works:** Tests decision-making framework. "Move fast, except when you shouldn't" is the right answer.

---

## 40. "What keeps you up at night?"

**Response:** "That a well-funded competitor shows up and outspends us before we establish the brand. We can't outspend anyone. We have to out-execute on product and customer love."

**Why this works:** Genuine vulnerability builds trust. It also shows you're thinking about real risks, not overconfident.

---

# COMPETITION & MARKET DYNAMICS

## 41. "Who are your competitors?"

**Response:** "Direct: 7shifts, Homebase, and restaurant POS systems adding payroll features. Indirect: spreadsheets, pen-and-paper, and accountants. Our real competition is inertia — managers who've always done it the hard way."

**Why this works:** Never say "no competition." That means no market or you haven't looked. Categorize competitors thoughtfully.

---

## 42. "Why won't Toast/Square just build this?"

**Response:** "They might! But they're horizontal platforms — they won't build Texas-specific tip pooling rules. And if they do build something basic, it validates the market and we become an acquisition target."

**Why this works:** Platform risk is real. Show you've thought about it without dismissing it.

---

## 43. "What's your moat?"

**Response:** "Three things: domain expertise encoded in our system, training data from every transcript we process, and switching costs once we're embedded in daily workflow. None of these exist on day one; they compound over time."

**Why this works:** Moats take time to build. Honest founders say "we're building a moat" not "we have an unassailable moat."

---

## 44. "How do you win against a funded competitor?"

**Response:** "By being better for a narrow segment. We're not building for all restaurants — we're building for Texas independent full-service restaurants. We'll know their problems better and ship features faster for that niche."

**Why this works:** Niche focus beats broad ambition early. Dominate a small pond before expanding.

---

## 45. "What's your competitive response plan?"

**Response:** "If a competitor enters: double down on customer success, lock in annual contracts, and accelerate feature development for our core ICP. We compete on love, not features."

**Why this works:** Having a response plan shows strategic thinking. Panic is not a strategy.

---

# DEAL TERMS & INVESTOR RELATIONSHIP

## 46. "What investor rights are you offering?"

**Response:** "Information rights: quarterly updates, annual financials. Pro-rata rights on future rounds. Advisory input welcomed. No board seats — we're too early for a board. No operational veto rights."

**Why this works:** Standard angel rights without giving up control. Information and pro-rata are normal; board seats at this stage are unusual.

---

## 47. "What protective provisions do you want?"

**Response:** "I want founder-favorable liquidation preferences — 1x non-participating. No full-ratchet anti-dilution. And explicit language that operational decisions remain with me as CEO."

**Why this works:** Protective provisions protect you. 1x non-participating is standard and fair. Full ratchet and participating preferred hurt founders.

---

## 48. "How will you keep us informed?"

**Response:** "Monthly email update: metrics, wins, losses, asks. Quarterly call if you want it. I believe in transparency — you'll know the good and the bad in real-time."

**Why this works:** Communication expectations should be set upfront. Investors hate being surprised by problems.

---

## 49. "What happens if we disagree on company direction?"

**Response:** "We discuss it. You share your perspective, I listen carefully. Then I make the call. If that's a problem, this isn't the right investment for you. I need advisors, not bosses."

**Why this works:** Critical for setting expectations. This is your non-negotiable — set it clearly upfront to avoid conflict later.

---

## 50. "What's the exit potential?"

**Response:** "Acquisition by a POS or payroll company is most likely — $20-50M range if we hit $3M ARR. IPO isn't realistic for this category. Strategic acquisition to someone building a restaurant platform is the bull case."

**Why this works:** Realistic exit expectations. Most startups exit via acquisition. Promising IPO at this stage is a red flag.

---

# FINANCIAL DEEP DIVES

## 51. "Walk me through your financial projections."

**Response:** "Year 1: 25 restaurants at $99/month = $30k ARR. Year 2: 100 restaurants = $120k ARR. Year 3: 300 restaurants plus upsells = $500k ARR. These assume 3 new customers per month ramping to 15 per month by year 3, with 5% monthly churn. Conservative? Maybe. But I'd rather under-promise."

**Why this works:** Investors have seen thousands of hockey-stick projections that never materialize. Showing conservative, bottoms-up math (customers × price) is more credible than top-down ("we'll capture 1% of the market"). Always be able to defend your assumptions.

---

## 52. "What's your gross margin?"

**Response:** "Around 75-80%. Our COGS is API costs — Whisper transcription and Claude parsing. At current volume, that's about $0.15 per shifty processed. At $99/month with ~60 shifties per restaurant, our cost is roughly $9/month per customer."

**Why this works:** Gross margin = (Revenue - Cost of Goods Sold) / Revenue. SaaS businesses should target 70-80%+. Knowing your unit-level costs shows operational sophistication.

---

## 53. "What are your fixed vs. variable costs?"

**Response:** "Almost entirely variable right now. Cloud hosting scales to zero when idle. API costs are per-request. My time is the only 'fixed' cost, and I'm not taking salary. This changes when we hire, but for now we have incredible operating leverage."

**Why this works:** High variable cost ratio means you don't bleed money when growth slows. High fixed costs create pressure to grow or die. Early-stage startups should minimize fixed costs.

---

## 54. "How do you think about pricing power?"

**Response:** "We have moderate pricing power because switching costs are high — once we're in their daily workflow, moving to a competitor means retraining staff and risking payroll errors. We're not charging based on value yet; there's room to raise prices as we add features."

**Why this works:** Pricing power = ability to raise prices without losing customers. It comes from switching costs, differentiation, and value delivered. Commodity products have no pricing power.

---

## 55. "What's your sensitivity to economic downturns?"

**Response:** "Mixed. Restaurant failures would hurt us — fewer customers. But survivors will need to cut costs, and we save labor hours. We're a cost-reduction tool, which often does well in recessions. That said, restaurants are cyclical, and I don't pretend otherwise."

**Why this works:** Economic sensitivity analysis shows maturity. Tools that save money (automation) often outperform tools that drive growth (marketing) in downturns. Be honest about your category's risks.

---

## 56. "Do you have any deferred revenue or contracts?"

**Response:** "Not yet — we're processing payroll but haven't activated billing. Once we do, I plan to offer annual prepay discounts (2 months free), which will create deferred revenue and improve cash flow predictability."

**Why this works:** Deferred revenue is cash collected for services not yet delivered. It's a liability on the balance sheet but great for cash flow. Annual contracts also reduce churn.

---

## 57. "What's your accounts receivable situation?"

**Response:** "We'll do credit card only — no invoicing, no AR. SMBs don't pay invoices reliably. Credit card billing with automatic retry eliminates collections headaches entirely."

**Why this works:** AR (accounts receivable) is money owed to you. SMB SaaS companies should avoid invoicing — it creates collection costs and cash flow uncertainty. Cards solve this.

---

## 58. "How do you handle revenue recognition?"

**Response:** "Straightforward monthly subscription — we recognize revenue as we deliver service each month. No complex multi-element arrangements. We keep the accounting simple on purpose."

**Why this works:** Revenue recognition rules (ASC 606) can get complex. Investors want to know you're not playing games with when you book revenue. Subscription = simple.

---

## 59. "What financial metrics will you track religiously?"

**Response:** "MRR, MRR growth rate, churn rate, CAC, and LTV. Those five tell the whole story. I'll report them monthly to you. Vanity metrics like 'shifties processed' matter less than revenue retention."

**Why this works:** Knowing which metrics matter shows financial sophistication. MRR (Monthly Recurring Revenue) and churn are the heartbeat of any SaaS business.

---

## 60. "What's your break-even point in customers?"

**Response:** "At $99/month with ~75% gross margin, each customer contributes ~$75/month toward fixed costs. If my loaded cost (salary + overhead) is $5k/month, I break even at 67 customers. At 100 customers, I'm profitable enough to reinvest or hire."

**Why this works:** Break-even analysis shows you understand your economics. It's simple division: fixed costs / contribution margin per customer.

---

# LEGAL & CORPORATE STRUCTURE

## 61. "What's your corporate structure?"

**Response:** "Delaware C-Corp. Clean standard setup. No weird share classes, no debt, no convertible notes outstanding. Ready for institutional investment if we go that route later."

**Why this works:** Delaware C-Corp is the standard for venture-backable companies. LLCs and S-Corps create tax complications for investors. If you're not a Delaware C-Corp, have a good reason.

---

## 62. "Who owns the IP?"

**Response:** "The company owns everything. I assigned all my prior work to the company via an IP assignment agreement. No ambiguity about who owns the code."

**Why this works:** IP assignment is critical. If the founder owns the code personally, the company has nothing. Investors will walk away from unclear IP ownership.

---

## 63. "Have you filed any patents?"

**Response:** "No, and I don't plan to. Software patents are expensive, hard to enforce, and wouldn't protect us anyway. Our moat is execution and domain expertise, not legal barriers."

**Why this works:** Patents rarely make sense for early-stage software companies. They're expensive ($15-30k) and take years. Most VCs don't care. Trade secrets and speed matter more.

---

## 64. "Are your contractors or employees properly classified?"

**Response:** "I've been solo so far. When I hire, I'll use a PEO or payroll service to ensure compliance. Misclassification is an expensive mistake I won't make."

**Why this works:** Worker misclassification (calling employees "contractors") is a ticking time bomb. It can trigger back taxes, penalties, and lawsuits. Investors screen for this.

---

## 65. "Have you done your 83(b) election?"

**Response:** "Yes, filed within 30 days of incorporating. All founder shares are fully vested with 83(b) election made. No tax surprises."

**Why this works:** 83(b) election lets you pay tax on shares at grant (when they're worth nothing) instead of at vesting (when they might be worth a lot). Missing this deadline is a costly, irreversible mistake.

---

## 66. "What's on your cap table?"

**Response:** "Simple. 10 million shares authorized and issued. I hold 6 million, Austin holds 4 million. No options granted yet, no other shareholders, no SAFEs or convertibles. Clean."

**Why this works:** A clean cap table is attractive. Messy cap tables with dozens of small investors, multiple note conversions, and unclear ownership create due diligence nightmares.

---

## 67. "Do you have an option pool?"

**Response:** "Not yet. I'll create one post-funding, probably 10-15% for future hires. I'd rather not dilute before I need to, but I understand investors often want this set up pre-investment."

**Why this works:** Option pools dilute existing shareholders. Creating one before investment means the dilution is shared; after means only new investors benefit. This is a negotiation point.

---

## 68. "Any litigation or legal threats?"

**Response:** "None. No lawsuits, no cease-and-desists, no IP disputes, no disgruntled former partners. I keep things clean and documented."

**Why this works:** Legal baggage scares investors. Even frivolous suits cost money to defend. Being able to say "none" is valuable.

---

## 69. "What contracts do you have in place?"

**Response:** "Terms of service for the web app, contractor agreements for any work I outsource, and an IP assignment for my own contributions. No customer contracts yet — we'll implement subscription agreements when billing goes live."

**Why this works:** Having basic legal infrastructure shows professionalism. Not having it suggests you're flying blind.

---

## 70. "What insurance do you have?"

**Response:** "None yet — it's on my list post-funding. We'll need general liability and probably E&O once we're processing real payroll data. Cyber liability too, eventually."

**Why this works:** Insurance protects against catastrophic losses. Not having it pre-revenue is understandable, but having a plan shows foresight. E&O (Errors & Omissions) protects against professional mistakes.

---

# CUSTOMER & SALES DYNAMICS

## 71. "What's your sales cycle?"

**Response:** "For owner-operators, it's short — one demo, one follow-up, decision within a week. For multi-unit operators with layers of management, it'll be longer. We're targeting the fast-decision makers first."

**Why this works:** Long sales cycles kill cash flow. Knowing your cycle and targeting shorter ones shows commercial awareness.

---

## 72. "Who's the decision maker?"

**Response:** "The owner or GM — whoever does the payroll today. It's not a committee decision at small independents. One person feels the pain, one person decides. That's our sweet spot."

**Why this works:** Enterprise sales have buying committees. SMB sales have one decision maker. Knowing who holds the budget and authority is fundamental to sales.

---

## 73. "What objections do you hear most?"

**Response:** "'I've always done it this way' is number one. 'What if it gets it wrong' is number two. We overcome the first by showing time savings in hard dollars. The second by demonstrating the approval workflow — they stay in control."

**Why this works:** If you don't know the objections, you haven't sold anything. Having rebuttals ready shows you've done real customer development.

---

## 74. "Why have you lost deals?"

**Response:** "Honestly, we haven't tried to close paying deals yet — we're in pilot mode at Papa Surf. But in conversations, I've lost interest when the restaurant uses a POS with built-in payroll. We're not competing with that."

**Why this works:** Lost deal analysis reveals market fit gaps. Not having lost deals because you haven't sold isn't a red flag at this stage, but acknowledge it honestly.

---

## 75. "What's your customer acquisition strategy?"

**Response:** "Three channels: local restaurant association events, referrals from Papa Surf once we prove value, and targeted LinkedIn outreach to owner-operators. No paid ads until we nail the sales conversation."

**Why this works:** CAC (Customer Acquisition Cost) matters. Starting with free/cheap channels and only adding paid marketing after proving conversion shows capital efficiency.

---

## 76. "What's your NRR expectation?"

**Response:** "Targeting 95% NRR initially — expecting some churn but minimal because restaurant payroll doesn't change much. Once we add upsells like scheduling and inventory, we'll push for 110%+ NRR."

**Why this works:** NRR (Net Revenue Retention) measures whether existing customers grow or shrink. 100% = stable. Below = shrinking base. Above = expansion revenue covers churn.

---

## 77. "How do you handle customer success?"

**Response:** "Right now, I do it personally. I onboard each restaurant, check in weekly, and handle support via text message. That doesn't scale, but it builds the playbook for when we hire."

**Why this works:** Founder-led customer success early creates deep understanding of customer needs. The playbook you build becomes the training manual for future hires.

---

## 78. "What does your onboarding look like?"

**Response:** "30-minute setup call: I walk them through the app, they record a test shifty, we review the output together. Then daily check-ins the first week. By week two, they're self-sufficient."

**Why this works:** Onboarding is where churn gets decided. Fast time-to-value = sticky customers. Slow, confusing onboarding = churn risk.

---

## 79. "Do you have any customer concentration risk?"

**Response:** "Right now? 100% concentration — one customer. That's obviously a problem we're solving with this raise. Goal is no single customer over 10% of revenue within 12 months."

**Why this works:** Customer concentration is dangerous — losing one big customer can tank the business. Diversification reduces risk. Be honest about current concentration.

---

## 80. "What's your support model?"

**Response:** "Text and email, with me responding within an hour during business hours. Restaurant managers don't do formal support tickets — they text. So that's how we'll always work, even at scale."

**Why this works:** Support model should fit the customer. SMB customers expect fast, casual support. Building enterprise ticketing systems for taco shop owners is wrong-headed.

---

# PRODUCT PHILOSOPHY

## 81. "How do you prioritize features?"

**Response:** "Customer pain severity times frequency. If something is painful and happens daily, it's top priority. If it's annoying but rare, it waits. I don't build features customers don't ask for."

**Why this works:** Feature prioritization frameworks show product maturity. Building what customers need (not what you think is cool) is the discipline that separates winners.

---

## 82. "How do you decide what NOT to build?"

**Response:** "If it serves less than 80% of our target customers, we don't build it. We're not customizing for edge cases. We'd rather lose the weird customer than bloat the product for everyone."

**Why this works:** Saying no is harder than saying yes. Products die from feature bloat. Having a clear "not for us" filter is a sign of focus.

---

## 83. "What's your approach to design?"

**Response:** "Mobile-first, minimal UI, zero training required. If a manager can't figure it out while standing in a busy kitchen, we failed. Design isn't about looking pretty — it's about reducing friction."

**Why this works:** Design thinking appropriate to your user context shows customer empathy. Restaurant managers don't have time for complex UIs.

---

## 84. "How do you handle feature requests?"

**Response:** "I log everything in a simple spreadsheet with the customer name and date. When three different customers ask for the same thing, it gets built. One-off requests stay logged but don't drive roadmap."

**Why this works:** Tracking requests prevents recency bias (building whatever the last customer asked for). Patterns across customers reveal real needs.

---

## 85. "What's your testing strategy?"

**Response:** "Automated tests on the critical path — payroll calculations, tip pooling logic. Manual testing on UI flows. We're at about 40% coverage. More than most early startups, less than I'd like."

**Why this works:** Testing shows engineering discipline. 100% coverage is unrealistic early-stage, but no testing is a red flag. Know your coverage and be honest.

---

## 86. "How do you handle technical debt?"

**Response:** "I track it in code comments and a debt.md file. Every month I spend one day paying down the worst debt. It's not glamorous, but it prevents the codebase from becoming unmaintainable."

**Why this works:** Tech debt is inevitable. Having a system to track and address it shows maturity. Ignoring it until the codebase collapses is amateur hour.

---

## 87. "What's your uptime commitment?"

**Response:** "We don't have an SLA yet, but we're on Google Cloud Run with automatic failover. In practice, uptime has been 99.9%+. When we go enterprise, we'll formalize SLAs with credits for downtime."

**Why this works:** Uptime matters more for some products than others. Payroll is high-stakes, so reliability is critical. Having infrastructure that scales and self-heals is important.

---

## 88. "How do you handle data backups?"

**Response:** "Daily automated backups to Google Cloud Storage with 30-day retention. I've done test restores. When you're dealing with payroll data, you can't afford to lose anything."

**Why this works:** Data loss is catastrophic. Having backup procedures AND testing restores shows operational discipline. Many founders have backups but never test them.

---

## 89. "What's your API strategy?"

**Response:** "No public API yet. Phase 1 is getting the core product right. Phase 2 might include an API for POS integrations. But I won't build infrastructure before demand exists."

**Why this works:** APIs enable ecosystem effects but are expensive to maintain. Building them prematurely is over-engineering. Having a plan for when/if to build shows strategic thinking.

---

## 90. "How do you think about platform vs. point solution?"

**Response:** "We're a point solution that could become a platform. Start by solving payroll incredibly well. Add scheduling when customers ask. Eventually you're the operating system for restaurant back-office. But you don't start there — you earn your way there."

**Why this works:** Platform ambitions are good; premature platform building is bad. Start narrow, expand with traction. Investors like focused execution more than grandiose day-one platforms.

---

# FOUNDER PSYCHOLOGY & MOTIVATION

## 91. "Why do you want to build a company instead of getting a job?"

**Response:** "I've worked for other people. I'm done with that. I want to build something that's mine, solve a problem I care about, and capture the upside if it works. The downside — working insane hours for uncertain pay — is worth it to me."

**Why this works:** Investors want founders who are intrinsically motivated, not just avoiding a job. Genuine ownership mentality means you'll push through the hard times.

---

## 92. "What will you do if this fails?"

**Response:** "Learn from it and try again. Probably something else in restaurant tech — I know the space. Or maybe apply my coding skills to a different vertical. Failure isn't the end; quitting the game is."

**Why this works:** Resilience matters. Founders who would be destroyed by failure are risky. Those who see it as tuition are more likely to eventually succeed.

---

## 93. "How do you handle stress?"

**Response:** "Exercise, sleep, and talking through problems out loud — sometimes to other people, sometimes to myself. I've learned that pushing through exhaustion makes me dumber, so I force myself to rest."

**Why this works:** Founder burnout is real. Self-awareness about stress management shows you'll be around for the long haul, not flame out in year two.

---

## 94. "What's your risk tolerance?"

**Response:** "High for calculated bets, low for reckless ones. I'll bet on things I can influence — product, sales, hustle. I won't bet on things I can't — regulatory changes, macro economy. I take intelligent risks."

**Why this works:** Risk tolerance should be high but not stupid. Distinguishing controllable from uncontrollable risk shows judgment.

---

## 95. "How do you stay motivated when things are hard?"

**Response:** "I remember why I started — watching managers waste hours on payroll they hate. Every shifty we process is an hour someone got back. The mission keeps me going when the work is tedious."

**Why this works:** Mission-driven founders persist longer than money-driven ones. Connecting daily work to larger purpose is a sustainability strategy.

---

## 96. "What's the hardest decision you've made on this project?"

**Response:** "Deciding to rebuild the transcription pipeline from scratch after the first version was unreliable. It cost me three weeks. But now it works. Killing your own work is hard but necessary."

**Why this works:** Willingness to kill sunk costs shows rationality. Many founders cling to bad decisions because they've invested time. That's a trap.

---

## 97. "How do you handle criticism?"

**Response:** "Depends on the source. From customers, I listen carefully — they're living the problem. From random people, I filter heavily. From investors and advisors, I consider seriously but decide independently."

**Why this works:** Taking all criticism equally is as bad as taking none. Source-weighting shows maturity. Investors want founders who listen but aren't pushovers.

---

## 98. "What's your learning style?"

**Response:** "Visual and hands-on. I learn by building, breaking, and rebuilding. Documents help when they're concise — one-pagers, checklists. Long-form theory puts me to sleep."

**Why this works:** Self-awareness about how you learn helps you structure your environment for success. It also helps investors understand how to work with you.

---

## 99. "Who do you go to for advice?"

**Response:** "Depends on the domain. Product questions, I think through alone. Business questions, I have a few founder friends I trust. Legal and financial, I hire experts. I don't ask for advice I won't consider seriously."

**Why this works:** Having a network shows you're not alone. Being selective about who you ask shows judgment. Asking everyone everything shows insecurity.

---

## 100. "What would make you give up?"

**Response:** "Running out of money with no path to more. Or spending two years unable to get anyone to pay. But I'm not close to either. This is year one — the time to push, not quit."

**Why this works:** Knowing your quit conditions isn't defeatist — it's rational. Running a zombie company helps no one. Investors want founders who'll shut down cleanly if it's not working.

---

# STRATEGIC THINKING

## 101. "Where do you want to be in 5 years?"

**Response:** "Running a 50-person company doing $10M ARR, serving thousands of restaurants. We're the verb for restaurant back-office — 'just Mise it.' Or we've been acquired by someone who can take it further. Both are wins."

**Why this works:** Vision shows ambition. Being open to acquisition shows pragmatism. Investors want a return, not founders who'll turn down good exits out of ego.

---

## 102. "What's your biggest strategic risk?"

**Response:** "Platform dependency. We rely on OpenAI for transcription and Anthropic for parsing. If either cuts us off or raises prices 10x, we're in trouble. Mitigation: we can swap to self-hosted models, but it'd take time."

**Why this works:** Platform risk (building on someone else's infrastructure) is real. Acknowledging it and having a contingency plan shows strategic awareness.

---

## 103. "How do you think about vertical vs. horizontal expansion?"

**Response:** "Vertical first — go deep in independent restaurants before going wide to other industries. Restaurants have quirks that don't translate. A landscaping company doesn't do tip pooling. Depth before breadth."

**Why this works:** Horizontal expansion is tempting but often premature. Proving you can dominate a niche is more valuable than being mediocre across many.

---

## 104. "Would you ever acquire a competitor?"

**Response:** "At this stage? No — we don't have the cash or attention. Later, if someone has a great customer base but bad product, we might acquire for customers. But we're years away from that being relevant."

**Why this works:** M&A strategy shows long-term thinking. But knowing you're not ready for it shows focus on what matters now.

---

## 105. "How do you think about partnerships?"

**Response:** "Partnerships where we're embedded in someone's workflow — like a POS integration — could be huge. Partnerships that are just co-marketing are usually a waste of time. I'd rather build than schmooze."

**Why this works:** Partnerships can be leveraged or distracting. Technical integrations have teeth; co-marketing often doesn't. Be selective.

---

## 106. "What would you do with 10x more money?"

**Response:** "Hire 3 people: a salesperson, a customer success person, and a junior engineer. Expand to three Texas metro areas simultaneously. More money wouldn't change strategy — it would accelerate execution."

**Why this works:** This tests whether more money would be wasted. If your answer is "I'd figure it out," you're not ready for more capital. Specific plans show readiness.

---

## 107. "What would you do with half the money you're asking for?"

**Response:** "Same plan, slower execution. I'd skip the marketing spend and focus purely on direct sales and referrals. Longer runway, tighter focus. We'd get to the same place in 24 months instead of 18."

**Why this works:** Flexibility on amount shows you're not dependent on a specific number. It also reveals your prioritization — what gets cut first.

---

## 108. "Who do you admire in business?"

**Response:** "Jason Fried at Basecamp — built a profitable company without VC. Tobi at Shopify — focused obsessively on the merchant. Both built empires by being opinionated and customer-obsessed."

**Why this works:** Role models reveal values. Choosing founders known for capital efficiency and focus sends different signals than choosing growth-at-all-costs types.

---

## 109. "What book has influenced your thinking?"

**Response:** "The Mom Test by Rob Fitzpatrick. It taught me how to have customer conversations that reveal truth instead of false positives. Every founder should read it before building anything."

**Why this works:** Book references show intellectual curiosity. The Mom Test is a great answer because it's practical and customer-focused, not abstract business theory.

---

## 110. "What's the most contrarian thing you believe about your market?"

**Response:** "That restaurants don't need more features — they need fewer, better ones. Every POS tries to do everything. We'll win by doing one thing perfectly and saying no to everything else."

**Why this works:** Contrarian views show independent thinking. Agreeing with conventional wisdom means you're competing on execution alone.

---

# OPERATIONAL DETAILS

## 111. "Walk me through a typical week."

**Response:** "Mornings: product work — coding, fixing bugs, improving features. Afternoons: customer conversations and business tasks. Evenings: planning and admin. Weekends: catch up on whatever slipped. It's not balanced, but it's effective."

**Why this works:** Knowing your own rhythm shows self-management. Investors want founders who work hard AND smart, not just long hours.

---

## 112. "How do you manage your time?"

**Response:** "I block mornings for deep work — no meetings, no calls. Afternoons are for communication. I use a simple task list and review it nightly. No fancy productivity systems; just discipline."

**Why this works:** Time management systems are personal, but having one matters. Founders who let the day run them instead of running the day are less effective.

---

## 113. "How do you communicate with your equity partner?"

**Response:** "Weekly call, usually 30 minutes. I share what's happening, he offers perspective. He trusts my judgment on day-to-day. Big decisions — like this raise — we align on together."

**Why this works:** Co-founder/partner communication is a common failure point. Having a rhythm that works shows the relationship is functional.

---

## 114. "What tools do you use to run the business?"

**Response:** "Google Workspace for docs and email, GitHub for code, Notion for notes and planning, Stripe when we turn on billing. Simple, cheap, industry-standard. I don't over-engineer the business side."

**Why this works:** Tool choices reveal operational philosophy. Over-tooling is a distraction. Under-tooling creates chaos. Simple and standard is usually right.

---

## 115. "How do you make decisions?"

**Response:** "For reversible decisions: fast, trust my gut, iterate. For irreversible decisions: slow down, gather input, sleep on it. Most decisions are reversible, so I bias toward speed."

**Why this works:** Decision-making frameworks show maturity. Amazon's "one-way vs. two-way door" concept is the idea here.

---

## 116. "What's your hiring philosophy?"

**Response:** "Hire slow, fire fast. I'd rather be understaffed than have the wrong person. When I hire, I look for ownership mentality and low ego. Skills can be taught; attitude can't."

**Why this works:** Hiring is the most leveraged activity a founder does. Philosophy around it reveals values. "Hire fast, fire slow" is a disaster pattern.

---

## 117. "How would you handle a bad hire?"

**Response:** "Direct conversation first — is there a fit issue we can fix? If not, quick and generous exit. Two weeks' severance even if not required. I won't let a bad hire linger and poison the team."

**Why this works:** Firing is uncomfortable. Founders who can't do it end up with dysfunctional teams. Being humane but decisive is the right stance.

---

## 118. "What's your approach to compensation?"

**Response:** "Modest salary plus meaningful equity. I want people who believe in the mission, not mercenaries chasing cash. Competitive enough to live comfortably; not enough to attract people just for the money."

**Why this works:** Comp philosophy signals culture. Overpaying attracts mercenaries. Underpaying loses good people. Equity alignment is key in startups.

---

## 119. "Will you relocate for the business?"

**Response:** "I'm in Texas, restaurants are everywhere. If a huge opportunity required relocation, I'd consider it. But I don't see geography as a constraint for a software business selling to SMBs nationwide."

**Why this works:** Some investors want founders in specific locations (Silicon Valley, etc.). Having a thoughtful answer about geography shows you've considered it.

---

## 120. "How do you stay close to customers as you scale?"

**Response:** "I'll always do some customer calls myself — even as CEO. It keeps me grounded. I'll also watch support tickets and sit in on customer success calls. Staying close to pain is how you stay relevant."

**Why this works:** Founder-customer distance increases with scale. Having a commitment to maintain connection shows you won't become ivory tower leadership.

---

# MARKET NUANCES

## 121. "What do you know about restaurants that most tech people don't?"

**Response:** "That margins are 3-5%, turnover is 70%+ annually, and managers are exhausted. They don't want software — they want their problem to go away. We succeed by being invisible, not impressive."

**Why this works:** Deep domain knowledge is your unfair advantage. Demonstrating insider understanding proves you're not a tourist in the market.

---

## 122. "How seasonal is your business?"

**Response:** "Restaurants have seasonality — summer and holidays are busy. But payroll happens every week regardless. Our revenue isn't directly seasonal, though churn might spike after slow winters."

**Why this works:** Understanding seasonality shows market sophistication. Businesses with severe seasonality need different cash management.

---

## 123. "What regulations affect you?"

**Response:** "Payroll regulations are complex, but we're not a payroll processor — we feed data to their existing system. We stay on the input side, not the compliance side. That's intentional."

**Why this works:** Regulatory positioning matters. Being adjacent to regulated activity without being regulated yourself is strategically valuable.

---

## 124. "How do tip regulations vary by state?"

**Response:** "Significantly. Texas is employer-friendly — fewer restrictions on tip pooling. California is complex — tip credits are different. We're starting in Texas precisely because regulations are simpler. We'll expand to other states as we encode their rules."

**Why this works:** Knowing regulatory variation by state proves domain expertise. It also justifies geographic focus — start where rules are simple.

---

## 125. "How do you see AI regulation affecting you?"

**Response:** "We're in a low-risk category — we're not making hiring decisions or doing surveillance. We're calculating math from voice input. If AI regulation comes, it'll target higher-stakes applications first."

**Why this works:** AI regulation is coming. Having a view on where your product falls in the risk spectrum shows awareness without fear-mongering.

---

## 126. "What happens to you if minimum wage keeps rising?"

**Response:** "Good for us. Higher labor costs increase pressure to automate. A $15/hour manager spending 4 hours on payroll is wasting $60/week. A $25/hour manager wasting those same hours is losing $100/week. Our value prop scales with wages."

**Why this works:** Macro trends can help or hurt. Framing minimum wage increases as a tailwind shows strategic thinking.

---

## 127. "How does labor shortage affect you?"

**Response:** "Mixed. Fewer workers means smaller payrolls — less complexity to manage. But labor shortage also drives automation adoption — managers can't afford to waste time. Net, probably neutral to slightly positive."

**Why this works:** Second-order thinking about market conditions shows sophistication. Not every trend is straightforwardly good or bad.

---

## 128. "What's the consolidation trend in restaurants?"

**Response:** "Chains are growing, independents are struggling. But there are still 300,000+ independent restaurants in the US. Even if that number shrinks 20%, there's more market than we can serve in a decade."

**Why this works:** Market size trends matter. Showing you've thought about whether your market is growing or shrinking is important.

---

## 129. "How does delivery/ghost kitchens affect you?"

**Response:** "Ghost kitchens have simpler payroll — fewer FOH staff, no tips from dine-in. They're not our ideal customer. We thrive where there's complexity: full-service with bartenders, servers, bussers, hosts."

**Why this works:** Market segmentation means not all restaurants are equal. Knowing which trends favor your ICP shows commercial awareness.

---

## 130. "What technology trends are you watching?"

**Response:** "Voice interfaces getting better and cheaper, local AI models that could reduce our API costs, and restaurant-specific vertical SaaS consolidation. I read what's happening and think about how it affects us."

**Why this works:** Staying current on tech trends shows you won't be caught off guard. Naming specific relevant trends (not just "AI is hot") is more credible.

---

# EDGE CASES & STRESS TESTS

## 131. "What happens if Austin wants out?"

**Response:** "We'd negotiate a buyback or find a buyer for his shares. We have a right of first refusal in our shareholder agreement. His equity doesn't create operational dependency — I run the company."

**Why this works:** Co-founder/partner breakups happen. Having legal structure (ROFR, vesting) to handle it shows foresight.

---

## 132. "What if your main customer churns?"

**Response:** "Right now that's existential — we have one customer. That's why this raise is about getting to 25+ customers fast. Diversification is job one."

**Why this works:** Acknowledging concentration risk and having a plan to address it is better than pretending it doesn't exist.

---

## 133. "What if you get sick or injured?"

**Response:** "Short-term: the system runs itself — shifties get processed, data flows. Medium-term: that's a problem. Part of why I want some funding is to build enough cushion that the company survives a month without me."

**Why this works:** Key person risk is real for solo founders. Acknowledging it and having mitigation (systems, buffer capital) is mature.

---

## 134. "What if OpenAI raises prices 5x?"

**Response:** "We switch to self-hosted Whisper — there's an open-source version. It's more work to deploy, but we're not trapped. We've architected to swap components if needed."

**Why this works:** Vendor lock-in is a strategic risk. Having contingency plans for key dependencies shows operational sophistication.

---

## 135. "What if a big breach hits your industry?"

**Response:** "We'd benefit from not being the one breached and suffer from reduced trust in all software. Net, it's a reason to over-invest in security now. We want to be the safe choice when customers get scared."

**Why this works:** Industry-wide risk affects you even if you're not the cause. Positioning as the secure option in a risky market is strategic.

---

## 136. "What if a lawsuit hits you?"

**Response:** "Depends on the type. Frivolous suits, we'd fight with insurance coverage. Legitimate liability, we'd settle and learn. We carry basic insurance and will upgrade as we scale. We also build the product to minimize liability — human approval on all output."

**Why this works:** Litigation is a cost of doing business. Having insurance and a thoughtful stance on liability shows you've thought it through.

---

## 137. "What if you can't raise your next round?"

**Response:** "We get to profitability on this money if needed. It's slower growth, but we survive. That's by design — I'm not building a company that dies without continuous outside capital."

**Why this works:** Default alive vs. default dead is a crucial distinction. Investors prefer companies that can survive without more funding even if growth slows.

---

## 138. "What if a recession hits?"

**Response:** "Restaurants suffer, no question. Some of our customers would close. But survivors would need to cut costs, and we're a cost-cutting tool. Historically, automation software does okay in recessions."

**Why this works:** Recession resilience varies by business type. Cost-cutting tools often outperform growth-driving tools when budgets tighten.

---

## 139. "What if your transcription AI hallucinates?"

**Response:** "That's why we have the approval screen. Every parsed result gets human review before affecting payroll. We're not automating away accountability — we're augmenting human judgment."

**Why this works:** AI hallucination is a real concern. Human-in-the-loop design is the mitigation. Showing you've thought about failure modes builds trust.

---

## 140. "What's your disaster recovery plan?"

**Response:** "Daily backups with tested restores. Multi-region cloud deployment for availability. If catastrophe hits, worst case we're down for hours, not days. For a critical system like payroll, that's the bare minimum."

**Why this works:** Disaster recovery shows operational maturity. "We haven't thought about it" is a red flag for any company handling important data.

---

# DUE DILIGENCE & TRUST

## 141. "Can I talk to your customer?"

**Response:** "Absolutely. I'll introduce you to the GM at Papa Surf. Ask him anything — how we work together, what problems we've solved, what's still rough. I have nothing to hide."

**Why this works:** Willingness to offer references is a trust signal. Hesitation suggests hidden problems. Enthusiastic openness is best.

---

## 142. "Can I see your code/product?"

**Response:** "Yes. I can do a full product demo anytime. Code review is fine too if you have someone technical — I'm proud of what I've built. I'll also share our architecture docs."

**Why this works:** Technical due diligence is normal for investors with technical backgrounds. Being eager to show code signals confidence.

---

## 143. "Can I see your financials?"

**Response:** "Sure — we have simple books right now. Bank statements, expense tracking spreadsheet, and projections. No audited financials at this stage, but full transparency on what's there."

**Why this works:** Financial transparency is baseline. Resistance to sharing is a red flag. At early stage, simple records are fine.

---

## 144. "Who else have you talked to about investing?"

**Response:** "You're the first serious conversation. I've had informal chats with a few people, but no other term sheets or commitments. I'm being selective about who I partner with."

**Why this works:** Social proof matters (other interest creates urgency) but honesty matters more. If they're first, say so. Don't fake competition.

---

## 145. "What do your references say about you?"

**Response:** "That I'm intense, follow through on commitments, and don't give up easily. Probably that I can be stubborn. I'd rather you hear it from them directly — want me to connect you?"

**Why this works:** Self-aware assessment of how others perceive you shows maturity. Offering connections proactively builds trust.

---

## 146. "Have you ever been sued or filed bankruptcy?"

**Response:** "No lawsuits. No bankruptcy. I got burned in a commercial real estate deal — lost money as a passive investor — but nothing that resulted in legal action. Clean record."

**Why this works:** Background checks are normal. Disclosing past setbacks proactively is better than having them discovered. Transparency builds trust.

---

## 147. "Is there anything in your background I should know?"

**Response:** "Nothing that would surprise you. No criminal record, no legal issues, no skeletons. The commercial real estate loss I mentioned is the only financial setback, and it taught me to be more careful."

**Why this works:** Open-ended background questions test honesty. Saying "nothing" confidently while acknowledging known issues is the right answer.

---

## 148. "Why should I trust you with my money?"

**Response:** "You shouldn't trust me blindly — you should verify. Talk to my customer, check my references, watch how I communicate. Trust is earned through transparency and follow-through. I'll show you both."

**Why this works:** Don't ask for blind trust. Offer evidence. The right answer is inviting verification, not claiming trustworthiness.

---

## 149. "What would you tell me if I said no?"

**Response:** "I'd ask why — genuinely want to understand. Then I'd thank you for your time and keep building. One investor passing doesn't change what I'm working on. But I hope you say yes."

**Why this works:** Graceful response to rejection shows maturity. Desperation or arguing is a red flag. Curiosity about the "no" is growth mindset.

---

## 150. "What questions do you have for me?"

**Response:** "What made you interested in this deal? What concerns do you have that I haven't addressed? And if we work together, what does your ideal communication cadence look like?"

**Why this works:** Asking smart questions shows you're evaluating them too. It also surfaces objections you can address. Never say "no questions."

---

# Quick Reference: Key Concepts

| Term | Definition |
|------|------------|
| **TAM/SAM/SOM** | Total/Serviceable/Obtainable market sizes |
| **CAC** | Customer Acquisition Cost |
| **LTV** | Lifetime Value of a customer |
| **MRR/ARR** | Monthly/Annual Recurring Revenue |
| **NRR** | Net Revenue Retention (includes expansion/churn) |
| **Churn** | Rate at which customers cancel |
| **Gross Margin** | (Revenue - COGS) / Revenue |
| **Runway** | Cash / Monthly Burn Rate |
| **1x Non-Participating** | Investor gets money back OR pro-rata share, not both |
| **Pro-Rata Rights** | Right to invest in future rounds to maintain % |
| **Anti-Dilution** | Protection against down rounds diluting ownership |
| **83(b) Election** | Tax election to pay on shares at grant, not vesting |
| **ROFR** | Right of First Refusal on share sales |
| **Drag-Along** | Majority can force minority to sell in acquisition |

---

*Study this. Know it cold. Confidence comes from preparation.*
