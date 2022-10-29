from enum import Enum
from typing import Dict, Any, List

import emoji
import qtawesome
from qthandy import vbox, vspacer, incr_font, decr_font, flow, hbox, transparent, pointy
from qtpy.QtCore import Qt, Signal, QSize
from qtpy.QtGui import QFont, QPalette
from qtpy.QtWidgets import QWidget, QLabel, QScrollArea, QFrame, QToolButton

EMOJI_DATA: Dict[str, Dict[str, Any]] = emoji.EMOJI_DATA

_PEOPLE_EMOJIES = [
    '🙂', '😀', '😃', '😄', '😁', '😅', '😆', '🤣', '😂', '🙃', '😉', '😊', '😇', '😎', '🤓', '🧐', '🥳', '🥰', '😍',
    '🤩', '😘', '😗', '😚', '😙', '😋', '😛',
    '😜', '🤪', '😝', '🤑', '🤗', '🤭', '🤫', '🤔', '😐', '🤐', '🤨', '😑', '😶', '😏', '😒', '🙄', '😬', '🤥', '😪',
    '😴', '😌', '😔', '🤤', '😷', '🤒', '🤕', '🤢', '🤮', '🤧', '🥵', '🥶', '🥴', '😵', '🤯', '😕', '😟', '🙁', '😮',
    '😯', '😲', '😳', '🥺', '😦', '😧', '😨', '😰', '😥', '😢', '😭', '😱', '😖', '😣', '😞', '😓', '😩', '😫', '😤',
    '😡', '😠', '🤬', '😈', '👿', '💀', '💩', '🤡', '👹', '👺', '👻', '👽', '👾', '🤖', '😺', '😸', '😹', '😻', '😼',
    '😽', '🙀', '😿', '😾', '🙈', '🙉', '🙊', '💋', '💌', '💘', '💝', '💖', '💗', '💓', '💞', '💕', '💟', '❣', '💔',
    '❤', '❤', '🧡', '💛', '💚', '💙', '💜', '🖤', '💯', '💢', '💥', '💫', '💦', '💨', '🕳', '💣', '💬', '🗨', '🗯',
    '💭', '💤', '👋', '🤚', '🖐',
    '✋', '🖖', '👌', '✌', '🤞', '🤟', '🤘', '🤙', '👈', '👉', '👆', '👇', '🖕', '☝', '👍', '👎', '✊', '👊', '🤛', '🤜',
    '👏', '🙌', '👐', '🤲', '🤝', '🙏', '✍', '💅', '🤳', '💪', '🦵', '🦶', '👂', '👃', '🧠', '👣', '🦷', '🦴', '👀',
    '👁', '👅', '👄', '🧑', '👶', '🧒', '👦', '👧', '👱', '👨', '🧔', '👩', '🧓', '👴', '👵',

    '🙍', '🙍‍♂‍', '🙍‍♀‍', '🙎', '🙎‍♂‍', '🙎‍♀‍', '🙅', '🙅‍♂‍', '🙅‍♀‍', '🙆', '🙆‍♂‍', '🙆‍♀‍', '💁', '💁‍♂‍',
    '💁‍♀‍', '🙋', '🙋‍♂‍', '🙋‍♀‍', '🙇', '🙇‍♂‍', '🙇‍♀‍', '🤦', '🤦‍♂', '🤦‍♀', '🤷', '🤷‍♂', '🤷‍♀', '👨‍⚕', '👩‍⚕',
    '👨‍✈', '👩‍✈', '👮', '👮‍♂', '👮‍♀', '💂‍♂', '💂‍♀', '👷', '👷‍♂', '👷‍♀', '🤴', '👸', '👳', '👳‍♂', '👳‍♀', '👲',
    '🧕', '🤵', '👰', '🤰', '🤱', '👼', '🎅', '🤶', '🦸', '🦸‍♂‍', '🦸‍♀‍', '🦹', '🦹‍♂‍', '🦹‍♀‍', '🧙', '🧙‍♂',
    '🧙‍♀', '🧚', '🧚‍♂', '🧚‍♀', '🧛', '🧛‍♂', '🧛‍♀', '🧜', '🧜‍♂', '🧜‍♀', '🧝', '🧝‍♂', '🧝‍♀', '🧞', '🧞‍♂',
    '🧞‍♀', '🧟', '🧟‍♂', '🧟‍♀', '💆', '💆‍♂', '💆‍♀', '💇', '💇‍♂', '💇‍♀', '🚶', '🚶‍♂', '🚶‍♀', '🏃', '🏃‍♂',
    '🏃‍♀', '💃', '🕺', '🕴', '👯', '👯‍♂', '👯‍♀', '🧖', '🧖‍♂', '🧖‍♀', '🧗', '🧗‍♂', '🧗‍♀', '🤺', '🏇', '⛷', '🏂',
    '🏌', '🏌️‍', '🏌️‍', '🏄', '🏄‍♂', '🏄‍♀', '🚣', '🚣‍♂', '🚣‍♀', '🏊', '🏊‍♂', '🏊‍♀', '⛹', '🏋', '🚴', '🚴‍♂',
    '🚴‍♀', '🚵', '🚵‍♂', '🚵‍♀', '🤸', '🤸‍♂', '🤸‍♀', '🤽', '🤽‍♂‍', '🤽‍♀‍', '🤾', '🤾‍♂‍', '🤾‍♀‍', '🤹', '🤹‍♂‍',
    '🤹‍♀‍', '🧘', '🧘‍♂‍', '🧘‍♀‍', '🛀', '🛌', '👪', '👨‍👩‍👦', '👨‍👩‍👧', '👨‍👩‍👧‍👦', '👨‍👩‍👦‍👦',
    '👨‍👩‍👧‍👧', '👨‍👨‍👦', '👨‍👨‍👧', '👨‍👨‍👧‍👦', '👨‍👨‍👦‍👦', '👨‍👨‍👧‍👧', '👩‍👩‍👦',
    '👩‍👩‍👧', '👩‍👩‍👧‍👦', '👩‍👩‍👦‍👦', '👩‍👩‍👧‍👧', '👨‍👦', '👨‍👦‍👦', '👨‍👧', '👨‍👧‍👦', '👨‍👧‍👧',
    '👩‍👦', '👩‍👦‍👦', '👩‍👧', '👩‍👧‍👦', '👩‍👧‍👧', '👫', '👬', '💏', '👩‍❤‍💋‍👨',
    '👨‍❤‍💋‍👨', '👩‍❤‍💋‍👩', '💑', '🗣', '👤', '👥',

]

