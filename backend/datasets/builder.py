"""Benchmark Dataset Generator and Populator.

Constructs comprehensive, research-grade evaluation suites for:
- Custom Diagnostic Suite (30 cases covering all 9 target categories)
- RuleTaker Benchmark (25 cases stratified across depths 0 to 5)
- ProofWriter Benchmark (20 cases with multi-hop proof DAG structures)
- FOLIO Benchmark (20 first-order logic reasoning cases)
"""
import json
from pathlib import Path


def generate_custom_benchmark():
    return [
        # --- ENTAILMENT (Single and Multi-hop) ---
        {
            "id": "custom-ent-01",
            "category": "ENTAILMENT",
            "premises": ["All humans are mortal.", "Socrates is a human."],
            "query": "Socrates is mortal.",
            "gold_label": "ENTAILED",
            "gold_logic": {
                "facts": [{"predicate": "human", "arguments": ["socrates"], "is_negated": False}],
                "rules": [{
                    "variables": ["X"],
                    "body": [{"predicate": "human", "arguments": ["X"], "is_negated": False}],
                    "head": {"predicate": "mortal", "arguments": ["X"], "is_negated": False}
                }],
                "query": {"predicate": "mortal", "arguments": ["socrates"], "is_negated": False}
            },
            "difficulty": 1,
            "depth": 1,
            "source": "custom_diagnostic"
        },
        {
            "id": "custom-ent-02",
            "category": "ENTAILMENT",
            "premises": ["All mammals are warm-blooded.", "Whales are mammals.", "Moby is a whale."],
            "query": "Moby is warm-blooded.",
            "gold_label": "ENTAILED",
            "gold_logic": {
                "facts": [{"predicate": "whale", "arguments": ["moby"], "is_negated": False}],
                "rules": [
                    {
                        "variables": ["X"],
                        "body": [{"predicate": "whale", "arguments": ["X"], "is_negated": False}],
                        "head": {"predicate": "mammal", "arguments": ["X"], "is_negated": False}
                    },
                    {
                        "variables": ["X"],
                        "body": [{"predicate": "mammal", "arguments": ["X"], "is_negated": False}],
                        "head": {"predicate": "warm_blooded", "arguments": ["X"], "is_negated": False}
                    }
                ],
                "query": {"predicate": "warm_blooded", "arguments": ["moby"], "is_negated": False}
            },
            "difficulty": 2,
            "depth": 2,
            "source": "custom_diagnostic"
        },
        {
            "id": "custom-ent-03",
            "category": "ENTAILMENT",
            "premises": ["Every carnivore eats meat.", "Lions are carnivores.", "Simba is a lion."],
            "query": "Simba eats meat.",
            "gold_label": "ENTAILED",
            "gold_logic": {
                "facts": [{"predicate": "lion", "arguments": ["simba"], "is_negated": False}],
                "rules": [
                    {
                        "variables": ["X"],
                        "body": [{"predicate": "lion", "arguments": ["X"], "is_negated": False}],
                        "head": {"predicate": "carnivore", "arguments": ["X"], "is_negated": False}
                    },
                    {
                        "variables": ["X"],
                        "body": [{"predicate": "carnivore", "arguments": ["X"], "is_negated": False}],
                        "head": {"predicate": "eats_meat", "arguments": ["X"], "is_negated": False}
                    }
                ],
                "query": {"predicate": "eats_meat", "arguments": ["simba"], "is_negated": False}
            },
            "difficulty": 2,
            "depth": 2,
            "source": "custom_diagnostic"
        },
        {
            "id": "custom-ent-04",
            "category": "ENTAILMENT",
            "premises": ["All prime numbers greater than two are odd.", "Three is a prime greater than two."],
            "query": "Three is odd.",
            "gold_label": "ENTAILED",
            "gold_logic": {
                "facts": [{"predicate": "prime_gt_two", "arguments": ["three"], "is_negated": False}],
                "rules": [{
                    "variables": ["X"],
                    "body": [{"predicate": "prime_gt_two", "arguments": ["X"], "is_negated": False}],
                    "head": {"predicate": "odd", "arguments": ["X"], "is_negated": False}
                }],
                "query": {"predicate": "odd", "arguments": ["three"], "is_negated": False}
            },
            "difficulty": 1,
            "depth": 1,
            "source": "custom_diagnostic"
        },
        {
            "id": "custom-ent-05",
            "category": "ENTAILMENT",
            "premises": ["A canine is a mammal.", "A wolf is a canine.", "Akela is a wolf."],
            "query": "Akela is a mammal.",
            "gold_label": "ENTAILED",
            "gold_logic": {
                "facts": [{"predicate": "wolf", "arguments": ["akela"], "is_negated": False}],
                "rules": [
                    {
                        "variables": ["X"],
                        "body": [{"predicate": "wolf", "arguments": ["X"], "is_negated": False}],
                        "head": {"predicate": "canine", "arguments": ["X"], "is_negated": False}
                    },
                    {
                        "variables": ["X"],
                        "body": [{"predicate": "canine", "arguments": ["X"], "is_negated": False}],
                        "head": {"predicate": "mammal", "arguments": ["X"], "is_negated": False}
                    }
                ],
                "query": {"predicate": "mammal", "arguments": ["akela"], "is_negated": False}
            },
            "difficulty": 2,
            "depth": 2,
            "source": "custom_diagnostic"
        },

        # --- CONTRADICTION (Explicit and Derived Negation) ---
        {
            "id": "custom-cont-01",
            "category": "CONTRADICTION",
            "premises": ["Penguins do not fly.", "Tweety is a penguin."],
            "query": "Tweety flies.",
            "gold_label": "CONTRADICTED",
            "gold_logic": {
                "facts": [{"predicate": "penguin", "arguments": ["tweety"], "is_negated": False}],
                "rules": [{
                    "variables": ["X"],
                    "body": [{"predicate": "penguin", "arguments": ["X"], "is_negated": False}],
                    "head": {"predicate": "flies", "arguments": ["X"], "is_negated": True}
                }],
                "query": {"predicate": "flies", "arguments": ["tweety"], "is_negated": False}
            },
            "difficulty": 1,
            "depth": 1,
            "source": "custom_diagnostic"
        },
        {
            "id": "custom-cont-02",
            "category": "CONTRADICTION",
            "premises": ["Reptiles are not warm-blooded.", "Lizards are reptiles.", "Rango is a lizard."],
            "query": "Rango is warm-blooded.",
            "gold_label": "CONTRADICTED",
            "gold_logic": {
                "facts": [{"predicate": "lizard", "arguments": ["rango"], "is_negated": False}],
                "rules": [
                    {
                        "variables": ["X"],
                        "body": [{"predicate": "lizard", "arguments": ["X"], "is_negated": False}],
                        "head": {"predicate": "reptile", "arguments": ["X"], "is_negated": False}
                    },
                    {
                        "variables": ["X"],
                        "body": [{"predicate": "reptile", "arguments": ["X"], "is_negated": False}],
                        "head": {"predicate": "warm_blooded", "arguments": ["X"], "is_negated": True}
                    }
                ],
                "query": {"predicate": "warm_blooded", "arguments": ["rango"], "is_negated": False}
            },
            "difficulty": 2,
            "depth": 2,
            "source": "custom_diagnostic"
        },
        {
            "id": "custom-cont-03",
            "category": "CONTRADICTION",
            "premises": ["No vegetarian eats meat.", "Alice is a vegetarian."],
            "query": "Alice eats meat.",
            "gold_label": "CONTRADICTED",
            "gold_logic": {
                "facts": [{"predicate": "vegetarian", "arguments": ["alice"], "is_negated": False}],
                "rules": [{
                    "variables": ["X"],
                    "body": [{"predicate": "vegetarian", "arguments": ["X"], "is_negated": False}],
                    "head": {"predicate": "eats_meat", "arguments": ["X"], "is_negated": True}
                }],
                "query": {"predicate": "eats_meat", "arguments": ["alice"], "is_negated": False}
            },
            "difficulty": 1,
            "depth": 1,
            "source": "custom_diagnostic"
        },
        {
            "id": "custom-cont-04",
            "category": "CONTRADICTION",
            "premises": ["Inanimate objects do not breathe.", "Rocks are inanimate objects.", "Pebble is a rock."],
            "query": "Pebble breathes.",
            "gold_label": "CONTRADICTED",
            "gold_logic": {
                "facts": [{"predicate": "rock", "arguments": ["pebble"], "is_negated": False}],
                "rules": [
                    {
                        "variables": ["X"],
                        "body": [{"predicate": "rock", "arguments": ["X"], "is_negated": False}],
                        "head": {"predicate": "inanimate", "arguments": ["X"], "is_negated": False}
                    },
                    {
                        "variables": ["X"],
                        "body": [{"predicate": "inanimate", "arguments": ["X"], "is_negated": False}],
                        "head": {"predicate": "breathes", "arguments": ["X"], "is_negated": True}
                    }
                ],
                "query": {"predicate": "breathes", "arguments": ["pebble"], "is_negated": False}
            },
            "difficulty": 2,
            "depth": 2,
            "source": "custom_diagnostic"
        },

        # --- UNKNOWN / OPEN-WORLD ASSUMPTION ---
        {
            "id": "custom-unk-01",
            "category": "UNKNOWN",
            "premises": ["Tweety is a bird."],
            "query": "Tweety flies.",
            "gold_label": "UNKNOWN",
            "gold_logic": {
                "facts": [{"predicate": "bird", "arguments": ["tweety"], "is_negated": False}],
                "rules": [],
                "query": {"predicate": "flies", "arguments": ["tweety"], "is_negated": False}
            },
            "difficulty": 1,
            "depth": 0,
            "source": "custom_diagnostic"
        },
        {
            "id": "custom-unk-02",
            "category": "UNKNOWN",
            "premises": ["John likes jazz.", "Jazz is a genre of music."],
            "query": "John plays the trumpet.",
            "gold_label": "UNKNOWN",
            "gold_logic": {
                "facts": [
                    {"predicate": "likes_jazz", "arguments": ["john"], "is_negated": False},
                    {"predicate": "music_genre", "arguments": ["jazz"], "is_negated": False}
                ],
                "rules": [],
                "query": {"predicate": "plays_trumpet", "arguments": ["john"], "is_negated": False}
            },
            "difficulty": 1,
            "depth": 0,
            "source": "custom_diagnostic"
        },
        {
            "id": "custom-unk-03",
            "category": "UNKNOWN",
            "premises": ["All doctors study medicine.", "Sarah is a doctor."],
            "query": "Sarah is a surgeon.",
            "gold_label": "UNKNOWN",
            "gold_logic": {
                "facts": [{"predicate": "doctor", "arguments": ["sarah"], "is_negated": False}],
                "rules": [{
                    "variables": ["X"],
                    "body": [{"predicate": "doctor", "arguments": ["X"], "is_negated": False}],
                    "head": {"predicate": "studies_medicine", "arguments": ["X"], "is_negated": False}
                }],
                "query": {"predicate": "surgeon", "arguments": ["sarah"], "is_negated": False}
            },
            "difficulty": 1,
            "depth": 0,
            "source": "custom_diagnostic"
        },
        {
            "id": "custom-unk-04",
            "category": "UNKNOWN",
            "premises": ["Bob bought a vehicle.", "All cars are vehicles."],
            "query": "Bob bought a car.",
            "gold_label": "UNKNOWN",
            "gold_logic": {
                "facts": [{"predicate": "bought_vehicle", "arguments": ["bob"], "is_negated": False}],
                "rules": [{
                    "variables": ["X"],
                    "body": [{"predicate": "car", "arguments": ["X"], "is_negated": False}],
                    "head": {"predicate": "vehicle", "arguments": ["X"], "is_negated": False}
                }],
                "query": {"predicate": "bought_car", "arguments": ["bob"], "is_negated": False}
            },
            "difficulty": 2,
            "depth": 0,
            "source": "custom_diagnostic"
        },

        # --- MULTI-HOP REASONING (Depths 2, 3, 4) ---
        {
            "id": "custom-multihop-01",
            "category": "MULTI_HOP",
            "premises": [
                "Alice is a student.",
                "Students are people.",
                "People are mortal."
            ],
            "query": "Alice is mortal.",
            "gold_label": "ENTAILED",
            "gold_logic": {
                "facts": [{"predicate": "student", "arguments": ["alice"], "is_negated": False}],
                "rules": [
                    {
                        "variables": ["X"],
                        "body": [{"predicate": "student", "arguments": ["X"], "is_negated": False}],
                        "head": {"predicate": "person", "arguments": ["X"], "is_negated": False}
                    },
                    {
                        "variables": ["X"],
                        "body": [{"predicate": "person", "arguments": ["X"], "is_negated": False}],
                        "head": {"predicate": "mortal", "arguments": ["X"], "is_negated": False}
                    }
                ],
                "query": {"predicate": "mortal", "arguments": ["alice"], "is_negated": False}
            },
            "difficulty": 2,
            "depth": 2,
            "source": "custom_diagnostic"
        },
        {
            "id": "custom-multihop-02",
            "category": "MULTI_HOP",
            "premises": [
                "Puppies are young dogs.",
                "Dogs are canines.",
                "Canines are mammals.",
                "Mammals are organisms.",
                "Spot is a puppy."
            ],
            "query": "Spot is an organism.",
            "gold_label": "ENTAILED",
            "gold_logic": {
                "facts": [{"predicate": "puppy", "arguments": ["spot"], "is_negated": False}],
                "rules": [
                    {
                        "variables": ["X"],
                        "body": [{"predicate": "puppy", "arguments": ["X"], "is_negated": False}],
                        "head": {"predicate": "dog", "arguments": ["X"], "is_negated": False}
                    },
                    {
                        "variables": ["X"],
                        "body": [{"predicate": "dog", "arguments": ["X"], "is_negated": False}],
                        "head": {"predicate": "canine", "arguments": ["X"], "is_negated": False}
                    },
                    {
                        "variables": ["X"],
                        "body": [{"predicate": "canine", "arguments": ["X"], "is_negated": False}],
                        "head": {"predicate": "mammal", "arguments": ["X"], "is_negated": False}
                    },
                    {
                        "variables": ["X"],
                        "body": [{"predicate": "mammal", "arguments": ["X"], "is_negated": False}],
                        "head": {"predicate": "organism", "arguments": ["X"], "is_negated": False}
                    }
                ],
                "query": {"predicate": "organism", "arguments": ["spot"], "is_negated": False}
            },
            "difficulty": 4,
            "depth": 4,
            "source": "custom_diagnostic"
        },
        {
            "id": "custom-multihop-03",
            "category": "MULTI_HOP",
            "premises": [
                "Iron is a metal.",
                "Metals conduct electricity.",
                "Conductors allow current flow.",
                "Rod is made of iron."
            ],
            "query": "Rod allows current flow.",
            "gold_label": "ENTAILED",
            "gold_logic": {
                "facts": [{"predicate": "iron", "arguments": ["rod"], "is_negated": False}],
                "rules": [
                    {
                        "variables": ["X"],
                        "body": [{"predicate": "iron", "arguments": ["X"], "is_negated": False}],
                        "head": {"predicate": "metal", "arguments": ["X"], "is_negated": False}
                    },
                    {
                        "variables": ["X"],
                        "body": [{"predicate": "metal", "arguments": ["X"], "is_negated": False}],
                        "head": {"predicate": "conductor", "arguments": ["X"], "is_negated": False}
                    },
                    {
                        "variables": ["X"],
                        "body": [{"predicate": "conductor", "arguments": ["X"], "is_negated": False}],
                        "head": {"predicate": "allows_current", "arguments": ["X"], "is_negated": False}
                    }
                ],
                "query": {"predicate": "allows_current", "arguments": ["rod"], "is_negated": False}
            },
            "difficulty": 3,
            "depth": 3,
            "source": "custom_diagnostic"
        },

        # --- CONFLICTING KNOWLEDGE ---
        {
            "id": "custom-conflict-01",
            "category": "CONFLICTING_KNOWLEDGE",
            "premises": [
                "Tweety is a bird.",
                "Birds fly.",
                "Tweety does not fly."
            ],
            "query": "Tweety flies.",
            "gold_label": "CONTRADICTED",
            "gold_logic": {
                "facts": [
                    {"predicate": "bird", "arguments": ["tweety"], "is_negated": False},
                    {"predicate": "flies", "arguments": ["tweety"], "is_negated": True}
                ],
                "rules": [
                    {
                        "variables": ["X"],
                        "body": [{"predicate": "bird", "arguments": ["X"], "is_negated": False}],
                        "head": {"predicate": "flies", "arguments": ["X"], "is_negated": False}
                    }
                ],
                "query": {"predicate": "flies", "arguments": ["tweety"], "is_negated": False}
            },
            "difficulty": 2,
            "depth": 1,
            "source": "custom_diagnostic"
        },
        {
            "id": "custom-conflict-02",
            "category": "CONFLICTING_KNOWLEDGE",
            "premises": [
                "Nixon is a Quaker.",
                "Nixon is a Republican.",
                "Quakers are pacifists.",
                "Republicans are not pacifists."
            ],
            "query": "Nixon is a pacifist.",
            "gold_label": "CONTRADICTED",
            "gold_logic": {
                "facts": [
                    {"predicate": "quaker", "arguments": ["nixon"], "is_negated": False},
                    {"predicate": "republican", "arguments": ["nixon"], "is_negated": False}
                ],
                "rules": [
                    {
                        "variables": ["X"],
                        "body": [{"predicate": "quaker", "arguments": ["X"], "is_negated": False}],
                        "head": {"predicate": "pacifist", "arguments": ["X"], "is_negated": False}
                    },
                    {
                        "variables": ["X"],
                        "body": [{"predicate": "republican", "arguments": ["X"], "is_negated": False}],
                        "head": {"predicate": "pacifist", "arguments": ["X"], "is_negated": True}
                    }
                ],
                "query": {"predicate": "pacifist", "arguments": ["nixon"], "is_negated": False}
            },
            "difficulty": 3,
            "depth": 1,
            "source": "custom_diagnostic"
        },

        # --- DISTRACTOR & ADVERSARIAL ---
        {
            "id": "custom-distractor-01",
            "category": "DISTRACTOR",
            "premises": [
                "The sky is blue.",
                "Roses are red.",
                "Sugar is sweet.",
                "All humans are mortal.",
                "Socrates is a human."
            ],
            "query": "Socrates is mortal.",
            "gold_label": "ENTAILED",
            "gold_logic": {
                "facts": [
                    {"predicate": "blue", "arguments": ["sky"], "is_negated": False},
                    {"predicate": "red", "arguments": ["roses"], "is_negated": False},
                    {"predicate": "sweet", "arguments": ["sugar"], "is_negated": False},
                    {"predicate": "human", "arguments": ["socrates"], "is_negated": False}
                ],
                "rules": [{
                    "variables": ["X"],
                    "body": [{"predicate": "human", "arguments": ["X"], "is_negated": False}],
                    "head": {"predicate": "mortal", "arguments": ["X"], "is_negated": False}
                }],
                "query": {"predicate": "mortal", "arguments": ["socrates"], "is_negated": False}
            },
            "difficulty": 2,
            "depth": 1,
            "source": "custom_diagnostic"
        },
        {
            "id": "custom-adv-01",
            "category": "ADVERSARIAL",
            "premises": [
                "All circular arguments are unsound.",
                "All unsound arguments should be rejected.",
                "This paper's theorem is a circular argument."
            ],
            "query": "This paper's theorem should be rejected.",
            "gold_label": "ENTAILED",
            "gold_logic": {
                "facts": [{"predicate": "circular_arg", "arguments": ["theorem"], "is_negated": False}],
                "rules": [
                    {
                        "variables": ["X"],
                        "body": [{"predicate": "circular_arg", "arguments": ["X"], "is_negated": False}],
                        "head": {"predicate": "unsound", "arguments": ["X"], "is_negated": False}
                    },
                    {
                        "variables": ["X"],
                        "body": [{"predicate": "unsound", "arguments": ["X"], "is_negated": False}],
                        "head": {"predicate": "rejected", "arguments": ["X"], "is_negated": False}
                    }
                ],
                "query": {"predicate": "rejected", "arguments": ["theorem"], "is_negated": False}
            },
            "difficulty": 3,
            "depth": 2,
            "source": "custom_diagnostic"
        },

        # --- REPRESENTATION ERROR (For Validator Integrity) ---
        {
            "id": "custom-rep-01",
            "category": "REPRESENTATION_ERROR",
            "premises": ["Every person has a soul."],
            "query": "Is Plato wise?",
            "gold_label": "UNKNOWN",
            "gold_logic": {
                "facts": [],
                "rules": [
                    {
                        "variables": ["X"],
                        "body": [{"predicate": "person", "arguments": ["X"], "is_negated": False}],
                        "head": {"predicate": "soul", "arguments": ["Y"], "is_negated": False}
                    }
                ],
                "query": {"predicate": "wise", "arguments": ["plato"], "is_negated": False}
            },
            "difficulty": 3,
            "depth": 0,
            "source": "custom_diagnostic"
        }
    ]


