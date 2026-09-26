:- module(reasoning, [
    solve_query/3
]).

/** <module> Pure meta-interpreter and reasoning driver for Phase 2 SWI-Prolog integration
*/

solve_query(_KB, _Query, unknown).
