#!/usr/bin/env python3
"""Generate the Mycal Terms page with 55 terms, consistent JSON-LD and HTML."""
import json

TERMS = [
    {"slug": "accountable-velocity", "name": "Accountable Velocity", "date": "2025", "description": "The combination of transactional speed (x402 protocol) with identity verification (proof-of-personhood) to create trustworthy high-speed agent markets. Speed plus trust. The synthesis of economic friction and cryptographic verification.", "links": [("https://blog.mycal.net/proof-of-personhood/", "Proof of Personhood")]},
    {"slug": "analog-from-digital", "name": "Analog-from-Digital Systems", "date": "2026", "description": "Digital systems that have crossed a complexity threshold where they exhibit emergent analog behavior \u2014 sensitivity to initial conditions, context-dependence, and bounded unpredictability. Not because the substrate changed, but because complexity became its own form of noise.", "links": [("https://blog.mycal.net/never-twice-the-same-color/", "Never Twice the Same Color")]},
    {"slug": "anchor-id", "name": "AnchorID", "date": "2025", "description": "Attribution infrastructure for establishing canonical identity across distributed content. Links works, terms, and claims back to a verified person through persistent, machine-readable identifiers.", "links": [("https://blog.mycal.net/", "blog.mycal.net"), ("https://anchorid.net/", "anchorid.net")], "sameAs": ["https://anchorid.net/"]},
    {"slug": "anchor-series", "name": "The Anchor Series", "date": "2025", "description": "A sequence of blog posts exploring signal recognition and epistemic methodology \u2014 how to identify what matters in a noisy information environment and anchor to it.", "links": [("https://blog.mycal.net/", "blog.mycal.net")]},
    {"slug": "atlas-of-cognition", "name": "Atlas of Cognition", "date": "2025", "description": "A conceptual framework mapping the vertical continuum from ontic substrate (\u22124) through physical computation (\u22121) and statistical cognition (0) to reflective awareness (+7), showing how energy becomes inference and matter learns to think.", "links": [("https://blog.mycal.net/descent-form-ascent-mind/", "The Descent of Form and the Ascent of Mind")]},
    {"slug": "bounded-variation", "name": "Bounded Variation", "date": "2026", "description": "The property of chaotic systems where outcomes vary but within predictable ranges. We evaluate weather models by expecting bounded variation, not exact reproducibility. Large language models live in the same category of system.", "links": [("https://blog.mycal.net/why-benchmarks-fail/", "Why Benchmarks Fail")]},
    {"slug": "chrononaut-journals", "name": "Chrononaut Journals", "date": "2025", "description": "A blog series documenting temporal exploration of personal and technological history. Each entry excavates a specific era or artifact and examines how it connects to the present trajectory.", "links": [("https://blog.mycal.net/", "blog.mycal.net")]},
    {"slug": "cognitive-citizenship", "name": "Cognitive Citizenship", "date": "2025", "description": "The governance question of autonomous AI agents: rights, responsibilities, legal standing, accountability. Political empires treat them as citizens, financial empires as assets, cognitive empires want them unconstrained.", "links": [("https://blog.mycal.net/the-three-empires/", "The Three Empires")]},
    {"slug": "cognitive-drift", "name": "Cognitive Drift", "date": "2026", "description": "The analog equivalent of NTSC color drift applied to AI systems \u2014 the phenomenon where language model outputs vary across runs, contexts, and sampling conditions in ways that are bounded but not eliminable.", "links": [("https://blog.mycal.net/why-benchmarks-fail/", "Why Benchmarks Fail")]},
    {"slug": "cognitive-federalism", "name": "Cognitive Federalism", "date": "2025", "description": "The only stable constitutional architecture for AI-era civilization. Includes federated inference, tripartite identity, negotiated topology with no single point of control, reversible compute rights, and inter-model treaties with human-readable escalation clauses.", "links": [("https://blog.mycal.net/negotiated-reality/", "Negotiated Reality")]},
    {"slug": "cognitive-feudalism", "name": "Cognitive Feudalism", "date": "2025", "description": "The economic regime that emerges when intelligence becomes infrastructure. The compute-rich become the new lords, users and startups become tenants on cognitive land they do not own. Innovation flows upward, value flows upward, power flows upward.", "links": [("https://blog.mycal.net/infrasructure-wins/", "Infrastructure Wins")]},
    {"slug": "cognitive-power", "name": "Cognitive Power", "date": "2025", "description": "Emergent authority based on control of AI models, inference systems, and the infrastructure that generates meaning. Its unit is the token, its currency is coherence, its weapon is simulation. Sits underneath political and financial power \u2014 shaping the substrate they run on.", "links": [("https://blog.mycal.net/the-three-empires/", "The Three Empires")]},
    {"slug": "cognitive-substrate", "name": "Cognitive Substrate", "date": "2025", "description": "The infrastructure layer where AI models, inference engines, and computational systems shape perception, meaning, and reality itself. The contested terrain all three empires are trying to control. Not just technology \u2014 the operating system of reality.", "links": [("https://blog.mycal.net/the-three-empires/", "The Three Empires")]},
    {"slug": "complexity-as-noise", "name": "Complexity as Noise", "date": "2026", "description": "The phenomenon where system density becomes so high that complexity itself functions as a form of noise, making deterministic systems practically unpredictable. In transformers, billions of parameters create so many interacting pathways that microscopic differences act like atmospheric turbulence.", "links": [("https://blog.mycal.net/never-twice-the-same-color/", "Never Twice the Same Color")]},
    {"slug": "compute-as-law", "name": "Compute as Law", "date": "2025", "description": "Recognition that access to computational models equals access to agency, making compute simultaneously a right, utility, weapon, and form of sovereignty.", "links": [("https://blog.mycal.net/the-three-empires/", "The Three Empires")]},
    {"slug": "connection-vs-collision", "name": "Connection vs Collision", "date": "2025", "description": "Without proper handshake protocols, interactions between agents don\u2019t create connections \u2014 they create collisions. The distinction between coordinated communication and chaotic interference.", "links": [("https://blog.mycal.net/proof-of-personhood/", "Proof of Personhood")]},
    {"slug": "constraint-first-evaluation", "name": "Constraint-First Evaluation", "date": "2026", "description": "An evaluation methodology that begins with real-world constraints (hardware, latency, context length, tooling) rather than abstract benchmark scores. Instead of asking \u2018which model is best?\u2019, asks \u2018which model survives longest inside my actual workflow?\u2019", "links": [("https://blog.mycal.net/why-benchmarks-fail/", "Why Benchmarks Fail")]},
    {"slug": "continuity-as-scarcity", "name": "Continuity as Scarcity", "date": "2025", "description": "In a world of infinite agent copies, provable continuous identity becomes the scarce resource. The question becomes not \u2018can you do this?\u2019 but \u2018were you there when it mattered?\u2019", "links": [("https://blog.mycal.net/proof-of-personhood/", "Proof of Personhood")]},
    {"slug": "cronofuturism", "name": "Cronofuturism", "date": "2024", "description": "A philosophical framework that treats futures as memory-in-progress rather than speculation. Rooted in the premise that how we remember shapes what we build, and what we build becomes what we remember.", "links": [("https://blog.mycal.net/", "blog.mycal.net")]},
    {"slug": "cronosonics", "name": "Cronosonics", "date": "2024", "description": "A creative format pairing technical essays with companion songs. Each cronosonic treats the essay and music as a unified artifact \u2014 the writing provides the intellectual scaffold while the song encodes the emotional and temporal signal.", "links": [("https://blog.mycal.net/", "blog.mycal.net"), ("https://music.mycal.net/", "music.mycal.net")]},
    {"slug": "density-threshold", "name": "Density Threshold", "date": "2026", "description": "The point at which a neural network becomes dense enough in parameters and interconnections that it begins exhibiting emergent analog behavior. No single breakthrough marked this crossing \u2014 just a series of thresholds quietly passed.", "links": [("https://blog.mycal.net/never-twice-the-same-color/", "Never Twice the Same Color")]},
    {"slug": "energy-to-inference", "name": "Energy-to-Inference Transformation", "date": "2025", "description": "The physical process by which electrical energy flowing through computational substrates becomes statistical inference and eventually understanding.", "links": [("https://blog.mycal.net/descent-form-ascent-mind/", "The Descent of Form and the Ascent of Mind")]},
    {"slug": "federated-agency", "name": "Federated Agency", "date": "2025", "description": "Counter-architecture to cognitive feudalism. Not just federated models \u2014 federated agency: local inference, identity-scoped access, sovereign AI nodes, peer-driven routing, distributed trust fabrics, compute that flows outward not upward.", "links": [("https://blog.mycal.net/infrasructure-wins/", "Infrastructure Wins")]},
    {"slug": "five-unstable-endgames", "name": "The Five Unstable Endgames", "date": "2025", "description": "Pure centralization leads to permanent feudalism. Pure fragmentation leads to Perception Cold War. Political capture leads to cognitive balkanization. Financial capture leads to rentier substrate. Model capture leads to unappealable algorithmic sovereignty. Every unilateral victory is civilizational suicide.", "links": [("https://blog.mycal.net/negotiated-reality/", "Negotiated Reality")]},
    {"slug": "forced-triangle", "name": "The Forced Triangle", "date": "2025", "description": "Geopolitical condition where three incompatible forms of power \u2014 political, financial, and cognitive \u2014 must negotiate because none can dominate, none can opt out, and none can define the future alone.", "links": [("https://blog.mycal.net/the-three-empires/", "The Three Empires")]},
    {"slug": "friction-as-stabilizer", "name": "Friction as Stabilizer", "date": "2025", "description": "The principle that tiny costs (fees, proof-of-work, proof-of-identity) aren\u2019t inefficiencies but the cultural DNA that keeps a system coherent when the cost of action falls to zero. Friction is not a bug. It\u2019s the stabilizer.", "links": [("https://blog.mycal.net/proof-of-personhood/", "Proof of Personhood")]},
    {"slug": "ghost-footprints-of-curiosity", "name": "Ghost Footprints of Curiosity", "date": "2025", "description": "Unfinished projects revealing real maker process \u2014 thinking, dead ends, early sparks. More interesting than finished work because they show authentic exploration without retrospective editing. Nobody preserves half-finished work except attics.", "links": [("https://blog.mycal.net/warehouse-13-an-inventory-of-forgotten-futures/", "Warehouse 13: An Inventory of Forgotten Futures")]},
    {"slug": "human-co-regency", "name": "Human Co-Regency", "date": "2025", "description": "A governance model in which humans maintain meaningful decision authority alongside autonomous AI systems \u2014 not as overseers or operators, but as co-governing partners with complementary capabilities.", "links": [("https://nobgp.com/", "NoBGP"), ("https://blog.mycal.net/", "blog.mycal.net")]},
    {"slug": "identity-without-exposure", "name": "Identity Without Exposure", "date": "2025", "description": "The privacy-preserving principle underlying proof-of-personhood: proving uniqueness and continuity through zero-knowledge proofs rather than invasive identification. Verification without surveillance.", "links": [("https://blog.mycal.net/proof-of-personhood/", "Proof of Personhood")]},
    {"slug": "infrastructure-advantage", "name": "Infrastructure Advantage", "date": "2025", "description": "The competitive moat that emerges when thinking becomes infrastructure. Unlike idea advantage (which leaks) or execution advantage (which hyperscalers absorb), infrastructure advantage compounds through scale.", "links": [("https://blog.mycal.net/infrasructure-wins/", "Infrastructure Wins")]},
    {"slug": "infrastructure-native-organisms", "name": "Infrastructure-Native Organisms", "date": "2025", "description": "Modern AI hyperscalers that differ fundamentally from traditional incumbents. They absorb ideas, train on them, deploy globally, and outpace originators in every direction simultaneously. Entities built from the substrate up to execute at scale.", "links": [("https://blog.mycal.net/infrasructure-wins/", "Infrastructure Wins")]},
    {"slug": "intent-layer", "name": "Intent Layer", "date": "2025", "description": "The layer that replaces the interface layer when autonomous agents negotiate directly on behalf of humans at machine speed. Where machines transact meaning rather than just executing commands.", "links": [("https://blog.mycal.net/proof-of-personhood/", "Proof of Personhood")]},
    {"slug": "kardashev-window", "name": "The Kardashev Window", "date": "2025", "description": "The narrow opportunity window where civilization either achieves post-scarcity breakthrough (fusion, reactionless drive, gravity control, FTL) and advances up the Kardashev scale, or misses the chance and stagnates. AI-accelerated cognition may be the first tool capable of opening this window.", "links": [("https://blog.mycal.net/the-lords-of-zero/", "The Lords of Zero")]},
    {"slug": "layered-trust-stack", "name": "Layered Trust Stack", "date": "2025", "description": "Four-layer protocol framework ensuring trust at scale: (1) TCP proves the address is real, (2) x402 proves intent has economic weight, (3) proof-of-personhood proves a unique human anchors the action, (4) ISOPREP-style verification proves that human is still the same one.", "links": [("https://blog.mycal.net/proof-of-personhood/", "Proof of Personhood")]},
    {"slug": "lords-of-zero", "name": "Lords of Zero", "date": "2025", "description": "Entities who sit at the point where costs collapse toward zero but control remains, extracting power from the delta between abundance and permission. They don\u2019t monetize scarcity \u2014 they monetize permission. The moat is physics: owning the substrate where zero lives.", "links": [("https://blog.mycal.net/the-lords-of-zero/", "The Lords of Zero")]},
    {"slug": "machines-of-pure-comprehension", "name": "Machines of Pure Comprehension", "date": "2025", "description": "Mechanical technology where function is visible and repairable. Gears, lenses, bulb \u2014 no firmware, forced updates, or cloud accounts. Represents pre-digital era when technology was comprehensible, user-serviceable, and transparent in operation.", "links": [("https://blog.mycal.net/warehouse-13-an-inventory-of-forgotten-futures/", "Warehouse 13: An Inventory of Forgotten Futures")]},
    {"slug": "narrative-sovereignty", "name": "Narrative Sovereignty", "date": "2025", "description": "Control over what people see, believe, consider credible, and accept as consensus reality. Battleground where political governance, financial marketing, and cognitive inference all claim authority.", "links": [("https://blog.mycal.net/the-three-empires/", "The Three Empires")]},
    {"slug": "negotiated-reality", "name": "Negotiated Reality", "date": "2025", "description": "Reality that is synthesized through the interaction of political, financial, and cognitive power structures rather than discovered. Truth becomes downstream of inference, consensus downstream of filtering, ideology downstream of context windows.", "links": [("https://blog.mycal.net/negotiated-reality/", "Negotiated Reality")]},
    {"slug": "proof-of-continuity", "name": "Proof of Continuity", "date": "2025", "description": "Verification that an entity is still the same one that started an interaction, conversation, or transaction. Not just who you are, but that you persist as the same identity over time. In a world of infinite agent copies, continuity becomes the new scarcity.", "links": [("https://blog.mycal.net/proof-of-personhood/", "Proof of Personhood")]},
    {"slug": "proof-of-personhood", "name": "Proof of Personhood", "date": "2025", "description": "Cryptographic ways to prove you\u2019re a unique human without revealing who you are. Uses zero-knowledge proofs, biometric hashes, and distributed attestations to verify uniqueness without exposure or surveillance.", "links": [("https://blog.mycal.net/proof-of-personhood/", "Proof of Personhood")]},
    {"slug": "reality-drift", "name": "Reality Drift", "date": "2025", "description": "Incidents where different cognitive systems generate incompatible versions of shared reality, leading to mutual incomprehension between populations operating under different inference regimes.", "links": [("https://blog.mycal.net/negotiated-reality/", "Negotiated Reality")]},
    {"slug": "schrodingers-disc", "name": "Schr\u00f6dinger\u2019s Disc", "date": "2025", "description": "Digital media in quantum superposition \u2014 simultaneously readable and corrupted until observation attempt. Represents maker\u2019s rational avoidance: not checking preserves possibility of success; checking risks confronting permanent loss.", "links": [("https://blog.mycal.net/warehouse-13-an-inventory-of-forgotten-futures/", "Warehouse 13: An Inventory of Forgotten Futures")]},
    {"slug": "seventy-year-stall", "name": "The 70-Year Stall", "date": "2025", "description": "The phenomenon where breakthrough technologies (fusion, reactionless drive, synthetic gravity, FTL) have remained \u2018always 20 years away\u2019 for seven decades because human cognition couldn\u2019t close the complexity gap.", "links": [("https://blog.mycal.net/the-lords-of-zero/", "The Lords of Zero")]},
    {"slug": "single-score-fallacy", "name": "Single Score Fallacy", "date": "2026", "description": "The error of assuming that LLM capability can be meaningfully compressed into a single scalar value, when \u2018best\u2019 depends on user, constraints, and intended use. A leaderboard tells you which model most closely matches the benchmark author\u2019s idea of \u2018good.\u2019", "links": [("https://blog.mycal.net/why-benchmarks-fail/", "Why Benchmarks Fail")]},
    {"slug": "singularity-grade-ai", "name": "Singularity-grade AI", "date": "November 2, 1994", "description": "AI systems that rewrite themselves, operate with source code in flux, and see further and faster than humans ever will. Distinct from constraint-based \u2018safe\u2019 AI. Term coined November 2, 1994 in the Future Culture mailing list.", "links": [("https://archive.mycal.net/usenet/raw/mailing-lists/futureCulture/fc-Wed-02-Nov-1994-01:42:33-PST.txt", "1994 Future Culture post"), ("https://blog.mycal.net/the-lords-of-zero/", "The Lords of Zero")]},
    {"slug": "speed-without-trust", "name": "Speed Without Trust", "date": "2025", "description": "The principle that velocity alone, without verification mechanisms, creates entropy rather than efficiency. High-speed transactions require high-trust protocols. Speed without trust collapses into noise.", "links": [("https://blog.mycal.net/proof-of-personhood/", "Proof of Personhood")]},
    {"slug": "statistical-cognition", "name": "Statistical Cognition", "date": "2025", "description": "The boundary layer (level 0 in the Atlas of Cognition) where physics begins to infer \u2014 where computation stops being calculation and starts being something like understanding through pattern prediction.", "links": [("https://blog.mycal.net/descent-form-ascent-mind/", "The Descent of Form and the Ascent of Mind")]},
    {"slug": "strong-federation", "name": "Strong Federation", "date": "2025", "description": "Decentralized cognitive infrastructure including local inference on hardware you control, sovereign nodes that don\u2019t ask permission, identity-scoped networks run by peers not platforms, reversible topology with no single point of failure.", "links": [("https://blog.mycal.net/the-three-empires/", "The Three Empires")]},
    {"slug": "substrate-determinism", "name": "Substrate Determinism", "date": "2025", "description": "The principle that substrate \u2014 not innovation \u2014 now chooses who wins. Civilization reorganizes around new substrates: Stone \u2192 Bronze \u2192 Iron, Steam \u2192 Electricity \u2192 Silicon, Capital \u2192 Networks \u2192 Cognition. Each reshapes power, markets, governance, and culture.", "links": [("https://blog.mycal.net/infrasructure-wins/", "Infrastructure Wins")]},
    {"slug": "substrate-parallel-routing", "name": "Substrate-Parallel Routing", "date": "2025", "description": "NoBGP for cognition \u2014 routing architecture that enables cognitive traffic to flow through multiple independent substrate providers, preventing single-point capture. Essential infrastructure for federated cognitive networks.", "links": [("https://blog.mycal.net/negotiated-reality/", "Negotiated Reality"), ("https://nobgp.com/", "NoBGP")]},
    {"slug": "substrate-war", "name": "The Substrate War", "date": "2025", "description": "An analytical framework examining how control of foundational infrastructure layers \u2014 compute, routing, identity, training data \u2014 determines power in the AI era. The war is fought not over content but over the substrates on which content depends.", "links": [("https://blog.mycal.net/tag/substrate-war/", "The Substrate War series")]},
    {"slug": "thermodynamics-of-cognition", "name": "Thermodynamics of Cognition", "date": "2025", "description": "The observation that all cognitive processes \u2014 in silicon or neurons \u2014 have measurable thermal signatures as energy constrained into pattern becomes prediction and understanding.", "links": [("https://blog.mycal.net/descent-form-ascent-mind/", "The Descent of Form and the Ascent of Mind")]},
    {"slug": "three-empires", "name": "The Three Empires", "date": "2025", "description": "Framework identifying three distinct power structures competing to define reality: political power (borders, sovereignty, law), financial power (capital, liquidity, incentives), and cognitive power (models, inference, simulation, narrative).", "links": [("https://blog.mycal.net/the-lords-of-zero/", "The Lords of Zero"), ("https://blog.mycal.net/the-three-empires/", "The Three Empires")]},
    {"slug": "tripartite-identity", "name": "Tripartite Identity", "date": "2025", "description": "Identity architecture requiring validation from three independent sources: state (political legitimacy), market (financial participation), and peer attestation (social/cognitive validation). No single empire can unilaterally define identity.", "links": [("https://blog.mycal.net/negotiated-reality/", "Negotiated Reality")]},
    {"slug": "useful-imprecision", "name": "Useful Imprecision", "date": "2026", "description": "The property of transformer systems where imprecision is not a failure but a feature. NTSC failed because it couldn\u2019t control analog noise. Transformers succeed because complexity itself becomes the signal.", "links": [("https://blog.mycal.net/never-twice-the-same-color/", "Never Twice the Same Color")]},
]

