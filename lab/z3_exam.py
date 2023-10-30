#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    extract-concat.py -
#    Copyright (C) 2014 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from z3 import *

a = BitVecVal(0x1,4)
a1 = BitVecVal(0x2,4)
a2 = BitVecVal(0x3,4)
a3 = BitVecVal(0x4,4)

# sic = 1^Extract(0, 0, a)^Extract(1, 1, a)^Extract(2, 2, a)^Extract(3, 3, a)^Extract(4, 4, a)^Extract(5, 5, a)^Extract(6, 6, a)^Extract(7, 7, a)
# print(sic)
# print(simplify(sic))
# print(sic.size())
con = Concat(a, a1, a2, a3)
print(simplify(con))

c = BitVecVal(0x1234, 16)
e = Extract(15, 4, c)
print(hex((simplify(e)).as_long()))