_ANIMALS_AND_NATURE_EMOJIES = [
    '🐵', '🐒', '🦍', '🐶', '🐕', '🐩', '🐺', '🦊', '🦝', '🐱', '🐈', '🦁', '🐯', '🐅', '🐆', '🐴', '🐎', '🦄', '🦓',
    '🦌', '🐮', '🐄', '🐂', '🐃', '🐷', '🐖', '🐗', '🐽', '🐏', '🐑', '🐐', '🐪', '🐫', '🦙', '🦒', '🐘', '🦏', '🦛',
    '🐭', '🐁', '🐀', '🐹', '🐰', '🐇', '🐿', '🦔', '🦇', '🐻', '🐨', '🐼', '🦘', '🦡', '🐾', '🦃', '🐔', '🐓', '🐣',
    '🐤', '🐥', '🐦', '🐧', '🕊', '🦅', '🦆', '🦢', '🦉', '🦜', '🐸', '🐊', '🐢', '🦎', '🐍', '🐲', '🐉', '🦕', '🦖',
    '🐳', '🐋', '🐬', '🐟', '🐠', '🐡', '🦈', '🐙', '🐚', '🐌', '🦋', '🐛', '🐜', '🐝', '🐞', '🦗', '🕷', '🕸', '🦂',
    '🦟', '🦠', '💐', '🌸', '💮', '🏵', '🌹', '🥀', '🌺', '🌻', '🌼', '🌷', '🌱', '🌲', '🌳', '🌴', '🌵', '🌾', '🌿',
    '☘', '🍀', '🍁', '🍂', '🍃',
]

