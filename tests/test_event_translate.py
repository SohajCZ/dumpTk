import pytest

from qtinter.event_translate import sequence_parser


@pytest.mark.parametrize(['sequence', 'result'],
                         [("A", {"Detail": "A", "Type": "KeyPress",
                                 "Mod2": None, "Mod1": None, }),
                          ("<1>", {"Detail": "1", "Type": "Button",
                                   "Mod2": None, "Mod1": None, }),
                          ("<KeyPress-A>", {"Detail": "A", "Type": "KeyPress",
                                            "Mod2": None, "Mod1": None, }),
                          ("<Button-1>", {"Detail": "1", "Type": "Button",
                                          "Mod2": None, "Mod1": None, }),
                          ("<Control-Button-1>", {"Detail": "1",
                                                  "Type": "Button",
                                                  "Mod2": "Control",
                                                  "Mod1": None, }),
                          ("<Control-Shift-Button-1>", {"Detail": "1",
                                                  "Type": "Button",
                                                  "Mod2": "Shift",
                                                  "Mod1": "Control", }),
                          ])
def test_sequence_parser(sequence, result):
    assert sequence_parser(sequence) == result
