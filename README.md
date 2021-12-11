# Logic Assignment

## Background

A formal system is specified as follows:

* Alphabet
  - Delimeter: `(`, `)`
  - Proposition variables: `p0`, `p1`...
  - Logic connectives
    * `~` (NEGATION)
    * `&` (CONJUNCTION)
    * `|` (DISJUNCTION)
    * `->` (IMPLY)
* Axioms
  1. All proprositions are well-defined formulas
  2. If `A` and `B` are wfs, the following are wfs too:
     1. `(A)` Paranthesis Rule
     2. `~A`
     3. `A&B`
     4. `A|B`
     5. `A->B`

## Tasks

- [ ] Imlement a parser/evaluator for the defined formal system
- [ ] Formalize the 4-Queen Problem and find one solution with the evaluator
- [ ] Find all solutions for the 4-Queen Problem
- [ ] Formalize and solve the 8-Queen Problem

