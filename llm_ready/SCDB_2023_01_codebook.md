# Supreme Court Database Code Book brick\_2023\_01

#### CONTRIBUTORS

#### **Harold Spaeth**

Michigan State University College of Law

#### **Lee Epstein**

Washington University in Saint Louis

#### **Ted Ruger**

University of Pennsylvania School of Law

#### **Sarah C. Benesh**

University of Wisconsin - Milwaukee Department of Political Science

#### **Jeffrey Segal**

Stony Brook University Department of Political Science

#### **Andrew D. Martin**

University of Michigan College of Literature, Science, and the Arts

*Document Crafted On December 24, 2023 @ 05:01*

## Table of Contents

#### INTRODUCTORY

- Introduction
- Citing to the SCDB

#### IDENTIFICATION VARIABLES

- SCDB Case ID
- SCDB Docket ID
- SCDB Issues ID
- SCDB Vote ID
- U.S. Reporter Citation
- Supreme Court Citation
- Lawyers Edition Citation
- LEXIS Citation
- Docket Number

#### BACKGROUND VARIABLES

- Case Name
- Petitioner
- Petitioner State
- Respondent
- Respondent State
- Manner in which the Court takes Jurisdiction
- Administrative Action Preceeding Litigation
- Administrative Action Preceeding Litigation State
- Three-Judge District Court
- Origin of Case
- Origin of Case State
- Source of Case
- Source of Case State
- Lower Court Disagreement

| 26 | Reason for Granting Cert                 |
|----|------------------------------------------|
| 27 | Lower Court Disposition                  |
| 28 | Lower Court Disposition Direction        |
|    |                                          |
|    | CHRONOLOGICAL VARIABLES                  |
| 29 | Date of Decision                         |
| 30 | Term of Court                            |
| 31 | Natural Court                            |
| 32 | Chief Justice                            |
| 33 | Date of Oral Argument                    |
| 34 | Date of Reargument                       |
|    |                                          |
|    | SUBSTANTIVE VARIABLES                    |
| 35 | Issue                                    |
| 36 | Issue Area                               |
| 37 | Decision Direction                       |
| 38 | Decision Direction Dissent               |
| 39 | Authority for Decision 1                 |
| 40 | Authority for Decision 2                 |
| 41 | Legal Provisions Considered by the Court |
| 42 | Legal Provision Supplement               |
| 43 | Legal Provision Minor Supplement         |
|    |                                          |
|    | OUTCOME VARIABLES                        |
| 44 | Decision Type                            |
| 45 | Declaration of Unconstitutionality       |
| 46 | Disposition of Case                      |
| 47 | Unusual Disposition                      |
| 48 | Winning Party                            |
| 49 | Formal Alteration of Precedent           |
|    |                                          |

#### VOTING & OPINION VARIABLES

| 50  | Vote Not Clearly Specified                  |
|-----|---------------------------------------------|
| 51  | Majority Opinion Writer                     |
| 52  | Majority Opinion Assigner                   |
| 53  | Split Vote                                  |
| 54  | Majority Votes                              |
| 55  | Minority Votes                              |
| 56  | Justice ID                                  |
| 57  | Justice Name                                |
| 58  | The Vote in the Case                        |
| 59  | Opinion                                     |
| 60  | Direction of the Individual Justice's Votes |
| 61  | Majority and Minority Voting by Justice     |
| 62  | First Agreement                             |
| 63  | Second Agreement                            |
|     |                                             |
|     | APPENDICES / DATA NORMALIZATIONS            |
| A1  | varAdminAction                              |
| A2  | varAuthorityDecision                        |
| A3  | varCaseDispositionLc                        |
| A4  | varCaseDispositionSc                        |
| A5  | varCaseDispositionUnusual                   |
| A6  | varCaseSources                              |
| A7  | varCertReason                               |
| A8  | varChiefs                                   |
| A9  | varDecisionDirection                        |
| A10 | varDecisionDirectionDissent                 |
| A11 | varDecisionTypes                            |
| A12 | varDeclarationUncon                         |
| A13 | varIssues                                   |

A14 varIssuesAreas

A15 varJurisdiction

A16 varJusticeDirection

| A17 | varJusticeMajority     |
|-----|------------------------|
| A18 | varJusticeOpinion      |
| A19 | varJustices            |
| A20 | varLawArea             |
| A21 | varLcDisagreement      |
| A22 | varLegalProvisions     |
| A23 | varNaturalCourt        |
| A24 | varParties             |
| A25 | varPartyWinning        |
| A26 | varPrecedentAlteration |
| A27 | varSplitVote           |
| A28 | varStates              |
| A29 | varThreeJudgeFdc       |
| A30 | varVote                |

A31 varVoteUnclear

## 1 Introduction

A Prefatory Note from Harold J. Spaeth, Distinguished University Professor, emeritus, Michigan State University;

Research Professor in the College of Law and in the Institute for Public Policy & Social Research.

The database to which this introduction pertains spans all four centuries of the Court's decisions, from its first decision in 1791 to the Court's most recent decision. As such, it contains sixty variables for each case which, in turn, are composed of 2,633 elements, or components. The data in any given case, therefore, is drawn from a universe of 157,980 data points. The likelihood of resulting error -- actual or debatable -- remains ever present, and so I invite users of the database to inform me not only of errors, but also of any comments or suggestions (good, bad, or indifferent) they care to make at spaeth@msu.edu.

The initial version of this database, which began with the Warren Court in 1953 and was back dated to the beginning of the Vinson Court in 1946, dates from the mid-1980's at the dawn of the desktop computing revolution and relies on pre-microcomputing and pre-internet conditions. As such, users needed knowledge of statistical software packages and the codified variables that the database contains. This new version, however, recognizes the existence of the 21st century by eliminating acquaintance with statistical software packages and coded variables. Plain English rules! But do note that the database can be uploaded into statistical packages to perform advanced calculations if a user so desires.

Aside from the foregoing, the major feature of this version of the database is an interface that is in line with modern technology and which will allow users to directly calculate and view relationships among the variables in the database. At present, this feature is available for the post-1946 terms; we are working on incorporating the legacy data.

I have specified decision rules governing the entry of data into the various variables, most particularly the legal provisions governing the Court's decisions and the issues to which cases pertain. These, however, are not set in concrete. You, of course, are free to redefine any and all variables on your copy of the database. If convention applies, I adhere to it. But for many variables and their specific entries, none exists.

Because the database now extends over four centuries, it is necessary to add, alter, and adjust a number of variables. I do so to keep the legacy cases (those decided between 1791 and the Court's acquisition of discretionary jurisdiction as a result of the Judges' Bill of 1925) as congruent as possible with the Court's modern decisions. These changes primarily apply to the issues the Court decides. Most notable is the addition of a set of common law issues. These account for much of the Court's heritage decisions, especially those of the 19th century, and have had little applicability to any but the parties to these cases.

In specifying the issue in the legacy cases I have chosen the one that best accords with what today's Court would consider the issue to be. For example, "prize cases," those in which vessels were captured on the high seas and brought into U.S. ports, are categorized either as Fifth Amendment takings clause cases or as cases pertaining to the jurisdiction of the federal district or appeals courts, depending on which issue the Court based its decision.This was done to provide a basis for continuity in the Court's decision making and to avoid undue segmentation of the Court's decisions. The same rule applies to various provisions pertaining to the Bill of Rights even though

the Fourteenth Amendment had not been ratified and no guarantees of the Bill of Rights had been made binding on the state and local governments.

Do recognize, however, that the foregoing paragraph applies only to the issue(s) the Court addressed and not to the legal provisions decided by the Court. The latter were largely nonexistent before the end of the Civil War. These early legacy decisions generally rested either on the common law or judicial fiat.

Because of current concerns I have given primacy to issues involving women and Native Americans in cases in which they are involved.

The major shortcomings of this beta version of the database are, first, the incomplete rendering of the legacy cases' (pre-1946) legal provisions. We had assumed that the structure of the legacy cases would follow the pattern of those decided in 1946 and thereafter. Unfortunately, we were mistaken. Multiple issues and legal provisions in the modern cases were coded contemporaneously as they were handed down except for Vinson Court decisions (1946-1952) which were coded as a group in the 1970's. I simply added a second or third record to the case when I initially coded it a few days after the Court handed it down. Given that these heritage cases had been decided in the 154 years between 1791 and 1945, it was of course impossible to have followed the current procedure of entering all case data within a few days of its decision. Adding this additional information would have postponed the release of this beta version of the database for several more years, to say nothing of the alpha version.

Hence, if you are analyzing issue, legal provision, or direction (liberal, conservative, indeterminate), keep in mind that the data pertain only to the first of what may comprise an additional number of issues or legal provisions for any given case. This will be no problem for many studies but for some your analysis may be incomplete. Thus, if you are analyzing all selfincrimination cases, or all those pertaining to the Judiciary Act of 1789, or all state police power cases that pertain to welfare or morals legislation you will have the bulk of such cases, but not quite all.

A second shortcoming is that only the case-centered version of the heritage database is available at present. This presents no problem if you are interested only in case citation, which most users are. The next major release will include a docket-centered version.

I wish to thank my former student, Distinguished University Professor Jeffrey Segal of the State University of New York at Stony Brook for his extremely valuable comments and suggestions on all phases and aspects of the database since its inception in the early 1980's. I also thank Harriet Dhanak, the former programming and software specialist in the Department of Political Science at Michigan State University, for her expert guidance and assistance. Her successor, Lawrence Kestenbaum, continued and extended the stellar services on which I had become dependent. Most recently I have relied on the superb technical knowledge and skills of John Schwarz of the Michigan State University Institute for Political and Social Science Research and his talented successor, Jess Sprague. Professor Tim Hagle of the University of Iowa continues to systematically inform me of errors and missing data that I have overlooked. My former graduate students, now well tenured scholars--Sara C. Benesh and Wendy L. Martinek--have shepherded me through the more arcane byways of current versions of statistical software packages. And though this feature of the database is now passe, their previous assistance has been key.

I also deeply appreciate the support provided me by the Michigan State University College of Law

and that of Milly Shiraev of the University's Institute for Political and Social Science Research.

Three outstanding individuals are most responsible for this version of the database. Lee Epstein, whose wide-ranging scholarly productivity is unmatched in the world of judicial scholarship and effectively compliments her hard driving even-handed taskmastership; Andrew D. Martin, former chair of the Department of Political Science, professor of law, and Director of the Center for Empirical Research in Law (CERL) at Washington University in St. Louis, and now Chancellor of Washington University in St. Louis, whose methodological competence knows no bounds; and Troy DeArmitt, former Technology Director of CERL. Without his masterful skills the database would still be locked into its primitive pre-microcomputer and pre-internet structure. Its transformation into the creatively designed and implemented database you have at hand is Troy's creation.

Compilation of this database has been supported by grants from the National Science Foundation. Without its assistance, the database would not exist.

#### Notes to All Users

