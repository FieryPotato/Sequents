class Proposition:
    """
    Base class for propositions.
    """
    
    def __init__(self, *args):
        self.content = [arg for arg in args]
 
    @property
    def complexity(self) -> int:
        return 1 + max(p.complexity for p in self.content) 
        
    @property
    def arity(self) -> int:
        return len(self.content) 


class Atom(Proposition):
    """
    Proposition class with no logical content.
    """
    
    def __init__(self, *args):
        if len(args) != 1:
            raise ValueError("Atoms contain one and only one sentence.")
        super().__init__(*args)
   
    @property
    def complexity(self) -> int:
        return 0


class Negation(Proposition):
    """
    Unary proposition signifying logical "not ...".
    """
    
    def __init__(self, *args):
        if len(args) != 1:
            raise ValueError("Negations contain one and only one sentence.")
        super().__init__(*args)


class Conjunction(Proposition):
    """
    Binary proposition signifying logical "... and ...".
    """

    def __init__(self, *args):
        super().__init__(*args)


class Conditional(Proposition):
    """
    Binary proposition signifying logical "if ... then ..."
    """
    def __init__(self, *args):
        super().__init__(*args)


class Disjunction(Proposition):
    """
    Binary proposition signifying logical "... or ..."
    """
    def __init__(self, *args):
        super().__init__(*args)