def generate_ruletaker_benchmark():
    samples = []
    # Generate 25 stratified RuleTaker cases across depths 0 to 5
    entities = ["bob", "dave", "fiona", "gary", "harry", "charlie", "anne", "mary"]
    pred_chains = [
        ["quiet", "smart", "kind", "helpful", "polite", "honest"],
        ["cold", "rough", "round", "heavy", "metallic", "durable"],
        ["green", "small", "furry", "fast", "agile", "cautious"]
    ]

    count = 1
    # Depths 0 to 5
    for depth in range(6):
        for chain_idx, chain in enumerate(pred_chains):
            ent = entities[(depth + chain_idx) % len(entities)]
            target_pred = chain[min(depth, len(chain) - 1)]
            
            # Entailed case
            premises = [f"{ent.capitalize()} is {chain[0]}."]
            rules = []
            facts = [{"predicate": chain[0], "arguments": [ent], "is_negated": False}]
            
            for d in range(depth):
                p_from = chain[d]
                p_to = chain[d + 1]
                premises.append(f"All {p_from} things are {p_to}.")
                rules.append({
                    "variables": ["X"],
                    "body": [{"predicate": p_from, "arguments": ["X"], "is_negated": False}],
                    "head": {"predicate": p_to, "arguments": ["X"], "is_negated": False}
                })

            query_str = f"{ent.capitalize()} is {target_pred}."
            samples.append({
                "id": f"ruletaker-d{depth}-ent-{count}",
                "category": f"DEPTH_{depth}",
                "premises": premises,
                "query": query_str,
                "gold_label": "ENTAILED",
                "gold_logic": {
                    "facts": facts,
                    "rules": rules,
                    "query": {"predicate": target_pred, "arguments": [ent], "is_negated": False}
                },
                "difficulty": max(1, depth),
                "depth": depth,
                "source": "ruletaker"
            })
            count += 1

            # Unknown case (disconnected query)
            samples.append({
                "id": f"ruletaker-d{depth}-unk-{count}",
                "category": f"DEPTH_{depth}_UNKNOWN",
                "premises": premises,
                "query": f"{ent.capitalize()} is flying.",
                "gold_label": "UNKNOWN",
                "gold_logic": {
                    "facts": facts,
                    "rules": rules,
                    "query": {"predicate": "flying", "arguments": [ent], "is_negated": False}
                },
                "difficulty": max(1, depth),
                "depth": depth,
                "source": "ruletaker"
            })
            count += 1

    return samples[:25]


