# Spec for Quantifiers:

## String Representations

Quantified propositions should coexist with sentential propositions.
They share a structure with negations as unary propositions, which is 
to say they have a space between their logical content and their 
propositional content and do not use parentheses to group them.

Atoms can be sentential (P, Q, The long moon creeps over the horizon, 
etc.) or first-order, which are displayed as single words with a 
Capitalized first letter, concatenated PascalCase words, or uppercase 
letters followed by one or more lowercase letters between angle 
brackets. E.g.  `P<a>`, `EatsWith<a, e>`, `Green<s>`.

Quantifiers are declared right before their propositional content.
At least one predicate in the proposition must have the quantifier's
variable as one or more of its names.

### Universal
- symbol: ∀ (U+2200)
- string: forall
- eg: `∀x LovesRaymond<x>`, `∀x ∀y (H<x, y> -> M<x, y>)`

### Existential
- symbol: ∃ (U+2203)
- string: exists
- eg: ∃x (Tasty<x> & Liquorice<x>)

