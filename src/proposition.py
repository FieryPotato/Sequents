from abc import ABC, abstractmethod
from collections import namedtuple

SIDES: set[str] = {'ant', 'con'}

tupseq = namedtuple('tupseq', ['ant', 'con'])


class Proposition(ABC): 
    """
    Base class for propositions.
    """

    def __init__(self, *args):
        self.content = [arg for arg in args]
        if len(self.content) != self.arity:
            raise ValueError(f'A {self.__class__} contains exactly '\
                             f'{self.arity} propositions.')
 
    @property
    def complexity(self) -> int:
        return 1 + max(p.complexity for p in self.content) 
    
    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.content})'

    def __eq__(self, other) -> bool:
        return self.__class__ == other.__class__ and self.content == other.content
            
    def __ne__(self, other) -> bool:
        return self.__class__ != other.__class__ or self.content != other.content
        
    def __hash__(self):
        return self == other

    def __gt__(self, other):
        return str(self) > str(other) 

    def __ge__(self, other):
        return self > other or self == other
            
    def __lt__(self, other):
        return str(self) < str(other)
    
    def __le__(self, other):
        return self < other or self == other

    @abstractmethod
    def decomposed(self, side) -> tuple[tupseq]:
        """
        Return results of decomposing an instance of the current
        proposition on input side.
        """
        pass

    class AtomicDecompositionError(Exception):
        def __init__(self, proposition):
            msg = f'{proposition} is an atom and cannot be decomposed.'
            super().__init__(msg)


class BinaryProposition(Proposition):
    """
    Super class for binary propositions.
    """
    arity = 2

    def __init__(self, *args):
        super().__init__(*args)
        for arg in args:
             if not isinstance(arg, Proposition):
                 raise TypeError(f'{self.__class__} arguments '\
                         f'must be Proposition not {type(arg)}')

    def __str__(self):
        return f'({self.content[0]} {self.symb} {self.content[1]})'

class Atom(Proposition):
    """
    Proposition class with no logical content.
    """
    arity = 1

    def __init__(self, *args):
        super().__init__(*args)
    
    def __str__(self) -> str:
        return f'{self.content[0]}'

    @property
    def complexity(self) -> int:
        return 0

    def decomposed(self, side) -> None:
        raise self.AtomicDecompositionError()


class Negation(Proposition):
    """
    Unary proposition signifying logical 'not ...'.
    """
    arity = 1

    def __init__(self, *args):
        super().__init__(*args)
        if not isinstance(args[0], Proposition):
            raise TypeError('Negation content must be Proposition, '\
                    f'not {type(args[0])}.')

    def __str__(self) -> str:
        return f'(~{self.content[0]})'

    def decomposed(self, side) -> tuple[tupseq]:
        assert side in SIDES
        if side == 'ant':
            return tupseq([], [self.content[0]]),
        return tupseq([self.content[0]], []),

class Conjunction(BinaryProposition):
    """
    Binary proposition signifying logical '... and ...'.
    """
    symb = '&'

    def __init__(self, *args):
        super().__init__(*args)

    def decomposed(self, side) -> tuple[tupseq]:
        assert side in SIDES
        if side == 'ant':
            return tupseq(self.content, []),
        return tupseq([], [self.content[0]]), tupseq([], [self.content[1]])


class Conditional(BinaryProposition):
    """
    Binary proposition signifying logical 'if ... then ...'
    """
    symb = '->'

    def __init__(self, *args):
        super().__init__(*args)
    
    def decomposed(self, side) -> tuple[tupseq]:
        assert side in SIDES
        if side == 'ant':
            return tupseq([], [self.content[0]]), tupseq([self.content[1]], [])
        return tupseq([self.content[0]], [self.content[1]]),


class Disjunction(BinaryProposition):
    """
    Binary proposition signifying logical '... or ...'
    """
    symb = 'v'

    def __init__(self, *args):
        super().__init__(*args)
    
    def decomposed(self, side) -> tuple[tupseq]:
        assert side in SIDES
        if side == 'ant':
            return tupseq([self.content[0]], []), tupseq([self.content[1]], [])
        return tupseq([], self.content),