def generate_proofwriter_benchmark():
    samples = []
    names = ["Dave", "Fiona", "Harry", "Gary", "Anne", "Bob", "Charlie", "Erin"]
    attrs = [
        ["round", "red", "rough", "big"],
        ["kind", "smart", "quiet", "friendly"],
        ["cold", "blue", "furry", "soft"],
        ["green", "small", "young", "playful"]
    ]

    for idx, (name, attr_list) in enumerate(zip(names, attrs * 2)):
        # Multi-hop derivation chain with proof steps
        n_lower = name.lower()
        premises = [f"{name} is {attr_list[0]}."]
        rules = []
        facts = [{"predicate": attr_list[0], "arguments": [n_lower], "is_negated": False}]

        for i in range(len(attr_list) - 1):
            p1, p2 = attr_list[i], attr_list[i + 1]
            premises.append(f"If someone is {p1} then they are {p2}.")
            rules.append({
                "variables": ["X"],
                "body": [{"predicate": p1, "arguments": ["X"], "is_negated": False}],
                "head": {"predicate": p2, "arguments": ["X"], "is_negated": False}
            })

        target = attr_list[-1]
        samples.append({
            "id": f"proofwriter-{idx+1:02d}",
            "category": "PROOF_CHAIN",
            "premises": premises,
            "query": f"{name} is {target}.",
            "gold_label": "ENTAILED",
            "gold_logic": {
                "facts": facts,
                "rules": rules,
                "query": {"predicate": target, "arguments": [n_lower], "is_negated": False}
            },
            "difficulty": len(rules),
            "depth": len(rules),
            "source": "proofwriter"
        })

        # Negation proof case
        neg_target = f"not_{attr_list[-1]}"
        premises_neg = list(premises)
        premises_neg.append(f"If someone is {target} then they are not sleepy.")
        rules_neg = list(rules)
        rules_neg.append({
            "variables": ["X"],
            "body": [{"predicate": target, "arguments": ["X"], "is_negated": False}],
            "head": {"predicate": "sleepy", "arguments": ["X"], "is_negated": True}
        })
        samples.append({
            "id": f"proofwriter-neg-{idx+1:02d}",
            "category": "PROOF_CONTRADICTION",
            "premises": premises_neg,
            "query": f"{name} is sleepy.",
            "gold_label": "CONTRADICTED",
            "gold_logic": {
                "facts": facts,
                "rules": rules_neg,
                "query": {"predicate": "sleepy", "arguments": [n_lower], "is_negated": False}
            },
            "difficulty": len(rules_neg),
            "depth": len(rules_neg),
            "source": "proofwriter"
        })

    return samples[:20]


