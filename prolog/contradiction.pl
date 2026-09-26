:- module(contradiction, [
    check_dual_query/5
]).

/** <module> Open-World Assumption Dual-Query Contradiction Analysis
 *
 * Evaluates both Query and Opposite(Query).
 * Returns:
 *   - entailed (Pos=true, Neg=false)
 *   - contradicted (Pos=false, Neg=true)
 *   - unknown (Pos=false, Neg=false)
 *   - conflict (Pos=true, Neg=true)
 */

check_dual_query(PosGoal, NegGoal, Status, ConflictDetected, MaxDepth) :-
    ( prove_goal_safe(PosGoal, MaxDepth) -> Pos = true ; Pos = false ),
    ( prove_goal_safe(NegGoal, MaxDepth) -> Neg = true ; Neg = false ),
    classify_results(Pos, Neg, Status, ConflictDetected).

prove_goal_safe(Goal, _MaxDepth) :-
    catch(user:call(Goal), _, fail).

classify_results(true, true, contradicted, true) :- !.
classify_results(true, false, entailed, false) :- !.
classify_results(false, true, contradicted, false) :- !.
classify_results(false, false, unknown, false) :- !.
