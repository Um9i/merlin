# This file is part of Merlin/Arthur.
# Merlin/Arthur is the Copyright (C)2009 of Elliot Rosemarine.

# Individual portions may be copyright by individual contributors, and
# are included in this collective work with permission of the copyright
# owners.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
 
from datetime import datetime
from django.http import HttpResponseRedirect
from sqlalchemy.sql import asc, desc
from Core.db import session
from Core.maps import Updates, Galaxy, Planet, PlanetHistory, Alliance, Intel
from Arthur.auth import render

def galaxy(request, x, y):
    now = datetime.now()
    d1 = datetime(now.year, now.month, now.day, now.hour)
    d2 = datetime(now.year, now.month, now.day)
    hours = (d1-d2).seconds/60/60
    tick = Updates.current_tick() - hours
    
    galaxy = Galaxy.load(x,y)
    if galaxy is None:
        return HttpResponseRedirect("/galaxies/")
    gh = galaxy.history(tick)
    
    Q = session.query(Planet, PlanetHistory, Intel.nick, Alliance.name)
    Q = Q.outerjoin(Planet.intel)
    Q = Q.outerjoin(Intel.alliance)
    Q = Q.outerjoin(Planet.history_loader)
    Q = Q.filter(PlanetHistory.tick == tick)
    Q = Q.filter(Planet.galaxy == galaxy)
    Q = Q.order_by(asc(Planet.z))
    return render("planets.tpl", request, planets=Q.all(), title=galaxy.name, intel=True, galaxy=galaxy, gh=gh)
