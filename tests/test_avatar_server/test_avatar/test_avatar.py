from src.AvatarServer.Avatar.avatar import Avatar


def test_avartar():
    # TODO: implement
    return
    avatar = Avatar(
        face="1",
        cap="2",
        longcoat="3",
        weapon="4",
    )

    assert avatar.to_array() == ["1", "2", "3", "4"]
    assert avatar.to_param() == [("face", "1"), ("cap", "2"), ("longcoat", "3"), ("weapon", "4")]
