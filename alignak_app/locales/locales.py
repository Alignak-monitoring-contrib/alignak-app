#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2018:
#   Matthieu Estrada, ttamalfor@gmail.com
#
# This file is part of (AlignakApp).
#
# (AlignakApp) is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# (AlignakApp) is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with (AlignakApp).  If not, see <http://www.gnu.org/licenses/>.

"""
    Locales
    +++++++
    Locales manage localization of Alignak-app
"""

import os
import sys
from gettext import GNUTranslations, NullTranslations
from logging import getLogger

from alignak_app.utils.config import settings

logger = getLogger(__name__)


def init_localization():  # pragma: no cover
    """
    Application localization

    :return: gettext translator method
    :rtype: method
    """
    try:
        # Language message file
        lang_filename = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "LC_MESSAGES/%s.mo" % settings.get_config('Alignak-app', 'locale')
        )
        logger.info(
            "Opening message file %s for locale %s",
            lang_filename, settings.get_config('Alignak-app', 'locale')
        )
        translation = GNUTranslations(open(lang_filename, "rb"))
        translation.install()
        _ = translation.gettext
    except IOError:
        logger.warning("Locale not found. Using default language messages (English)")
        null_translation = NullTranslations()
        null_translation.install()
        _ = null_translation.gettext
    except Exception as e:  # pragma: no cover - should not happen
        logger.error("Locale not found. Exception: %s", str(e))
        null_translation = NullTranslations()
        null_translation.install()
        _ = null_translation.gettext

    return _
