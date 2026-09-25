<!--
  Kashyap Nasit — profile README.
  Every visual is a hand-built, animated SVG in /assets/readme: no JavaScript, fonts embedded, GitHub-safe.
-->

<div align="center">

<a href="https://kashyap-portfolio-site.vercel.app/">
  <img src="./assets/readme/hero.svg" width="100%" alt="Kashyap Nasit — computer science undergraduate from Surat, India. Engineering clarity from complexity. Field notes: lost a week to one wrong denominator, now audits every fraction; simulates the silicon lottery for fun but hasn't won a real one; converts chai into confidence scores; believes every messy dataset is just a shy database."/>
</a>

<br/>

<a href="https://kashyap-portfolio-site.vercel.app/"><img src="./assets/readme/btn-portfolio.svg" width="23%" alt="Portfolio"/></a>
<a href="https://www.linkedin.com/in/kashyap-nasit-5240b3341/"><img src="./assets/readme/btn-linkedin.svg" width="23%" alt="LinkedIn"/></a>
<a href="https://leetcode.com/u/Kashyap_Nasit_2007/"><img src="./assets/readme/btn-leetcode.svg" width="23%" alt="LeetCode"/></a>
<a href="mailto:kashyapnasit12345@gmail.com"><img src="./assets/readme/btn-email.svg" width="23%" alt="Email"/></a>

</div>

<br/><br/>

<img src="./assets/readme/sec-01-thesis.svg" width="100%" alt="I. Thesis — chaos is just order we haven't simulated yet"/>

<img src="./assets/readme/thesis.svg" width="100%" alt="A rotating 3D Lorenz attractor. The Lorenz system, 1963: dx/dt = σ(y − x), dy/dt = x(ρ − z) − y, dz/dt = xy − βz. Deterministic rules, unpredictable outcomes. Simulate them and chaos turns legible — find the rules underneath the noise."/>

<br/><br/>

<img src="./assets/readme/sec-02-manifest.svg" width="100%" alt="II. Manifest — how I think about engineering"/>

<img src="./assets/readme/about.svg" width="100%" alt="Every system hides a story. I enjoy discovering how it works, why it breaks, and how it can become better. Driven by curiosity, guided by understanding, defined by creation. whoami: kashyap-nasit, CS undergrad. Role: engineer-in-progress. Focus: AI, data, systems. Location: Surat, Gujarat, India. CGPA 7.71/10. Mission: engineering clarity from complexity."/>

<br/><br/>

<img src="./assets/readme/sec-03-systems.svg" width="100%" alt="III. Systems — not projects, engineered answers to specific questions"/>

<p align="center">
  <a href="https://github.com/kashyapnasit109/Nexus"><img src="./assets/readme/card-01-nexus.svg" width="49%" alt="No. 01 Nexus — attendance intelligence from a photo of a timetable. OCR, Gemini Flash, Node.js, MongoDB."/></a>
  <a href="https://github.com/kashyapnasit109/DOQ_KB"><img src="./assets/readme/card-02-doq.svg" width="49%" alt="No. 02 DOQ — construction intelligence: scattered invoices, PDFs and field updates into one structured source of truth. Next.js, LLM agents, PDF parsing, MongoDB. Active development."/></a>
</p>
<p align="center">
  <a href="https://github.com/kashyapnasit109/Silicon-Lottery"><img src="./assets/readme/card-03-wafer.svg" width="49%" alt="No. 03 Silicon Lottery — simulating manufacturing variance and chip binning. TypeScript, simulation, computer architecture."/></a>
  <img src="./assets/readme/card-04-db.svg" width="49%" alt="No. 04 Healthcare Management System — a database layer built for concurrent multi-module use. SQL, schema design, query optimization."/>
</p>
<p align="center">
  <img src="./assets/readme/card-05-ev.svg" width="49%" alt="No. 05 EV Analytics — India's EV market, cleaned and modeled in Power BI. Power BI, DAX, data modeling."/>
  <a href="https://kashyap-portfolio-site.vercel.app/"><img src="./assets/readme/card-06-web.svg" width="49%" alt="No. 06 Personal Portfolio — built from scratch, not templated. HTML, CSS, JavaScript, Vercel."/></a>
</p>