- 1. The Supreme Court Database's research team continuously updates the database. Accordingly, we urge you to pay attention to the date your version appeared on the website and to check whether it is the current one.
- 2. The codebook now provides five pieces of information for each variable: the name of the variable as it appears in the current version of the Database, the name Spaeth used in previous versions (if applicable), any normalization (changes we made when converting from Spaeth's format to the new web version), and, of course, a description of the variable and a list of its values.
  - *End of Content for Variable 1. Introduction -*

## 2 Citing to the SCDB

To cite to the Supreme Court Database, please employ either of the following: Harold J. Spaeth, Lee Epstein, Andrew D. Martin, Jeffrey A. Segal, Theodore J. Ruger, and Sara C. Benesh. 2023 Supreme Court Database, Version 2023 Release 01. URL: http://supremecourtdatabase.org

Harold J. Spaeth, Lee Epstein, et al. 2023 Supreme Court Database, Version 2023 Release 1. URL: http://supremecourtdatabase.org

Please be sure to include the specific Version Number; e.g., 'Version 2023 Release 01' in your citation as this will indicate the particular version of the database being employed at the time of your reference. This matter is of great importance as the database will be updated with newly announced decisions, corrections, and the addition of new data for existing cases.

*- End of Content for Variable 2. Citing to the SCDB -*

## 3 SCDB Case ID

| Variable Name | Spaeth Name | Normalizations |
|---------------|-------------|----------------|
| caseId        | n/a         | n/a            |

This is the first of four unique internal identification numbers.

The first four digits are the term. The next four are the case within the term (starting at 001 and counting up).

*- End of Content for Variable 3. SCDB Case ID -*

## 4 SCDB Docket ID

| Variable Name | Spaeth Name | Normalizations |
|---------------|-------------|----------------|
| docketId      | n/a         | n/a            |

This is the second of four unique internal identification numbers.

The first four digits are the term. The next four are the case within the term (starting at 001 and counting up). The last two are the number of dockets consolidated under the U.S. Reports citation (starting at 01 and counting up).

*- End of Content for Variable 4. SCDB Docket ID -*

## 5 SCDB Issues ID

| Variable Name | Spaeth Name | Normalizations |
|---------------|-------------|----------------|
| caseIssuesId  | n/a         | n/a            |

This is the third of four unique internal identification numbers.

The first four digits are the term. The next four are the case within the term (starting at 001 and counting up). The next two are the number of dockets consolidated under the U.S. Reports citation (starting at 01 and counting up). The last two are the number of issues and legal provisions within the case (starting at 01 and counting up).

*- End of Content for Variable 5. SCDB Issues ID -*

## 6 SCDB Vote ID

| Variable Name | Spaeth Name | Normalizations |
|---------------|-------------|----------------|
| voteId        | n/a         | n/a            |

This is the fourth of four unique internal identification numbers.

The first four digits are the term. The next four are the case within the term (starting at 001 and counting up). The next two are the number of dockets consolidated under the U.S. Reports citation (starting at 01 and counting up). The next two are the number of issues and legal provisions within the case (starting at 01 and counting up). The next two indicate a split vote within an issue or legal provision (01 for only one vote; 02 if a split vote). The final two represent the vote in the case (usually runs 01 to 09, but fewer if less than all justices participated).

*- End of Content for Variable 6. SCDB Vote ID -*

## 7 U.S. Reporter Citation

| Variable Name | Spaeth Name | Normalizations |
|---------------|-------------|----------------|
| usCite        | US          | n/a            |

The next four variables provide the citation to each case from the official United States Reports (US) and the three major unofficial Reports, the Supreme Court Reporter (S.CT), the Lawyers' Edition of the United States Reports(LEd), and the LEXIS cite.

Especially note that these four Reporters are not identical in the cases they report. Slight differences exist among the per curiam and non-orally argued decisions and whether or not multiple citations accompany the lead decision under the original citation. Our listing derives primarily from that of the Lawyer's Edition, supplemented by the US Reports.

Except for memorandum decisions at the back of each volume, we include virtually every decision the Court has made during its four centuries of existence.

Also note that LEXIS cites have the advantage of being unique; the other reporters can have multiple cases on the same page.

Further note that pagination does not invariably proceed chronologically throughout the volumes. Hence, do not assume that because a given citation has a higher page number than that of another case it was decided on the same or a later date as the other case. The only accurate way to sequence the cases chronologically is by indexing or otherwise sequencing each case's date of decision (date of decision).

*- End of Content for Variable 7. U.S. Reporter Citation -*

## 8 Supreme Court Citation

| Variable Name | Spaeth Name | Normalizations |
|---------------|-------------|----------------|
| sctCite       | SCT         | n/a            |

See variable U.S. Reporter Citation (usCite).

*- End of Content for Variable 8. Supreme Court Citation -*

## 9 Lawyers Edition Citation

| Variable Name | Spaeth Name | Normalizations |
|---------------|-------------|----------------|
| ledCite       | LED         | n/a            |
|               |             |                |

See variable U.S. Reporter Citation.

*- End of Content for Variable 9. Lawyers Edition Citation -*

## 10 LEXIS Citation

| Variable Name | Spaeth Name | Normalizations |
|---------------|-------------|----------------|
| lexisCite     | n/a         | n/a            |

See variable U.S. Reporter Citation (usCite).

*- End of Content for Variable 10. LEXIS Citation -*

## 11 Docket Number

| Variable Name | Spaeth Name | Normalizations |
|---------------|-------------|----------------|
| docket        | DOCKET      | n/a            |
|               |             |                |

This variable contains the docket number that the Supreme Court has assigned to the case. Prior to the first two terms of the Burger Court (1969-1970), different cases coming to the Court in different terms could have the same docket number. The Court eliminated the possibility of such duplication by including the last two digits of the appropriate term before the assigned docket number. Since the 1971 Term, the Court has also operated with a single docket. Cases filed pursuant to the Court's appellate jurisdiction have a two-digit number corresponding to the term in which they were filed, followed by a hyphen and a number varying from one to five digits. Cases invoking the Court's original jurisdiction have a number followed by the abbreviation, "Orig."

During much of the legacy period, docket number do not exist in the Reports; a handful of more modern cases also lack a docket number. For these, the docket variable has no entry.

For administrative purposes, the Court uses the letters, "A," "D," and "S," in place of the term year to identify applications ("A") for stays or bail, proceedings of disbarment or discipline of attorneys ("D"), and matters being held indefinitely for one reason or another ("S"). These occur infrequently and then almost always in the Court's summary orders at the back of each volume of the U.S.Reports. The database excludes these cases, the overwhelming majority of which are denials of petition for certiorari.

Note that the Court can consolidate multiple petitions--each with its own docket number--under one U.S. cite. If you are interested in only the first (lead) case, use the database organized by Supreme Court citation. If you are interested in all the cases consolidated under one cite, select the data organized by docket. Multiple docket numbers under a single case citation almost always contain the same issue as the lead case and differ only in the parties to the case and its origin and source

For the first release of the legacy dataset, only data by citation are available. Users interested in the Vinson Court forward can still download or analyze the data by citation or docket.

*- End of Content for Variable 11. Docket Number -*

## 12 Case Name

| Variable Name | Spaeth Name | Normalizations |
|---------------|-------------|----------------|
| caseName      | n/a         | n/a            |

This is the name of the case. We derived the post-heritage names from WESTLAW and then did a bit of tidying so that they appear in a consistent format. With the exception of various Latin phrases and abbreviations, all words are now in upper case.

The names of the heritage cases are taken from the LAWYERS' EDITION of the Reports. If you are searching for a particular case and do not find it, it likely results because of a variant name. The citation of the case should, however, enable you to find the desired case.

Note that case name is tied to the docket number. In other words, if multiple cases appear under the same citation, the case name will be that of the particular case, not the lead case.

*- End of Content for Variable 12. Case Name -*

## 13 Petitioner

| Variable Name | Spaeth Name | Normalizations   |
|---------------|-------------|------------------|
| petitioner    | PARTY_1     | varParties (311) |
|               |             |                  |

The next four variables identify the parties to the case. "Petitioner" refers to the party who petitioned the Supreme Court to review the case. This party is variously known as the petitioner or the appellant. "Respondent" refers to the party being sued or tried and is also known as the appellee. Variables "petitioner" and "respondent" provide detailed information about all parties, except the identity of the state if a state (or one of its subdivisions) is a party, petitioner and respondent variables note only whether a state is a party, not the state's name. See variables Petitioner State and Respondent State for the name.

The specific codes that appear below were created inductively, with petitioner and respondent characterized as the Court's opinion identifies them.

In describing the parties in the cases before it, the justices employ terminology that places them in the context of the litigation in which they are involved. Accordingly, an employer who happens to be a manufacturer will be identified as the former if its role in the litigation is that of an employer and as the latter if its role is that of a business. Because the justices describe litigants in this fashion, a fairly limited vocabulary characterizes them. Note that the list of parties also includes the list of administrative agencies and officials contained in administrative action preceding litigation.

Also note that the Court's characterization of the parties applies whether the petitioner and respondent are actually single entities or whether many other persons or legal entities have associated themselves with the lawsuit. That is, the presence of the phrase, et al., following the name of a party does not preclude the Court from characterizing that party as though it were a single entity. Thus, each docket number will show a single petitioner and a single respondent, regardless of how many legal entities were actually involved.

The decision rules governing the identification of parties are as follows.

- 1. Parties are identified by the labels given them in the opinion or judgment of the Court except where the Reports title a party as the "United States" or as a named state. Textual identification of parties is typically provided prior to Part I of the Court's opinion. The official syllabus, the summary that appears on the title page of the case, may be consulted as well. In describing the parties, the Court employs terminology that places them in the context of the specific lawsuit in which they are involved. E.g., "employer" rather than "business" in a suit by an employee; as a "minority," "female," or "minority female" employee rather than "employee" in a suit alleging discrimination by an employer.
- 2. Where a choice of identifications exists that which provides information not provided by the legal provision or the issue is chosen. E.g., a federal taxpayer or an attorney accused of a crime as taxpayer or attorney rather than accused person, particularly if neither the lawType nor the Issue variable identifies the case as a tax matter or one involving an attorney.
- 3. Identify the parties by reference to the following list and by the list of federal agencies provided in the adminAction variable.

The Supreme Court Database Codebook

*- End of Content for Variable 13. Petitioner -*

## 14 Petitioner State

| Variable Name   | Spaeth Name | Normalizations |  |
|-----------------|-------------|----------------|--|
| petitionerState | PARTY_1     | varStates (64) |  |
|                 |             |                |  |

This variable identifies the state if the state or any one of the below is the petitioner. The exceptions are courts, judicial districts, or judges. If they are federal courts or federal judges, the "state" is always the United States. The same holds for other federal employees or officials.

- !"specified state board or department of education
- !"city, town, township, village, or borough government or governmental unit
- !"state commission, board, committee, or authority
- !"county government or county governmental unit
- !"state department or agency
- !"court or judicial district
- !"governmental employee or job applicant
- !"female governmental employee or job applicant
- !"minority governmental employee or job applicant
- !"minority female governmental employee or job applicant
- !"federal government corporation
- !"retired or former governmental employee
- !"U.S. House of Representatives interstate compact
- !"judge
- !"state legislature, house, or committee
- !"local governmental unit other than a county, city, town, township, village, or borough
- !"governmental official, or an official of an agency established under an interstate compact
- !"state or U.S. supreme court
- !"local school district or board of education
- !"U.S. Senate
- !"U.S. senator
- !"foreign nation or instrumentality
- !"state or local governmental taxpayer, or executor of the estate of
- !"state college or university

See Petitioner variable for more details.

*- End of Content for Variable 14. Petitioner State -*

## 15 Respondent

| respondent<br>PARTY_2<br>varParties (311) | Variable Name | Spaeth Name | Normalizations |  |
|-------------------------------------------|---------------|-------------|----------------|--|
|-------------------------------------------|---------------|-------------|----------------|--|

See Petitioner variable.

*- End of Content for Variable 15. Respondent -*

## 16 Respondent State

| Variable Name   | Spaeth Name | Normalizations |
|-----------------|-------------|----------------|
| respondentState | PARTY_2     | varStates (64) |

This variable identifies the state if the state or any one of the following is the respondent:

- !"specified state board or department of education
- !"city, town, township, village, or borough government or governmental unit
- !"state commission, board, committee, or authority
- !"county government or county governmental unit
- !"state department or agency
- !"court or judicial district
- !"governmental employee or job applicant
- !"female governmental employee or job applicant
- !"minority governmental employee or job applicant
- !"minority female governmental employee or job applicant
- !"retired or former governmental employee
- !"judge
- !"state legislature, house, or committee
- !"local governmental unit other than a county, city, town, township, village, or borough
- !"governmental official, or an official of an agency established under an interstate compact
- !"state or U.S. supreme court
- !"local school district or board of education
- !"state or local governmental taxpayer, or executor of the estate of
- !"state college or university

See Petitioner variable for more details.

*- End of Content for Variable 16. Respondent State -*

## 17 Manner in which the Court takes Jurisdiction

| jurisdiction<br>JUR<br>varJurisdiction (14) |
|---------------------------------------------|
|---------------------------------------------|

The Court uses a variety of means whereby it undertakes to consider cases that it has been petitioned to review. These are listed below. The most important ones are the writ of certiorari, the writ of appeal, and for legacy cases the writ of error, appeal, and certification.

A few notes are in order. First, there are handful of cases that fall into more than one category. Marbury v. Madison, 5 U.S. 137 (1803), for example, was an original jurisdiction and a mandamus case. We code these cases on the basis of the writ. So Marbury is a coded as mandamus, not original jurisdiction.

Second, some legacy cases are "original" motions or requests for the Court to take jurisdiction but were heard or filed in another court. See, for example, Ex parte Matthew Addy S.S. & Commerce Corp., 256 U.S. 417 (1921), asking the Court to issue a writ of mandamus to a federal judge. Again, we do not code these as "original" jurisdiction cases but rather on the basis of the writ.

*- End of Content for Variable 17. Manner in which the Court takes Jurisdiction -*

## 18 Administrative Action Preceeding Litigation

**Variable Name** adminAction **Spaeth Name** ADMIN **Normalizations** varAdminAction (125)

This variable pertains to administrative agency activity occurring prior to the onset of litigation. Note that the activity may involve an administrative official as well as that of an agency. The general rule for an entry in this variable is whether administrative action occurred in the context of the case. Note too that this variable identifies the specific federal agency. If the action occurred in a state agency, adminAction is coded as 117 (State Agency). See the variable adminActionState for the identity of the state.

Determination of whether administration action occurred in the context of the case was made by reading the material which appears in the summary of the case (the material preceding the Court's opinion) and, if necessary, those portions of the prevailing opinion headed by a I or II.

Action by an agency official is considered to be administrative action except when such an official acts to enforce criminal law.

If an agency or agency official "denies" a "request" that action be taken, such denials are considered agency action.

If two federal agencies are mentioned (e.g., INS and BIA), the one whose action more directly bears on the dispute will appear; otherwise the agency that acted more recently. If a state and federal agency are mentioned, the federal agency will appear.

Excluded from entry in this variable are:

- !"A "challenge" to an unapplied agency rule, regulation, etc. A request for an injunction or a declaratory judgment against agency action which, though anticipated, has not yet occurred.
- !"A mere request for an agency to take action when there is no evidence that the agency did so.
- !"Agency or official action to enforce criminal law. The hiring and firing of political appointees or the procedures whereby public officials are appointed to office.
- !"Attorney general preclearance actions pertaining to voting. Filing fees or nominating petitions required for access to the ballot.
- !"Actions of courts martial.
- !"Land condemnation suits and quiet title actions instituted in a court.
- !"Federally funded private nonprofit organizations.

The Supreme Court Database Codebook

Nite that the following list of agencies amy also be found as a petitoner or respondent variable.

*- End of Content for Variable 18. Administrative Action Preceeding Litigation -*

## 19 Administrative Action Preceeding Litigation State

Administrative action may be either state or federal. If administrative action was taken by a state or a subdivision thereof, this variable identifies the state. See adminAction for federal agencies and for the coding rules.

When a state agency or official acts as an agent of a federal agency, it is identified as such.

*- End of Content for Variable 19. Administrative Action Preceeding Litigation State -*

## 20 Three-Judge District Court

| Variable Name | Spaeth Name | Normalizations       |
|---------------|-------------|----------------------|
| threeJudgeFdc | J3          | varThreeJudgeFdc (2) |

This variable will be checked if the case was heard by a three-judge federal district court (occasionally called "as specially constituted district court"). Beginning in the early 1900s, Congress required three-judge district courts to hear certain kinds of cases. More modern-day legislation has reduced the kinds of lawsuits that must be heard by such a court. As a result, the frequency is less for the Burger Court than for the Warren Court, and all but nonexistent for the Rehnquist and Roberts Courts.

*- End of Content for Variable 20. Three-Judge District Court -*

## 21 Origin of Case

**Variable Name** caseOrigin **Spaeth Name** ORIGIN **Normalizations** varCaseSources (211)

The focus of this variable is the court in which the case originated, not the administrative agency (see adminAction and adminActionState). For this reason a number of cases show a state or federal appellate court as the one in which the case originated rather than a court of first instance (trial court). This variable has no entry for cases that originated in the United States Supreme Court. Note too that caseOrigin does not identify the name of the state if the case originated in a state court. For the state name, see variable caseOriginState.

The courts in the District of Columbia present a special case in part because of their complex history. (The Federal Judicial Center's website provides a succinct description, at: http://www.fjc.gov/history/home.nsf/page/courts\_special\_dc.html). Below there is a separate code for the Supreme Court of the District of Columbia, which at times had the powers of a circuit court and at others was a trial court. The current federal courts, the U.S. District Court for the District of Columbia (previously known as the Supreme Court of the District of Columbia) and the District Court for the District of Columbia) and the U.S. Court of Appeals for the District of Columbia Circuit (a successor to the Court of Appeals for the District of Columbia) also, of course, have their own separate codes. Local trial (including today's superior court) and appellate courts (including today's District of Columbia Court of Appeals, the highest court in the District of Columbia) are treated as state courts here and as District of Columbia under the caseOriginState variable.

Other general coding notes:

- !"Cases that arise on a petition of habeas corpus and those removed to the federal courts from a state court are defined as originating in the federal, rather than a state, court system.
- !"This variable has no entry if the case arose under the Supreme Court's original jurisdiction and in other proceedings with which no other court was involved.
- !"A petition for a writ of habeas corpus begins in the federal district court, not the state trial court.
- !"Cases removed to a federal court originate there.

Coding notes with special relevance to the legacy database:

- !"The originating (caseOrigin) and source (caseSource) court is often the same because many cases went from trial directly to the Supreme Court. For these cases, lcDisposition (how the source court treated the originating court's decision) will be empty. An exception is the Supreme Court of the District of Columbia, which had a trial and general session. See, e.g., Thaw v. Ritchie, 136 U.S. 519 (1890), in which the court in general term reversed the trial court.
- !"We identify courts based on the naming conventions of the day. In the legacy data, users will see that many source and origin courts are "United States Circuit Court for the \_\_\_ District of \_\_\_.

Because of the plethora of districts (and changes in districts), we do not, however, differentiate among districts in a state. E.g., New York U.S. Circuit for (all) District(s) of New York includes all the districts in New York. For concise histories of the circuit and district courts, see the Federal Judicial Center's website at: http://www.fjc.gov/history/home.nsf/page/index.html.

Also see source of case (caseSource).

*- End of Content for Variable 21. Origin of Case -*

## 22 Origin of Case State

| Variable Name   | Spaeth Name | Normalizations |
|-----------------|-------------|----------------|
| caseOriginState | ORIGIN      | varStates (64) |
|                 |             |                |

If the case originated in a state court, this variable identifies the state. For more details, see the variable caseOrigin.

*- End of Content for Variable 22. Origin of Case State -*

## 23 Source of Case

| Variable Name | Spaeth Name | Normalizations       |
|---------------|-------------|----------------------|
| caseSource    | SOURCE      | varCaseSources (211) |
|               |             |                      |

This variable identifies the court whose decision the Supreme Court reviewed. If the case originated in the same court whose decision the Supreme Court reviewed, the entry in the caseOrigin should be the same as here. This variable has no entry if the case arose under the Supreme Court's original jurisdiction.

If caseSource is a state court, the value of this variable will be 300 (State Supreme Court), 302 (State Appellate Court) or 303 (State Trial Court). Variable caseSourceState identifies the name of the state.

*- End of Content for Variable 23. Source of Case -*

## 24 Source of Case State

| Variable Name   | Spaeth Name | Normalizations |  |
|-----------------|-------------|----------------|--|
| caseSourceState | SOURCE      | varStates (64) |  |
|                 |             |                |  |

If the source of the case (i.e., the court whose decision the Supreme Court reviewed) is a state court, this variable identifies the state. See also Source of Case (caseSource).

*- End of Content for Variable 24. Source of Case State -*

## 25 Lower Court Disagreement

| Variable Name  | Spaeth Name | Normalizations        |
|----------------|-------------|-----------------------|
| lcDisagreement | DISS        | varLcDisagreement (2) |

An entry in this variable indicates that the Supreme Court's majority opinion mentioned that one or more of the members of the court whose decision the Supreme Court reviewed dissented. The presence of such disagreement is limited to a statement to this effect somewhere in the majority opinion. I.e, "divided," "dissented,"

"disagreed," "split." A reference, without more, to the "majority" or "plurality" does not necessarily evidence dissent. The other judges may have concurred.

If a case arose on habeas corpus, a dissent will be indicated if either the last federal court or the last state court to review the case contained one. E.g., Townsend v. Sain, 9 Led 2d 770 (1963). A dissent will also be indicated if the highest court with jurisdiction to hear the case declines to do so by a divided vote. E.g., Simpson v. Florida, 29 L ed 2d 549 (1971).

Note that the focus of this variable tends to be a statement that a dissent occurred rather than the fact of such an occurrence. The fact of a dissent is not always mentioned in the majority opinion. It may be irrelevant. See, for example, McNally v. United States, 483 U.S. 350 (1987), and United States v. Gray and McNally, 790 F.2d 1290 (1986).

If the lower court denies an en banc petition by a divided vote and the Supreme Court discusses same, lower court disagreement exists.

If the lower court denies an en banc petition by a divided vote and the Supreme Court's opinion discusses same, a dissent occurs.

*- End of Content for Variable 25. Lower Court Disagreement -*

## 26 Reason for Granting Cert

| Variable Name | Spaeth Name | Normalizations     |
|---------------|-------------|--------------------|
| certReason    | CERT        | varCertReason (13) |
|               |             |                    |

This variable provides the reason, if any, that the Court gives for granting the petition for certiorari. If the case did not arise on certiorari, this variable will be so coded even if the Court provides a reason why it agreed to hear the case. The Court, however, rarely provides a reason for taking jurisdiction by writs other than certiorari.

*- End of Content for Variable 26. Reason for Granting Cert -*

## 27 Lower Court Disposition

**Variable Name** lcDisposition **Spaeth Name** LODIS **Normalizations** varCaseDispositionLc (12)

This variable specifies the treatment the court whose decision the Supreme Court reviewed accorded the decision of the court it reviewed; e.g., whether the court below the Supreme Court---typically a federal court of appeals or a state supreme court---affirmed, reversed, remanded, etc. the decision of the court it reviewed---typically a trial court.

lcDisposition will not contain an entry if the decision the Supreme Court reviewed is that of a trial court or if the case arose under the Supreme Court's original jurisdiction (see the jurisdiction variable). The former occurs frequently in the legacy data.

The decision rules governing this information follow:

- 1. We adhere to the language used in the "holding" in the summary of the case on the title page or prior to Part I of the Court's opinion. Exceptions to the literal language are the following:
- 2. Where the Court overrules the lower court, we treat this a petition or motion granted.
- 3. Where the court whose decision the Supreme Court is reviewing refuses to enforce or enjoins the decision of the court, tribunal, or agency which it reviewed, we treat this as reversed.
- 4. Where the court whose decision the Supreme Court is reviewing enforces the decision of the court, tribunal, or agency which it reviewed, we treat this as affirmed.
- 5. Where the court whose decision the Supreme Court is reviewing sets aside the decision of the court, tribunal, or agency which it reviewed, we treat this as vacated; if the decision is set aside and remanded, we treat it as vacated and remanded.

Also see disposition of case and direction of the lower court's decision (lcDispositionDirection).

*- End of Content for Variable 27. Lower Court Disposition -*

## 28 Lower Court Disposition Direction

**Variable Name** lcDispositionDirection **Spaeth Name** LCTDIR

**Normalizations** varDecisionDirection (3)

This variable specifies whether the decision of the court whose decision the Supreme Court reviewed was itself liberal or conservative as these terms are defined in the direction of decision variable (decisionDirection).

lcDispositionDirection permits determination of whether the Supreme Court's disposition of the case upheld or overturned a liberal or a conservative lower court decision.

With some adjustments, we coded this variable according to the following rules:

- !"If issue has a private law entry (140010-140080) and the direction of the Court's decision (decisionDirection) is unspecifiable, then the lower court's direction is unspecifiable.
- !"If issue has an interstate relations (110010-110030) or miscellaneous (130010, 130020) entry and decisionDirection is unspecifiable, then the lower court's direction is unspecifiable.
- !"If jurisdiction is original or certification, then the lower court's direction is unspecifiable.
- !"If the Supreme Court affirmed or dismissed the case, then the lower court's direction is the same as the Supreme Court's direction.
- !"If the Supreme Court reversed, reversed and remanded, vacated and remanded, or remanded, then the lower court's direction is the opposite and not the same as the Supreme Court's direction. For example, if the Supreme Court reversed and its decision is liberal then the lower court's direction is conservative.

Cases remaining after imposing these rules were hand coded.

Also see disposition of case by the court whose decision the Supreme Court reviewed (lcDisposition), direction of decision (decisionDirection), disposition of case (caseDisposition), and winning party (partyWinning).

*- End of Content for Variable 28. Lower Court Disposition Direction -*

## 29 Date of Decision

| Variable Name | Spaeth Name | Normalizations |
|---------------|-------------|----------------|
| dateDecision  | DEC         | n/a            |

This variable contains the year, month, and day that the Court announced its decision in the case. For volumes 2-107 of the U.S. Reports (1791-1882), we relied on Dates of Supreme Court Decisions and Arguments (http://www.supremecourt.gov/opinions/datesofdecisions.pdf), prepared by Anne Ashmore of the Library of the Supreme Court, because many early reporters do not list the date of decision.

*- End of Content for Variable 29. Date of Decision -*

## 30 Term of Court

| Variable Name | Spaeth Name | Normalizations |
|---------------|-------------|----------------|
| term          | TERM        | n/a            |
|               |             |                |

This variable identifies the term in which the Court handed down its decision. For cases argued in one term and reargued and decided in the next, term indicates the latter.

Historically, the nature of how a term is defined has changed. Below is a listing of the more significant changes to the term definitions over time.

- !"1791: First Monday in February (second session in August, dispensed with in 1802)
- !"Starting in 1827: term starts second Monday of January
- !"Starting in 1844: term starts first Monday of December, still called the 1845 term
- !"Starting in 1850: court starts calling it the December 1850 term; there are thus two 1850 terms in the dataset. The January 1850 term (50 U.S.) and the December 1850 term (51 U.S.).
- !"Starting in 1873: second Monday in October
- !"Starting in 1917: first Monday in October

*<sup>-</sup> End of Content for Variable 30. Term of Court -*

## 31 Natural Court

**Variable Name** naturalCourt **Spaeth Name** NATCT **Normalizations** varNaturalCourt (116)

Although most judicial research is chronologically organized by the term of the Court or by chief justice, many users employ "natural courts" as their analytical frame of reference.

A natural court is a period during which no personnel change occurs. Scholars have subdivided them into "strong" and "weak" natural courts, but no convention exists as to the dates on which they begin and end. Options include 1) date of confirmation, 2) date of seating, 3) cases decided after seating, and 4) cases argued and decided after seating. A strong natural court is delineated by the addition of a new justice or the departure of an incumbent. A weak natural court, by comparison, is any group of sitting justices even if lengthy vacancies occurred.

The values below divide the Courts into strong natural courts, each of which begins when the Reports first specify that the new justice is present but not necessarily participating in the reported case. Similarly, a natural court ends on the date when the Reports state that an incumbent justice has died, retired, or resigned. The courts are numbered consecutively by chief justice as the code at the left-hand margin indicates.

Note, especially, that the Court was without a chief justice during the 1836 term. This was the period between Marshall's death and Taney's confirmation.

For more on delineating natural courts, see See Edward V. Heck, "Justice Brennan and the Heyday of Warren Court Liberalism," 20 Santa Clara Law Review 841 (1980) 842-843 and "Changing Voting Patterns in the Burger Court: The Impact of Personnel Change," 17 San Diego Law Review 1021 (1980) 1038; Harold J. Spaeth and Michael F. Altfeld, "Measuring Power on the Supreme Court: An Alternative to the Power Index," 26 Jurimetrics 48 (1985) 55.

*- End of Content for Variable 31. Natural Court -*

## 32 Chief Justice

| Variable Name | Spaeth Name | Normalizations |
|---------------|-------------|----------------|
| chief         | CHIEF       | varChiefs (17) |
|               |             |                |

This variable identifies the chief justice during whose tenure the case was decided.

*- End of Content for Variable 32. Chief Justice -*

## 33 Date of Oral Argument

| Variable Name | Spaeth Name | Normalizations |
|---------------|-------------|----------------|
| dateArgument  | ORAL        | n/a            |

