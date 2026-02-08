# PRIVACY POLICY

<div class="doc-header">
<strong>MISE, INC.</strong><br>
Privacy Policy
</div>

**Effective Date:** /TextEffectiveDate/

---

## 1. INTRODUCTION

**Mise, Inc.** ("**Mise**," "**we**," "**us**," or "**our**") respects your privacy and is committed to protecting the personal information you share with us. This Privacy Policy explains how we collect, use, disclose, and safeguard information when you use the Mise platform, website, and services (collectively, the "**Service**").

This Privacy Policy applies to all users of the Service, including restaurant owners, managers, and authorized personnel who interact with the Service ("**Users**"), as well as individuals whose personal information may be contained in data submitted to the Service by Users (such as employees referenced in payroll voice recordings).

By using the Service, you consent to the practices described in this Privacy Policy. If you do not agree with this Privacy Policy, please do not use the Service.

---

## 2. INFORMATION WE COLLECT

### 2.1 Information You Provide

<div class="info-category">

**Account Information**
> Name, email address, phone number
> Business name and address
> Job title and role
> Account credentials (username, password)

</div>

<div class="info-category">

**Voice Data**
> Audio recordings submitted through the Service
> Transcripts generated from voice recordings
> Corrections and edits to transcripts

</div>

<div class="info-category">

**Payroll Information**
> Employee names and identifiers
> Hours worked, shift times, roles
> Tip amounts, tipouts, and wage calculations
> Approval and review actions

</div>

<div class="info-category">

**Inventory Information**
> Product names and counts
> Inventory session data and shelfy locations
> Product catalog information
> Vendor and pricing data

</div>

<div class="info-category">

**Payment Information**
> Billing address
> Payment method details (processed by third-party payment processors — we do not store full credit card numbers)

</div>

<div class="info-category">

**Communications**
> Customer support inquiries
> Feedback and suggestions
> Email correspondence

</div>

### 2.2 Information Collected Automatically

**Usage Data** — Features used and actions taken, session duration and frequency, error logs and performance data, workflow completion rates

**Device Information** — Device type, operating system, browser type and version, IP address, unique device identifiers

**Cookies and Tracking** — We use cookies and similar technologies to maintain session state and analyze usage patterns. We do not use cookies for advertising or cross-site tracking.

### 2.3 Information About Third Parties

**Employee Data in Voice Recordings.** When you submit voice recordings to the Service (for example, to report payroll shifts or inventory counts), those recordings frequently contain personal information about your employees, including names, hours worked, and tip amounts. **You are the data controller for this employee data.** Mise processes it solely on your behalf to provide the Service.

### 2.4 Information from Third-Party Sources

> (a) Identity verification services
> (b) Payment processors (payment confirmation and billing status)
> (c) Analytics providers (usage patterns and aggregated data)

---

## 3. HOW WE USE YOUR INFORMATION

We use the information we collect for the following purposes:

| Purpose | Legal Basis | Examples |
|---------|-------------|----------|
| **Service Provision** | Contract performance | Process voice recordings, calculate payroll, track inventory, manage accounts |
| **Service Improvement** | Legitimate interest | Improve transcription accuracy, develop features, analyze usage (using aggregated/de-identified data) |
| **Communications** | Contract performance / Legitimate interest | Send service notifications, respond to support inquiries, provide account updates |
| **Security & Compliance** | Legal obligation / Legitimate interest | Detect fraud, enforce Terms of Service, comply with legal obligations |
| **Billing** | Contract performance | Process payments, manage subscriptions, send invoices |

**We do NOT use your information for:**

> (a) Selling your personal information to third parties;
>
> (b) Serving targeted advertising;
>
> (c) Building consumer profiles unrelated to the Service; or
>
> (d) Any purpose incompatible with the purposes disclosed in this Privacy Policy.

---

## 4. HOW WE SHARE YOUR INFORMATION

We may share your information only in the following circumstances:

### 4.1 Service Providers (Sub-Processors)

We share information with third-party service providers who assist us in operating the Service. These providers are contractually obligated to use your information only as directed by us and to maintain appropriate security measures.

| Provider | Purpose | Data Shared |
|----------|---------|-------------|
| **Google Cloud Platform** | Cloud hosting, storage, computing | All Service data (encrypted at rest and in transit) |
| **Google BigQuery** | Structured data storage and querying | Payroll records, inventory data, operational data |
| **OpenAI** (Whisper) | Voice transcription | Audio recordings (processed, not retained by OpenAI per our agreement) |
| **Anthropic** (Claude) | AI processing and data extraction | Transcripts (processed, not retained by Anthropic per our agreement) |
| **Payment Processor** | Payment processing | Billing information |

