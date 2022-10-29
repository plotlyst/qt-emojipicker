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

    '🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘', '🌙', '🌚', '🌛', '🌜', '🌡', '☀', '🌝', '🌞', '🪐', '⭐', '🌟',
    '🌠', '🌌', '☁', '⛅', '⛈', '🌤', '🌥', '🌦', '🌧', '🌨', '🌩', '🌪', '🌫', '🌬', '🌀', '🌈', '🌂', '☂', '☔', '⛱',
    '⚡', '❄', '☃', '⛄', '☄', '🔥', '💧', '🌊',
]

_FOOD_AND_DRINK = [
    '🍇', '🍈', '🍉', '🍊', '🍋', '🍌', '🍍', '🥭', '🍎', '🍏', '🍐', '🍑', '🍒', '🍓', '🫐', '🥝', '🍅', '🫒', '🥥',
    '🥑', '🍆', '🥔', '🥕', '🌽', '🌶', '🫑', '🥒', '🥬', '🥦', '🧄', '🧅', '🍄', '🥜', '🫑', '🌰', '🍞', '🥐', '🥖',
    '🫓', '🥨', '🥯', '🥞', '🧇', '🧀', '🍖', '🍗', '🥩', '🥓', '🍔', '🍟', '🍕', '🌭', '🥪', '🌮', '🌯', '🫔', '🥙',
    '🧆', '🥚', '🍳', '🥘', '🍲', '🫕', '🥣', '🥗', '🍿', '🧈', '🧂', '🥫', '🍱', '🍘', '🍙', '🍚', '🍛', '🍜', '🍝',
    '🍠', '🍢', '🍣', '🍤', '🍥', '🥮', '🍡', '🥟', '🥠', '🥡', '🦀', '🦞', '🦐', '🦑', '🦪', '🍨', '🍧', '🍦', '🍩',
    '🍪', '🎂', '🍰', '🧁', '🥧', '🍫', '🍬', '🍭', '🍮', '🍯', '🍼', '🥛', '☕', '🫖', '🍵', '🍶', '🍾', '🍷', '🍸',
    '🍹', '🍺', '🍻', '🥂', '🥃', '🥤', '🧋', '🧃', '🧉', '🧊', '🥢', '🍽', '🍴', '🥄', '🔪', '🧋', '🏺',
]

_TRAVEL_AND_PLACES = [
    '🌍', '🌎', '🌏', '🌐', '🗺', '🧭', '⛰', '🏔', '🌋', '🗻', '🏕', '🏖', '🏜', '🏝', '🏞', '🏟', '🏛', '🏗', '🧱',
    '🪨', '🪵', '🛖', '🏘', '🏚', '🏠', '🏡', '🏢', '🏣', '🏤', '🏥', '🏦', '🏨', '🏩', '🏪', '🏫', '🏬', '🏭', '🏯',
    '🏰', '💒', '🗼', '🗽', '⛪', '🕌', '🛕', '🕍', '⛩', '🕋', '⛲', '⛺', '🌁', '🌃', '🏙', '🌅', '🌄', '🌆', '🌇', '🌉',
    '♨', '🎠', '🎡', '🎢', '💈', '🎪', '🚂', '🚃', '🚄', '🚅', '🚆', '🚇', '🚈', '🚉', '🚊', '🚝', '🚞', '🚋', '🚌',
    '🚍', '🚎', '🚐', '🚑', '🚒', '🚓', '🚔', '🚕', '🚖', '🚗', '🚘', '🚙', '🛻', '🚚', '🚛', '🚜', '🏎', '🏍', '🛵',
    '🦽', '🦼',
]

