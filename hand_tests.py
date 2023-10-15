import hand
from card import Card

def test_hand_type():
    my_hand = hand.Hand([Card(2, 0), Card(3, 0), Card(4, 0), Card(5, 0), Card(6, 0)])
    assert my_hand.get_hand_type() == hand.STRAIGHT_FLUSH
    my_hand = hand.Hand([Card(2, 0), Card(3, 0), Card(4, 0), Card(5, 0), Card(14, 0)])
    assert my_hand.get_hand_type() == hand.STRAIGHT_FLUSH
    my_hand = hand.Hand([Card(2, 0), Card(3, 0), Card(4, 0), Card(5, 0), Card(6, 1)])
    assert my_hand.get_hand_type() == hand.STRAIGHT
    my_hand = hand.Hand([Card(2, 0), Card(3, 0), Card(4, 0), Card(5, 0), Card(14, 1)])
    assert my_hand.get_hand_type() == hand.STRAIGHT
    my_hand = hand.Hand([Card(2, 0), Card(3, 0), Card(4, 0), Card(5, 1), Card(6, 1)])
    assert my_hand.get_hand_type() == hand.STRAIGHT
    my_hand = hand.Hand([Card(2,0), Card(2,1), Card(6,0), Card(7,0), Card(8,0)])
    assert my_hand.get_hand_type() == hand.ONE_PAIR
    my_hand = hand.Hand([Card(2,0), Card(2,1), Card(6,0), Card(6,1), Card(8,0)])
    assert my_hand.get_hand_type() == hand.TWO_PAIR
    my_hand = hand.Hand([Card(2,0), Card(2,1), Card(2,2), Card(6,1), Card(8,0)])
    assert my_hand.get_hand_type() == hand.THREE_OF_A_KIND
    my_hand = hand.Hand([Card(2,0), Card(2,1), Card(2,2), Card(2,3), Card(8,0)])
    assert my_hand.get_hand_type() == hand.FOUR_OF_A_KIND
    my_hand = hand.Hand([Card(2,0), Card(2,1), Card(2,2), Card(6,1), Card(6,0)])
    assert my_hand.get_hand_type() == hand.FULL_HOUSE

def test_hand_comparison():
    my_hand = hand.Hand([Card(2, 0), Card(3, 0), Card(4, 0), Card(5, 0), Card(6, 0)])
    my_hand2 = hand.Hand([Card(2, 0), Card(3, 0), Card(4, 0), Card(5, 0), Card(7, 0)])
    assert not my_hand2.is_straight()
    assert my_hand > my_hand2
    my_hand = hand.Hand([Card(2, 0), Card(3, 0), Card(4, 0), Card(5, 0), Card(7, 0)])
    my_hand2 = hand.Hand([Card(2, 0), Card(3, 0), Card(4, 0), Card(5, 1), Card(6, 0)])
    assert my_hand > my_hand2
    my_hand = hand.Hand([Card(2, 0), Card(3, 0), Card(4, 0), Card(5, 1), Card(6, 1)])
    my_hand2 = hand.Hand([Card(2, 0), Card(3, 0), Card(4, 0), Card(6, 1), Card(6, 2)])
    assert my_hand > my_hand2
    #compare of a kinds with each other and others
    my_hand = hand.Hand([Card(2, 0), Card(2, 1), Card(2, 2), Card(2, 3), Card(6, 1)])
    my_hand2 = hand.Hand([Card(2, 0), Card(2, 1), Card(2, 2), Card(6, 1), Card(6, 2)])
    assert my_hand > my_hand2
    my_hand = hand.Hand([Card(2, 0), Card(2, 1), Card(2, 2), Card(2, 3), Card(6, 1)])
    my_hand2 = hand.Hand([Card(2, 0), Card(2, 1), Card(2, 2), Card(2, 3), Card(7, 1)])
    assert my_hand2 > my_hand
    my_hand = hand.Hand([Card(2, 0), Card(2, 1), Card(2, 2), Card(2, 3), Card(6, 1)])
    my_hand2 = hand.Hand([Card(2, 0), Card(2, 1), Card(2, 2), Card(2, 3), Card(6, 2)])
    assert (not my_hand2 > my_hand) and (not my_hand > my_hand2)
    #compare full houses
    my_hand = hand.Hand([Card(2, 0), Card(2, 1), Card(2, 2), Card(6, 1), Card(6, 2)])
    my_hand2 = hand.Hand([Card(2, 0), Card(2, 1), Card(2, 2), Card(7, 1), Card(7, 2)])
    assert my_hand2 > my_hand


if __name__ == '__main__':
    test_hand_type()
    test_hand_comparison()
    print('Tests passed')