:- module(proof, [
    normalize_proof_steps/3
]).

/** <module> Proof step normalization and serialization in Prolog
 */

normalize_proof_steps([], CurrentId, []) :- !.

normalize_proof_steps([fact(Goal)|Rest], CurrentId, [step(CurrentId, 'FACT', Goal, [])|OutRest]) :-
    NextId is CurrentId + 1,
    normalize_proof_steps(Rest, NextId, OutRest).

normalize_proof_steps([rule(Head, Body, SubTrace)|Rest], CurrentId, [step(CurrentId, 'INFERENCE', Head, SubIds)|OutRest]) :-
    normalize_proof_steps(SubTrace, CurrentId, SubSteps),
    extract_step_ids(SubSteps, SubIds),
    NextId is CurrentId + 1,
    normalize_proof_steps(Rest, NextId, RestSteps),
    append(SubSteps, RestSteps, OutRest).

extract_step_ids([], []).
extract_step_ids([step(Id, _, _, _)|Rest], [Id|RestIds]) :-
    extract_step_ids(Rest, RestIds).