_ACTIVITIES = [

    '🎃', '🎄', '🎆', '🎇', '🧨', '✨', '🎈', '🎉', '🎊', '🎋', '🎍', '🎎', '🎏', '🎑', '🧧', '🎀', '🎁', '🎗', '🎟',
    '🎫', '🎖', '🏆', '🏅', '🥇', '🥈', '🥉', '⚽', '⚾', '🥎', '🏀', '🏐', '🏈', '🏉', '🎾', '🥏', '🎳', '🏏', '🏑',
    '🏒', '🥍', '🏓', '🏸', '🥊', '🥋', '🥅', '⛳', '⛸', '🎣', '🤿', '🎽', '🎿', '🛷', '🥌', '🎯', '🪀', '🪁', '🎱',
    '🔮', '🪄', '🧿', '🪄', '🎮', '🕹', '🎰', '🎲', '🧩', '🧸', '🪅', '🪆', '🪆', '♠', '♥', '♣', '♟', '🃏', '🀄', '🎴',
    '🎭', '🖼', '🎨', '🧵', '🪡', '🧶', '🪢', '🎷', '🪗', '🎸', '🎹', '🎺', '🎻', '🪕', '🥁', '🪘',
]

_OBJECTS = [
    '⌛', '⏳', '⌚', '⏰', '⏱', '⏲', '🕰', '🕛', '🕧', '🕐', '🕜', '🕑', '🕝', '🕒', '🕞', '🕓', '🕟', '🕔', '🕠', '🕕',
    '🕡', '🕖', '🕢', '🕗', '🕣', '🕘', '🕤', '🕙', '🕥', '🕚', '🕦', '👓', '🕶', '🥽', '🥼', '🦺', '👔', '👕', '👖',
    '🧣', '🧤', '🧥', '🧦', '👗', '👘', '🥻', '🩱', '🩲', '🩳', '👙', '👚', '👛', '👜', '👝', '🛍', '🎒', '🩴', '👞',
    '👟', '🥾', '🥿', '👠', '👡', '🩰', '👢', '👑', '👒', '🎩', '🎓', '🧢', '🪖', '⛑', '📿', '💄', '💍', '💎', '✏', '✒',
    '🖋', '🖊', '🖌', '🖍', '📝', '💼', '📁', '📂', '🗂', '📅', '📆', '📇', '📈', '📉', '📊', '📋', '📌', '📍', '📎',
    '🖇', '📏', '📐', '✂', '🗃', '🗄', '🗑', '🔨', '🪓', '⛏', '⚒', '🛠', '🗡', '⚔', '🔫', '🪃', '🏹', '🛡', '🪚', '🔧',
    '🪛', '🔩', '⚙', '🗜', '⚖', '🦯', '🔗', '⛓', '🪝', '🧰', '🧲', '🪜', '🚪', '🛗', '🪞', '🪟', '🛏', '🛋', '🪑', '🚽',
    '🪠', '🚿', '🛁', '🪤', '🪒', '🧴', '🧷', '🧹', '🧺', '🧻', '🪣', '🧼', '🫧', '🪥', '🧽', '🧯', '🛒', '🚬', '⚰',
    '🪦', '⚱', '🗿', '🪧', '🪪',
]