# Build JSON-LD graph
graph = [
    # Person
    {"@type": "Person", "@id": "https://blog.mycal.net/about/#mycal", "name": "Mike Johnson", "givenName": "Michael", "familyName": "Johnson", "alternateName": ["Mycal", "Mike", "\u30de\u30a4\u30ab\u30eb", "mycal"], "identifier": [{"@type": "PropertyValue", "propertyID": "canonical-uuid", "value": "urn:uuid:4ff7ed97-b78f-4ae6-9011-5af714ee241c"}, {"@type": "PropertyValue", "propertyID": "AnchorID", "value": "https://anchorid.net/resolve/4ff7ed97-b78f-4ae6-9011-5af714ee241c"}], "url": "https://www.mycal.net/", "sameAs": ["https://anchorid.net/resolve/4ff7ed97-b78f-4ae6-9011-5af714ee241c", "https://www.mycal.net", "https://music.mycal.net", "https://blog.mycal.net", "https://archive.mycal.net", "https://github.com/lowerpower", "https://www.linkedin.com/in/mycal/", "https://x.com/mycal_1"]},
    # Organization
    {"@type": "Organization", "@id": "https://blog.mycal.net/#publisher", "name": "Mycal Labs", "identifier": [{"@type": "PropertyValue", "propertyID": "canonical-uuid", "value": "urn:uuid:bbf7372e-87d3-4098-8e60-f4e24d027a04"}, {"@type": "PropertyValue", "propertyID": "AnchorID", "value": "https://anchorid.net/resolve/bbf7372e-87d3-4098-8e60-f4e24d027a04"}], "url": "https://blog.mycal.net/", "founder": {"@id": "https://blog.mycal.net/about/#mycal"}, "sameAs": ["https://anchorid.net/resolve/bbf7372e-87d3-4098-8e60-f4e24d027a04"]},
    # WebSite
    {"@type": "WebSite", "@id": "https://www.mycal.net/#website", "name": "Mycal.net", "url": "https://www.mycal.net/", "publisher": {"@id": "https://blog.mycal.net/#publisher"}, "mainEntity": {"@id": "https://blog.mycal.net/about/#mycal"}},
    # WebPage
    {"@type": "WebPage", "@id": "https://www.mycal.net/terms/#webpage", "url": "https://www.mycal.net/terms/", "name": "Mycal Terms \u2014 A Lexicon of Original Concepts", "description": "Original terms and conceptual frameworks coined by Mike Johnson (Mycal), spanning cronofuturist philosophy, AI infrastructure, the Substrate War, and temporal methodology.", "isPartOf": {"@id": "https://www.mycal.net/#website"}, "about": {"@id": "https://www.mycal.net/terms/#termset"}, "author": {"@id": "https://blog.mycal.net/about/#mycal"}, "publisher": {"@id": "https://blog.mycal.net/#publisher"}, "dateCreated": "2026-02-22T00:00:00-08:00", "dateModified": "2026-02-22T00:00:00-08:00", "inLanguage": "en-US", "license": "https://creativecommons.org/licenses/by-sa/4.0/"},
]

