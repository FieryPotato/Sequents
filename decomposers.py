import rules
from sequent import Sequent


RULE_DICT = {
    'ant': {
        '~': rules.LeftNot,
        '&': rules.LeftMultAnd,
    },
    'con': {
        '~': rules.RightNot,
        'v': rules.RightMultOr,
        '->': rules.RightMultIf,
    }
}


def get_rule(sequent: Sequent) -> rules.Rule:
    prop, side, index = sequent.first_complex_prop()
    sequent_minus_prop = sequent.remove_proposition_at(side, index)
    rule = RULE_DICT[side][prop.symb]
    return rule(prop, sequent_minus_prop)
