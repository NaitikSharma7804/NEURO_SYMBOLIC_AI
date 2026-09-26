:- module(inference, [
    prove_goal/3,
    prove_conjunction/3
]).

/** <module> Pure meta-interpreter for deductive inference with cycle detection
 *
 * Implements bounded depth deductive proof search over asserted facts and rules.
 */

prove_goal(Goal, Trace, MaxDepth) :-
    prove_goal_bounded(Goal, [], Trace, MaxDepth).

% Base case: Goal matches an asserted ground fact
prove_goal_bounded(Goal, _Visited, [fact(Goal)], _Depth) :-
    user:call(Goal).

% Recursive case: Goal matches head of a rule Head :- Body
prove_goal_bounded(Goal, Visited, [rule(Goal, Body, SubTrace)], Depth) :-
    Depth > 0,
    \+ member(Goal, Visited),
    user:clause(Goal, Body),
    NewDepth is Depth - 1,
    prove_conjunction(Body, [Goal|Visited], SubTrace, NewDepth).

% Conjunction handling (Body1, Body2)
prove_conjunction((A, B), Visited, [TraceA, TraceB], Depth) :-
    !,
    prove_goal_bounded(A, Visited, TraceA, Depth),
    prove_goal_bounded(B, Visited, TraceB, Depth).

prove_conjunction(true, _Visited, [true], _Depth) :- !.

prove_conjunction(Goal, Visited, Trace, Depth) :-
    prove_goal_bounded(Goal, Visited, Trace, Depth).
