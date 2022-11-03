from qtemoji import EmojiView


def test_emoji_view(qtbot):
    view = EmojiView()
    qtbot.addWidget(view)
    view.show()