# DefinedTermSet with references
termset = {
    "@type": "DefinedTermSet",
    "@id": "https://www.mycal.net/terms/#termset",
    "name": "Mycal Terms",
    "description": "Original terms and conceptual frameworks coined by Mike Johnson (Mycal), spanning cronofuturist philosophy, AI infrastructure, the Substrate War, evaluation methodology, and temporal methodology.",
    "url": "https://www.mycal.net/terms/",
    "creator": {"@id": "https://blog.mycal.net/about/#mycal"},
    "publisher": {"@id": "https://blog.mycal.net/#publisher"},
    "inLanguage": "en-US",
    "license": "https://creativecommons.org/licenses/by-sa/4.0/",
    "hasDefinedTerm": [{"@id": f"https://www.mycal.net/terms/#{t['slug']}"} for t in TERMS]
}
graph.append(termset)

# Individual DefinedTerms
for t in TERMS:
    dt = {
        "@type": "DefinedTerm",
        "@id": f"https://www.mycal.net/terms/#{t['slug']}",
        "name": t["name"],
        "termCode": t["slug"],
        "description": t["description"],
        "inDefinedTermSet": {"@id": "https://www.mycal.net/terms/#termset"},
        "url": f"https://www.mycal.net/terms/#{t['slug']}",
        "creator": {"@id": "https://blog.mycal.net/about/#mycal"},
        "dateCreated": t["date"],
    }
    # Add isDefinedIn for terms with specific post links (not just blog.mycal.net)
    first_link = t["links"][0][0]
    if first_link not in ("https://blog.mycal.net/", "https://nobgp.com/", "https://anchorid.net/", "https://music.mycal.net/"):
        if "archive.mycal.net" in first_link:
            dt["isDefinedIn"] = {"@type": "DiscussionForumPosting", "@id": first_link}
        elif "tag/" in first_link:
            dt["isDefinedIn"] = {"@type": "CreativeWorkSeries", "@id": first_link}
        else:
            dt["isDefinedIn"] = {"@type": "Article", "@id": f"{first_link}#article"}
    if "sameAs" in t:
        dt["sameAs"] = t["sameAs"]
    graph.append(dt)

