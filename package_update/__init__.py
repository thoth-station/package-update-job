#!/usr/bin/env python3
# package-update-job
# Copyright(C) 2020 Kevin Postlethwait
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Keep packages up to date in our database."""

from thoth.common import __version__ as __common__version__
from thoth.storages import __version__ as __storages__version__
__name__ = "package-update"
__version__ = "0.8.5"
__service_version__ = f"{__version__}+storage.{__storages__version__}.common.{__common__version__}"
__author__ = "Kevin Postlethwait <k.postlethwait24@gmail.com>"