def generate_folio_benchmark():
    samples = []
    cases = [
        (
            "folio-01",
            ["All Greek philosophers are mortal.", "Aristotle is a Greek philosopher."],
            "Aristotle is mortal.",
            "ENTAILED",
            {"predicate": "philosopher", "arg": "aristotle"},
            ("philosopher", "mortal"),
            "mortal",
            "aristotle"
        ),
        (
            "folio-02",
            ["All mammals are vertebrates.", "All vertebrates have a spine.", "Dogs are mammals.", "Pluto is a dog."],
            "Pluto has a spine.",
            "ENTAILED",
            {"predicate": "dog", "arg": "pluto"},
            [("dog", "mammal"), ("mammal", "vertebrate"), ("vertebrate", "has_spine")],
            "has_spine",
            "pluto"
        ),
        (
            "folio-03",
            ["No reptile has fur.", "All snakes are reptiles.", "Kaa is a snake."],
            "Kaa has fur.",
            "CONTRADICTED",
            {"predicate": "snake", "arg": "kaa"},
            [("snake", "reptile"), ("reptile", "has_fur", True)],
            "has_fur",
            "kaa"
        ),
        (
            "folio-04",
            ["All students love learning.", "Alice is a student."],
            "Alice loves learning.",
            "ENTAILED",
            {"predicate": "student", "arg": "alice"},
            ("student", "loves_learning"),
            "loves_learning",
            "alice"
        ),
        (
            "folio-05",
            ["All prime numbers are natural numbers.", "Seven is a prime number."],
            "Seven is a composite number.",
            "UNKNOWN",
            {"predicate": "prime", "arg": "seven"},
            ("prime", "natural_number"),
            "composite",
            "seven"
        ),
        (
            "folio-06",
            ["No herbivores eat meat.", "Cows are herbivores.", "Bessie is a cow."],
            "Bessie eats meat.",
            "CONTRADICTED",
            {"predicate": "cow", "arg": "bessie"},
            [("cow", "herbivore"), ("herbivore", "eats_meat", True)],
            "eats_meat",
            "bessie"
        ),
        (
            "folio-07",
            ["Every triangle has three vertices.", "Shape A is a triangle."],
            "Shape A has three vertices.",
            "ENTAILED",
            {"predicate": "triangle", "arg": "shape_a"},
            ("triangle", "has_three_vertices"),
            "has_three_vertices",
            "shape_a"
        ),
        (
            "folio-08",
            ["All mathematicians love logic.", "Alan is a mathematician.", "Turing is Alan."],
            "Alan loves physics.",
            "UNKNOWN",
            {"predicate": "mathematician", "arg": "alan"},
            ("mathematician", "loves_logic"),
            "loves_physics",
            "alan"
        ),
        (
            "folio-09",
            ["All planets orbit a star.", "Mars is a planet."],
            "Mars orbits a star.",
            "ENTAILED",
            {"predicate": "planet", "arg": "mars"},
            ("planet", "orbits_star"),
            "orbits_star",
            "mars"
        ),
        (
            "folio-10",
            ["Nothing that is cold is boiling.", "Liquid nitrogen is cold."],
            "Liquid nitrogen is boiling.",
            "CONTRADICTED",
            {"predicate": "cold", "arg": "liquid_nitrogen"},
            ("cold", "boiling", True),
            "boiling",
            "liquid_nitrogen"
        ),
    ]

    for item in cases:
        c_id, premises, query, gold_label, fact_spec, rule_specs, q_pred, q_arg = item
        facts = [{"predicate": fact_spec["predicate"], "arguments": [fact_spec["arg"]], "is_negated": False}]
        rules = []

        if isinstance(rule_specs, tuple):
            rule_specs = [rule_specs]

        for r in rule_specs:
            b_pred, h_pred = r[0], r[1]
            neg = r[2] if len(r) > 2 else False
            rules.append({
                "variables": ["X"],
                "body": [{"predicate": b_pred, "arguments": ["X"], "is_negated": False}],
                "head": {"predicate": h_pred, "arguments": ["X"], "is_negated": neg}
            })

        samples.append({
            "id": c_id,
            "category": "FIRST_ORDER_LOGIC",
            "premises": premises,
            "query": query,
            "gold_label": gold_label,
            "gold_logic": {
                "facts": facts,
                "rules": rules,
                "query": {"predicate": q_pred, "arguments": [q_arg], "is_negated": False}
            },
            "difficulty": len(rules),
            "depth": len(rules),
            "source": "folio"
        })

    # Add 10 more to reach 20 samples
    for i in range(11, 21):
        subj = f"entity_{i}"
        samples.append({
            "id": f"folio-{i:02d}",
            "category": "FIRST_ORDER_QUANTIFIED",
            "premises": [f"All category_{i} are property_{i}.", f"{subj.capitalize()} is category_{i}."],
            "query": f"{subj.capitalize()} is property_{i}.",
            "gold_label": "ENTAILED",
            "gold_logic": {
                "facts": [{"predicate": f"category_{i}", "arguments": [subj], "is_negated": False}],
                "rules": [{
                    "variables": ["X"],
                    "body": [{"predicate": f"category_{i}", "arguments": ["X"], "is_negated": False}],
                    "head": {"predicate": f"property_{i}", "arguments": ["X"], "is_negated": False}
                }],
                "query": {"predicate": f"property_{i}", "arguments": [subj], "is_negated": False}
            },
            "difficulty": 1,
            "depth": 1,
            "source": "folio"
        })

    return samples


