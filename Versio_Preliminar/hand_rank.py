from collections import namedtuple


class Card(namedtuple('Card', 'face, suit')):
    def __repr__(self):
        return ''.join(self)


suit = '♥ ♦ ♣ ♠'.split()
# ordered strings of faces
faces = '2 3 4 5 6 7 8 9 10 11 12 13 14'
lowaces = '14 2 3 4 5 6 7 8 9 10 11 12 13'
# faces as lists
face = faces.split()
lowace = lowaces.split()


def straight_flush(hand):
    f, fs = ((lowace, lowaces) if any(card.face == '2' for card in hand)
             else (face, faces))
    ordered = sorted(hand, key=lambda card: (f.index(card.face), card.suit))
    first, rest = ordered[0], ordered[1:]
    if (all(card.suit == first.suit for card in rest) and
            ' '.join(card.face for card in ordered) in fs):
        return 8, ordered[-1].face
    return False


def poker(hand):
    allfaces = [f for f, s in hand]
    allftypes = set(allfaces)
    if len(allftypes) != 2:
        return False
    for f in allftypes:
        if allfaces.count(f) == 4:
            allftypes.remove(f)
            return 7, [f, allftypes.pop()]
    else:
        return False


def full_house(hand):
    allfaces = [f for f, s in hand]
    allftypes = set(allfaces)
    if len(allftypes) != 2:
        return False
    for f in allftypes:
        if allfaces.count(f) == 3:
            allftypes.remove(f)
            return 6, [f, allftypes.pop()]
    else:
        return False


def flush(hand):
    allstypes = {s for f, s in hand}
    if len(allstypes) == 1:
        allfaces = [f for f, s in hand]
        return 5, sorted(allfaces,
                         key=lambda f: face.index(f),
                         reverse=True)
    return False


def straight(hand):
    f, fs = ((lowace, lowaces) if any(card.face == '2' for card in hand)
             else (face, faces))
    ordered = sorted(hand, key=lambda card: (f.index(card.face), card.suit))
    first, rest = ordered[0], ordered[1:]
    if ' '.join(card.face for card in ordered) in fs:
        return 4, ordered[-1].face
    return False


def three_kind(hand):
    allfaces = [f for f, s in hand]
    allftypes = set(allfaces)
    if len(allftypes) <= 2:
        return False
    for f in allftypes:
        if allfaces.count(f) == 3:
            allftypes.remove(f)
            return (3, [f] +
                    sorted(allftypes,
                           key=lambda f: face.index(f),
                           reverse=True))
    else:
        return False


def two_pair(hand):
    allfaces = [f for f, s in hand]
    allftypes = set(allfaces)
    pairs = [f for f in allftypes if allfaces.count(f) == 2]
    if len(pairs) != 2:
        return False
    p0, p1 = pairs
    other = [(allftypes - set(pairs)).pop()]
    return 2, pairs + other if face.index(p0) > face.index(p1) else pairs[::-1] + other


def pair(hand):
    allfaces = [f for f, s in hand]
    allftypes = set(allfaces)
    pairs = [f for f in allftypes if allfaces.count(f) == 2]
    if len(pairs) != 1:
        return False
    allftypes.remove(pairs[0])
    return 1, pairs + sorted(allftypes,
                             key=lambda f: face.index(f),
                             reverse=True)


def high_card(hand):
    allfaces = [f for f, s in hand]
    return 0, sorted(allfaces,
                     key=lambda f: face.index(f),
                     reverse=True)


handrankorder = (straight_flush, poker, full_house,
                 flush, straight, three_kind,
                 two_pair, pair, high_card)


def rank(cards):
    hand = handy(cards)
    for ranker in handrankorder:
        rank = ranker(hand)
        if rank:
            break
    assert rank, "Invalid: Failed to rank cards: %r" % cards
    return rank


def handy(cards='2♥ 2♦ 2♣ 13♣ 12♦'):
    hand = []
    for card in cards.split():
        f, s = card[:-1], card[-1]
        assert f in face, "Invalid: Don't understand card face %r" % f
        assert s in suit, "Invalid: Don't understand card suit %r" % s
        hand.append(Card(f, s))
    assert len(hand) == 5, "Invalid: Must be 5 cards in a hand, not %i" % len(hand)
    assert len(
        set(hand)) == 5, "Invalid: All cards in the hand must be unique %r" % cards
    return hand
