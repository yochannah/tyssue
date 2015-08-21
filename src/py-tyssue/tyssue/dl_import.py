#! /usr/bin/env python
# -*- coding: utf-8 -*-
# tyssue -- a mulitphysics biological tissues simulation library
#
#
# addapted from graph_tool -- a general graph manipulation python module
#
# Copyright (C) 2006-2015 Tiago de Paula Peixoto <tiago@skewed.de>
# Copyright (C) 2015 Guillaume Gay <guillaume@damcb.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os.path

## see https://docs.python.org/3.4/whatsnew/3.3.html?highlight=dlfcn
from os import RTLD_LAZY, RTLD_GLOBAL

dl_flags = RTLD_LAZY | RTLD_GLOBAL

# try:
#     from DLFCN import RTLD_LAZY, RTLD_GLOBAL
#     dl_flags = RTLD_LAZY | RTLD_GLOBAL
# except ImportError:
#     # handle strange python installations, by importing from the deprecated dl
#     # module, otherwise from ctypes
#     try:
#         from dl import RTLD_LAZY, RTLD_GLOBAL
#         dl_flags = RTLD_LAZY | RTLD_GLOBAL
#     except ImportError:
#         from ctypes import RTLD_GLOBAL
#         dl_flags = RTLD_GLOBAL

__all__ = ["dl_import"]


def dl_import(import_expr):
    """Import module according to import_expr, but with RTLD_GLOBAL enabled."""
    # we need to get the locals and globals of the _calling_ function. Thus, we
    # need to go deeper into the call stack
    call_frame = sys._getframe(1)
    local_dict = call_frame.f_locals
    global_dict = call_frame.f_globals

    # RTLD_GLOBAL needs to be set in dlopen() if we want typeinfo and friends to
    # work properly across DSO boundaries. See http://gcc.gnu.org/faq.html#dso

    orig_dlopen_flags = sys.getdlopenflags()
    sys.setdlopenflags(dl_flags)

    try:
        exec(import_expr, local_dict, global_dict)
    finally:
        sys.setdlopenflags(orig_dlopen_flags)  # reset it to normal case to
                                               # avoid unnecessary symbol
                                               # collision