print(len(_PEOPLE_EMOJIES))
print(len(_ANIMALS_AND_NATURE_EMOJIES))
print('-----')
print(len(_PEOPLE_EMOJIES) + len(_ANIMALS_AND_NATURE_EMOJIES))


class EmojiCategory(Enum):
    PEOPLE = 1
    ANIMALS_NATURE = 2


class _EmojiCategoryButton(QToolButton):
    def __init__(self, parent=None):
        super(_EmojiCategoryButton, self).__init__(parent)
        transparent(self)
        pointy(self)
        self.setIconSize(QSize(24, 24))


class EmojiPicker(QWidget):
    def __init__(self, parent=None):
        super(EmojiPicker, self).__init__(parent)
        vbox(self)

        self._toolbar = QWidget(self)
        hbox(self._toolbar)

        self._emojiView = EmojiView(self)

        self.layout().addWidget(self._toolbar)
        self.layout().addWidget(self._emojiView)

        self._addCategoryFilter(EmojiCategory.PEOPLE)
        self._addCategoryFilter(EmojiCategory.ANIMALS_NATURE)

    def _addCategoryFilter(self, category: EmojiCategory):
        btnFilter = _EmojiCategoryButton()
        if category == EmojiCategory.PEOPLE:
            btnFilter.setIcon(qtawesome.icon('fa5.smile'))
        elif category == EmojiCategory.ANIMALS_NATURE:
            btnFilter.setIcon(qtawesome.icon('fa5s.dog'))

        btnFilter.clicked.connect(lambda: self._emojiView.scrollToCategory(category))
        self._toolbar.layout().addWidget(btnFilter)


class EmojiView(QScrollArea):
    def __init__(self, parent=None):
        super(EmojiView, self).__init__(parent)
        self._emojiFont = QFont('Noto Emoji')
        self._emojiFont.setPointSize(self._emojiFont.pointSize() + 6)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setWidgetResizable(True)

        widget = QWidget(self)
        widget.setPalette(QPalette(Qt.GlobalColor.white))
        self.setWidget(widget)
        self._layout = vbox(widget, spacing=4)

        self.setFrameStyle(QFrame.Shape.NoFrame)

        self._lblPerson = QLabel('Smileys & People')
        self._lblAnimals = QLabel('Animals & Nature')
        self._addEmojis(self._lblPerson, _PEOPLE_EMOJIES)
        self._addEmojis(self._lblAnimals, _ANIMALS_AND_NATURE_EMOJIES)

    def scrollToCategory(self, category: EmojiCategory):
        lbl = self._label(category)
        if lbl:
            self.verticalScrollBar().setValue(lbl.pos().y())

    def _addEmojis(self, title: QLabel, emojis: List[str]):
        incr_font(title)
        self._layout.addWidget(vspacer(25))
        self._layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignLeft)
        _widget = QWidget(self)
        _widget.setFont(self._emojiFont)
        flow(_widget, 2, 5)
        for _emoji in emojis:
            _widget.layout().addWidget(_EmojiLabel(_emoji, self))
        self._layout.addWidget(_widget)

    def _label(self, category: EmojiCategory):
        if category == EmojiCategory.PEOPLE:
            return self._lblPerson
        elif category == EmojiCategory.ANIMALS_NATURE:
            return self._lblAnimals


class _EmojiLabel(QLabel):
    clicked = Signal(str)

    def __init__(self, emoji: str, parent=None):
        super(_EmojiLabel, self).__init__(emoji, parent)
        self._emoji = emoji
        pointy(self)
        self.setAutoFillBackground(True)
        self._greyPalette = QPalette()
        self._greyPalette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.lightGray)
        self._whitePalette = QPalette()
        self._whitePalette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.white)

    def enterEvent(self, QEnterEvent):
        self.setPalette(self._greyPalette)

    def leaveEvent(self, QEvent):
        self.setPalette(self._whitePalette)

    def mousePressEvent(self, QMouseEvent):
        decr_font(self)

    def mouseReleaseEvent(self, QMouseEvent):
        incr_font(self)
        self.clicked.emit(self._emoji)