### 4.2 Business Transfers

If Mise is involved in a merger, acquisition, financing, dissolution, or sale of all or a portion of its assets, your information may be transferred as part of that transaction. We will provide notice before your information becomes subject to a different privacy policy.

### 4.3 Legal Requirements

We may disclose information if required to do so by law, subpoena, court order, or legal process, or if we believe in good faith that disclosure is necessary to:

> (a) Comply with applicable law or legal obligations;
>
> (b) Protect the rights, property, or safety of Mise, our users, or the public;
>
> (c) Prevent fraud or enforce our Terms of Service; or
>
> (d) Respond to an emergency involving danger of death or serious physical injury.

### 4.4 With Your Consent

We may share information with your explicit consent or at your direction, including when you instruct us to export data to third-party services (such as MarginEdge for inventory).

### 4.5 Aggregated and De-Identified Data

We may share aggregated or de-identified information that cannot reasonably be used to identify you or your business. Such data is not subject to the restrictions in this Privacy Policy.

---

## 5. VOICE DATA PRACTICES

Given the sensitive nature of voice data, we provide the following detailed disclosures:

<div class="highlight-box">

**What We Record**
Only voice memos explicitly submitted by Users through the Service. We do **NOT** continuously record, passively listen, or monitor ambient audio. Recording begins only when a User actively initiates a recording session.

**How We Process Voice Data**
1. User initiates a recording through the Mise app or web interface
2. Audio file is securely transmitted to our servers (encrypted in transit via TLS)
3. Audio is sent to OpenAI Whisper for transcription
4. Transcript is processed by Anthropic Claude to extract structured data (shifts, counts, etc.)
5. Structured results are presented to the User for review and approval
6. User approves, edits, or rejects the results

**Audio Storage**
- Audio files are stored in Google Cloud Storage, encrypted at rest
- Audio files are retained for 90 days from the date of upload (see Section 8)
- Transcripts and structured data derived from audio are retained for the duration of your account plus 3 years

**Third-Party Processing**
- **OpenAI** (Whisper transcription) — Audio is processed via API; per our agreement, OpenAI does not retain audio data after processing for API customers
- **Anthropic** (Claude AI processing) — Transcripts are processed via API; per our agreement, Anthropic does not use API data for model training

We maintain data processing agreements with these providers that include obligations regarding data security, processing limitations, and data deletion.

</div>

---

## 6. VOICE DATA AND BIOMETRIC INFORMATION

**6.1 Biometric Data Notice.** Certain state laws (including the Illinois Biometric Information Privacy Act and similar statutes in Texas, Washington, and other states) regulate the collection and use of biometric information, which may include voiceprints derived from audio recordings.

**6.2 Our Practices.** Mise does **NOT** create, collect, store, or use voiceprints or biometric identifiers derived from voice recordings. Our transcription process converts speech to text — it does not extract biometric characteristics, speaker identification features, or voice signatures.

**6.3 No Biometric Template Creation.** The Service does not compare voices, identify speakers by voice characteristics, or create biometric templates. Speaker identification in transcripts (e.g., attributing a reported shift to a named employee) is based on the spoken content of the recording (e.g., "Sarah worked Tuesday"), not on voice biometric analysis.

---

## 7. PAYROLL DATA PRACTICES

Payroll data is particularly sensitive. Here is how we handle it:

| Data We Process | Data We Do NOT Collect |
|-----------------|------------------------|
| Employee names and roles | Social Security numbers |
| Hours worked and tip amounts | Bank account or routing numbers |
| Calculated wages and tipouts | Tax withholding information |
| Shift dates and times | Direct deposit details |
| Approval/review actions | W-4 or I-9 information |

**7.1 Accidental Sensitive Data.** If a User inadvertently includes sensitive personal information in a voice recording (such as a Social Security number, bank account number, or medical information), Mise will make reasonable efforts to flag and redact such information upon discovery. However, Mise cannot guarantee detection of all inadvertently disclosed sensitive information. Users should avoid including sensitive data in voice recordings.

**7.2 Your Responsibility.** You are responsible for ensuring that any employee data you submit to the Service complies with applicable privacy and employment laws and that you have an appropriate legal basis (such as legitimate business interest or consent) for processing such data through the Service.