This variable contains the day, month, and year that the case was orally argued before the Court. dateArgument has no entry for cases that were not orally argued. For volumes 2-107 of the U.S. Reports (1791-1882), we used Dates of Supreme Court Decisions and Arguments (http://www.supremecourt.gov/opinions/datesofdecisions.pdf), prepared by Anne Ashmore of the Library of the Supreme Court, because many of the early reports do not list the date of argument.

On some occasions, oral argument extended over more than a single day. In such cases, only the first date is specified.

*- End of Content for Variable 33. Date of Oral Argument -*

## 34 Date of Reargument

| Variable Name | Spaeth Name | Normalizations |
|---------------|-------------|----------------|
| dateRearg     | REORAL      | n/a            |

On those infrequent occasions when the Court orders that a case be reargued, this variable specifies the date of such argument following the same day, month, and year sequence used in the preceding variable (dateArgue).

*- End of Content for Variable 34. Date of Reargument -*

## 35 Issue

| Variable Name<br>Spaeth Name<br>issue<br>ISSUE | Normalizations<br>varIssues (278) |
|------------------------------------------------|-----------------------------------|
|------------------------------------------------|-----------------------------------|

This variable identifies the issue for each decision. Although criteria for the identification of issues are hard to articulate, the focus here is on the subject matter of the controversy (e.g., sex discrimination, state tax, affirmative action) rather than its legal basis (e.g., the equal protection clause) (see the variable lawType).

This variable and its counterpart, issue area, cover the waterfront of the Court's decisions. However, neither of them provide the specificity that users commonly want. The three legal provision variables reduce the generic quality of issue and issue area to a more specific level. They are discussed in the first of the legal provisions below.

Because the database extends over four centuries of the Court's decisions during which time the Court's jurisdiction changed drastically, the description of many specific variables does not provide a good fit. Thus, for example, 'debtors' rights,' which locates in the civil rights issue area, contains many nineteenth century cases that have little, if anything, to do with civil rights as understood today. Nor do a vast majority of early takings cases have any reference to due process, and many of the early criminal procedure cases don't involve crimes at all. Conversely, to have lumped all railroad cases, bar none, into one variable would have erased the many types of situations in which nineteenth and early twentieth century railroads found themselves.

This situation results because the original (Spaeth) database began with the Warren Court, followed by its predecessor, the Vinson Court. We made a decision to retain the twentieth century listing and apply it as best we could to the eighteenth and nineteenth century decisions. We found it possible with the addition of only the seven common law law decisions (variables 140010-140070), plus a couple of others. Obviously, this decision produced definitonal stretching. Users, of course, may redefine issues to suit themselves

This variable identifies issues on the basis of the Court's own statements as to what the case is about. The objective is to categorize the case from a public policy standpoint, a perspective that the legal basis for decision (lawType) commonly disregards.

A few issues pertain only to the heritage (legacy) cases; those decided between 1791 and 1946. These include the private action category, typically common law issues: real property, personal property, contracts, evidence, civil procedure, wills and trusts, and commercial transactions. Others pertain to slavery, land claims (mostly state and territorial), executive authority vis-a-vis congress or the states, and incorporation of foreign territories.

Unlike the lawType variable where the number of legal provisions at issue has no preordained upper bound, each legal provision should generally not have more than a single issue applied to it. A second issue should apply only when a preference for one rather than the other cannot readily be made. Of the many thousand records in the database, few have a legal basis for decision that applies to a second issue. (If you are interested in decisions with more than one issue or legal provision, use one of the datasets organized by issue/legal provision.)

Because the database spans the entire four-century history of the Supreme Court, It is desirable

that the list of modern issues be related to those of the eighteenth and nineteenth centuries. Thus, in specifying the issue in a legacy case, the one that best accords with what today's Court would consider it to be is chosen. This produces a bit of tension, most all of which only requires a broadening of the scope of the relevant issues, rather than the creation of new time-specific ones. Thus, although state and local governments were not bound to adhere to the provisions of the Bill of Rights until well after the passage of the Fourteenth Amendment, many cases did arise involving aspects of the First Amendment, search and seizure, notice and hearing, etc. These are treated compatibly with the modern use of the relevant provision of the Bill of Rights.

The same rule applies to statutory issues, such as rules of procedure. Although their legal provision is Supreme Court Rules, they are coded as issues of civil (90110) or criminal (10370) procedure even though they antedate the relevant Rules of Civil and Criminal Procedure.

Prize cases in which vessels on the high seas are captured and brought into American ports and the confiscation acts resulting from the Civil War and World War I are treated either as due process takings clause cases (40070) or as cases involving the jurisdiction of the federal courts (90320 or 90330) to decide the legality of the capture or confiscation.

The variable codes 260 issues, each of which has an identifying number. They are ordered below by their larger issue area: criminal procedure (10010-10600), civil rights (20010-20410), First Amendment (30010-30020), due process (40010-40070), privacy (50010-50040), attorneys (60010-60040), unions (70010-70210), economic activity (80010-80350), judicial power (90010-90520), federalism (100010-100130), interstate relation (110010-110030), federal taxation (120010-120040), miscellaneous (130010-130020), and private law (140010-140080). These comprise the codes for a separate variable, Issue Area, that is described immediately following this one.

The scope of these categories is as follows: criminal procedure encompasses the rights of persons accused of crime, except for the due process rights of prisoners (issue 40040).

Civil rights includes non-First Amendment freedom cases which pertain to classifications based on race (including American Indians), age, indigency, voting, residency, military or handicapped status, gender, and alienage. Purists may wish to treat the military issues (20230, 20240, 20250) and Indian cases (20150, 20160) as economic activity, while others may wish to include the privacy category as a subset of civil rights.

First Amendment encompasses the scope of this constitutional provision, but do note that not every case in the First Amendment group directly involves the interpretation and application of a provision of the First Amendment. Some, for example, may only construe a precedent, or the reviewability of a claim based on the First Amendment, or the scope of an administrative rule or regulation that impacts the exercise of First Amendment freedoms. In other words, not every record that displays a First Amendment issue will correspondingly display a provision of the First Amendment in its legal provision variable (lawType).

Due process is limited to non-criminal guarantees and, like First Amendment issues, need not show 207 (Fifth Amendment Due Process) or 230 (Fourteenth Amendment Due Process) in the lawType variable. Some of you may wish to include state court assertion of jurisdiction over nonresident defendants and the takings clause as part of judicial power and economic activity, respectively, rather than due process.

The four issues comprising privacy may be treated as a subset of civil rights.

Because of their peculiar role in the judicial process, a separate attorney category has been created, which also includes their compensation and licenses, along with trhose of governmental officials and employees. You may wish to include these issues with economic activity, however.

Unions encompass those issues involving labor union activity. You may wish to redefine this category for yourself or combine it, in whole or in part, with economic activity.

Economic activity is largely commercial and business related; it includes tort actions and employee actions vis-a-vis employers. Issues 80140 (government corruption)and 80150 (zoning) are only tangential to the other issues located in economic activity.

Judicial power concerns the exercise of the judiciary's own power. To the extent that a number of these issues concern federal-state court relationships, you may wish to include them in the federalism category.

Federalism pertains to conflicts and other relationships between the federal government and the states, except for those between the federal and state courts. Interstate relations contain three types of disputes which occur between or among states.

Federal taxation concerns the Internal Revenue Code and related statutes. Miscellaneous contains three groups of cases that do not fit into any other category.

Private law relates to disputes between private persons involving real and personal property, contracts, evidence, civil procedure, torts, wills and trusts, and commercial transactions. Prior to the passage of the Judges' Bill of 1925 much -- arguably most -- of the Court's cases concerned such issues. The Judges' Bill gave the Court control of its docket, as a result of which such cases have disappeared from the Court's docket in preference to litigation of more general applicability.

If interest lies in a particular issue that has a specific legal or constitutional component, comprehensive coverage may be insured by listing not only the issue(s) that bear thereon, but also the appropriate code(s) from the lawType variable. Thus, if the right to counsel is the focus, issues 10120, 20320, and 20330 will fall within its scope, as will code 214 (Sixth Amendment Right to Counsel) from the lawType variable. Also recognize that the party variables (petitioner, petitionerState, respondent,

respondentState) may also help locate the cases of interest.

Note that jury instructions (10220) need not necessarily occur in the context of criminal action. This is especially so in heritage cases.

Issue 80110 (state regulation of business) also includes that of local governments. These are combined with state regulation because many heritage cases involve both.

Issue 90110 (federal rules of civil procedure) includes Supreme Court Rules, the Federal Rules of Evidence, the Federal Rules of Civil Procedure in civil litigation, Circuit Court Rules, state rules, and admiralty rules.

Natonal supremacy cases, in the context of federal-state conflicts (10050-100120)involve the general welfare, contract, supremacy, or interstate commerce causes, or the enforcement clause of the 14th Amendment. These cases are distinguishable from the pre-empton cases (100020 abd 100030) because they have a constitutional basis for decision.

Note that the legal provision variable and the first five background variables may supplement specification of case issue. Thus, for example, if you are interested in the huge mass of railroad cases generally that prevailed in the late nineteenth and early twentieth century decisions, case name will be of more help than the issues pertaining to railroad litigation.

*- End of Content for Variable 35. Issue -*

## 36 Issue Area

| Variable Name<br>Spaeth Name<br>Normalizations<br>issueArea<br>VALUE<br>varIssuesAreas (14) |  |
|---------------------------------------------------------------------------------------------|--|
|---------------------------------------------------------------------------------------------|--|

This variable simply separates the issues identified in the preceding variable (issue) into the following larger categories: criminal procedure (issues 10010-10600), civil rights (issues 20010-20410), First Amendment (issues 30010-30020), due process (issues 40010-40070), privacy (issues 50010-50040), attorneys' or governmental officials' fees or compensation (issues 60010-60040), unions (issues 70010-70210), economic activity (issues 80010-80350), judicial power (issues 90010-90520), federalism (issues 100010-100130), interstate relation (issues 110010-110030), federal taxation (issues 120010-120040), miscellaneous (issues 130010-130020), and private law (issues 140010-140080).

The contents of these issue areas are both over- and under-specfied; especially those of largest size: criminal procedure, civil rights,and economic ativity. In the interests of precision, users focusing on this variable would be wise to specify the components of a specific issue area that their analyses include or exclude.

Note that some of the issues in an issue area will have a distinctive direction at variance from the issue area's overal direction. E.g., the liability variables 80060, 80070, and 80080. See decision direction.

*- End of Content for Variable 36. Issue Area -*

## 37 Decision Direction

| decisionDirection<br>DIR<br>varDecisionDirection (3) | Variable Name | Spaeth Name | Normalizations |
|------------------------------------------------------|---------------|-------------|----------------|
|------------------------------------------------------|---------------|-------------|----------------|

In order to determine whether the Court supports or opposes the issue to which the case pertains, this variable codes the ideological "direction" of the decision.

Specification of direction comports with conventional usage for the most part except for the interstate relations, private law, and the miscellaneous issues. "Unspecifiable" has been entered either because the issue does not lend itself to a liberal or conservative description (e.g., a boundary dispute between two states, real property, wills and estates), or because no convention exists as to which is the liberal side and which is the conservative side (e.g., the legislative veto). This variable will also contain "unspecifiable" where one state sues another under the original jurisdiction of the Supreme Court and where parties or issue cannot be determined because of a tied vote or lack of information.

Note especially that the direction (pro- or anti-liability)of the three liability variables (80060, 80070, and 80080) depend on the disposition the Court made of the case, and which party won or lost. For 80070 -- non-governmental liability - a liberal vote and case decision support the injured person, organiation, or thing (res). For 80060 - governmental liability - a vote and case outcome that supports government is invariably defined as liberal. Note that if the injured entity is the other party in the case, said party loses, by definition. On the other hand, of course, if the injured entity wins, then of necessity the government loses. Where liability is assigned to both plaintiff and respondent, direction is considered indetermnable.

For purposes of the governmental liability issue, government includes state and local governmental entities, foreign governments, and governmentally owned property. In the rare instance of a conflict between governmental body and an injured person, organiation, or thing the governmental outcome controls directionality. Most such conflicts, however, locate in other issues; e.g., attorneys' and governemtnal employees' compensation or fees, and military personnel and veterans.

It bears emphasizing that the entry for directionality is determined by reference to the issue variable. If you are using the Case Centered Dataset organized by split votes, it is entirely possible for a citation to relate to a second issue whose direction is opposite that of the first issue. For example, in Air Pollution Variance Board of the State of Colorado v. Western Alfalfa Corporation, 416 U.S. 861 (1974), the Court decided that the Fourth Amendment was not violated by a health inspector's warrantless entry onto the property of a business to inspect smoke pollution. The first issue (search and seizure) is coded conservative; the second issue (natural resources) is coded liberal.

In order to determine whether an outcome is liberal (=2) or conservative (=1), the following scheme is employed.

1. In the context of issues pertaining to criminal procedure, civil rights, First Amendment, due process, privacy, and attorneys, liberal (2)=

- !"pro-person accused or convicted of crime, or denied a jury trial
- !"pro-civil liberties or civil rights claimant, especially those exercising less protected civil rights (e.g., homosexuality)
- !"pro-child or juvenile
- !"pro-indigent
- !"pro-Indian
- !"pro-affirmative action
- !"pro-neutrality in establishment clause cases
- !"pro-female in abortion
- !"pro-underdog
- !"anti-slavery
- !"incorporation of foreign territories
- !"anti-government in the context of due process, except for takings clause cases where a progovernment, anti-owner vote is considered liberal except in criminal forfeiture cases or those where the taking is pro-business
- !"violation of due process by exercising jurisdiction over nonresident
- !"pro-attorney or governmental official in non-liability cases
- !"pro-accountability and/or anti-corruption in campaign spending
- !"pro-privacy vis-a-vis the 1st Amendment where the privacy invaded is that of mental incompetents
- !"pro-disclosure in Freedom of Information Act issues except for employment and student records

#### conservative (1)=the reverse of above

- 2. In the context of issues pertaining to unions and economic activity, liberal (2)=
  - !"pro-union except in union antitrust where liberal = pro-competition
  - !"pro-government
  - !"anti-business
  - !"anti-employer
  - !"pro-competition
  - !"pro-injured person
  - !"pro-indigent
  - !"pro-small business vis-a-vis large business
  - !"pro-state/anti-business in state tax cases
  - !"pro-debtor
  - !"pro-bankrupt
  - !"pro-Indian
  - !"pro-environmental protection
  - !"pro-economic underdog
  - !"pro-consumer
  - !"pro-accountability in governmental corruption
  - !"pro-original grantee, purchaser, or occupant in state and territorial land claims

- !"anti-union member or employee vis-a-vis union
- !"anti-union in union antitrust
- !"anti-union in union or closed shop
- !"pro-trial in arbitration

```
conservative (1)= reverse of above
```

- 3. In the context of issues pertaining to judicial power, liberal (2)=
  - #"pro-exercise of judicial power
  - #"pro-judicial "activism"
  - #"pro-judicial review of administrative action

```
conservative (1)=reverse of above
```

- 4. In the context of issues pertaining to federalism, liberal (2)=
  - #"pro-federal power
  - #"pro-executive power in executive/congressional disputes
  - #"anti-state

```
conservative (1)=reverse of above
```

- 5. In the context of issues pertaining to federal taxation, liberal (2)= pro-United States; conservative (1)= pro-taxpayer
- 6. In interstate relations and private law issues, unspecifiable (3) for all such cases.
- 7. In miscellaneous, incorporation of foreign territories and executive authority vis-a-vis congress or the states or judcial authority vis-a-vis state or federal legislative authority = (2); legislative veto = (1).
- *End of Content for Variable 37. Decision Direction -*

## 38 Decision Direction Dissent

Variable Name decisionDirectionDissent

Spaeth Name DIRD Normalizations varDecisionDirectionDissent (2)

Once in a great while the majority as well as the dissenting opinion in a case will both support or, conversely, oppose the issue to which the case pertains. For example, the majority and the dissent may both assert that the rights of a person accused of crime have been violated. The only difference between them is that the majority votes to reverse the accused's conviction and remand the case for a new trial, while the dissent holds that the accused's conviction should be reversed, period. In such cases, the entry in the decisionDirection variable should be determined relative to whether the majority or the dissent more substantially supported the issue to which the case pertains, and an entry should appear in this variable. In the foregoing example, the direction of decision variable (decisionDirection) should show a 0(conservative) because the majority provided the person accused of crime with less relief than does the dissent, and direction based on dissent should show a 1 (liberal) The person accused of crime actually won the case, but won less of a victory than the dissent would have provided.

- End of Content for Variable 38. Decision Direction Dissent -

## 39 Authority for Decision 1

**Variable Name** authorityDecision1 **Spaeth Name** AUTHDEC1 **Normalizations** varAuthorityDecision (7)

This variable and the next one (authorityDecision2) specify the bases on which the Supreme Court rested its decision with regard to each legal provision that the Court considered in the case (see variable lawType).

Neither of them lends itself to objectivity. Many cases arguably rest on more than two bases for decision. Given

that the Court's citation of its precedents also qualifies as a common law decision and that most every case can be considered as at least partially based thereon, common law is the default basis for the Court's decisions. With the exception of decrees and brief non-orally argued decisions you may safely add common law to those cases lacking a second basis for decision.

Because one of these bases commonly occurs conjoined with another, the interpretation of the substantive provisions of a federal statute and the Supreme Court's exercise of its supervisory power over the lower federal courts; two separate variables (authorityDecision1, authorityDecision2) follow. The coding is the same in both. In the foregoing example, the first variable will contain a "4," the second a "3." In a case involving congressional acquiescence to longstanding administrative construction of a statute, these variables should appear as "5" and "4." If two bases are identified, and if one is more heavily emphasized, it should appear in the first of the two variables.

Considerable congruence should obtain between the entry in these variables and the code that appears in the lawType variable. Thus, if a constitutional provision appears in the lawType variable, a "1" or a "2" will typically appear in either authorityDecision1 or authorityDecision2. Similarly, if lawType displays a statute, either authorityDecision1 or authorityDecision2 will likely show a "4."

A common exception is where the Court determines the constitutionality of a federal statute, or where judge-made rules are applied to determine liability under various federal statutes, including civil rights acts (e.g., Pulliam v. Allen, 466 U.S. 522), or the propriety of the federal courts' use of state statutes of limitations to adjudicate federal statutory claims (e.g., Burnett v. Grattan, 468 U.S. 42).

The decision rules governing each of the authority for decision codes are as follows:

For a code of 1: The majority determined the constitutionality of some action taken by some unit or official of the federal government, including an interstate compact.

Enter a "1" if 139 appears in the lawSupp variable.

Enter a "1" if 111 appears in the lawSupp variable.

For a code of 2: Did the majority determine the constitutionality of some action taken by some unit or official of a state or local government? If so, enter a "2."

For a code of 3: If the rules governing codes "1-2," "4-7" are answered negatively or do not apply, enter a "3." A "3," then, serves as the residual code for these variables.

Enter a "3" if 508 appears in the lawSupp variable.

Non-statutorily based Judicial Power topics in the issue variable generally warrant a "3."

Most cases arising under the Court's original jurisdiction should receive a "3."

All cases containing a "4" in the type of decision variable = 3.

Enter a "3" in cases in which the Court denied or dismissed the petition for review or where the decision of a lower court is affirmed by a tie vote.

For a code of 4: Did the majority interpret a federal statute, treaty, or court rule? If so, enter a "4."

Enter a "4" rather than a "3" if the Court interprets a federal statute governing the powers or jurisdiction of a federal court. In other words, a statutory basis for a court's exercise of power or jurisdiction does not require that a "3" supplement a "4"; the latter alone suffices.

Enter a "4" rather than a "2" where the Court construes a state law as incompatible with a federal law.

Do not enter only a "4" where an administrative agency or official acts "pursuant to" a statute. All agency action is purportedly done pursuant to legislative authorization of one sort or another. A "4" may be coupled to a "5" (see below) only if the Court interprets the statute to determine if administrative action is proper.

In workers' compensation litigation involving statutory interpretation and, in addition, a discussion of jury determination and/or the sufficiency of the evidence, enter either a "4" and a "3" or a "3" and a "4." If no statute is identified in the syllabus, only enter a "3."

For a code of 5: Did the majority treats federal administrative action in arriving at its decision? If so, enter a "5."

Enter a "5' and a "4," but not a "5" alone, where an administrative official interprets a federal statute.

Enter a "5" if the issue = 90120.

For a code of 6: Did the majority say in approximately so many words that under its diversity jurisdiction it is interpreting state law? If so, enter a "6."

For a code of 7: Did the majority indicate that it used a judge-made "doctrine" or "rule?" If so, enter a "7." Where such is used in conjunction with a federal law or enacted rule, a "7" and "4" should appear in the two variables of this record.

Enter a "7" if the Court without more merely specifies the disposition the Court has made of the case and cites one or more of its own previously decided cases; but enter a "3" if the citation is

qualified by the word, "see."

Enter a "7" if the case concerns admiralty or maritime law, or some other aspect of the law of nations other than a treaty, which qualifies as a "4."

Enter a "7" if the case concerns the retroactive application of a constitutional provision or a previous decision of the Court.

Enter a "7" if the case concerns an exclusionary rule, the harmless error rule (though not the statute), the abstention doctrine, comity, res judicata, or collateral estoppel. Note that some of these, especially comity issues, likely warrant an entry in both authorityDecision variables: a "7" as well as a "3."

Enter a "7" if the case concerns a "rule" or "doctrine" that is not specified as related to or connected with a constitutional or statutory provision (e.g., 376 U.S. 398).

*- End of Content for Variable 39. Authority for Decision 1 -*

## 40 Authority for Decision 2

**Variable Name** authorityDecision2 **Spaeth Name** AUTHDEC2 **Normalizations** varAuthorityDecision (7)

See variable Authority for Decision 1 (authorityDecision1).

*- End of Content for Variable 40. Authority for Decision 2 -*

## 41 Legal Provisions Considered by the Court

**Variable Name** lawType **Spaeth Name** LAW **Normalizations** varLawArea (8)

This variable and its components (lawSupp and lawMinor) identify the constitutional provision(s), statute(s), or court rule(s) that the Court considered in the case. The difference between them is that lawSupp and lawMinor are coded finely; they identify the specific law, constitutional provision or rule at issue (e.g., Article I, Section 1; the Federal Election Campaign Act; the Federal Rules of Evidence). lawType is coded more broadly (e.g., constitution, federal statute, court rules). Do not assume that these three legal provisions are ordinally ordered. They are not. Any one of them can be considered more important to the Court's decision than either of the others. And that also applies to the issue and issue area of the case. Importance is a matter to be determined by the user's objectives.

Because of our ignorance of the overall contents of the pre-1946 decision making, we simply adhered to the structure and distinctive characteristics of the modern Court. Accordingly, we created a modernized interface that did not adequately comport with the distinctive features of the heritage cases. Not only did they treat distinctive constitutional provisions as one (e.g., upholding or voiding governmental action on the combined basis of due process and equal protection), with the interstate commerce clause thrown in for good measure. Furthermore, these early Courts also created a much used non-textual constitutional provision: freedom of contract, which was treated independently of the Constitution's contract clause.

Relatedly, we mistakenly allowed for only one type 0f legal provision (i.e. Constitution, constitutional amendment, federal statute, court rules, other, infrequently litigated statutes, and state or local law) per case record.) If a second or third legal provision warranted inclusion into the case record, entirely new and separate records needed to be created. This is not a serious problem with the post-1946 Courts, but it definitely is with the preceding ones.