<details>
<summary><b>No. 01 — Nexus · field notes</b></summary>
<br/>

> **Question** — Can attendance be logged accurately from a photo of a timetable, without manual entry?
>
> **Architecture** — Timetable and attendance-sheet images pass through OCR to extract raw text, which is then interpreted by the Gemini Flash API to identify students, subjects and presence — producing structured records stored in MongoDB.
>
> **Engineering challenges** — Timetable layouts vary significantly across classes, which initially broke OCR parsing; the extraction logic had to be made layout-agnostic. A separate bug in the AI-generated attendance-percentage logic used an incorrect denominator, silently distorting results until it was traced and corrected.
>
> **Outcome** — A working pipeline that turns unstructured classroom documents into reliable, queryable attendance data.
>
> `Gemini Flash API` `OCR` `Node.js` `MongoDB` · [repository →](https://github.com/kashyapnasit109/Nexus)

</details>

<details>
<summary><b>No. 02 — DOQ — Construction Intelligence Platform · field notes</b></summary>
<br/>

> **Question** — Can raw financial documents and informal site updates be turned into structured operational knowledge?
>
> **Architecture** — Transaction PDFs are auto-parsed into a structured database with an AI chatbot layered on top for querying. An LLM-driven ingestion pipeline is being built to read WhatsApp and Telegram messages from site workers and convert them into structured progress records, with human review for low-confidence extractions.
>
> **Engineering challenges** — Informal, inconsistent field messages (typos, mixed language, shorthand) resist naive parsing — the pipeline needs a confidence-scoring layer rather than a binary parse/fail approach.
>
> **Outcome** — A construction management platform where financial and operational data flow into one structured system instead of scattered documents and chat threads. *Currently under active development.*
>
> **Roadmap** — WhatsApp integration · Telegram integration · Multi-agent extraction pipeline
>
> `Next.js` `LLM Agents` `PDF Parsing` `MongoDB` · [repository →](https://github.com/kashyapnasit109/DOQ_KB)

</details>

<details>
<summary><b>No. 03 — Silicon Lottery · field notes</b></summary>
<br/>

> **Question** — Why do two chips from the same production line perform differently?
>
> **Architecture** — A Computer Organization & Architecture project simulating manufacturing variance in processor dies, and modeling how that variance produces the real-world phenomenon of chip binning.
>
> **Outcome** — A working explanation, backed by simulation, of why hardware yield and overclocking headroom aren't uniform even within the same silicon batch.
>
> `Computer Architecture` `Simulation` `TypeScript` · [repository →](https://github.com/kashyapnasit109/Silicon-Lottery)

</details>

<details>
<summary><b>No. 04 — Healthcare Management System · field notes</b></summary>
<br/>

> **Question** — How do you design a database layer that stays reliable as multiple modules read and write against it concurrently?
>
> **Architecture** — A collaborative 4-person build; I owned schema design, query optimization and data integrity for the system's core workflows.
>
> **Outcome** — A functioning healthcare management system with a database layer built to hold up under real multi-module usage.
>
> `SQL` `Database Design`

</details>

<details>
<summary><b>No. 05 — EV Analytics — Indian Market · field notes</b></summary>
<br/>

> **Question** — What do adoption and performance trends across India's EV market actually look like once the noise is cleaned out?
>
> **Architecture** — Raw EV datasets cleaned and modeled, then visualized in an interactive Power BI dashboard covering range, charging behavior and market growth.
>
> **Outcome** — A dashboard that turns a messy public dataset into a clear, explorable view of the Indian EV landscape. Built for a data science course.
>
> `Power BI` `Data Modeling` `DAX`

</details>

<details>
<summary><b>No. 06 — Personal Portfolio · field notes</b></summary>
<br/>

> **Question** — What's the simplest, fastest way to represent my work without relying on a template?
>
> **Architecture** — A responsive site built from scratch to showcase projects and background.
>
> **Outcome** — My own space on the internet, built rather than templated.
>
> `HTML` `CSS` `JavaScript` · [live site →](https://kashyap-portfolio-site.vercel.app/) · [repository →](https://github.com/kashyapnasit109/Personal_Portfolio)

</details>

<sub>Also shipped: <a href="https://github.com/kashyapnasit109/forage-midas">forage-midas</a> — JPMorgan Chase Advanced Software Engineering program (Forage), in Java.</sub>

<br/><br/>

<img src="./assets/readme/sec-04-method.svg" width="100%" alt="IV. Method — the one shape all my work shares"/>

<img src="./assets/readme/method.svg" width="100%" alt="Entropy to structure: scattered particles pass through a lens and settle into an ordered lattice. Unstructured signal in, structured knowledge out — the same shape in Nexus, DOQ and EV Analytics."/>

<br/><br/>

<img src="./assets/readme/sec-05-craft.svg" width="100%" alt="V. Craft — the instruments behind the systems"/>

<img src="./assets/readme/craft.svg" width="100%" alt="Languages: C, C++, Java, Python, JavaScript, TypeScript, PHP, SQL. Backend: Node.js, Express, Next.js, MongoDB, MySQL, REST APIs, Git. Applied AI: LLM agents, OCR pipelines, Gemini API, machine learning, scikit-learn. Data: Pandas, NumPy, Matplotlib, Streamlit, Power BI, DAX. Domains: system design, computer networks, computer architecture, business analytics, AI/ML."/>

<img src="./assets/readme/marquee.svg" width="100%" alt="Tools: Python, C++, Java, JavaScript, TypeScript, Node.js, Express, Next.js, MongoDB, MySQL, Gemini, scikit-learn, Pandas, NumPy, Streamlit, PHP, Git, Vercel"/>

<br/><br/>

<img src="./assets/readme/sec-06-inquiry.svg" width="100%" alt="VI. Inquiry — open questions, and where my attention orbits"/>

<img src="./assets/readme/questions.svg" width="100%" alt="Open questions. Q1: What makes a parser truly layout-agnostic? (raised by Nexus) Q2: How should a pipeline behave when it is only partly sure? (raised by DOQ) Q3: Can many small agents read a messy message better than one large one? (raised by DOQ's roadmap)"/>

<img src="./assets/readme/orbit.svg" width="100%" alt="Currently exploring: OCR pipelines, Gemini API, LLM agents, confidence scoring, data engineering, multi-agent extraction, system design, conversational data, machine learning."/>

<br/><br/>

<img src="./assets/readme/sec-07-signal.svg" width="100%" alt="VII. Signal — activity, streaks and deliberate practice"/>

<div align="center">

<img src="https://github-readme-stats.vercel.app/api?username=kashyapnasit109&show_icons=true&include_all_commits=true&hide_border=true&bg_color=0C0C13&title_color=B9B1FF&icon_color=5EEAD4&text_color=B6B6C8&ring_color=8B7CF6&border_radius=16" height="170" alt="GitHub stats"/>
<img src="https://streak-stats.demolab.com?user=kashyapnasit109&hide_border=true&border_radius=16&background=0C0C13&stroke=1D1D2A&ring=8B7CF6&fire=5EEAD4&currStreakNum=ECECF4&sideNums=ECECF4&currStreakLabel=B9B1FF&sideLabels=B6B6C8&dates=8A8AA0" height="170" alt="Contribution streak"/>

<img src="https://github-readme-activity-graph.vercel.app/graph?username=kashyapnasit109&bg_color=0C0C13&color=B6B6C8&line=8B7CF6&point=5EEAD4&area=true&area_color=8B7CF6&hide_border=true&radius=16&custom_title=Contribution%20signal" width="100%" alt="Contribution activity graph"/>

<img src="https://raw.githubusercontent.com/kashyapnasit109/kashyapnasit109/output/snake-dark.svg" width="100%" alt="Contribution snake"/>

<a href="https://leetcode.com/u/Kashyap_Nasit_2007/"><img src="https://leetcard.jacoblin.cool/Kashyap_Nasit_2007?theme=dark&font=JetBrains%20Mono&ext=heatmap&border=0&radius=16" width="60%" alt="LeetCode stats"/></a>

<br/><br/>

<img src="https://komarev.com/ghpvc/?username=kashyapnasit109&style=flat-square&color=8B7CF6&label=PROFILE+VIEWS" alt="Profile views"/>

</div>

<br/>

<img src="./assets/readme/footer.svg" width="100%" alt="If you can simulate it, you can master it. — Kashyap Nasit, Surat, India. Built from scratch, no template."/>
