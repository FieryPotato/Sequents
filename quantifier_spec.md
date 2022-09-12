# Spec for Quantifiers:

## String Representations

Quantified propositions should coexist with sentential propositions.
They share a structure with negations as unary propositions, which is 
to say they have a space between their logical content and their 
propositional content and do not use parentheses to group them.

Atoms can be sentential (P, Q, The long moon creeps over the horizon, 
etc.) or first-order, which are displayed as single words with a 
Capitalized first letter, concatenated PascalCase words, or uppercase 
letters followed by one or more names. Names must contain at least two
letters and be entirely lowercase, separated by commas. E.g. 
`P<socrates>`, `EatsWith<seamus, fork>`, `Green<grass>`.

Quantifiers are declared right before their propositional content.
At least one predicate in the proposition must have the quantifier's
variable as one or more of its names. Variables are single lowercase
letters. `P<s>`, `EatsWith<x, y>`. Note that variables are always
bound by some quantifier. `P<s>` is malformed if it is not a sub-
proposition of a Quantifier whose variable is 's'.

### Universal
- symbol: ∀ (U+2200, html: &forall;)
- string: forall
- eg: `forallx LovesRaymond<x>`, `∀x ∀y (H<x, y> -> M<x, y>)`

### Existential
- symbol: ∃ (U+2203, html: &exist;)
- string: exists
- eg: existsx (Tasty\<x\> & Liquorice\<x\>), `∃y ~ ∃x ~ D<x, y>`

## Proposition

### Properties
All propositions will gain the following properties:
- names: tuple[str] = a collection of all names in the proposition, 
which is to say anything inside angle brackets
- unbound\_variables: tuple[str] = a collection of variables which are
not bound by a quantifier. A proposition in this state which is not
the subproposition of another quantified proposition that binds those
variables is maformed.

In addition to the content property, quantified propositions have a 
variable property which stores the character it was initialized with.

All propositions will gain the 'instantiate' method, which replaces 
all instances of a given variable with an input name. Note that for 
quantifiers, this will overlap the behaviour of the decomposition 
algorithm as it should in those cases return the proposition's content 
without the quantifier.