_SYMBOLS = [
    '🔇', '🔈', '🔉', '🔊', '📢', '📣', '📯', '🔔', '🔕', '🎼', '🎵', '🎶', '🎙', '🎚', '🎛', '🎤', '🎧', '📻', '📱',
    '📲', '☎', '📞', '📟', '📠', '🔋', '🪫', '🔌', '💻', '🖥', '🖨', '⌨', '🖱', '🖲', '💽', '💾', '💿', '📀', '🧮',
    '🎥', '🎞', '📽', '🎬', '📺', '📷', '📸', '📹', '📼', '🔍', '🔎', '🕯', '💡', '🔦', '🏮', '📔', '📕', '📖', '📗',
    '📘', '📙', '📚', '📓', '📒', '📃', '📜', '📄', '📰', '🗞', '📑', '🔖', '🏷', '💰', '🪙', '💴', '💵', '💶', '💷',
    '💸', '💳', '🧾', '💹', '✉', '📧', '📩', '📤', '📥', '📦', '📫', '📪', '📬', '📭', '📮', '🗳', '🔒', '🔓', '🔏',
    '🔐', '🔑', '🗝', '⚗', '🧪', '🧫', '🧬', '🔬', '🔭', '📡', '💉', '🩸', '💊', '🩹', '🩼', '🩺', '🩻', '🏧', '🚮',
    '🚰', '♿', '🚹', '🚺', '🚻', '🚼', '🚾', '🛂', '🛂', '🛄', '🛅', '⚠', '🚸', '⛔', '🚫', '🚳', '🚭', '🚯', '🚱',
    '🚷', '📵', '🔞', '☢', '☣', '⬆', '↗', '➡', '↘', '⬇', '↙', '⬅', '↖', '↕', '↔', '↩', '↪', '⤴', '⤵', '🔃', '🔄', '🔙',
    '🔚', '🔛', '🔜', '🔝', 'R', '🛐', '⚛', '🕉', '✡', '☸', '☯', '✝', '☦', '☪', '☮', '🕎', '🔯', 'Z', '♈', '♉', '♊',
    '♋', '♌', '♍', '♎', '♏', '♐', '♑', '♒', '♓', '⛎', 'A', '🔀', '🔁', '🔂', '▶', '⏸', '⏩', '⏭', '⏯', '◀', '⏪', '⏮',
    '🔼', '⏫', '🔽', '⏬', '⏹', '⏺', '⏏', '🎦', '🔅', '🔆', '📶', '📳', '📴', 'G', '♀', '♂', '⚧', 'M', '✖', '➕', '➖',
    '➗', '🟰', '♾', 'P', '‼', '⁉', '❓', '❔', '❗', '❕', '〰', 'C', '💱', '💲', 'O', '⚕', '♻', '⚜', '🔱', '📛', '🔰', '⭕',
    '✅', '☑', '✔', '❌', '❎', '➰', '➿', '〽', '✳', '✴', '❇', '©', '®', '™', 'K', '#', '*', '0', '1', '2', '3', '4', '5',
    '6', '7', '8', '9', '🔟', 'A', '🔠', '🔡', '🔢', '🔣', '🔤', '🅰', '🆎', '🅱', '🅾', '🆑', '🆒', '🆓', 'ℹ', '🆔',
    'Ⓜ', '🆕', '🆖', '🆗', '🅿', '🆘', '🆙', '🆚', 'J', '🈁', '🈂', '🈷', '🈶', '🈯', '🉐', '🈹', '🈚', '🈲', '🉑',
    '🈸', '🈴', '🈳', '㊗', '㊙', '🈺', '🈵', 'G', '🔴', '🟠', '🟡', '🟢', '🔵', '🟣', '🟤', '⚫', '⚪', '🟥', '🟧', '🟨',
    '🟩', '🟦', '🟪', '🟫', '⬛', '⬜', '🔶', '🔷', '🔸', '🔹', '🔺', '🔻', '💠', '🔘', '🔳', '🔲',
]