At the other extreme, this database does allow for the inclusion of infrequently litigated federal statutes, but not those of the state and local governments. Users interested in the Court's treatment of the states are likely interested in the sort of state laws at issue and the result of Supreme Court action. E.g., did the Court treat all morals legislation the same; i.e., temperance, prostitution, obscenity, gambling, regardless of states or human litigants? Consult the variables 'origin of case State' and 'source of case State.' To determine the specifics of state or local law, consult the opinion of the case itself. Although a major objective of this database was to make it self-standing, we were not able to achieve this objective because of inadequate oversight and limited resources. To have included this datum would have been a counsel of perfection. Unfortunately, the other principle investigators and I are incapable of attaining such a status.

The basic criterion to determine the legal provision(s) is the "summary" in the Lawyers' Edition. Supplementary is a reference to it in at least one of the numbered holdings in the summary of the United States Reports. This summary, which the Lawyers' Edition of the U.S. Reports labels "Syllabus By Reporter Of Decisions," appears in the official Reports immediately after the date of decision and before the main opinion in the case. Where this summary lacks numbered holdings, it is treated as though it has but one number.

Be aware that the Reports do not cite a given statute the same in every case. Hence, the total

number of cases in which a case is the legal provision considered by the Court may be higher than the database reports.

Observe that where a state or local government allegedly abridges a provision of the Bill of Rights even though it has not been made binding on the states because it has not been "incorporated" into the due process clause of the Fourteenth Amendment, identification is to the specific guarantee rather than to the Fourteenth Amendment.

The legal basis for decision need not be formally stated. For example, a reference in the summary to the appointment of counsel under the Constitution or to the self-incrimination clause warrants entry of the appropriate code. (E.g., United States v. Knox, 396 U.S. 77; Lassiter v. Department of Social Services, 452 U.S. 18).

Also note that occasionally a holding may pertain to more than one legal basis for decision. In such cases, the additional basis or bases are specified as though they are numbered holdings, or as though they are a holding without numbers.

By no means does every record have an entry in the lawType variable. Only constitutional provisions, federal statutes, and court rules are entered here. This variable typically will have no entry in cases that concern the Supreme Court's supervisory authority over the lower federal courts; those where the Supreme Court's decision does not rest on a constitutional provision, federal statute, or court rule; provisions of the common law; decrees; and nonstatutory cases arising under the Court's original jurisdiction.

In cases where the Court considers multiple legal provisions no attempt is made to order their appearance. Where the constitutionality of a federal law is challenged, to give either the constitutional provision or the statute primacy would be arbitrary. To the extent that any order characterizes these lawType entries, it likely is the sequence in which they appear in the summary.

Beyond the foregoing, observe that an entry should appear in this variable only when the summary indicates that the majority opinion discusses the legal provision at issue. The mere fact that the Court exercises a certain power (e.g., its original jurisdiction, as in Arkansas v. Tennessee, 397 U.S. 91), or makes reference in its majority opinion rather than in the summary that a certain constitutional provision, statute, or frequently used common law rule applies (e.g., the "equal footing" principle which pertains to the admission of new states under Article IV, section 3, clause 2 of the Constitution, as Utah v. United States, 403 U.S. 9, illustrates) provides no warrant for any entry.

There are three exceptions to this "discussion" requirement, the first of which dismisses the writ of certiorari as "improvidently granted" either in so many words (e.g., Johnson v. United States, 401 U.S. 846) or dismisses it on this basis implicitly (e.g., Baldonado v. California, 366 U.S. 417). In such cases, the code 508 should appear. More often than not, these cases have no summary. Note that the phrase is a term of art: 1) it overrides any substantive provision that the summary may mention (e.g., Conway v. California Adult Authority, 396 U.S. 107); 2) it does not apply where the Supreme Court takes jurisdiction on appeal.

In the second exception the Court, without discussion, remands a case to a lower court for consideration in light of an earlier decision. The summary of the earlier case is then consulted and the instant case coded with the entry that appeared there (e.g., Wheaton v. California, 386 U.S. 267). If a discussion in the summary precedes the remand, this variable should be governed by that discussion as well as the basis for decision in the case that the lower court is instructed to consider. Usually these bases will be identical (e.g., Maxwell v. Bishop, 398 U.S. 262).

The third exception to the "discussion" criterion involves the legality of administrative agency action without specific reference to the statute under which the agency acted. Inasmuch as administrative agencies may only act pursuant to statute, the majority opinion was consulted to determine the statute in question (e.g., National Labor Relations Board v. United Insurance Co. of America, 390 U.S. 254). The same situation may characterize the statute under which a court exercises jurisdiction (e.g., the Court of Claims in United States v. King, 395 U.S. 1).

As indicated, this variable should usually lack an entry if the numbered holding(s) indicates that the Court's decision rests on its supervisory authority over the federal judiciary, the common law, or diversity jurisdiction.

Note that where a state or local government allegedly abridges a provision of the Bill of Rights that has been made binding on the states because it has been incorporated into the due process clause of the Fourteenth Amendment, identification is to the specific guarantee rather than to the Fourteenth Amendment Due Process Clause.

International treaties and conventions, which rarely serve as the basis for the Court's decision, are identified (in the lawSupp variable) as a treaty (509), an interstate compact as Interstate Compact (510), an executive order as Executive Order (511), and a statute of a territory of the U.S., which is not in the U.S. Code or the Statutes at Large, as Territory Statute (512).

A case that challenges the constitutionality of a federal statute, court or common law rule will usually contain at least two legal bases for decision: the constitutional provision as well as the challenged statute or rule.

Where a heading concerns the review of agency action under a statute, but the statute is not identified, it is ascertained from the opinion (e.g., National Labor Relations Board v. United Insurance Co. of America, 390 U.S. 254). So also where the decision turns on the statutory jurisdiction of a federal court, and the holding does not specify it (e.g., United States v. King, 395 U.S. 1).

*- End of Content for Variable 41. Legal Provisions Considered by the Court -*

## 42 Legal Provision Supplement

| Variable Name | Spaeth Name | Normalizations           |
|---------------|-------------|--------------------------|
| lawSupp       | LAW         | varLegalProvisions (206) |
|               |             |                          |

See variable Legal Provisions Considered by the Court.

*- End of Content for Variable 42. Legal Provision Supplement -*

## 43 Legal Provision Minor Supplement

| Variable Name | Spaeth Name | Normalizations |
|---------------|-------------|----------------|
| lawMinor      | LAW         | n/a            |
|               |             |                |

This variable, lawMinor, is reserved for infrequently litigated statutes. Statutes substantially absent from the decision making of the modern Courts will be found in this variable. For these, lawMinor identifies the law at issue. Note: This is a string variable.

*- End of Content for Variable 43. Legal Provision Minor Supplement -*

## 44 Decision Type

| decisionType<br>DEC_TYPE<br>varDecisionTypes (7) |
|--------------------------------------------------|
|--------------------------------------------------|

decisionType=1: Cases the Court decides by a signed opinion. Note that for the 1946 terms to present, decisionType=1 cases are those that the Court decided by a signed opinion and in which it heard oral arguments. This is true for the 1791-1945 terms too. When both these conditions are met, the case is coded as decisionType=1. But the second condition—oral argument—is no longer necessary for a decisionType=1 classification. That's because the dates of oral argument were not reported for many cases that were likely argued (if only because the reporter noted, "After argument…"). We are working to locate these (many) missing dates and would appreciate any leads from users.

Jettisoning the oral argument requirement also means that there are many cases that were probably not orally argued but that are included as decisionType=1 cases because a justice is listed as delivering the opinion of the Court. For users that want to examine cases we know for sure were orally argued, we suggest selecting on dateArgument—with the important caveat that you will miss cases that were likely argued but are lacking a date.

decisionType=2: Cases decided with an opinion but without hearing oral argument; i.e., per curiam opinions. In the legacy data, decisionType2 cases include cases in which the Court (or reporter) did not use the term "per curiam" but rather "The Court [said]," "By the Court," or "By direction of the Court." If these cases identify the author of the opinion, we code an opinion writer.

decisionType=4: Decrees. This infrequent type of decision usually arises under the Court's original jurisdiction and involves state boundary disputes. The justices will typically appoint a special master to take testimony and render a report, the bulk of which generally becomes the Court's decision. The presence of the label, "decree," distinguishes this type of decision from the others.

decisionType=5: Cases decided by an equally divided vote. When a justice fails to participate in a case or when the Court has a vacancy, the participating justices may cast a tie vote. In such cases, the Reports merely state that "the judgment is affirmed by an equally divided vote" and the name of any nonparticipating justice(s). Their effect is to uphold the decision of the court whose decision the Supreme Court reviewed.

decisionType=6: This decision type is a variant of decisionType=1 cases. It differs from type 1 in that no individual justice's name appears as author of the Court's opinion. Instead, these unsigned orally argued cases are labeled as decided "per curiam." The difference between this type and decisionType=2 is the occurrence of oral argument in the former but not the latter. In both types the opinion of the Court is unsigned.

decisionType=7: Judgments of the Court. This decision type is also a variant of the formally decided cases. It differs from type 1 in that less than a majority of the participating justices agree with the opinion produced by the justice assigned to write the Court's opinion. Except for those interested only in the authors of the opinions of the Court, decisionType=7 should be included in analyses of the Court's formally decided cases. See also the notes under decisionType=1.

The database does not contain all of the non-orally argued per curiam decisions (decisionType=2). The Reports contain large numbers of brief, non-orally argued per curiam decisions. The database includes only those for which the Court has provided a summary, as well as those without a summary in which one or more of the justices wrote an opinion.

Along similar lines, the database also does not contain memorandum decisions or "back-of-thebook" U.S. Reports cases with the exceptions of, first, volumes 131 and 154. In these volumes, the reporters included (in the Appendices) cases previously omitted or "not hitherto reported in full." Second, we are trying to include all orally argued cases in the back-of-the-book (the Database already contains "front-of-the-book" orally argued cases). All decisionType=5 orally argued cases, even if in the back of the book, already have been entered. We are in the process of adding decisionType=6 back-of-the-book cases. In the vast majority of these, the Court dismissed the case with a one-line sentence.

*- End of Content for Variable 44. Decision Type -*

## 45 Declaration of Unconstitutionality

**Variable Name** declarationUncon **Spaeth Name** UNCON **Normalizations** varDeclarationUncon (4)

An entry in this variable indicates that the Court either declared unconstitutional an act of Congress; a state or territorial statute, regulation, or constitutional provision; or a municipal or other local ordinance. In coding this variable we consulted several sources. Most helpful was the Congressional Research Service's Constitution of the United States of America: Analysis and Interpretation (CONAN) (https://www.congress.gov/constitution-annotated) and the appendix to volume 131 of the U.S. Reports.

Note that the Court need not necessarily specify in so many words that a law has been declared unconstitutional. That commonly occurred in legacy decisions (pre-1946); e.g., Wllcox v. Consolidted Gas Co. of New York, 53 L Ed 382 (1909).

The summary frequently, though not invariably, will indicate such action in its statement of the Court's holdings. Hence, where such action may have occurred, it may be necessary to read carefully the opinion of the Court to determine whether an entry should be made in this variable.

Where federal law pre-empts a state statute or a local ordinance, unconstitutionality does not result unless the Court's opinion so states. Nor are administrative regulations the subject of declarations of unconstitutionality unless the declaration also applies to the law on which it is based. Also excluded are federal or state court-made rules; e.g., Virginia Supreme Court v. Friedman, 487 U.S. 59 (1988).

*- End of Content for Variable 45. Declaration of Unconstitutionality -*

## 46 Disposition of Case

| Variable Name   | Spaeth Name | Normalizations            |
|-----------------|-------------|---------------------------|
| caseDisposition | DIS         | varCaseDispositionSc (11) |
|                 |             |                           |

The treatment the Supreme Court accorded the court whose decision it reviewed is contained in this variable; e.g., affirmed, vacated, reversed and remanded, etc. The values here are the same as those for lcDisposition (how the court whose decision the Supreme Court reviewed disposed of the case). For original jurisdiction cases, this variable will be empty unless the Court's disposition falls under 1 or 9 below (stay, petition, or motion granted; petition denied or appeal dismissed). For cases in which the Court granted a motion to dismiss, caseDisposition is coded as 9 (petition denied or appeal dismissed). There is "no disposition" if the Court denied a motion to dismiss.

The information relevant to this variable may be found near the end of the summary that begins on the title page of each case, or preferably at the very end of the opinion of the Court.

As in the lcDisposition variable, the value label pertaining to the specific language used by the Court is entered. If incongruence between the Court's language and the above codes occurs, consult variable caseDispositionUnusual.

In cases containing multiple docket numbers, not every docket number will necessarily receive the same disposition. Hence, in focusing on the outcome of the Court's decisions, users might want to consider the datasets in which cases are organized by docket rather than citation.

Note for users of the Justice Centered Database: The entry in this variable governs whether the individual justices voted with the majority or in dissent.

*- End of Content for Variable 46. Disposition of Case -*

## 47 Unusual Disposition

Variable Name caseDispositionUnusual

Spaeth Name DISQ Normalizations varCaseDispositionUnusual (2)

An entry (1) will appear in this variable to signify that the Court made an unusual disposition of the cited case which does not match the coding scheme of the preceding variable. The disposition that appears closest to the unusual one made by the Court should be selected for inclusion in the preceding variable, caseDisposition.

- End of Content for Variable 47. Unusual Disposition -

## 48 Winning Party

| Variable Name | Spaeth Name | Normalizations      |
|---------------|-------------|---------------------|
| partyWinning  | WIN         | varPartyWinning (3) |
|               |             |                     |

This variable indicates whether the petitioning party (i.e., the plaintiff or the appellant) emerged victorious. The victory the Supreme Court provided the petitioning party may not have been total and complete (e.g., by vacating and remanding the matter rather than an unequivocal reversal), but the disposition is nonetheless a favorable one.

With some adjustments, we coded this variable according to the following rules:

- !"The petitioning party lost if the Supreme Court affirmed (caseDisposition=2) or dismissed the case/denied the petition (caseDisposition=9).
- !"The petitioning party won in part or in full if the Supreme Court reversed (caseDisposition=3), reversed and remanded (caseDisposition= 4), vacated and remanded (caseDisposition=5), affirmed and reversed in part (caseDisposition=6), affirmed and reverse in part and remanded (caseDisposition=7), or vacated (caseDisposition=8)
- !"The petitioning party won or lost may be unclear if the Court certified to/from a lower court.
  - *End of Content for Variable 48. Winning Party -*

## 49 Formal Alteration of Precedent

**Variable Name** precedentAlteration **Spaeth Name** ALT\_PREC **Normalizations** varPrecedentAlteration (2)

A "1" will appear in this variable if the majority opinion effectively says that the decision in this case "overruled" one or more of the Court's own precedents. Occasionally, in the absence of language in the prevailing opinion, the dissent will state clearly and persuasively that precedents have been formally altered: e.g., the two landmark reapportionment cases: Baker v. Carr, 369 U.S. 186 (1962), and Gray v. Sanders, 372 U.S. 368 (1963). Once in a great while the majority opinion will state--again in so many words--that an earlier decision overruled one of the Court's own precedents, even though that earlier decision nowhere says so. E.g, Patterson v. McLean Credit Union, 485 U.S. 617 (1988), in which the majority said that Braden v. 30th Judicial Circuit of Kentucky, 410 U.S. 484, 35 L Ed 2d 443 (1973) overruled a 1948 decision. On the basis of this later language, the earlier decision will contain a "1" in this variable. Alteration also extends to language in the majority opinion that states that a precedent of the Supreme Court has been "disapproved," or is "no longer good law."

Note, however, that alteration does not apply to cases in which the Court "distinguishes" a precedent. Such language in no way changes the scope of the precedent contained in the case that has been distinguished.

In addition to following these rules, we consulted several sources. Again, the Congressional Research Service's Constitution of the United States of America: Analysis and Interpretation (CONAN) (https://www.congress.gov/constitution-annotated) was most helpful.

Do not assume that each record of a given case indicates the formal alteration of a separate precedent. A given citation may have several docket numbers, each of which is governed by a single opinion in which only one precedent was altered. Conversely, an opinion in a citation with a single docket number may alter a whole series of Supreme Court precedents. To determine the number of altered precedents, carefully read the prevailing opinion in each citation that has an entry in this variable.

*- End of Content for Variable 49. Formal Alteration of Precedent -*

## 50 Vote Not Clearly Specified

**Variable Name** voteUnclear **Spaeth Name** VOTEQ **Normalizations** varVoteUnclear (2)

The votes in a case are those specified in the opinions.

Do note, however, that the majority opinion in a number of Marshall Court decisions reports that unnamed justices were in disagreement about the resolution of the case. These do not identify who the dissenters were. We, therefore, look to the majority opinion itself to specify who voted how.

In the vast majority of cases, the individual justices clearly indicate whether or not they agree with the disposition made by the majority. For a small number of cases clarity may be lacking, as when a justice concurs in part and dissents in part. A justice will typically use this or equivalent language to indicate agreement with the reasoning in a portion of the majority opinion while disagreeing with the majority's disposition of the case, or vice-versa.

A close reading of the justice's opinion usually indicates whether he or she has concurred (i.e., agreed with the majority's disposition) or dissented from the disposition made by the majority. But in the rare case where a justice does not clearly indicate which it is, this variable will so indicate.

*- End of Content for Variable 50. Vote Not Clearly Specified -*

## 51 Majority Opinion Writer

| Variable Name | Spaeth Name | Normalizations    |
|---------------|-------------|-------------------|
| majOpinWriter | MOW         | varJustices (118) |
|               |             |                   |

This variable identifies the author of the Court's opinion or judgment, as the case may be.

