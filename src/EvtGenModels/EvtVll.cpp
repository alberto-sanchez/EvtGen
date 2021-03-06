
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

#include "EvtGenModels/EvtVll.hh"

#include "EvtGenBase/EvtDiracSpinor.hh"
#include "EvtGenBase/EvtGenKine.hh"
#include "EvtGenBase/EvtPDL.hh"
#include "EvtGenBase/EvtParticle.hh"
#include "EvtGenBase/EvtPatches.hh"
#include "EvtGenBase/EvtReport.hh"
#include "EvtGenBase/EvtVector4C.hh"

#include <iostream>
#include <stdlib.h>
#include <string>

std::string EvtVll::getName()
{
    return "VLL";
}

EvtDecayBase* EvtVll::clone()
{
    return new EvtVll;
}

void EvtVll::init()
{
    // check that there are 0 arguments
    checkNArg( 0 );
    checkNDaug( 2 );

    checkSpinParent( EvtSpinType::VECTOR );

    checkSpinDaughter( 0, EvtSpinType::DIRAC );
    checkSpinDaughter( 1, EvtSpinType::DIRAC );
}

void EvtVll::initProbMax()
{
    setProbMax( 1.0 );
}

void EvtVll::decay( EvtParticle* p )
{
    p->initializePhaseSpace( getNDaug(), getDaugs() );

    EvtParticle *l1, *l2;
    l1 = p->getDaug( 0 );
    l2 = p->getDaug( 1 );

    EvtVector4C l11, l12, l21, l22;
    l11 = EvtLeptonVCurrent( l1->spParent( 0 ), l2->spParent( 0 ) );
    l12 = EvtLeptonVCurrent( l1->spParent( 0 ), l2->spParent( 1 ) );
    l21 = EvtLeptonVCurrent( l1->spParent( 1 ), l2->spParent( 0 ) );
    l22 = EvtLeptonVCurrent( l1->spParent( 1 ), l2->spParent( 1 ) );

    EvtVector4C eps0 = p->eps( 0 );
    EvtVector4C eps1 = p->eps( 1 );
    EvtVector4C eps2 = p->eps( 2 );

    double M2 = p->mass();
    M2 *= M2;
    double m2 = l1->mass();
    m2 *= m2;

    double norm = 1.0 / sqrt( 2 * M2 + 4 * m2 - 4 * m2 * m2 / M2 );

    vertex( 0, 0, 0, norm * ( eps0 * l11 ) );
    vertex( 0, 0, 1, norm * ( eps0 * l12 ) );
    vertex( 0, 1, 0, norm * ( eps0 * l21 ) );
    vertex( 0, 1, 1, norm * ( eps0 * l22 ) );

    vertex( 1, 0, 0, norm * ( eps1 * l11 ) );
    vertex( 1, 0, 1, norm * ( eps1 * l12 ) );
    vertex( 1, 1, 0, norm * ( eps1 * l21 ) );
    vertex( 1, 1, 1, norm * ( eps1 * l22 ) );

    vertex( 2, 0, 0, norm * ( eps2 * l11 ) );
    vertex( 2, 0, 1, norm * ( eps2 * l12 ) );
    vertex( 2, 1, 0, norm * ( eps2 * l21 ) );
    vertex( 2, 1, 1, norm * ( eps2 * l22 ) );

    return;
}