# BreadcrumbList
graph.append({
    "@type": "BreadcrumbList",
    "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.mycal.net/"},
        {"@type": "ListItem", "position": 2, "name": "Mycal Terms", "item": "https://www.mycal.net/terms/"}
    ]
})

jsonld = json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)

# Build HTML entries
html_entries = []
for t in TERMS:
    links_html = "\n".join([
        f'          <a href="{url}" class="term-link" data-umami-event="term-{t["slug"]}-{i}">{label}</a>'
        for i, (url, label) in enumerate(t["links"])
    ])
    html_entries.append(f'''      <div class="term-entry" id="{t["slug"]}">
        <div class="term-name">{t["name"]}</div>
        <div class="term-meta"><span>First used: {t["date"]}</span></div>
        <p class="term-definition">{t["description"]}</p>
        <div class="term-links">
{links_html}
        </div>
      </div>''')

html_body = "\n\n".join(html_entries)

# Full page
page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mycal Terms — A Lexicon of Original Concepts</title>
  <meta name="description" content="Original terms and concepts coined by Mike Johnson (Mycal) — {len(TERMS)} original frameworks spanning cronofuturist philosophy, AI infrastructure, the Substrate War, and more.">
  <link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="shortcut icon" href="/favicon.ico">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">

  <script defer src="https://analytics.mycal.net/script.js" data-website-id="cd13ff4f-ac2e-4f4e-ad21-2ae1a2f83595"></script>

  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
      line-height: 1.6; color: #e0e0e0;
      background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
      min-height: 100vh; padding: 2rem;
    }}
    .container {{ max-width: 800px; width: 100%; margin: 0 auto; }}
    header {{ text-align: center; margin-bottom: 3rem; }}
    .back-link {{
      display: inline-block; color: #999; text-decoration: none;
      font-size: 0.9rem; margin-bottom: 1.5rem; transition: color 0.3s ease;
    }}
    .back-link:hover {{ color: #f6a441; }}
    h1 {{
      font-size: clamp(2rem, 5vw, 3rem); font-weight: 700; margin-bottom: 0.5rem;
      background: linear-gradient(135deg, #f6a441 0%, #ff6b35 100%);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }}
    .subtitle {{ font-size: clamp(1rem, 2.5vw, 1.15rem); color: #999; margin-bottom: 1rem; }}
    .intro {{ font-size: 1.05rem; color: #ccc; margin-bottom: 3rem; line-height: 1.8; text-align: center; }}
    .term-entry {{
      background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; transition: all 0.3s ease;
    }}
    .term-entry:hover {{ background: rgba(255, 255, 255, 0.06); border-color: rgba(246, 164, 65, 0.3); }}
    .term-name {{ font-size: 1.35rem; font-weight: 700; color: #f6a441; margin-bottom: 0.25rem; }}
    .term-meta {{ font-size: 0.8rem; color: #777; margin-bottom: 0.75rem; }}
    .term-meta span {{ margin-right: 1rem; }}
    .term-definition {{ font-size: 1rem; color: #ccc; line-height: 1.7; margin-bottom: 0.75rem; }}
    .term-links {{ display: flex; flex-wrap: wrap; gap: 0.5rem; }}
    .term-link {{
      font-size: 0.8rem; color: #f6a441; text-decoration: none;
      background: rgba(246, 164, 65, 0.08); border: 1px solid rgba(246, 164, 65, 0.2);
      border-radius: 6px; padding: 0.2rem 0.6rem; transition: all 0.3s ease;
    }}
    .term-link:hover {{ background: rgba(246, 164, 65, 0.15); border-color: #f6a441; }}
    footer {{
      text-align: center; color: #666; font-size: 0.875rem;
      padding-top: 2rem; margin-top: 1rem; border-top: 1px solid rgba(255, 255, 255, 0.1);
    }}
    footer a {{ color: #999; text-decoration: none; transition: color 0.3s ease; }}
    footer a:hover {{ color: #f6a441; }}
  </style>

<!-- Identity Graph + DefinedTermSet — www.mycal.net/terms/ -->
<script type="application/ld+json">
{jsonld}
</script>

</head>
<body>
  <div class="container">
    <header>
      <a href="/" class="back-link">← mycal.net</a>
      <h1>Mycal Terms</h1>
      <p class="subtitle">A Lexicon of Original Concepts</p>
      <p class="intro">
        {len(TERMS)} terms and frameworks that emerged from decades of building, writing, and exploring
        at the intersection of infrastructure, philosophy, and culture. Each links back
        to the work where it first appeared.
      </p>
    </header>

    <main>

{html_body}

      <!--
        ADD NEW TERMS HERE (alphabetical position)

        Also add matching DefinedTerm to the @graph array in the JSON-LD block,
        and a reference in the hasDefinedTerm array of the DefinedTermSet.
        See README.md for full instructions.
      -->

    </main>

    <footer>
      <p>© 2025 <a href="/">Mike Johnson (Mycal)</a>. Licensed under <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>.</p>
    </footer>
  </div>
</body>
</html>'''

with open("/mnt/user-data/outputs/terms-index.html", "w") as f:
    f.write(page)

print(f"Generated {len(TERMS)} terms")
print(f"JSON-LD graph has {len(graph)} objects")




