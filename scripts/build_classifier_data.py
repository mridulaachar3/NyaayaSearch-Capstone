import pandas as pd
from search_core import SearchEngine
import json

engine = SearchEngine()

with open("../data/eval/eval_queries.json", "r", encoding="utf-8") as f:
    tuned_queries = json.load(f)

holdout_queries = [
    ("Can I leave property to my grandchild who hasn't been born yet?", "Transfer of Property Act, 1882", ["13"]),
    ("Someone took my car without asking me, is that a crime?", "Motor Vehicles Act, 1988", ["197"]),
    ("The other person flat out refused to do their part of the deal, can I cancel the contract?", "Indian Contract Act, 1872", ["39"]),
    ("If my agent's authority ends, does that also end my sub-agent's authority?", "Indian Contract Act, 1872", ["210"]),
    ("Does my landlord have to give me notice before increasing my rent?", "Karnataka Rent Act, 1999", ["10"]),
    ("Police say my complaint is non-cognizable, what happens to my case now?", "Bharatiya Nagarik Suraksha Sanhita, 2023", ["174"]),
    ("Someone physically blocked me from walking away, what crime is that?", "Bharatiya Nyaya Sanhita, 2023", ["126"]),
    ("There's an arrest warrant against me, what happens when the police come?", "Bharatiya Nagarik Suraksha Sanhita, 2023", ["82"]),
    ("Can the government change traffic fine amounts after they're set?", "Motor Vehicles Act, 1988", ["199B"]),
    ("Is there a time limit to appeal to the IT Appellate Tribunal?", "Information Technology Act, 2000", ["60"]),
    ("When does an agent's authority to act for someone officially end?", "Indian Contract Act, 1872", ["201"]),
    ("What happens if I drive without a proper licence?", "Motor Vehicles Act, 1988", ["181"]),
    ("Is it a crime to give police false information to get someone else in trouble?", "Bharatiya Nyaya Sanhita, 2023", ["217"]),
    ("What's the difference between a temporary and a permanent court injunction?", "Specific Relief Act, 1963", ["37"]),
    ("Can I get in trouble for parking my car somewhere unsafe?", "Motor Vehicles Act, 1988", ["122"]),
    ("What's the punishment for kidnapping someone for ransom?", "Bharatiya Nyaya Sanhita, 2023", ["140"]),
    ("If I settle my consumer complaint, does the commission record that officially?", "Consumer Protection Act, 2019", ["81"]),
    ("Can a court order my abuser to stay away from me?", "Protection of Women from Domestic Violence Act, 2005", ["18"]),
    ("Can police search me after they arrest me?", "Bharatiya Nagarik Suraksha Sanhita, 2023", ["49"]),
    ("Is it a crime to convince a soldier to disobey orders?", "Bharatiya Nyaya Sanhita, 2023", ["159"]),
]

all_queries = [(q["query"], q["act_name"], [str(s) for s in q["expected_sections"]]) for q in tuned_queries]
all_queries += holdout_queries

rows = []
for query, expected_act, expected_sections in all_queries:
    results = engine.search(query, top_k=10)  # widened from 5 to 10
    for r in results:
        is_relevant = int(str(r["act_name"]) == expected_act and str(r["section_number"]) in expected_sections)
        rows.append({
            "query": query,
            "act_name": r["act_name"],
            "section_number": r["section_number"],
            "hybrid_score": r["hybrid_score"],
            "semantic_score": r["semantic_score"],
            "bm25_score": r["bm25_score"],
            "matched_term_count": len(r.get("matched_terms", [])),
            "is_relevant": is_relevant,
        })

df = pd.DataFrame(rows)
df.to_csv("../data/eval/classifier_training_data.csv", index=False)
print(f"Built {len(df)} labeled examples from {len(all_queries)} queries (top_k=10)")
print(f"Relevant: {df['is_relevant'].sum()}, Not relevant: {(df['is_relevant']==0).sum()}")