---

## 8. DATA SECURITY

We implement appropriate technical and organizational measures to protect your information, including:

> (a) **Encryption in transit** — All data transmitted between your device and our servers is encrypted using TLS 1.2 or higher;
>
> (b) **Encryption at rest** — All data stored on our servers is encrypted using AES-256 encryption via Google Cloud Platform's default encryption;
>
> (c) **Access controls** — Role-based access controls limit access to personal data to authorized personnel who require it for their job function;
>
> (d) **Infrastructure security** — Our infrastructure is hosted on Google Cloud Platform, which maintains SOC 2 Type II, ISO 27001, and other industry-standard security certifications;
>
> (e) **Security monitoring** — We monitor our systems for unauthorized access and security incidents; and
>
> (f) **Incident response** — We maintain an incident response plan to address potential data breaches.

**No Guarantee.** While we implement commercially reasonable security measures, no method of electronic transmission or storage is 100% secure. We cannot guarantee the absolute security of your information.

**Breach Notification.** In the event of a data breach affecting your personal information, we will notify you and applicable regulatory authorities as required by applicable law.

---

## 9. DATA RETENTION

We retain your information for as long as necessary to provide the Service, comply with legal obligations, resolve disputes, and enforce our agreements.

| Data Type | Retention Period | Basis |
|-----------|------------------|-------|
| Account information | Duration of account + 3 years after deletion | Legitimate interest, legal compliance |
| Voice recordings (audio files) | 90 days from date of upload | Service provision |
| Transcripts and structured data | Duration of account + 3 years after deletion | Service provision, legal compliance |
| Payroll reports | Duration of account + 7 years after deletion | Federal/state record retention requirements |
| Payment and billing records | 7 years from date of transaction | Tax and financial compliance |
| Usage logs and analytics | 2 years | Service improvement |

**Deletion.** When information is no longer needed and no legal retention obligation applies, we delete or irreversibly anonymize it. You may request earlier deletion as described in Section 10.

---

## 10. YOUR RIGHTS AND CHOICES

Depending on your location, you may have certain rights regarding your personal information:

| Right | Description |
|-------|-------------|
| **Access** | Request a copy of the personal information we hold about you |
| **Correction** | Request correction of inaccurate or incomplete information |
| **Deletion** | Request deletion of your personal information (subject to legal retention requirements) |
| **Portability** | Request a portable copy of your data in a structured, commonly used, machine-readable format |
| **Opt-Out of Marketing** | Opt out of marketing communications at any time (Service notifications are not marketing) |
| **Objection** | Object to certain processing of your information based on legitimate interest |
| **Restriction** | Request that we restrict processing of your information in certain circumstances |

**How to Exercise Your Rights:** Contact us at privacy@getmise.io with your request. Please include sufficient information for us to verify your identity.

**Response Time:** We will acknowledge your request within 10 business days and provide a substantive response within 30 days, or as required by applicable law. If we need additional time, we will notify you of the extension and the reason.

**Verification.** We may need to verify your identity before processing your request to protect against unauthorized access to personal information.

---

## 11. CALIFORNIA PRIVACY RIGHTS (CCPA/CPRA)

If you are a California resident, you have rights under the California Consumer Privacy Act, as amended by the California Privacy Rights Act (collectively, "**CCPA**"):

**Right to Know** — You may request information about the categories and specific pieces of personal information we have collected about you in the preceding 12 months, the categories of sources, the business purposes for collection, and the categories of third parties with whom we share it.

**Right to Delete** — You may request deletion of your personal information, subject to certain exceptions (such as legal retention requirements).

**Right to Correct** — You may request correction of inaccurate personal information.

**Right to Opt-Out of Sale or Sharing** — Mise does **NOT** sell personal information. Mise does **NOT** share personal information for cross-context behavioral advertising purposes. If these practices change, we will provide a "Do Not Sell or Share My Personal Information" link.

**Right to Limit Use of Sensitive Personal Information** — To the extent we process sensitive personal information (such as account credentials), we use it only for purposes permitted under the CCPA, including providing the Service you requested.

**Non-Discrimination** — We will not discriminate against you for exercising your CCPA rights. We will not deny you goods or services, charge different prices, or provide a different level of quality for exercising these rights.

**Authorized Agents.** You may designate an authorized agent to submit a request on your behalf. We may require verification of the agent's authority.

**To submit a CCPA request:** Contact us at privacy@getmise.io or by mail at the address in Section 16.

---