_FLAGS = [
    '🏁', '🚩', '🎌', '🏴', '🏳', '🏳️‍🌈', '🏳️‍⚧', '🏴‍☠️', '🇦🇨', '🇦🇩', '🇦🇪', '🇦🇫', '🇦🇬', '🇦🇮', '🇦🇱',
    '🇦🇲', '🇦🇴', '🇦🇶', '🇦🇷', '🇦🇸', '🇦🇹', '🇦🇺', '🇦🇼', '🇦🇽', '🇦🇿', '🇧🇦', '🇧🇧', '🇧🇩', '🇧🇪',
    '🇧🇫', '🇧🇬', '🇧🇭', '🇧🇮', '🇧🇯', '🇧🇱', '🇧🇲', '🇧🇳', '🇧🇴', '🇧🇶', '🇧🇷', '🇧🇸', '🇧🇹', '🇧🇻',
    '🇧🇼', '🇧🇾', '🇧🇿', '🇨🇦', '🇨🇨', '🇨🇩', '🇨🇫', '🇨🇬', '🇨🇭', '🇨🇮', '🇨🇰', '🇨🇱', '🇨🇲', '🇨🇳',
    '🇨🇴', '🇨🇵', '🇨🇷', '🇨🇺', '🇨🇻', '🇨🇼', '🇨🇽', '🇨🇾', '🇩🇪', '🇩🇬', '🇩🇯', '🇩🇰', '🇩🇲', '🇩🇴',
    '🇩🇿', '🇪🇦', '🇪🇨', '🇪🇪', '🇪🇬', '🇪🇭', '🇪🇷', '🇪🇸', '🇪🇹', '🇪🇺', '🇫🇮', '🇫🇯', '🇫🇰', '🇫🇲',
    '🇫🇴', '🇫🇷', '🇬🇦', '🇬🇧', '🇬🇩', '🇬🇪', '🇬🇫', '🇬🇬', '🇬🇭', '🇬🇮', '🇬🇱', '🇬🇲', '🇬🇳', '🇬🇵',
    '🇬🇶', '🇬🇷', '🇬🇸', '🇬🇹', '🇬🇺', '🇬🇼', '🇬🇾', '🇭🇰', '🇭🇲', '🇭🇳', '🇭🇷', '🇭🇹', '🇭🇺', '🇮🇨',
    '🇮🇩', '🇮🇪', '🇮🇱', '🇮🇲', '🇮🇳', '🇮🇴', '🇮🇶', '🇮🇷', '🇮🇸', '🇮🇹', '🇯🇪', '🇯🇲', '🇯🇴', '🇯🇵',
    '🇰🇪', '🇰🇬', '🇰🇭', '🇰🇭', '🇰🇮', '🇰🇲', '🇰🇳', '🇰🇵', '🇰🇷', '🇰🇼', '🇰🇾', '🇰🇿', '🇱🇦', '🇱🇧',
    '🇱🇨', '🇱🇮', '🇱🇰', '🇱🇷', '🇱🇸', '🇱🇹', '🇱🇻', '🇱🇾', '🇲🇦', '🇲🇨', '🇲🇩', '🇲🇪', '🇲🇬', '🇲🇭',
    '🇲🇰', '🇲🇱', '🇲🇲', '🇲🇳', '🇲🇴', '🇲🇵', '🇲🇶', '🇲🇷', '🇲🇸', '🇲🇹', '🇲🇺', '🇲🇻', '🇲🇼', '🇲🇽',
    '🇲🇾', '🇲🇿', '🇳🇦', '🇳🇨', '🇳🇪', '🇳🇫', '🇳🇬', '🇳🇮', '🇳🇱', '🇳🇴', '🇳🇵', '🇳🇷', '🇳🇺', '🇳🇿',
    '🇴🇲', '🇵🇦', '🇵🇪', '🇵🇫', '🇵🇬', '🇵🇭', '🇵🇰', '🇵🇱', '🇵🇲', '🇵🇳', '🇵🇷', '🇵🇸', '🇵🇹', '🇵🇼',
    '🇵🇾', '🇶🇦', '🇷🇪', '🇷🇸', '🇷🇺', '🇷🇼', '🇸🇦', '🇸🇧', '🇸🇨', '🇸🇩', '🇸🇪', '🇸🇬', '🇸🇭', '🇸🇮',
    '🇸🇯', '🇸🇰', '🇸🇱', '🇸🇲', '🇸🇳', '🇸🇴', '🇸🇷', '🇸🇸', '🇸🇹', '🇸🇻', '🇸🇽', '🇸🇾', '🇸🇿', '🇹🇦',
    '🇹🇨', '🇹🇩', '🇹🇫', '🇹🇬', '🇹🇭', '🇹🇯', '🇹🇰', '🇹🇱', '🇹🇲', '🇹🇳', '🇹🇴', '🇹🇷', '🇹🇹', '🇹🇻',
    '🇹🇼', '🇹🇿', '🇺🇦', '🇺🇬', '🇺🇲', '🇺🇳', '🇺🇸', '🇺🇾', '🇺🇿', '🇻🇦', '🇻🇨', '🇻🇪', '🇻🇬', '🇻🇮',
    '🇻🇮', '🇻🇺', '🇼🇫', '🇼🇸', '🇽🇰', '🇾🇪', '🇾🇹', '🇿🇦', '🇿🇲', '🇿🇼', '🏴󠁧󠁢󠁥󠁮󠁧󠁿', '🏴󠁧󠁢󠁳󠁣󠁴󠁿',
    '🏴󠁧󠁢󠁷󠁬󠁳󠁿',

]


