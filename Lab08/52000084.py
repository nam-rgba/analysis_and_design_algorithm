from typing import List, Optional, Tuple

class Man:
    def __init__(self, name: str, preferences: List[str]):
        self.name = name
        self.preferences = preferences
        self.partner: Optional[str] = None

    def propose(self) -> Optional[str]:
        if self.preferences:
            return self.preferences.pop(0)
        else:
            return None

    def set_partner(self, woman_name: str):
        self.partner = woman_name


class Woman:
    def __init__(self, name: str, preferences: List[str]):
        self.name = name
        self.preferences = preferences
        self.partner: Optional[str] = None

    def accept_proposal(self, man_name: str):
        self.partner = man_name


def select_free_man(men: List[Man]) -> Optional[Man]:
    """
    Selects a free man from the input list of men.
    Args:
        men (List[Man]): List of men.
    Returns:
        Optional[Man]: A free man or None if all men are taken.
    """
    return next((man for man in men if man.partner is None), None)


def propose(men: List[Man], women: List[Woman], current_man: Man) -> Tuple[List[Man], List[Woman]]:
    """
    Models the proposing process. The function takes lists of men and women,
    and a currently considered man. It returns the changed lists of men and women
    with their corresponding changed status.

    Args:
        men (List[Man]): List of men.
        women (List[Woman]): List of women.
        current_man (Man): Currently considered man.

    Returns:
        Tuple[List[Man], List[Woman]]: Updated lists of men and women.
    """
    proposed_woman_name = current_man.propose()

    # Find the corresponding woman object
    proposed_woman = next(woman for woman in women if woman.name == proposed_woman_name)

    # Check if the woman is free
    if proposed_woman.partner is None:
        proposed_woman.accept_proposal(current_man.name)
        current_man.set_partner(proposed_woman_name)
    else:
        # If the woman is taken, check if she prefers the current man
        current_partner_index = proposed_woman.preferences.index(proposed_woman.partner)
        new_man_index = proposed_woman.preferences.index(current_man.name)

        if new_man_index < current_partner_index:
            # The woman prefers the current man over her current partner
            former_partner = next(man for man in men if man.name == proposed_woman.partner)
            former_partner.set_partner(None)

            proposed_woman.accept_proposal(current_man.name)
            current_man.set_partner(proposed_woman_name)

    return men, women


def stable_marriage(men: List[Man], women: List[Woman]) -> Tuple[List[Man], List[Woman]]:
    """
    Solves the Stable Marriage problem.

    Args:
        men (List[Man]): List of men.
        women (List[Woman]): List of women.

    Returns:
        Tuple[List[Man], List[Woman]]: Lists of men and women with their stable partners.
    """
    while any(man.partner is None for man in men):
        free_man = select_free_man(men)
        updated_men, updated_women = propose(men, women, free_man)
        men, women = updated_men, updated_women

    return men, women


# Example usage:
men_list = [Man("Bob", ["Lea", "Ann", "Sue"]),
            Man("Jim", ["Lea", "Sue", "Ann"]),
            Man("Tom", ["Sue", "Lea", "Ann"]),]

women_list = [Woman("Ann", ["Jim", "Bob", "Tom"]),
              Woman("Lea", ["Tom", "Bob", "Jim"]),
              Woman("Sue", ["Jim", "Tom", "Bob"])]

final_men, final_women = stable_marriage(men_list, women_list)

# Print the final matching
for man in final_men:
    print(f"{man.name}'s partner: {man.partner}")

