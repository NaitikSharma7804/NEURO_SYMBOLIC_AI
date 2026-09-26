:- module(reasoning, [
    solve_query/5
]).

use_module(inference).
use_module(contradiction).
use_module(proof).

/** <module> Master Prolog Symbolic Reasoning Driver
 *
 * Coordinates goal evaluation, contradiction analysis, and proof trace extraction.
 */

solve_query(PosGoal, NegGoal, Status, ConflictDetected, ProofTrace) :-
    check_dual_query(PosGoal, NegGoal, Status, ConflictDetected, 10),
    ( Status == entailed ->
        ( prove_goal(PosGoal, Trace, 10) -> normalize_proof_steps(Trace, 1, ProofTrace) ; ProofTrace = [] )
    ; Status == contradicted ->
        ( prove_goal(NegGoal, Trace, 10) -> normalize_proof_steps(Trace, 1, ProofTrace) ; ProofTrace = [] )
    ; ProofTrace = []
    ).