class EmojiCategory(Enum):
    PEOPLE = 1
    ANIMALS_NATURE = 2
    FOOD_AND_DRINK = 3
    TRAVEL_AND_PLACES = 4
    ACTIVITIES = 5
    OBJECTS = 6
    SYMBOLS = 7
    FLAGS = 8


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
        palette = QPalette()
        self.setAutoFillBackground(True)
        palette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.white)
        self.setPalette(palette)

        self._toolbar = QWidget(self)
        hbox(self._toolbar)

        self._emojiView = EmojiView(self)

        self.layout().addWidget(self._toolbar)
        self.layout().addWidget(self._emojiView)

        self._addCategoryFilter(EmojiCategory.PEOPLE)
        self._addCategoryFilter(EmojiCategory.ANIMALS_NATURE)
        self._addCategoryFilter(EmojiCategory.FOOD_AND_DRINK)
        self._addCategoryFilter(EmojiCategory.TRAVEL_AND_PLACES)
        self._addCategoryFilter(EmojiCategory.ACTIVITIES)
        self._addCategoryFilter(EmojiCategory.OBJECTS)
        self._addCategoryFilter(EmojiCategory.SYMBOLS)
        self._addCategoryFilter(EmojiCategory.FLAGS)

    def _addCategoryFilter(self, category: EmojiCategory):
        btnFilter = _EmojiCategoryButton()
        if category == EmojiCategory.PEOPLE:
            btnFilter.setIcon(qtawesome.icon('fa5.smile'))
        elif category == EmojiCategory.ANIMALS_NATURE:
            btnFilter.setIcon(qtawesome.icon('fa5s.dog'))
        elif category == EmojiCategory.FOOD_AND_DRINK:
            btnFilter.setIcon(qtawesome.icon('fa5s.hamburger'))
        elif category == EmojiCategory.TRAVEL_AND_PLACES:
            btnFilter.setIcon(qtawesome.icon('fa5s.car'))
        elif category == EmojiCategory.ACTIVITIES:
            btnFilter.setIcon(qtawesome.icon('fa5s.basketball-ball'))
        elif category == EmojiCategory.OBJECTS:
            btnFilter.setIcon(qtawesome.icon('fa5s.camera'))
        elif category == EmojiCategory.SYMBOLS:
            btnFilter.setIcon(qtawesome.icon('fa5s.hashtag'))
        elif category == EmojiCategory.FLAGS:
            btnFilter.setIcon(qtawesome.icon('fa5s.flag'))

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
        self.setWidget(widget)
        self._layout = vbox(widget, spacing=4)

        self.setFrameStyle(QFrame.Shape.NoFrame)

        self._lblPerson = QLabel('Smileys & People')
        self._lblAnimals = QLabel('Animals & Nature')
        self._lblFood = QLabel('Food & Drink')
        self._lblTravel = QLabel('Travel & Places')
        self._lblActivities = QLabel('Activities')
        self._lblObjects = QLabel('Objects')
        self._lblSymbols = QLabel('Symbols')
        self._lblFlags = QLabel('Flags')
        self._addEmojis(self._lblPerson, _PEOPLE_EMOJIES)
        self._addEmojis(self._lblAnimals, _ANIMALS_AND_NATURE_EMOJIES)
        self._addEmojis(self._lblFood, _FOOD_AND_DRINK)
        self._addEmojis(self._lblTravel, _TRAVEL_AND_PLACES)
        self._addEmojis(self._lblActivities, _ACTIVITIES)
        self._addEmojis(self._lblObjects, _OBJECTS)
        self._addEmojis(self._lblSymbols, _SYMBOLS)
        self._addEmojis(self._lblFlags, _FLAGS)

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
        elif category == EmojiCategory.FOOD_AND_DRINK:
            return self._lblFood
        elif category == EmojiCategory.TRAVEL_AND_PLACES:
            return self._lblTravel
        elif category == EmojiCategory.ACTIVITIES:
            return self._lblActivities
        elif category == EmojiCategory.OBJECTS:
            return self._lblObjects
        elif category == EmojiCategory.SYMBOLS:
            return self._lblSymbols
        elif category == EmojiCategory.FLAGS:
            return self._lblFlags


class _EmojiLabel(QLabel):
    clicked = Signal(str)

    def __init__(self, emoji_: str, parent=None):
        super(_EmojiLabel, self).__init__(emoji_, parent)
        self._emoji = emoji_
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
