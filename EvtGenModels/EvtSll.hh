
/***********************************************************************
* Copyright 1998-2020 CERN for the benefit of the EvtGen authors       *
*                                                                      *
* This file is part of EvtGen.                                         *
*                                                                      *
* EvtGen is free software: you can redistribute it and/or modify       *
* it under the terms of the GNU General Public License as published by *
* the Free Software Foundation, either version 3 of the License, or    *
* (at your option) any later version.                                  *
*                                                                      *
* EvtGen is distributed in the hope that it will be useful,            *
* but WITHOUT ANY WARRANTY; without even the implied warranty of       *
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        *
* GNU General Public License for more details.                         *
*                                                                      *
* You should have received a copy of the GNU General Public License    *
* along with EvtGen.  If not, see <https://www.gnu.org/licenses/>.     *
***********************************************************************/

#ifndef EVTSLL_HH
#define EVTSLL_HH

#include "EvtGenBase/EvtDecayAmp.hh"

class EvtParticle;

//Class to handle decays of the form SCALAR -> DIRAC DIRAC.

class EvtSll : public EvtDecayAmp {
  public:
    std::string getName() override;
    EvtDecayBase* clone() override;

    void init() override;

    void decay( EvtParticle* p ) override;
};

#endif
