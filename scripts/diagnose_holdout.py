from search_core import SearchEngine

engine = SearchEngine()

test_cases = [
    ("Can I leave property to my grandchild who hasn't been born yet?", "Transfer of Property Act, 1882", "13"),
    ("The other person flat out refused to do their part of the deal, can I cancel the contract?", "Indian Contract Act, 1872", "39"),
    ("Someone physically blocked me from walking away, what crime is that?", "Bharatiya Nyaya Sanhita, 2023", "126"),
    ("Is there a time limit to appeal to the IT Appellate Tribunal?", "Information Technology Act, 2000", "60"),
]

for query, expected_act, expected_section in test_cases:
    print(f"\n=== {query} ===")
    print(f"Expecting: {expected_act}, Section {expected_section}")
    results = engine.search(query, top_k=30)

    found_rank = None
    for rank, r in enumerate(results, start=1):
        if str(r["act_name"]) == expected_act and str(r["section_number"]) == expected_section:
            found_rank = rank
            break

    print(f"Found at rank: {found_rank if found_rank else 'NOT in top 30'}")
    print("Top 3:")
    for r in results[:3]:
        print(f"  - {r['act_name']} Section {r['section_number']} (score: {r['hybrid_score']:.3f}) - {r['section_title']}")