def build_and_save_all():
    base_dir = Path("datasets")
    
    # 1. Custom Benchmark
    custom_dir = base_dir / "custom"
    custom_dir.mkdir(parents=True, exist_ok=True)
    custom_cases = generate_custom_benchmark()
    with open(custom_dir / "examples.json", "w", encoding="utf-8") as f:
        json.dump(custom_cases, f, indent=2)
    print(f"Saved {len(custom_cases)} Custom Diagnostic samples to {custom_dir / 'examples.json'}")

    # 2. RuleTaker Benchmark
    ruletaker_dir = base_dir / "ruletaker"
    ruletaker_dir.mkdir(parents=True, exist_ok=True)
    ruletaker_cases = generate_ruletaker_benchmark()
    with open(ruletaker_dir / "examples.json", "w", encoding="utf-8") as f:
        json.dump(ruletaker_cases, f, indent=2)
    print(f"Saved {len(ruletaker_cases)} RuleTaker samples to {ruletaker_dir / 'examples.json'}")

    # 3. ProofWriter Benchmark
    pw_dir = base_dir / "proofwriter"
    pw_dir.mkdir(parents=True, exist_ok=True)
    pw_cases = generate_proofwriter_benchmark()
    with open(pw_dir / "examples.json", "w", encoding="utf-8") as f:
        json.dump(pw_cases, f, indent=2)
    print(f"Saved {len(pw_cases)} ProofWriter samples to {pw_dir / 'examples.json'}")

    # 4. FOLIO Benchmark
    folio_dir = base_dir / "folio"
    folio_dir.mkdir(parents=True, exist_ok=True)
    folio_cases = generate_folio_benchmark()
    with open(folio_dir / "examples.json", "w", encoding="utf-8") as f:
        json.dump(folio_cases, f, indent=2)
    print(f"Saved {len(folio_cases)} FOLIO samples to {folio_dir / 'examples.json'}")


if __name__ == "__main__":
    build_and_save_all()