*Note: This variable relies on the Justices ID for its values. For a more detailed description of these identifiers, please visit the [detail page for the Justices variable.](http://scdbadmin.wustl.edu/_brickSql/documentation.php?var=justice) Note that the justice normalizations changed with the SCDB\_2012\_01 release of the database.*

*- End of Content for Variable 51. Majority Opinion Writer -*

## 52 Majority Opinion Assigner

**Variable Name** majOpinAssigner **Spaeth Name** MOA **Normalizations** varJustices (118)

This variable identifies the assigner of the opinion or judgment of the Court, as the case may be. These data are drawn from the membership in the final (report vote) coalition and from the rules governing opinion assignment: If the chief justice is a member of the majority vote coalition at the conference vote, he assigns the opinion; if not, the senior associate justice who is a member of the majority at the conference vote does so. According to several scholarly studies, considerable voting shifts occur between the final conference vote (where the assignment is made) and the vote that appears in the Reports. As a result, in approximately 16 percent of the cases, a person other than the one identified by the database actually assigned the opinion.

To partially overcome this discrepancy, users may consult the expanded versions of the database, available at http://www.cas.sc.edu/poli/juri/, but which include only the Vinson, Warren, and Burger Courts, plus the 1986-1993 terms of the Rehnquist Court. Assigners in these Courts are identified by reference to the justices' docket books.

*Note: This variable relies on the Justices ID for its values. For a more detailed description of these identifiers, please visit the [detail page for the Justices variable.](http://scdbadmin.wustl.edu/_brickSql/documentation.php?var=justice) Note that the justice normalizations changed with the SCDB\_2012\_01 release of the database.*

*- End of Content for Variable 52. Majority Opinion Assigner -*

## 53 Split Vote

| Variable Name | Spaeth Name | Normalizations   |
|---------------|-------------|------------------|
| splitVote     | n/a         | varSplitVote (2) |
|               |             |                  |

This variable indicates whether the vote variables (e.g., majVotes, minVotes) pertain to the vote on the first or second issue (or legal provision). Because split votes are so rare over 99 percent of the votes are on the first issue.

Users interested in analyzing cases with split votes should use the dataset that organizes cases by legal provision and split votes.

*- End of Content for Variable 53. Split Vote -*

## 54 Majority Votes

| Variable Name | Spaeth Name | Normalizations |
|---------------|-------------|----------------|
| majVotes      | n/a         | n/a            |

This variable specifies the number of justices voting in the majority; minVotes indicates the number of justices voting in dissent.

In non-legacy cases, a quorum requires the participation of six justices for a decision on the merits.

The number that appears in this variable pertains to the number of justices who agree with the disposition made by the majority (see caseDisposition) and not to the justices' vote on any particular issue in the case. Thus, for example, in Bates v. Arizona State Bar, 433 U.S. 350 (1977), the vote in the case was 5 to 4, even though all participants agreed that the disciplinary rule prohibiting attorney advertising did not violate the Sherman Act. Unlike the majority, the dissenters disagreed that the rule violated the First Amendment.

Please note: Because the early reporters did not always note whether a Justice was absent for a particular case, we consulted the front matter to each volume of the U.S. Reports. For example, volume 77 states: "The Chief Justice did not participate in any of the judgments reported in this volume after page 151. Nor did Mr. Justice Nelson participate in those reported between pages 141 and 410." Sometimes it was simply impossible determine non-participation. E.g., from the January Term 1834: Justice Duvall "was prevented from attending the Court until some time after the commencement of the term."

See also Minority Votes (minVotes) and Vote Not Clearly Specified (voteUnclear).

*- End of Content for Variable 54. Majority Votes -*

## 55 Minority Votes

| Variable Name | Spaeth Name | Normalizations |
|---------------|-------------|----------------|
| minVotes      | n/a         | n/a            |

This variable specifies the number of votes in dissent. Only dissents on the merits are specified in this variable.

Justices who dissent from a denial or dismissal of certiorari or who disagree with the Court's assertion of jurisdiction count as not participating in the decision.

For more details, see the variable Majority Votes (majVotes).

*- End of Content for Variable 55. Minority Votes -*

## 56 Justice ID

| Variable Name | Spaeth Name | Normalizations    |
|---------------|-------------|-------------------|
| justice       | HAR-BRY     | varJustices (118) |
|               |             |                   |

This variable provides a unique identification number for each of the justices. Even though several justices served as both associate and chief justice they receive only one identification number.

This variable appears in the Justice Centered Datasets only.

Some notes about the organization of the justice ids.

- 1. The numeric value on the left is the unique identifier.
- 2. The shortened name to the right of the numeric (e.g. JJay) is for readability. Astute eyes will observe that these text descriptors are not always unique, as in the case of JRutledge (ids 2 and 9). The reason for this is id's 2 and 9 reference the same individual. The source of the two ids is the justice served a split term.
- 3. In situations where two different individuals would share a short name, the short descriptor will be incremented with a numeral on the end as in the case of JHalan1 (id 45) and JHarlan2 (id 91). These descriptors were made unique because they reference different individuals.

*Please note that release SCDB\_2012\_01 saw a renormalization to the justice ids. This was to correct an exclusion of an early justice. Below you will find the current listing. The original variable assignments may be seen [here.](http://scdbadmin.wustl.edu/_brickSql/_media/scdbJusticesIdsLegacy.csv.zip) If you perform a search based on early database releases (prior to SCDB\_2012\_01) all justice references have been updated to ensure fidelity.*

*- End of Content for Variable 56. Justice ID -*

## 57 Justice Name

| Variable Name | Spaeth Name | Normalizations    |
|---------------|-------------|-------------------|
| justiceName   | n/a         | varJustices (118) |
|               |             |                   |

This is a string variable indicating the first initial for the five justices with a common surname (Harlan, Johnson, Marshall, Roberts, and White) and last name of each justice. This variable appears in the Justice Centered Datasets only.

*Note: This is a denormalized, human-readable version of the justice ID variable. For a more detailed description of these identifiers, please visit the [detail page for the Justices variable.](http://scdbadmin.wustl.edu/_brickSql/documentation.php?var=justice) Note that the justice normalizations changed with the SCDB\_2012\_01 release of the database.*

*- End of Content for Variable 57. Justice Name -*

## 58 The Vote in the Case

**Variable Name** vote **Spaeth Name** HARV to BRYV **Normalizations** varVote (8)

This variable provides information about each justice's vote in the case. It appears in the Justice Centered Datasets only. A regular concurrence is when the justice agrees with the Court's opinion as well as its disposition. A special concurence (i.e., a concurence in the judgment) is when the justice agrees with the Court's disposition but not its opinion. A jurisdictional dissent is when the justice disagrees with the Court's assertion or denial of jurisdiction. Such votes are counted as nonparticipations.

Determination of how a given justice voted is by no means a simple matter of culling the Reports. The justices do not always make their options clear.

Two problems, in particular, afflict efforts to specify votes: 1) whether the vote is a regular or a special concurrence, and 2) the treatment to be accorded a vote "concurring in part and dissenting in part."

The first typically manifests itself when a justice joins the opinion of the Court "except for . . ." Because such exceptions typically tend to approach de minimis status, these are coded as regular concurrences. For example, Chief Justice Burger concurred in the opinion of the Court in New York Gaslight Club, Inc. v. Carey, except for "footnote 6 thereof." 447 U.S. 54, at 71. Similarly, Blackmun's agreement with the Court in Pruneyard Shopping Center v. Robins, except for "that sentence thereof . . ." 447 U.S. 74, at 88. Where the Reports identify a justice as "concurring" or "concurring in part" said justice is treated as a member of the majority opinion coalition (i.e., as = 3), rather than a merely concurring in the result (i.e., as = 4).

Whereas the preceding problem pertains to determining which type of concurrence a vote is, the problem with votes concurring and dissenting in part is whether they are special concurrences (= 4) or dissents (= 2). This matter was addressed previously in connection with the variable voteUnclear (vote not clearly specified). A vote concurring and dissenting in part is listed as a special concurrence if the justice(s) doing so does not disagree with the majority's disposition of the case. This may occur when: 1) the justice concurring and dissenting in part only voices disagreement with some or all of the majority's reasoning; 2) when said justice disapproves of the majority's deciding or refusing to decide additional issues involved in the case; or 3) when in a case in which dissent has been voiced, the justice(s) concurring and dissenting in part votes to dispose of the case in a manner more closely approximating that of the majority than that of the dissenter(s).

In cases where determination of whether a vote concurring and dissenting in part is the former or the latter is not beyond cavil, an entry will appear in the voteUnclear variable of the affected case to allow users to make an independent judgment, if they are so minded. Note, however, that listing such votes as dissents (= 2) or special concurrences (= 4) has no effect on whether or not an opinion is written (the opinion variable).

See also notes under the majority vote (majVote) variable.

*- End of Content for Variable 58. The Vote in the Case -*

## 59 Opinion

**Variable Name** opinion **Spaeth Name** HARO to BRYO **Normalizations** varJusticeOpinion (3)

This variable indicates the opinion, if any, that the justice wrote. It appears in the Justice Centered Datasets only.

Because determination of whether a justice wrote an opinion is no simple matter, rules must be formulated.

- 1. A justice authors no opinion unless he or she specifies a reason for his or her vote. A bare citation to a previously decided case or a simple statement that the author concurs or dissents because of agreement with a lower court's opinion suffices as an opinion
- 2. Where a justice specifies that the opinion applies to an additional case or cases, the opinion is counted as so many separate ones. Thus, the opinions of Brennan and Marshall in Mobile v. Bolden, 446 U.S. 55, also apply to Williams v. Brown, 446 U.S. 236. Hence, each of these opinions is counted as though it were two separate opinions.
- 3. When a justice joins the substance of another justice's opinion, without any personal expression of views, that justice is listed as joining the other's opinion (see variables firstAgreement and secondAgreement) and not as an author unless he or she also writes an opinion.

Thus, in United States v. Havens, 446 U.S. 620, Justices Stewart and Stevens are listed as joining Brennan's dissenting opinion notwithstanding that the pertinent language reads: "Mr. Justice Brennan, joined by Mr. Justice Marshall and joined in Part I by Mr. Justice Stewart and Mr. Justice Stevens, dissenting." 446 U.S. at 629. The opinion contains two parts of roughly equal length. Failure to list the latter pair as joiners would have required that they appear as dissenting without opinion, a manifestly inaccurate result. Similarly, Justice White's language in Parratt v. Taylor, 451 U.S. 527, at 545: "I join the opinion of the Court but with the reservations stated by my Brother Blackmun in his concurring opinion," is not listed as as opinion by White. He rather appears as joining Blackmun's concurrence. Conversely, where a justice, in his or her own words only partially agrees with one or more opinions authored by others, he or she is listed as an author. Two examples of Justice Stewart illustrate: "Mr. Justice Stewart dissents for the reasons expressed in Part I of the dissenting opinion of Mr. Justice Powell." (Dougherty County Board of Education v. White, 439 U.S. 32, at 47) "Mr. Justice Stewart concurs in the judgment, agreeing with all but Part II of the opinion of the Court, and with Part I of the concurring opinion of Mr. Justice Stevens." (Jenkins v. Anderson, 447 U.S. 231, at 241).

- 4. When two or more justices jointly author an opinion, an entry will so indicate. Joint authorship, however, does not include per curiam opinions.
- *End of Content for Variable 59. Opinion -*

## 60 Direction of the Individual Justice's Votes

**Variable Name** direction **Spaeth Name** HARDIR-BRYDIR **Normalizations** varJusticeDirection (2)

This variable indicates whether the justice cast a liberal or conservative vote. For the definitions of liberal and conservative, see variable decisionDirection. A missing value code indicates that the decisionDirection was unspecifiable or that that justice did not participate.

This variable appears in the Justice Centered Datasets only.

*- End of Content for Variable 60. Direction of the Individual Justice's Votes -*

## 61 Majority and Minority Voting by Justice

| Variable Name | Spaeth Name | Normalizations         |
|---------------|-------------|------------------------|
| majority      | HARM - BRYM | varJusticeMajority (2) |
|               |             |                        |

Analysts commonly want to know the frequency with which given justices vote with the majority and/or in dissent overall or in certain sets of circumstances. This variable provides that information for each justice.

This variable appears in the Justice Centered Datasets only.

*- End of Content for Variable 61. Majority and Minority Voting by Justice -*

## 62 First Agreement

This variable (and Second Agreement) denotes whether the justice agreed with a dissent or concurrence written by another justice (indicated by the justice's id number). Two agreements are coded---one in this variable and the second in secondAgreement. For more details, see the opinion variable.

This variable appears in the Justice Centered Datasets only.

*Note: This variable relies on the Justices ID for its values. For a more detailed description of these identifiers, please visit the [detail page for the Justices variable.](http://scdbadmin.wustl.edu/_brickSql/documentation.php?var=justice) Note that the justice normalizations changed with the SCDB\_2012\_01 release of the database.*

*- End of Content for Variable 62. First Agreement -*

## 63 Second Agreement

**Variable Name** secondAgreement **Spaeth Name** HARA2 - BRYA2 **Normalizations** varJustices (118)

See variable First Agreement (firstAgreement).

This variable appears in the Justice Centered Datasets only.

*Note: This variable relies on the Justices ID for its values. For a more detailed description of these identifiers, please visit the [detail page for the Justices variable.](http://scdbadmin.wustl.edu/_brickSql/documentation.php?var=justice) Note that the justice normalizations changed with the SCDB\_2012\_01 release of the database.*

*- End of Content for Variable 63. Second Agreement -*

## Appendix

This appendix contains an exhaustive list of the numeric codes used for all numeric variables in the Supreme Court Database. In the language of database administration, these lists are called normalizations. In the language of statistical software, these lists are called value labels. All of the data files available for software that supports them, e.g., Stata, R, and SPSS, include all of these value labels. The naming convention used throughout is varVariableName.

## A1 varAdminAction

*125 Distinct Values*

varAdminAction is used in conjunction with: *adminAction*

- Army and Air Force Exchange Service
- Atomic Energy Commission
- Secretary or administrative unit or personnel of the U.S. Air Force
- Department or Secretary of Agriculture
- Alien Property Custodian
- Secretary or administrative unit or personnel of the U.S. Army
- Board of Immigration Appeals
- Bureau of Indian Affairs
- Bureau of Prisons
- Bonneville Power Administration
- Benefits Review Board
- Civil Aeronautics Board
- Bureau of the Census
- Central Intelligence Agency
- Commodity Futures Trading Commission
- Department or Secretary of Commerce
- Comptroller of Currency
- Consumer Product Safety Commission
- Civil Rights Commission
- Civil Service Commission, U.S.
- Customs Service or Commissioner or Collector of Customs
- Defense Base Closure and REalignment Commission
- Drug Enforcement Agency
- Department or Secretary of Defense (and Department or Secretary of War)
- Department or Secretary of Energy
- Department or Secretary of the Interior
- Department of Justice or Attorney General
- Department or Secretary of State
- Department or Secretary of Transportation
- Department or Secretary of Education

- U.S. Employees' Compensation Commission, or Commissioner
- Equal Employment Opportunity Commission
- Environmental Protection Agency or Administrator
- Federal Aviation Agency or Administration
- Federal Bureau of Investigation or Director
- Federal Bureau of Prisons
- Farm Credit Administration
- Federal Communications Commission (including a predecessor, Federal Radio Commission)
- Federal Credit Union Administration
- Food and Drug Administration
- Federal Deposit Insurance Corporation
- Federal Energy Administration
- Federal Election Commission
- Federal Energy Regulatory Commission
- Federal Housing Administration
- Federal Home Loan Bank Board
- Federal Labor Relations Authority
- Federal Maritime Board
- Federal Maritime Commission
- Farmers Home Administration
- Federal Parole Board
- Federal Power Commission
- Federal Railroad Administration
- Federal Reserve Board of Governors
- Federal Reserve System
- Federal Savings and Loan Insurance Corporation
- Federal Trade Commission
- Federal Works Administration, or Administrator
- General Accounting Office
- Comptroller General
- General Services Administration
- Department or Secretary of Health, Education and Welfare
- Department or Secretary of Health and Human Services
- Department or Secretary of Housing and Urban Development
- Administrative agency established under an interstate compact (except for the MTC)
- Interstate Commerce Commission
- Indian Claims Commission
- Immigration and Naturalization Service, or Director of, or District Director of, or Immigration and Naturalization Enforcement
- Internal Revenue Service, Collector, Commissioner, or District Director of
- Information Security Oversight Office
- Department or Secretary of Labor
- Loyalty Review Board
- Legal Services Corporation
- Merit Systems Protection Board
- Multistate Tax Commission
- National Aeronautics and Space Administration

- Secretary or administrative unit or personnel of the U.S. Navy
- National Credit Union Administration
- National Endowment for the Arts
- National Enforcement Commission
- National Highway Traffic Safety Administration
- National Labor Relations Board, or regional office or officer
- National Mediation Board
- National Railroad Adjustment Board
- Nuclear Regulatory Commission
- National Security Agency
- Office of Economic Opportunity
- Office of Management and Budget
- Office of Price Administration, or Price Administrator
- Office of Personnel Management
- Occupational Safety and Health Administration
- Occupational Safety and Health Review Commission
- Office of Workers' Compensation Programs
- Patent Office, or Commissioner of, or Board of Appeals of
- Pay Board (established under the Economic Stabilization Act of 1970)
- Pension Benefit Guaranty Corporation
- U.S. Public Health Service
- Postal Rate Commission
- Provider Reimbursement Review Board
- Renegotiation Board
- Railroad Adjustment Board
- Railroad Retirement Board
- Subversive Activities Control Board
- Small Business Administration
- Securities and Exchange Commission
- Social Security Administration or Commissioner
- Selective Service System
- Department or Secretary of the Treasury
- Tennessee Valley Authority
- United States Forest Service
- United States Parole Commission
- Postal Service and Post Office, or Postmaster General, or Postmaster
- United States Sentencing Commission
- Veterans' Administration or Board of Veterans' Appeals
- War Production Board
- Wage Stabilization Board
- State Agency
- Unidentifiable
- Office of Thrift Supervision
- Department of Homeland Security
- Board of General Appraisers
- Board of Tax Appeals
- General Land Office or Commissioners
- NO Admin Action

#### 125 Processing Tax Board of Review

## A2 varAuthorityDecision

*7 Distinct Values*

varAuthorityDecision is used in conjunction with: *authorityDecision1 authorityDecision2*

#### **Values:**

- 1 judicial review (national level)
- 2 judicial review (state level)
- 3 Supreme Court supervision of lower federal or state courts or original jurisdiction
- 4 statutory construction
- 5 interpretation of administrative regulation or rule, or executive order
- 6 diversity jurisdiction
- 7 federal common law

## A3 varCaseDispositionLc

*12 Distinct Values*

varCaseDispositionLc is used in conjunction with: *lcDisposition*

#### **Values:**

- 1 stay, petition, or motion granted
- 2 affirmed
- 3 reversed
- 4 reversed and remanded
- 5 vacated and remanded
- 6 affirmed and reversed (or vacated) in part
- 7 affirmed and reversed (or vacated) in part and remanded
- 8 vacated
- 9 petition denied or appeal dismissed
- 10 modify
- 11 remand
- 12 unusual disposition

## A4 varCaseDispositionSc

*11 Distinct Values*

varCaseDispositionSc is used in conjunction with: *caseDisposition*

#### **Values:**

- 1 stay, petition, or motion granted
- 2 affirmed (includes modified)
- 3 reversed
- 4 reversed and remanded
- 5 vacated and remanded
- 6 affirmed and reversed (or vacated) in part
- 7 affirmed and reversed (or vacated) in part and remanded
- 8 vacated
- 9 petition denied or appeal dismissed
- 10 certification to or from a lower court
- 11 no disposition

## A5 varCaseDispositionUnusual

*2 Distinct Values*

varCaseDispositionUnusual is used in conjunction with: *caseDispositionUnusual*

#### **Values:**

- 0 no unusual disposition specified
- 1 unusual disposition

## A6 varCaseSources

*211 Distinct Values*

varCaseSources is used in conjunction with: *caseOrigin*

*caseSource*

- 1 U.S. Court of Customs and Patent Appeals
- 2 U.S. Court of International Trade
- 3 U.S. Court of Claims, Court of Federal Claims
- 4 U.S. Court of Military Appeals, renamed as Court of Appeals for the Armed Forces
- 5 U.S. Court of Military Review
- 6 U.S. Court of Veterans Appeals
- 7 U.S. Customs Court
- 8 U.S. Court of Appeals, Federal Circuit

- U.S. Tax Court
- Temporary Emergency U.S. Court of Appeals
- U.S. Court for China
- U.S. Consular Courts
- U.S. Commerce Court
- Territorial Supreme Court
- Territorial Appellate Court
- Territorial Trial Court
- Emergency Court of Appeals
- Supreme Court of the District of Columbia
- Bankruptcy Court
- U.S. Court of Appeals, First Circuit
- U.S. Court of Appeals, Second Circuit
- U.S. Court of Appeals, Third Circuit
- U.S. Court of Appeals, Fourth Circuit
- U.S. Court of Appeals, Fifth Circuit
- U.S. Court of Appeals, Sixth Circuit
- U.S. Court of Appeals, Seventh Circuit
- U.S. Court of Appeals, Eighth Circuit
- U.S. Court of Appeals, Ninth Circuit
- U.S. Court of Appeals, Tenth Circuit
- U.S. Court of Appeals, Eleventh Circuit
- U.S. Court of Appeals, District of Columbia Circuit (includes the Court of Appeals for the District of Columbia but not the District of Columbia Court of Appeals, which has local jurisdiction)
- Alabama Middle U.S. District Court
- Alabama Northern U.S. District Court
- Alabama Southern U.S. District Court
- Alaska U.S. District Court
- Arizona U.S. District Court
- Arkansas Eastern U.S. District Court
- Arkansas Western U.S. District Court
- California Central U.S. District Court
- California Eastern U.S. District Court
- California Northern U.S. District Court
- California Southern U.S. District Court
- Colorado U.S. District Court
- Connecticut U.S. District Court
- Delaware U.S. District Court
- District Of Columbia U.S. District Court
- Florida Middle U.S. District Court
- Florida Northern U.S. District Court
- Florida Southern U.S. District Court
- Georgia Middle U.S. District Court
- Georgia Northern U.S. District Court
- Georgia Southern U.S. District Court
- Guam U.S. District Court
- Hawaii U.S. District Court

- Idaho U.S. District Court
- Illinois Central U.S. District Court
- Illinois Northern U.S. District Court
- Illinois Southern U.S. District Court
- Indiana Northern U.S. District Court
- Indiana Southern U.S. District Court
- Iowa Northern U.S. District Court
- Iowa Southern U.S. District Court
- Kansas U.S. District Court
- Kentucky Eastern U.S. District Court
- Kentucky Western U.S. District Court
- Louisiana Eastern U.S. District Court
- Louisiana Middle U.S. District Court
- Louisiana Western U.S. District Court
- Maine U.S. District Court
- Maryland U.S. District Court
- Massachusetts U.S. District Court
- Michigan Eastern U.S. District Court
- Michigan Western U.S. District Court
- Minnesota U.S. District Court
- Mississippi Northern U.S. District Court
- Mississippi Southern U.S. District Court
- Missouri Eastern U.S. District Court
- Missouri Western U.S. District Court
- Montana U.S. District Court
- Nebraska U.S. District Court
- Nevada U.S. District Court
- New Hampshire U.S. District Court
- New Jersey U.S. District Court
- New Mexico U.S. District Court
- New York Eastern U.S. District Court
- New York Northern U.S. District Court
- New York Southern U.S. District Court
- New York Western U.S. District Court
- North Carolina Eastern U.S. District Court
- North Carolina Middle U.S. District Court
- North Carolina Western U.S. District Court
- North Dakota U.S. District Court
- Northern Mariana Islands U.S. District Court
- Ohio Northern U.S. District Court
- Ohio Southern U.S. District Court
- Oklahoma Eastern U.S. District Court
- Oklahoma Northern U.S. District Court
- Oklahoma Western U.S. District Court
- Oregon U.S. District Court
- Pennsylvania Eastern U.S. District Court
- Pennsylvania Middle U.S. District Court
- Pennsylvania Western U.S. District Court

- Puerto Rico U.S. District Court
- Rhode Island U.S. District Court
- South Carolina U.S. District Court
- South Dakota U.S. District Court
- Tennessee Eastern U.S. District Court
- Tennessee Middle U.S. District Court
- Tennessee Western U.S. District Court
- Texas Eastern U.S. District Court
- Texas Northern U.S. District Court
- Texas Southern U.S. District Court
- Texas Western U.S. District Court
- Utah U.S. District Court
- Vermont U.S. District Court
- Virgin Islands U.S. District Court
- Virginia Eastern U.S. District Court
- Virginia Western U.S. District Court
- Washington Eastern U.S. District Court
- Washington Western U.S. District Court
- West Virginia Northern U.S. District Court
- West Virginia Southern U.S. District Court
- Wisconsin Eastern U.S. District Court
- Wisconsin Western U.S. District Court
- Wyoming U.S. District Court
- Louisiana U.S. District Court
- Washington U.S. District Court
- West Virginia U.S. District Court
- Illinois Eastern U.S. District Court
- South Carolina Eastern U.S. District Court
- South Carolina Western U.S. District Court
- Alabama U.S. District Court
- U.S. District Court for the Canal Zone
- Georgia U.S. District Court
- Illinois U.S. District Court
- Indiana U.S. District Court
- Iowa U.S. District Court
- Michigan U.S. District Court
- Mississippi U.S. District Court
- Missouri U.S. District Court
- New Jersey Eastern U.S. District Court (East Jersey U.S. District Court)
- New Jersey Western U.S. District Court (West Jersey U.S. District Court)
- New York U.S. District Court
- North Carolina U.S. District Court
- Ohio U.S. District Court
- Pennsylvania U.S. District Court
- Tennessee U.S. District Court
- Texas U.S. District Court
- Virginia U.S. District Court
- Norfolk U.S. District Court

- Wisconsin U.S. District Court
- Kentucky U.S. Distrcrict Court
- New Jersey U.S. District Court
- California U.S. District Court
- Florida U.S. District Court
- Arkansas U.S. District Court
- District of Orleans U.S. District Court
- State Supreme Court
- State Appellate Court
- State Trial Court
- Eastern Circuit (of the United States)
- Middle Circuit (of the United States)
- Southern Circuit (of the United States)
- Alabama U.S. Circuit Court for (all) District(s) of Alabama
- Arkansas U.S. Circuit Court for (all) District(s) of Arkansas
- California U.S. Circuit for (all) District(s) of California
- Connecticut U.S. Circuit for the District of Connecticut
- Delaware U.S. Circuit for the District of Delaware
- Florida U.S. Circuit for (all) District(s) of Florida
- Georgia U.S. Circuit for (all) District(s) of Georgia
- Illinois U.S. Circuit for (all) District(s) of Illinois
- Indiana U.S. Circuit for (all) District(s) of Indiana
- Iowa U.S. Circuit for (all) District(s) of Iowa
- Kansas U.S. Circuit for the District of Kansas
- Kentucky U.S. Circuit for (all) District(s) of Kentucky
- Louisiana U.S. Circuit for (all) District(s) of Louisiana
- Maine U.S. Circuit for the District of Maine
- Maryland U.S. Circuit for the District of Maryland
- Massachusetts U.S. Circuit for the District of Massachusetts
- Michigan U.S. Circuit for (all) District(s) of Michigan
- Minnesota U.S. Circuit for the District of Minnesota
- Mississippi U.S. Circuit for (all) District(s) of Mississippi
- Missouri U.S. Circuit for (all) District(s) of Missouri
- Nevada U.S. Circuit for the District of Nevada
- New Hampshire U.S. Circuit for the District of New Hampshire
- New Jersey U.S. Circuit for (all) District(s) of New Jersey
- New York U.S. Circuit for (all) District(s) of New York
- North Carolina U.S. Circuit for (all) District(s) of North Carolina
- Ohio U.S. Circuit for (all) District(s) of Ohio
- Oregon U.S. Circuit for the District of Oregon
- Pennsylvania U.S. Circuit for (all) District(s) of Pennsylvania
- Rhode Island U.S. Circuit for the District of Rhode Island
- South Carolina U.S. Circuit for the District of South Carolina
- Tennessee U.S. Circuit for (all) District(s) of Tennessee
- Texas U.S. Circuit for (all) District(s) of Texas
- Vermont U.S. Circuit for the District of Vermont
- Virginia U.S. Circuit for (all) District(s) of Virginia
- West Virginia U.S. Circuit for (all) District(s) of West Virginia

- Wisconsin U.S. Circuit for (all) District(s) of Wisconsin
- Wyoming U.S. Circuit for the District of Wyoming
- Circuit Court of the District of Columbia
- Nebraska U.S. Circuit for the District of Nebraska
- Colorado U.S. Circuit for the District of Colorado
- Washington U.S. Circuit for (all) District(s) of Washington
- Idaho U.S. Circuit Court for (all) District(s) of Idaho
- Montana U.S. Circuit Court for (all) District(s) of Montana
- Utah U.S. Circuit Court for (all) District(s) of Utah
- South Dakota U.S. Circuit Court for (all) District(s) of South Dakota
- North Dakota U.S. Circuit Court for (all) District(s) of North Dakota
- Oklahoma U.S. Circuit Court for (all) District(s) of Oklahoma
- Court of Private Land Claims

## A7 varCertReason

*13 Distinct Values*

varCertReason is used in conjunction with: *certReason*

#### **Values:**

- case did not arise on cert or cert not granted
- federal court conflict
- federal court conflict and to resolve important or significant question
- putative conflict
- conflict between federal court and state court
- state court conflict
- federal court confusion or uncertainty
- state court confusion or uncertainty
- federal court and state court confusion or uncertainty
- to resolve important or significant question
- to resolve question presented
- no reason given
- other reason

## A8 varChiefs

*17 Distinct Values*

varChiefs is used in conjunction with: *chief*

#### **Values:**

Jay

- 2 Rutledge
- 3 Ellsworth
- 4 Marshall
- 5 Taney
- 6 Chase
- 7 Waite
- 8 Fuller
- 9 White
- 10 Taft
- 11 Hughes
- 12 Stone
- 13 Vinson
- 14 Warren
- 15 Burger
- 16 Rehnquist
- 17 Roberts

## A9 varDecisionDirection

*3 Distinct Values*

varDecisionDirection is used in conjunction with: *lcDispositionDirection decisionDirection*

#### **Values:**

- 1 conservative
- 2 liberal
- 3 unspecifiable

## A10 varDecisionDirectionDissent

*2 Distinct Values*

varDecisionDirectionDissent is used in conjunction with: *decisionDirectionDissent*

#### **Values:**

- 0 dissent in opposite direction
- 1 majority and dissent in same direction

## A11 varDecisionTypes

*7 Distinct Values*

varDecisionTypes is used in conjunction with: *decisionType*

#### **Values:**

- 1 opinion of the court (orally argued)
- 2 per curiam (no oral argument)
- 4 decrees
- 5 equally divided vote
- 6 per curiam (orally argued)
- 7 judgment of the Court (orally argued)
- 8 seriatim

## A12 varDeclarationUncon

*4 Distinct Values*

varDeclarationUncon is used in conjunction with: *declarationUncon*

#### **Values:**

- 1 no declaration of unconstitutionality
- 2 act of congress declared unconstitutional
- 3 state or territorial law, reg, or const provision unconstitutional
- 4 municipal or other local ordinance unconstitutional

## A13 varIssues

*278 Distinct Values*

varIssues is used in conjunction with:

*issue*

| 10010 | involuntary confession                                                                    |
|-------|-------------------------------------------------------------------------------------------|
| 10020 | habeas corpus                                                                             |
| 10030 | plea bargaining: the constitutionality of and/or the circumstances of its exercise        |
| 10040 | retroactivity (of newly announced or newly enacted constitutional or statutory<br>rights) |
| 10050 | search and seizure (other than as pertains to vehicles or Crime Control Act)              |
| 10060 | search and seizure, vehicles                                                              |
| 10070 | search and seizure, Crime Control Act                                                     |
| 10080 | contempt of court or congress                                                             |
| 10090 | self-incrimination (other than as pertains to Miranda or immunity from prosecution)       |

| 10100 | Miranda warnings                                                                                                                                                    |
|-------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 10110 | self-incrimination, immunity from prosecution                                                                                                                       |
| 10120 | right to counsel (cf. indigents appointment of counsel or inadequate representation)                                                                                |
| 10130 | cruel and unusual punishment, death penalty (cf. extra legal jury influence, death<br>penalty)                                                                      |
| 10140 | cruel and unusual punishment, non-death penalty (cf. liability, civil rights acts)                                                                                  |
| 10150 | line-up                                                                                                                                                             |
| 10160 | discovery and inspection (in the context of criminal litigation only, otherwise<br>Freedom of Information Act and related federal or state statutes or regulations) |
| 10170 | double jeopardy                                                                                                                                                     |
| 10180 | ex post facto (state)                                                                                                                                               |
| 10190 | extra-legal jury influences: miscellaneous                                                                                                                          |
| 10200 | extra-legal jury influences: prejudicial statements or evidence                                                                                                     |
| 10210 | extra-legal jury influences: contact with jurors outside courtroom                                                                                                  |
| 10220 | extra-legal jury influences: jury instructions (not necessarily in criminal cases)                                                                                  |
| 10230 | extra-legal jury influences: voir dire (not necessarily a criminal case)                                                                                            |
| 10240 | extra-legal jury influences: prison garb or appearance                                                                                                              |
| 10250 | extra-legal jury influences: jurors and death penalty (cf. cruel and unusual<br>punishment)                                                                         |
| 10260 | extra-legal jury influences: pretrial publicity                                                                                                                     |
| 10270 | confrontation (right to confront accuser, call and cross-examine witnesses)                                                                                         |
| 10280 | subconstitutional fair procedure: confession of error                                                                                                               |
| 10290 | subconstitutional fair procedure: conspiracy (cf. Federal Rules of Criminal<br>Procedure: conspiracy)                                                               |
| 10300 | subconstitutional fair procedure: entrapment                                                                                                                        |
| 10310 | subconstitutional fair procedure: exhaustion of remedies                                                                                                            |
| 10320 | subconstitutional fair procedure: fugitive from justice                                                                                                             |
| 10330 | subconstitutional fair procedure: presentation, admissibility, or sufficiency of<br>evidence (not necessarily a criminal case)                                      |
| 10340 | subconstitutional fair procedure: stay of execution                                                                                                                 |
| 10350 | subconstitutional fair procedure: timeliness                                                                                                                        |
| 10360 | subconstitutional fair procedure: miscellaneous                                                                                                                     |
| 10370 | Federal Rules of Criminal Procedure                                                                                                                                 |
| 10380 | statutory construction of criminal laws: assault                                                                                                                    |
| 10390 | statutory construction of criminal laws: bank robbery                                                                                                               |
| 10400 | statutory construction of criminal laws: conspiracy (cf. subconstitutional fair<br>procedure: conspiracy)                                                           |
| 10410 | statutory construction of criminal laws: escape from custody                                                                                                        |
| 10420 | statutory construction of criminal laws: false statements (cf. statutory construction<br>of criminal laws: perjury)                                                 |
| 10430 | statutory construction of criminal laws: financial (other than in fraud or internal<br>revenue)                                                                     |
| 10440 | statutory construction of criminal laws: firearms                                                                                                                   |
| 10450 | statutory construction of criminal laws: fraud                                                                                                                      |
| 10460 | statutory construction of criminal laws: gambling                                                                                                                   |
| 10470 | statutory construction of criminal laws: Hobbs Act; i.e., 18 USC 1951                                                                                               |
| 10480 | statutory construction of criminal laws: immigration (cf. immigration and<br>naturalization)                                                                        |
| 10490 | statutory construction of criminal laws: internal revenue (cf. Federal Taxation)                                                                                    |
| 10500 | statutory construction of criminal laws: Mann Act and related statutes                                                                                              |

| 10510 | statutory construction of criminal laws: narcotics includes regulation and<br>prohibition of alcohol                                      |
|-------|-------------------------------------------------------------------------------------------------------------------------------------------|
| 10520 | statutory construction of criminal laws: obstruction of justice                                                                           |
| 10530 | statutory construction of criminal laws: perjury (other than as pertains to statutory<br>construction of criminal laws: false statements) |
| 10540 | statutory construction of criminal laws: Travel Act, 18 USC 1952                                                                          |
| 10550 | statutory construction of criminal laws: war crimes                                                                                       |
| 10560 | statutory construction of criminal laws: sentencing guidelines                                                                            |
| 10570 | statutory construction of criminal laws: miscellaneous                                                                                    |
| 10580 | jury trial (right to, as distinct from extra-legal jury influences)                                                                       |
| 10590 | speedy trial                                                                                                                              |
| 10600 | miscellaneous criminal procedure (cf. due process, prisoners' rights, comity:<br>criminal procedure)                                      |
| 20010 | voting                                                                                                                                    |
| 20020 | Voting Rights Act of 1965, plus amendments                                                                                                |
| 20030 | ballot access (of candidates and political parties)                                                                                       |
| 20040 | desegregation (other than as pertains to school desegregation, employment<br>discrimination, and affirmative action)                      |
| 20050 | desegregation, schools                                                                                                                    |
| 20060 | employment discrimination: on basis of race, age, religion, illegitimacy, national<br>origin, or working conditions.                      |
| 20070 | affirmative action                                                                                                                        |
| 20075 | slavery or indenture                                                                                                                      |
| 20080 | sit-in demonstrations (protests against racial discrimination in places of public<br>accommodation)                                       |
| 20090 | reapportionment: other than plans governed by the Voting Rights Act                                                                       |
| 20100 | debtors' rights                                                                                                                           |
| 20110 | deportation (cf. immigration and naturalization)                                                                                          |
| 20120 | employability of aliens (cf. immigration and naturalization)                                                                              |
| 20130 | sex discrimination (excluding sex discrimination in employment)                                                                           |
| 20140 | sex discrimination in employment (cf. sex discrimination)                                                                                 |
| 20150 | Indians (other than pertains to state jurisdiction over)                                                                                  |
| 20160 | Indians, state jurisdiction over                                                                                                          |
| 20170 | juveniles (cf. rights of illegitimates)                                                                                                   |
| 20180 | poverty law, constitutional                                                                                                               |
| 20190 | poverty law, statutory: welfare benefits, typically under some Social Security Act<br>provision.                                          |
| 20200 | illegitimates, rights of (cf. juveniles): typically inheritance and survivor's benefits,<br>and paternity suits                           |
| 20210 | handicapped, rights of: under Rehabilitation, Americans with Disabilities Act, and<br>related statutes                                    |
| 20220 | residency requirements: durational, plus discrimination against nonresidents                                                              |
| 20230 | military: draftee, or person subject to induction                                                                                         |
| 20240 | military: active duty                                                                                                                     |
| 20250 | military: veteran                                                                                                                         |
| 20260 | immigration and naturalization: permanent residence                                                                                       |
| 20270 | immigration and naturalization: citizenship                                                                                               |
| 20280 | immigration and naturalization: loss of citizenship, denaturalization                                                                     |
| 20290 | immigration and naturalization: access to public education                                                                                |
| 20300 | immigration and naturalization: welfare benefits                                                                                          |

| 20310 | immigration and naturalization: miscellaneous                                                                                                              |
|-------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 20320 | indigents: appointment of counsel (cf. right to counsel)                                                                                                   |
| 20330 | indigents: inadequate representation by counsel (cf. right to counsel)                                                                                     |
| 20340 | indigents: payment of fine                                                                                                                                 |
| 20350 | indigents: costs or filing fees                                                                                                                            |
| 20360 | indigents: U.S. Supreme Court docketing fee                                                                                                                |
| 20370 | indigents: transcript                                                                                                                                      |
| 20380 | indigents: assistance of psychiatrist                                                                                                                      |
| 20390 | indigents: miscellaneous                                                                                                                                   |
| 20400 | liability, civil rights acts (cf. liability, governmental and liability, nongovernmental;<br>cruel and unusual punishment, non-death penalty)              |
| 20410 | miscellaneous civil rights (cf. comity: civil rights)                                                                                                      |
| 30010 | First Amendment, miscellaneous (cf. comity: First Amendment)                                                                                               |
| 30020 | commercial speech, excluding attorneys                                                                                                                     |
| 30030 | libel, defamation: defamation of public officials and public and private persons                                                                           |
| 30040 | libel, privacy: true and false light invasions of privacy                                                                                                  |
| 30050 | legislative investigations: concerning internal security only                                                                                              |
| 30060 | federal or state internal security legislation: Smith, Internal Security, and related<br>federal statutes                                                  |
| 30070 | loyalty oath or non-Communist affidavit (other than bar applicants, government<br>employees, political party, or teacher)                                  |
| 30080 | loyalty oath: bar applicants (cf. admission to bar, state or federal or U.S. Supreme<br>Court)                                                             |
| 30090 | loyalty oath: government employees                                                                                                                         |
| 30100 | loyalty oath: political party                                                                                                                              |
| 30110 | loyalty oath: teachers                                                                                                                                     |
| 30120 | security risks: denial of benefits or dismissal of employees for reasons other than<br>failure to meet loyalty oath requirements                           |
| 30130 | conscientious objectors (cf. military draftee or military active duty) to military<br>service                                                              |
| 30140 | campaign spending (cf. governmental corruption):                                                                                                           |
| 30150 | protest demonstrations (other than as pertains to sit-in demonstrations):<br>demonstrations and other forms of protest based on First Amendment guarantees |
| 30160 | free exercise of religion                                                                                                                                  |
| 30170 | establishment of religion (other than as pertains to parochiaid:)                                                                                          |
| 30180 | parochiaid: government aid to religious schools, or religious requirements in public<br>schools                                                            |
| 30190 | obscenity, state (cf. comity: privacy): including the regulation of sexually explicit<br>material under the 21st Amendment                                 |
| 30200 | obscenity, federal                                                                                                                                         |
| 40010 | due process: miscellaneous (cf. loyalty oath), the residual code                                                                                           |
| 40020 | due process: hearing or notice (other than as pertains to government employees or<br>prisoners' rights)                                                    |
| 40030 | due process: hearing, government employees                                                                                                                 |
| 40040 | due process: prisoners' rights and defendants' rights                                                                                                      |
| 40050 | due process: impartial decision maker                                                                                                                      |
| 40060 | due process: jurisdiction (jurisdiction over non-resident litigants)                                                                                       |
| 40070 | due process: takings clause, or other non-constitutional governmental taking of<br>property                                                                |
| 50010 | privacy (cf. libel, comity: privacy)                                                                                                                       |
| 50020 | abortion: including contraceptives                                                                                                                         |

| 50030          | right to die                                                                                                                                                         |
|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 50040          | Freedom of Information Act and related federal or state statutes or regulations                                                                                      |
| 60010          | attorneys' and governmental employees' or officials' fees or compensation or<br>licenses                                                                             |
| 60020          | commercial speech, attorneys (cf. commercial speech)                                                                                                                 |
| 60030          | admission to a state or federal bar, disbarment, and attorney discipline (cf. loyalty<br>oath: bar applicants)                                                       |
| 60040          | admission to, or disbarment from, Bar of the U.S. Supreme Court                                                                                                      |
| 70010          | arbitration (in the context of labor-management or employer-employee relations)<br>(cf. arbitration)                                                                 |
| 70020          | union antitrust: legality of anticompetitive union activity                                                                                                          |
| 70030          | union or closed shop: includes agency shop litigation                                                                                                                |
| 70040          | Fair Labor Standards Act                                                                                                                                             |
| 70050          | Occupational Safety and Health Act                                                                                                                                   |
| 70060          | union-union member dispute (except as pertains to union or closed shop)                                                                                              |
| 70070          | labor-management disputes: bargaining                                                                                                                                |
| 70080          | labor-management disputes: employee discharge                                                                                                                        |
| 70090          | labor-management disputes: distribution of union literature                                                                                                          |
| 70100          | labor-management disputes: representative election                                                                                                                   |
| 70110          | labor-management disputes: antistrike injunction                                                                                                                     |
| 70120          | labor-management disputes: jurisdictional dispute                                                                                                                    |
| 70130          | labor-management disputes: right to organize                                                                                                                         |
| 70140          | labor-management disputes: picketing                                                                                                                                 |
| 70150          | labor-management disputes: secondary activity                                                                                                                        |
| 70160          | labor-management disputes: no-strike clause                                                                                                                          |
| 70170          | labor-management disputes: union representatives                                                                                                                     |
| 70180          | labor-management disputes: union trust funds (cf. ERISA)                                                                                                             |
| 70190          | labor-management disputes: working conditions                                                                                                                        |
| 70200          | labor-management disputes: miscellaneous dispute                                                                                                                     |
| 70210          | miscellaneous union                                                                                                                                                  |
| 80010          | antitrust (except in the context of mergers and union antitrust)                                                                                                     |
| 80020          |                                                                                                                                                                      |
|                | mergers                                                                                                                                                              |
| 80030<br>80040 | bankruptcy (except in the context of priority of federal fiscal claims)<br>sufficiency of evidence: typically in the context of a jury's determination of            |
|                | compensation for injury or death                                                                                                                                     |
| 80050          | election of remedies: legal remedies available to injured persons or things                                                                                          |
| 80060          | liability, governmental: tort or contract actions by or against government or<br>governmental officials other than defense of criminal actions brought under a civil |
| 80070          | rights action.<br>liability, other than as in sufficiency of evidence, election of remedies, punitive<br>damages                                                     |
| 80080          | liability, punitive damages                                                                                                                                          |
| 80090          | Employee Retirement Income Security Act (cf. union trust funds)                                                                                                      |
| 80100          | state or local government tax                                                                                                                                        |
| 80105          | state and territorial land claims                                                                                                                                    |
| 80110          | state or local government regulation, especially of business (cf. federal pre-emption                                                                                |
|                | of state court jurisdiction, federal pre-emption of state legislation or regulation)                                                                                 |
| 80120          | federal or state regulation of securities                                                                                                                            |
| 80130          | natural resources - environmental protection (cf. national supremacy: natural<br>resources, national supremacy: pollution)                                           |

| 80140 | corruption, governmental or governmental regulation of other than as in campaign<br>spending                                                                               |
|-------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 80150 | zoning: constitutionality of such ordinances, or restrictions on owners' or lessors'<br>use of real property                                                               |
| 80160 | arbitration (other than as pertains to labor-management or employer-employee                                                                                               |
|       | relations (cf. union arbitration)                                                                                                                                          |
| 80170 | federal or state consumer protection: typically under the Truth in Lending; Food,<br>Drug and Cosmetic; and Consumer Protection Credit Acts                                |
| 80180 | patents and copyrights: patent                                                                                                                                             |
| 80190 | patents and copyrights: copyright                                                                                                                                          |
| 80200 | patents and copyrights: trademark                                                                                                                                          |
| 80210 | patents and copyrights: patentability of computer processes                                                                                                                |
| 80220 | federal or state regulation of transportation regulation: railroad                                                                                                         |
| 80230 | federal and some few state regulations of transportation regulation: boat                                                                                                  |
| 80240 | federal and some few state regulation of transportation regulation:truck, or motor                                                                                         |
|       | carrier                                                                                                                                                                    |
| 80250 | federal and some few state regulation of transportation regulation: pipeline (cf.<br>federal public utilities regulation: gas pipeline)                                    |
| 80260 | federal and some few state regulation of transportation regulation: airline                                                                                                |
| 80270 | federal and some few state regulation of public utilities regulation: electric power                                                                                       |
| 80280 | federal and some few state regulation of public utilities regulation: nuclear power                                                                                        |
| 80290 | federal and some few state regulation of public utilities regulation: oil producer                                                                                         |
| 80300 | federal and some few state regulation of public utilities regulation: gas producer                                                                                         |
| 80310 | federal and some few state regulation of public utilities regulation: gas pipeline (cf.                                                                                    |
|       | federal transportation regulation: pipeline)                                                                                                                               |
| 80320 | federal and some few state regulation of public utilities regulation: radio and                                                                                            |
|       | television (cf. cable television)                                                                                                                                          |
| 80330 | federal and some few state regulation of public utilities regulation: cable television                                                                                     |
|       | (cf. radio and television)                                                                                                                                                 |
| 80340 | federal and some few state regulations of public utilities regulation: telephone or<br>telegraph company                                                                   |
| 80350 | miscellaneous economic regulation                                                                                                                                          |
| 90010 | comity: civil rights                                                                                                                                                       |
| 90020 | comity: criminal procedure                                                                                                                                                 |
| 90030 | comity: First Amendment                                                                                                                                                    |
|       |                                                                                                                                                                            |
| 90040 | comity: habeas corpus                                                                                                                                                      |
| 90050 | comity: military                                                                                                                                                           |
| 90060 | comity: obscenity                                                                                                                                                          |
| 90070 | comity: privacy                                                                                                                                                            |
| 90080 | comity: miscellaneous                                                                                                                                                      |
| 90090 | comity primarily removal cases, civil procedure (cf. comity, criminal and First<br>Amendment); deference to foreign judicial tribunals                                     |
| 90100 | assessment of costs or damages: as part of a court order                                                                                                                   |
| 90110 | Federal Rules of Civil Procedure including Supreme Court Rules, application of the<br>Federal Rules of Evidence, Federal Rules of Appellate Procedure in civil litigation, |
| 90120 | Circuit Court Rules, and state rules and admiralty rules<br>judicial review of administrative agency's or administrative official's actions and                            |
|       | procedures                                                                                                                                                                 |
| 90130 | mootness (cf. standing to sue: live dispute)                                                                                                                               |
| 90140 | venue                                                                                                                                                                      |
| 90150 | no merits: writ improvidently granted                                                                                                                                      |

| 90160  | no merits: dismissed or affirmed for want of a substantial or properly presented                                                                            |
|--------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
|        | federal question, or a nonsuit<br>no merits: dismissed or affirmed for want of jurisdiction (cf. judicial administration:                                   |
| 90170  | Supreme Court jurisdiction or authority on appeal from federal district courts or                                                                           |
|        | courts of appeals)                                                                                                                                          |
| 90180  | no merits: adequate non-federal grounds for decision                                                                                                        |
| 90190  | no merits: remand to determine basis of state or federal court decision (cf. judicial                                                                       |
|        | administration: state law)                                                                                                                                  |
| 90200  | no merits: miscellaneous                                                                                                                                    |
| 90210  | standing to sue: adversary parties                                                                                                                          |
| 90220  | standing to sue: direct injury                                                                                                                              |
| 90230  | standing to sue: legal injury                                                                                                                               |
| 90240  | standing to sue: personal injury                                                                                                                            |
| 90250  | standing to sue: justiciable question                                                                                                                       |
| 90260  | standing to sue: live dispute                                                                                                                               |
| 90270  | standing to sue: parens patriae standing                                                                                                                    |
| 90280  | standing to sue: statutory standing                                                                                                                         |
| 90290  | standing to sue: private or implied cause of action                                                                                                         |
| 90300  | standing to sue: taxpayer's suit                                                                                                                            |
| 90310  | standing to sue: miscellaneous                                                                                                                              |
| 90320  | judicial administration: jurisdiction or authority of federal district courts or                                                                            |
|        | territorial courts                                                                                                                                          |
| 90330  | judicial administration: jurisdiction or authority of federal courts of appeals                                                                             |
| 90340  | judicial administration: Supreme Court jurisdiction or authority on appeal or writ of<br>error, from federal district courts or courts of appeals (cf. 753) |
| 90350  | judicial administration: Supreme Court jurisdiction or authority on appeal or writ of<br>error, from highest state court                                    |
| 90360  | judicial administration: jurisdiction or authority of the Court of Claims                                                                                   |
| 90370  | judicial administration: Supreme Court's original jurisdiction                                                                                              |
| 90380  | judicial administration: review of non-final order                                                                                                          |
| 90390  | judicial administration: change in state law (cf. no merits: remand to determine<br>basis of state court decision)                                          |
| 90400  | judicial administration: federal question (cf. no merits: dismissed for want of a                                                                           |
|        | substantial or properly presented federal question)                                                                                                         |
| 90410  | judicial administration: ancillary or pendent jurisdiction                                                                                                  |
| 90420  | judicial administration: extraordinary relief (e.g., mandamus, injunction)                                                                                  |
| 90430  | judicial administration: certification (cf. objection to reason for denial of certiorari                                                                    |
|        | or appeal)                                                                                                                                                  |
| 90440  | judicial administration: resolution of circuit conflict, or conflict between or among<br>other courts                                                       |
| 90450  | judicial administration: objection to reason for denial of certiorari or appeal                                                                             |
| 90460  | judicial administration: collateral estoppel or res judicata                                                                                                |
| 90470  | judicial administration: interpleader                                                                                                                       |
| 90480  | judicial administration: untimely filing                                                                                                                    |
| 90490  | judicial administration: Act of State doctrine                                                                                                              |
| 90500  | judicial administration: miscellaneous                                                                                                                      |
|        |                                                                                                                                                             |
| 90510  | Supreme Court's certiorari, writ of error, or appeals jurisdiction                                                                                          |
| 90520  | miscellaneous judicial power, especially diversity jurisdiction                                                                                             |
| 100010 | federal-state ownership dispute (cf. Submerged Lands Act)                                                                                                   |
| 100020 | federal pre-emption of state court jurisdiction                                                                                                             |

| 100030 | federal pre-emption of state legislation or regulation. cf. state regulation of<br>business. rarely involves union activity. Does not involve constitutional |
|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
|        | interpretation unless the Court says it does.                                                                                                                |
| 100040 | Submerged Lands Act (cf. federal-state ownership dispute)                                                                                                    |
| 100050 | national supremacy: commodities                                                                                                                              |
| 100060 | national supremacy: intergovernmental tax immunity                                                                                                           |
| 100070 | national supremacy: marital and family relationships and property, including<br>obligation of child support                                                  |
| 100080 | national supremacy: natural resources (cf. natural resources - environmental<br>protection)                                                                  |
| 100090 | national supremacy: pollution, air or water (cf. natural resources - environmental                                                                           |
|        | protection)                                                                                                                                                  |
| 100100 | national supremacy: public utilities (cf. federal public utilities regulation)                                                                               |
| 100110 | national supremacy: state tax (cf. state tax)                                                                                                                |
| 100120 | national supremacy: miscellaneous                                                                                                                            |
| 100130 | miscellaneous federalism                                                                                                                                     |
| 110010 | boundary dispute between states                                                                                                                              |
| 110020 | non-real property dispute between states                                                                                                                     |
| 110030 | miscellaneous interstate relations conflict                                                                                                                  |
| 110033 | incorporation of foreign territories                                                                                                                         |
| 120010 | federal taxation, typically under provisions of the Internal Revenue Code                                                                                    |
| 120020 | federal taxation of gifts, personal, business, or professional expenses                                                                                      |
| 120030 | priority of federal fiscal claims: over those of the states or private entities                                                                              |
| 120040 | miscellaneous federal taxation (cf. national supremacy: state tax)                                                                                           |
| 130010 | legislative veto                                                                                                                                             |
| 130015 | executive authority vis-a-vis congress or the states                                                                                                         |
| 130020 | miscellaneous                                                                                                                                                |
| 140010 | real property                                                                                                                                                |
| 140020 | personal property                                                                                                                                            |
| 140030 | contracts                                                                                                                                                    |
| 140040 | evidence                                                                                                                                                     |
| 140050 | civil procedure                                                                                                                                              |
| 140060 | torts                                                                                                                                                        |
| 140070 | wills and trusts                                                                                                                                             |
| 140080 | commercial transactions                                                                                                                                      |
|        |                                                                                                                                                              |

## A14 varIssuesAreas

*14 Distinct Values*

varIssuesAreas is used in conjunction with: *issueArea*

- Criminal Procedure
- Civil Rights
- First Amendment
- Due Process

- Privacy
- Attorneys
- Unions
- Economic Activity
- Judicial Power
- Federalism
- Interstate Relations
- Federal Taxation
- Miscellaneous
- Private Action

## A15 varJurisdiction

*14 Distinct Values*

varJurisdiction is used in conjunction with: *jurisdiction*

#### **Values:**

- cert
- appeal
- bail
- certification
- docketing fee
- rehearing or restored to calendar for reargument
- injunction
- mandamus
- original
- prohibition
- stay
- writ of error
- writ of habeas corpus
- unspecified, other

## A16 varJusticeDirection

*2 Distinct Values*

varJusticeDirection is used in conjunction with: *direction*

- conservative
- liberal

## A17 varJusticeMajority

*2 Distinct Values*

varJusticeMajority is used in conjunction with: *majority*

#### **Values:**

- 1 dissent
- 2 majority

## A18 varJusticeOpinion

*3 Distinct Values*

varJusticeOpinion is used in conjunction with: *opinion*

#### **Values:**

- 1 justice wrote no opinion
- 2 justice wrote an opinion
- 3 justice co-authored an opinion

## A19 varJustices

*118 Distinct Values*

varJustices is used in conjunction with: *majOpinWriter majOpinAssigner justice justiceName firstAgreement secondAgreement*

- 1 JJay
- 2 JRutledge1
- 3 WCushing
- 4 JWilson
- 5 JBlair
- 6 JIredell

- TJohnson
- WPaterson
- JRutledge2
- SChase
- OEllsworth
- BWashington
- AMoore
- JMarshall
- WJohnson
- HBLivingston
- TTodd
- GDuvall
- JStory
- SThompson
- RTrimble
- JMcLean
- HBaldwin
- JMWayne
- RBTaney
- PPBarbour
- JCatron
- JMcKinley
- PVDaniel
- SNelson
- LWoodbury
- RCGrier
- BRCurtis
- JACampbell
- NClifford
- NHSwayne
- SFMiller
- DDavis
- SJField
- SPChase
- WStrong
- JPBradley
- WHunt
- MRWaite
- JHarlan1
- WBWoods
- SMatthews
- HGray
- SBlatchford
- LQLamar
- MWFuller
- DJBrewer
- HBBrown
- GShiras

- HEJackson
- EDEWhite
- RWPeckham
- JMcKenna
- OWHolmes
- WRDay
- WHMoody
- HHLurton
- CEHughes1
- WVanDevanter
- JRLamar
- MPitney
- JCMcReynolds
- LDBrandeis
- JHClarke
- WHTaft
- GSutherland
- PButler
- ETSanford
- HFStone
- CEHughes2
- OJRoberts
- BNCardozo
- HLBlack
- SFReed
- FFrankfurter
- WODouglas
- FMurphy
- JFByrnes
- RHJackson
- WBRutledge
- HHBurton
- FMVinson
- TCClark
- SMinton
- EWarren
- JHarlan2
- WJBrennan
- CEWhittaker
- PStewart
- BRWhite
- AJGoldberg
- AFortas
- TMarshall
- WEBurger
- HABlackmun
- LFPowell
- WHRehnquist

- JPStevens
- SDOConnor
- AScalia
- AMKennedy
- DHSouter
- CThomas
- RBGinsburg
- SGBreyer
- JGRoberts
- SAAlito
- SSotomayor
- EKagan
- NMGorsuch
- BMKavanaugh
- ACBarrett
- KBJackson

## A20 varLawArea

*8 Distinct Values*

varLawArea is used in conjunction with: *lawType*

#### **Values:**

- Constitution
- Constitutional Amendment
- Federal Statute
- Court Rules
- Other
- Infrequently litigated statutes
- State or local law or regulation
- No Legal Provision

## A21 varLcDisagreement

*2 Distinct Values*

varLcDisagreement is used in conjunction with: *lcDisagreement*

- no mention that dissent occurred
- dissent in ct whose dec the sct reviewed

## A22 varLegalProvisions

*206 Distinct Values*

varLegalProvisions is used in conjunction with: *lawSupp*

- Article I, Section 1 (delegation of powers)
- Article I, Section 10 (state bill of attainder, ex post facto law, or bills of credit)
- Article I, Section 2, Paragraph 1 (composition of the House of Representatives)
- Article I, Section 2, Paragraph 3 (apportionment of Representatives)
- Article I, Section 4, Paragraph 1 (elections clause)
- Article I, Section 5, Paragraph 1 (congressional qualifications)
- Article I, Section 6, Paragraph 1 (speech or debate clause)
- Article I, Section 6, Paragraph 2 (civil appointments)
- Article I, Section 7, Paragraph 1 (origination clause)
- Article I, Section 7, Paragraph 2 (separation of powers)
- Article I, Section 8, Paragraph 1 (taxing, spending, general welfare, or uniformity clause)
- Article I, Section 8, Paragraph 3 (interstate commerce clause)
- Article I, Section 8, Paragraph 4 (bankruptcy clause)
- Article I, Section 8, Paragraph 7 (postal power)
- Article I, Section 8, Paragraph 8 (patent and copyright clause)
- Article I, Section 8, Paragraph 11 (war power)
- Article I, Section 8, Paragraph 14 (governance of the armed forces)
- Article I, Section 8, Paragraph 15 (call-up of militia)
- Article I, Section 8, Paragraph 16 (organizing the militia)
- Article I, Section 8, Paragraph 17 (governance of the District of Columbia and lands purchased from the states)
- Article I, Section 8, Paragraph 18 (necessary and proper clause)
- Article I, Section 9, Paragraph 2 (suspension of the writ of habeas corpus)
- Article I, Section 9, Paragraph 3 (bill of attainder or ex post facto law)
- Article I, Section 9, Paragraph 4 (direct tax)
- Article I, Section 9, Paragraph 5 (export clause)
- Article I, Section 9, Paragraph 6 (preference to ports)
- Article I, Section 9, Paragraph 7 (appropriations clause)
- Article I, Section 10 (state bill of attainder or ex post facto law)
- Article I, Section 10, Paragraph 1 (contract clause)
- Article I, Section 10, Paragraph 2 (export-import clause)
- Article I, Section 10, Paragraph 3 (compact clause)
- Article II, Section 1 (executive power)
- Article II, Section 1, Paragraph 8 (oath provision)
- Article II, Section 2 (commander-in-chief)
- Article II, Section 2, Paragraph 1 (presidential pardoning power)
- Article II, Section 2, Paragraph 2 (appointments clause)

- Article III, Section 1, Paragraph 1 (judicial power)
- Article III, Section 1, Paragraph 2 (good behavior and compensation clause of federal judges)
- Article III, Section 2 (extent of judicial power)
- Article III, Section 2, Paragraph 1 (case or controversy requirement)
- Article III, Section 2, Paragraph 2 (original jurisdiction)
- Article III, Section 2, Paragraph 3 (vicinage requirement)
- Article III, Section 3 (treason clause)
- Article IV, Section 1 (full faith and credit clause)
- Article IV, Section 2, Paragraph 1 (privileges and immunities clause)
- Article IV, Section 2, Paragraph 2 (extradition clause)
- Article IV, Section 3, Paragraph 2 (property clause)
- Article IV, Section 4 (guarantee clause)
- Article VI, Section 2 (supremacy clause)
- Article VI, Section 3 (oath provision)
- Amendment Clause
- Article V, Section 1 (courts)
- 'contract clause' (No Article to be added)
- 'freedom of contract' (Again, no article)
- First Amendment (speech, press, and assembly)
- First Amendment (association)
- First Amendment (free exercise of religion)
- First Amendment (establishment of religion)
- First Amendment (petition clause)
- Fourth Amendment
- Fifth Amendment (double jeopardy)
- Fifth Amendment (due process)
- Fifth Amendment (grand jury)
- Fifth Amendment (Miranda warnings)
- Fifth Amendment (self-incrimination)
- Fifth Amendment (takings clause)
- Fifth Amendment (equal protection)
- Sixth Amendment (right to confront and cross-examine, compulsory process)
- Sixth Amendment (right to counsel)
- Sixth Amendment (right to trial by jury)
- Sixth Amendment (speedy trial)
- Sixth Amendment (other provisions)
- Seventh Amendment
- Eighth Amendment (prohibition of excessive bail)
- Eighth Amendment (prohibition of excessive fines)
- Eighth Amendment (cruel and unusual punishment)
- Ninth Amendment
- Tenth Amendment
- Eleventh Amendment
- Twelfth Amendment
- Thirteenth Amendment (both sections 1 and 2)
- Fourteenth Amendment (privileges and immunities clause)
- Fourteenth Amendment (reduction in representation clause)

- Fourteenth Amendment (citizenship clause)
- Fourteenth Amendment (due process)
- Fourteenth Amendment (equal protection)
- Fourteenth Amendment (enforcement clause)
- Fifteenth Amendment (other provisions)
- Fifteenth Amendment (enforcement clause)
- Sixteenth Amendment
- Seventeenth Amendment
- Twenty-First Amendment
- Twenty-Fourth Amendment
- Second Amendment
- Fourteenth Amendment (due process and equal protection)
- Fourteenth Amendment (takings clause)
- Americans with Disabilities Act
- Age Discrimination in Employment
- Aid to Families with Dependent Children provisions of the Social Security Act, plus amendments
- Clean Air, plus amendments
- Administrative Procedure, or Administrative Orders Review
- Atomic Energy
- Bankruptcy Code, Bankruptcy Act or Rules, or Bankruptcy Reform Act of 1978
- Medicaid provisions of the Social Security Act
- Medicare provisions of the Social Security Act
- Clayton
- Reconstruction Civil Rights Acts (42 U.S.C. § 1978)
- Reconstruction Civil Rights Acts (42 U.S.C. § 1981)
- Reconstruction Civil Rights Acts (42 U.S.C. § 1982)
- Reconstruction Civil Rights Acts (42 U.S.C. § 1983)
- Reconstruction Civil Rights Acts (42 U.S.C. § 1985)
- Reconstruction Civil Rights Acts (42 U.S.C. § 1986)
- Civil Rights Act of 1964 (public accommodations)
- Civil Rights Act of 1957
- Civil Rights Act of 1991
- Statutory provisions of the District of Columbia
- Equal Access to Justice
- Education Amendments of 1972
- Employee Retirement Income Security, as amended
- Elementary and Secondary Education
- Federal False Claims
- Communication Act of 1934, as amended
- Federal Employees' Compensation
- Civil Rights Attorney's Fees Awards
- Federal Employers' Liability, as amended
- Federal Election Campaign
- Family Educational Rights and Privacy (Buckley Amendment)
- Federal Food, Drug, and Cosmetic, and related statutes
- Federal Insecticide, Fungicide, and Rodenticide
- Fair Labor Standards

- Freedom of Information, Sunshine, or Privacy Act
- Federal Power
- Federal Trade Commission
- Federal Water Pollution Control (Clean Water), plus amendments
- Omnibus Crime Control and Safe Streets, National Firearms, Organized Crime Control, Comprehensive Crime Control, or Gun Control Acts
- Education of the Handicapped, Education for All Handicapped Children, or Individuals with Disabilities Education Acts, or related statutes, as amended
- 28 U.S.C. § 2241-2255 (habeas corpus)
- Fair Housing
- Interstate Commerce, as amended
- Immigration and Naturalization, Immigration, Nationality, or Illegal Immigration Reform and Immigrant Responsibility Acts, as amended
- Internal Revenue Code and pre-IRC revenue acts
- Internal Security (also see 369)
- Jencks
- Jones, or Death on the High Seas
- Longshoremen and Harbor Workers' Compensation
- Labor-Management Relations
- Labor-Management Reporting and Disclosure
- Motor Carrier
- Miller
- National Environmental Policy
- Natural Gas, or Natural Gas Policy Acts
- National Labor Relations, as amended
- Norris-LaGuardia
- Occupational Safety and Health
- Public Utility Regulatory Policy
- Rehabilitation
- Religious Freedom Restoration
- Racketeer Influenced and Corrupt Organizations
- Railway Labor
- Robinson-Patman
- Securities Act of 1933, the Securities and Exchange Act of 1934, or the Williams Act
- Selective Service, Military Selective Service, or Universal Military Service and Training Acts
- Sherman
- Submerged Lands Acts
- Smith, Subversive Activities Control, Communist Control, or other similar federal legislation (also see 346)
- Social Security, as amended, including Social Security Disability Benefits Reform Act
- Supplemental Security Income
- State Law
- Truth in Lending
- Federal Tort Claims, or Alien Tort Statute
- Tucker
- Trading with the Enemy Act, as amended
- Universal Code of Military Justice
- Voting Rights Act of 1965, plus amendments

- Reconstruction Civil Rights Acts (42 U.S.C. § 1971)
- Reconstruction Civil Rights Acts (42 U.S.C. § 1999)
- Civil Rights Act of 1964 (Title II)
- Civil Rights Act of 1964 (Title IV)
- Civil Rights Act of 1964 (other)
- Civil Rights Act of 1964 (Title VII)
- Civil Rights Act of 1964 (Title IX)
- Civil Rights Act of 1964 (Title VI)
- Federal Arbitration Act
- Judiciary Act of 1789
- Federal Rules of Civil Procedure, including Appellate Procedure, or relevant rules of a circuit court Judicial Code, and admiralty rules
- Federal Rules of Criminal Procedure, or relevant rules of a circuit court
- Federal Rules of Evidence
- Supreme Court Rules
- Abstention Doctrine
- Retroactive application of a constitutional right
- Exclusionary Rule (Fourth Amendment)
- Exclusionary Rule (Right to Counsel)
- Exclusionary Rule (Miranda warnings)
- Harmless Error
- Res Judicata
- Estoppel
- Writ Improvidently Granted
- Treaty
- Interstate Compact
- Executive Order
- Territory Statute
- International Law
- Emergency Price Control
- Infrequently litigated statutes
- State or Local Law Regulation
- No Legal Provision

## A23 varNaturalCourt

*116 Distinct Values*

varNaturalCourt is used in conjunction with: *naturalCourt*

- Jay 1
- Jay 2
- Jay 3
- Jay 4

- Rutledge 1
- No Chief (Post-Rutledge)
- Ellsworth 1
- Ellsworth 2
- Ellsworth 3
- Marshall 1
- Marshall 2
- Marshall 3
- Marshall 4
- Marshall 5
- Marshall 6
- Marshall 7
- Marshall 8
- Marshall 9
- Marshall 10
- Taney 1
- Taney 2
- Taney 3
- Taney 4
- Taney 5
- Taney 6
- Taney 7
- Taney 8
- Taney 9
- Taney 10
- Taney 11
- Taney 12
- Taney 13
- Taney 14
- Taney 15
- Chase 1
- Chase 2
- Chase 3
- Waite 1
- Waite 2
- Waite 3
- Waite 4
- Waite 5
- Waite 6
- Waite 7
- Fuller 1
- Fuller 2
- Fuller 3
- Fuller 4
- Fuller 5
- Fuller 6
- Fuller 7
- Fuller 8

- Fuller 9
- Fuller 10
- Fuller 11
- Fuller 12
- No Chief (Post-Fuller)
- White 1
- White 2
- White 3
- White 4
- White 5
- Taft 1
- Taft 2
- Taft 3
- Taft 4
- Taft 5
- Hughes 1 Hughes 2
- Hughes 3
- Hughes 4
- Hughes 5
- Hughes 6
- Hughes 7
- Hughes 8
- Stone 1
- Stone 2
- Stone 3
- Vinson 1
- Vinson 2
- Vinson 3
- Warren 1
- Warren 2
- Warren 3
- Warren 4
- Warren 5
- Warren 6
- Warren 7
- Warren 8
- Warren 9
- Warren 10
- Warren 11
- Burger 1
- Burger 2
- Burger 3
- Burger 4
- Burger 5
- Burger 6
- Burger 7
- Rehnquist 1

- Rehnquist 2
- Rehnquist 3
- Rehnquist 4 Rehnquist 5
- Rehnquist 6
- Rehnquist 7
- Roberts 1
- Roberts 2
- Roberts 3
- Roberts 4
- Roberts 5
- Roberts 6
- Roberts 7
- Roberts 8
- Roberts 9
- Roberts 10

## A24 varParties

*311 Distinct Values*

varParties is used in conjunction with: *petitioner respondent*

- attorney general of the United States, or his office
- specified state board or department of education
- city, town, township, village, or borough government or governmental unit
- state commission, board, committee, or authority
- county government or county governmental unit, except school district
- court or judicial district
- state department or agency
- governmental employee or job applicant
- female governmental employee or job applicant
- minority governmental employee or job applicant
- minority female governmental employee or job applicant
- not listed among agencies in the first Administrative Action variable
- retired or former governmental employee
- U.S. House of Representatives
- interstate compact
- judge
- state legislature, house, or committee
- local governmental unit other than a county, city, town, township, village, or borough
- governmental official, or an official of an agency established under an interstate compact

- state or U.S. supreme court
- local school district or board of education
- U.S. Senate
- U.S. senator
- foreign nation or instrumentality
- state or local governmental taxpayer, or executor of the estate of
- state college or university
- United States
- State
- person accused, indicted, or suspected of crime
- advertising business or agency
- agent, fiduciary, trustee, or executor
- airplane manufacturer, or manufacturer of parts of airplanes
- airline
- distributor, importer, or exporter of alcoholic beverages
- alien, person subject to a denaturalization proceeding, or one whose citizenship is revoked
- American Medical Association
- National Railroad Passenger Corp.
- amusement establishment, or recreational facility
- arrested person, or pretrial detainee
- attorney, or person acting as such;includes bar applicant or law student, or law firm or bar association
- author, copyright holder
- bank, savings and loan, credit union, investment company
- bankrupt person or business, or business in reorganization
- establishment serving liquor by the glass, or package liquor store
- water transportation, stevedore
- bookstore, newsstand, printer, bindery, purveyor or distributor of books or magazines
- brewery, distillery
- broker, stock exchange, investment or securities firm
- construction industry
- bus or motorized passenger transportation vehicle
- business, corporation
- buyer, purchaser
- cable TV
- car dealer
- person convicted of crime
- tangible property, other than real estate, including contraband
- chemical company
- child, children, including adopted or illegitimate
- religious organization, institution, or person
- private club or facility
- coal company or coal mine operator
- computer business or manufacturer, hardware or software
- consumer, consumer organization
- creditor, including institution appearing as such; e.g., a finance company
- person allegedly criminally insane or mentally incompetent to stand trial

- defendant
- debtor
- real estate developer
- disabled person or disability benefit claimant
- distributor
- person subject to selective service, including conscientious objector
- drug manufacturer
- druggist, pharmacist, pharmacy
- employee, or job applicant, including beneficiaries of
- employer-employee trust agreement, employee health and welfare fund, or multiemployer pension plan
- electric equipment manufacturer
- electric or hydroelectric power utility, power cooperative, or gas and electric company
- eleemosynary institution or person
- environmental organization
- employer. If employer's relations with employees are governed by the nature of the employer's business (e.g., railroad, boat), rather than labor law generally, the more specific designation is used in place of Employer.
- farmer, farm worker, or farm organization
- father
- female employee or job applicant
- female
- movie, play, pictorial representation, theatrical production, actor, or exhibitor or distributor of
- fisherman or fishing company
- food, meat packing, or processing company, stockyard
- foreign (non-American) nongovernmental entity
- franchiser
- franchisee
- lesbian, gay, bisexual, transexual person or organization
- person who guarantees another's obligations
- handicapped individual, or organization of devoted to
- health organization or person, nursing home, medical clinic or laboratory, chiropractor
- heir, or beneficiary, or person so claiming to be
- hospital, medical center
- husband, or ex-husband
- involuntarily committed mental patient
- Indian, including Indian tribe or nation
- insurance company, or surety
- inventor, patent assigner, trademark owner or holder
- investor
- injured person or legal entity, nonphysically and non-employment related
- juvenile
- government contractor
- holder of a license or permit, or applicant therefor
- magazine
- male
- medical or Medicaid claimant
- medical supply or manufacturing co.

- racial or ethnic minority employee or job applicant
- minority female employee or job applicant
- manufacturer
- management, executive officer, or director, of business entity
- military personnel, or dependent of, including reservist
- mining company or miner, excluding coal, oil, or pipeline company
- mother
- auto manufacturer
- newspaper, newsletter, journal of opinion, news service
- radio and television network, except cable tv
- nonprofit organization or business
- nonresident
- nuclear power plant or facility
- owner, landlord, or claimant to ownership, fee interest, or possession of land as well as chattels
- shareholders to whom a tender offer is made
- tender offer
- oil company, or natural gas producer
- elderly person, or organization dedicated to the elderly
- out of state noncriminal defendant
- political action committee
- parent or parents
- parking lot or service
- patient of a health professional
- telephone, telecommunications, or telegraph company
- physician, MD or DO, dentist, or medical society
- public interest organization
- physically injured person, including wrongful death, who is not an employee
- pipe line company
- package, luggage, container
- political candidate, activist, committee, party, party member, organization, or elected official
- indigent, needy, welfare recipient
- indigent defendant
- private person
- prisoner, inmate of penal institution
- professional organization, business, or person
- probationer, or parolee
- protester, demonstrator, picketer or pamphleteer (non-employment related), or nonindigent loiterer
- public utility
- publisher, publishing company
- radio station
- racial or ethnic minority
- person or organization protesting racial or ethnic segregation or discrimination
- racial or ethnic minority student or applicant for admission to an educational institution
- realtor
- journalist, columnist, member of the news media

- resident
- restaurant, food vendor
- retarded person, or mental incompetent
- retired or former employee
- railroad
- private school, college, or university
- seller or vendor
- shipper, including importer and exporter
- shopping center, mall
- spouse, or former spouse
- stockholder, shareholder, or bondholder
- retail business or outlet
- student, or applicant for admission to an educational institution
- taxpayer or executor of taxpayer's estate, federal only
- tenant or lessee
- theater, studio
- forest products, lumber, or logging company
- person traveling or wishing to travel abroad, or overseas travel agent
- trucking company, or motor carrier
- television station
- union member
- unemployed person or unemployment compensation applicant or claimant
- union, labor organization, or official of
- veteran
- voter, prospective voter, elector, or a nonelective official seeking reapportionment or redistricting of legislative districts (POL)
- wholesale trade
- wife, or ex-wife
- witness, or person under subpoena
- network
- slave
- slave-owner
- bank of the united states
- timber company
- u.s. job applicants or employees
- Army and Air Force Exchange Service
- Atomic Energy Commission
- Secretary or administrative unit or personnel of the U.S. Air Force
- Department or Secretary of Agriculture
- Alien Property Custodian
- Secretary or administrative unit or personnel of the U.S. Army
- Board of Immigration Appeals
- Bureau of Indian Affairs
- Bonneville Power Administration
- Benefits Review Board
- Civil Aeronautics Board
- Bureau of the Census
- Central Intelligence Agency

- Commodity Futures Trading Commission
- Department or Secretary of Commerce
- Comptroller of Currency
- Consumer Product Safety Commission
- Civil Rights Commission
- Civil Service Commission, U.S.
- Customs Service or Commissioner of Customs
- Defense Base Closure and REalignment Commission
- Drug Enforcement Agency
- Department or Secretary of Defense (and Department or Secretary of War)
- Department or Secretary of Energy
- Department or Secretary of the Interior
- Department of Justice or Attorney General
- Department or Secretary of State
- Department or Secretary of Transportation
- Department or Secretary of Education
- U.S. Employees' Compensation Commission, or Commissioner
- Equal Employment Opportunity Commission
- Environmental Protection Agency or Administrator
- Federal Aviation Agency or Administration
- Federal Bureau of Investigation or Director
- Federal Bureau of Prisons
- Farm Credit Administration
- Federal Communications Commission (including a predecessor, Federal Radio Commission)
- Federal Credit Union Administration
- Food and Drug Administration
- Federal Deposit Insurance Corporation
- Federal Energy Administration
- Federal Election Commission
- Federal Energy Regulatory Commission
- Federal Housing Administration
- Federal Home Loan Bank Board
- Federal Labor Relations Authority
- Federal Maritime Board
- Federal Maritime Commission
- Farmers Home Administration
- Federal Parole Board
- Federal Power Commission
- Federal Railroad Administration
- Federal Reserve Board of Governors
- Federal Reserve System
- Federal Savings and Loan Insurance Corporation
- Federal Trade Commission
- Federal Works Administration, or Administrator
- General Accounting Office
- Comptroller General
- General Services Administration

- Department or Secretary of Health, Education and Welfare
- Department or Secretary of Health and Human Services
- Department or Secretary of Housing and Urban Development
- Interstate Commerce Commission
- Indian Claims Commission
- Immigration and Naturalization Service, or Director of, or District Director of, or Immigration and Naturalization Enforcement
- Internal Revenue Service, Collector, Commissioner, or District Director of
- Information Security Oversight Office
- Department or Secretary of Labor
- Loyalty Review Board
- Legal Services Corporation
- Merit Systems Protection Board
- Multistate Tax Commission
- National Aeronautics and Space Administration
- Secretary or administrative unit of the U.S. Navy
- National Credit Union Administration
- National Endowment for the Arts
- National Enforcement Commission
- National Highway Traffic Safety Administration
- National Labor Relations Board, or regional office or officer
- National Mediation Board
- National Railroad Adjustment Board
- Nuclear Regulatory Commission
- National Security Agency
- Office of Economic Opportunity
- Office of Management and Budget
- Office of Price Administration, or Price Administrator
- Office of Personnel Management
- Occupational Safety and Health Administration
- Occupational Safety and Health Review Commission
- Office of Workers' Compensation Programs
- Patent Office, or Commissioner of, or Board of Appeals of
- Pay Board (established under the Economic Stabilization Act of 1970)
- Pension Benefit Guaranty Corporation
- U.S. Public Health Service
- Postal Rate Commission
- Provider Reimbursement Review Board
- Renegotiation Board
- Railroad Adjustment Board
- Railroad Retirement Board
- Subversive Activities Control Board
- Small Business Administration
- Securities and Exchange Commission
- Social Security Administration or Commissioner
- Selective Service System
- Department or Secretary of the Treasury
- Tennessee Valley Authority

- 410 United States Forest Service
- 411 United States Parole Commission
- 412 Postal Service and Post Office, or Postmaster General, or Postmaster
- 413 United States Sentencing Commission
- 414 Veterans' Administration
- 415 War Production Board
- 416 Wage Stabilization Board
- 417 General Land Office of Commissioners
- 418 Transportation Security Administration
- 419 Surface Transportation Board
- 420 U.S. Shipping Board Emergency Fleet Corp.
- 421 Reconstruction Finance Corp.
- 422 Department or Secretary of Homeland Security
- 501 Unidentifiable
- 600 International Entity

## A25 varPartyWinning

*3 Distinct Values*

varPartyWinning is used in conjunction with: *partyWinning*

#### **Values:**

- 0 no favorable disposition for petitioning party apparent
- 1 petitioning party received a favorable disposition
- 2 favorable disposition for petitioning party unclear

## A26 varPrecedentAlteration

*2 Distinct Values*

varPrecedentAlteration is used in conjunction with: *precedentAlteration*

#### **Values:**

- 0 no determinable alteration of precedent
- 1 precedent altered

## A27 varSplitVote

*2 Distinct Values*

varSplitVote is used in conjunction with:

#### *splitVote*

#### **Values:**

- first vote on issue/legal provision
- second vote on issue/legal provision

## A28 varStates

*64 Distinct Values*

varStates is used in conjunction with: *petitionerState respondentState adminActionState caseOriginState caseSourceState*

- Alabama
- Alaska
- American Samoa
- Arizona
- Arkansas
- California
- Colorado
- Connecticut
- Delaware
- District of Columbia
- Federated States of Micronesia
- Florida
- Georgia
- Guam
- Hawaii
- Idaho
- Illinois
- Indiana
- Iowa
- Kansas
- Kentucky
- Louisiana
- Maine
- Marshall Islands
- Maryland
- Massachusetts
- Michigan
- Minnesota

- Mississippi
- Missouri
- Montana
- Nebraska
- Nevada
- New Hampshire
- New Jersey
- New Mexico
- New York
- North Carolina
- North Dakota
- Northern Mariana Islands
- Ohio
- Oklahoma
- Oregon
- Palau
- Pennsylvania
- Puerto Rico
- Rhode Island
- South Carolina
- South Dakota
- Tennessee
- Texas
- Utah
- Vermont
- Virgin Islands
- Virginia
- Washington
- West Virginia
- Wisconsin
- Wyoming
- United States
- Interstate Compact
- Philippines
- Indian
- Dakota

## A29 varThreeJudgeFdc

*2 Distinct Values*

varThreeJudgeFdc is used in conjunction with: *threeJudgeFdc*

#### **Values:**

no mention that a 3-judge ct heard case

1 3-judge district ct heard case

## A30 varVote

*8 Distinct Values*

varVote is used in conjunction with: *vote*

#### **Values:**

- 1 voted with majority or plurality
- 2 dissent
- 3 regular concurrence
- 4 special concurrence
- 5 judgment of the Court
- 6 dissent from a denial or dismissal of certiorari , or dissent from summary affirmation of an appeal
- 7 jurisdictional dissent
- 8 justice participated in an equally divided vote

## A31 varVoteUnclear

*2 Distinct Values*

varVoteUnclear is used in conjunction with: *voteUnclear*

- 0 vote clearly specified
- 1 the vote in the case not clear