## 12. FLORIDA PRIVACY DISCLOSURES

As a company headquartered in Florida, we comply with the Florida Digital Bill of Rights (effective July 1, 2024, for qualifying controllers). To the extent applicable:

> (a) We do not sell your personal data;
>
> (b) We do not process personal data for targeted advertising based on data collected from other websites or applications;
>
> (c) We do not process sensitive personal data without your consent; and
>
> (d) Florida residents may exercise rights of access, correction, deletion, and portability by contacting us at privacy@getmise.io.

---

## 13. CHILDREN'S PRIVACY

The Service is **NOT** intended for individuals under the age of 18. We do not knowingly collect personal information from children under the age of 18. If we learn that we have collected information from a child under 18, we will promptly delete such information. If you believe we have inadvertently collected information from a child, please contact us immediately at privacy@getmise.io.

---

## 14. DO NOT TRACK

Some web browsers transmit "Do Not Track" signals. Because there is no uniform standard for how "Do Not Track" signals should be interpreted, the Service does not currently respond to "Do Not Track" signals. We do not track users across third-party websites for advertising purposes.

---

## 15. INTERNATIONAL DATA TRANSFERS

The Service is operated from the United States. If you are located outside the United States, please be aware that your information will be transferred to, stored, and processed in the United States, where data protection laws may differ from those of your country of residence.

By using the Service from outside the United States, you expressly consent to the transfer and processing of your information in the United States. If you do not consent, please do not use the Service.

---

## 16. THIRD-PARTY LINKS AND SERVICES

The Service may contain links to third-party websites or integrate with third-party services (such as MarginEdge for inventory management). This Privacy Policy does not apply to the practices of third parties. We encourage you to review the privacy policies of any third-party services you access through or in connection with the Service.

---

## 17. CHANGES TO THIS PRIVACY POLICY

We may update this Privacy Policy from time to time. When we make material changes, we will:

> (a) Post the updated Privacy Policy on our website with the new effective date;
>
> (b) Send an email notification to the address associated with your account; and
>
> (c) Provide notice through the Service.

Material changes will not take effect until at least thirty (30) days after notice is provided. Your continued use of the Service after the effective date of changes constitutes acceptance of the updated Privacy Policy. If you do not agree with the changes, you should stop using the Service and contact us to delete your account.

---

## 18. DATA PROTECTION CONTACT

If you have questions, concerns, or complaints regarding this Privacy Policy or our privacy practices, please contact:

<div class="contact-block">

**Mise, Inc.**
7901 4th St. North #9341
St. Petersburg, FL 33702

**Privacy inquiries:** privacy@getmise.io
**General inquiries:** support@getmise.io
**Data Protection Contact:** Jonathan Flaig, President and CEO

</div>

If you are not satisfied with our response, you may have the right to lodge a complaint with a data protection authority in your jurisdiction.

---

## APPENDIX A: CCPA DISCLOSURES

### Categories of Personal Information Collected (Preceding 12 Months)

| CCPA Category | Examples | Collected | Source | Business Purpose |
|---------------|----------|-----------|--------|------------------|
| A. Identifiers | Name, email, IP address, account ID | Yes | User, Automatic | Service provision, communications |
| B. Customer Records (Cal. Civ. Code §1798.80(e)) | Account info, billing info | Yes | User | Account management, billing |
| C. Protected Classification Characteristics | None collected | No | — | — |
| D. Commercial Information | Subscription history, transaction records | Yes | User, Automatic | Billing, service provision |
| E. Biometric Information | None collected (see Section 6) | No | — | — |
| F. Internet/Network Activity | Usage data, access logs, features used | Yes | Automatic | Service improvement, security |
| G. Geolocation | IP-based approximate location | Yes | Automatic | Security, compliance |
| H. Sensory Data | Voice recordings submitted by Users | Yes | User | Core service provision |
| I. Professional/Employment Info | Job title, employer, role | Yes | User | Account setup |
| J. Education Information | None collected | No | — | — |
| K. Inferences | Usage patterns, workflow preferences | Yes | Automatic | Service improvement |
| L. Sensitive Personal Information | Account credentials (login/password) | Yes | User | Authentication |

### Retention Periods

See Section 9 for detailed retention periods by data type.

### Sale and Sharing

Mise has **NOT** sold or shared (for cross-context behavioral advertising) any personal information in the preceding 12 months.

---

<div class="footer-notice">
<em>This document requires attorney review before publication.</em>
</div>
