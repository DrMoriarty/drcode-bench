from formatter import bullet_list


def test_bullet_list():
    assert bullet_list(["a", "b"]) == "- a\n- b"
    assert bullet_list(["x"]) == "- x"
