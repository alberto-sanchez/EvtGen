
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

#include "EvtGenBase/EvtManyDeltaFuncLineShape.hh"

#include "EvtGenBase/EvtBlattWeisskopf.hh"
#include "EvtGenBase/EvtPDL.hh"
#include "EvtGenBase/EvtPatches.hh"
#include "EvtGenBase/EvtPropBreitWigner.hh"
#include "EvtGenBase/EvtPropBreitWignerRel.hh"
#include "EvtGenBase/EvtRandom.hh"
#include "EvtGenBase/EvtSpinType.hh"
#include "EvtGenBase/EvtTwoBodyVertex.hh"

EvtManyDeltaFuncLineShape::EvtManyDeltaFuncLineShape()
{
}

EvtManyDeltaFuncLineShape::EvtManyDeltaFuncLineShape( double mass, double width,
                                                      double maxRange,
                                                      EvtSpinType::spintype sp )
{
    _mass = mass;
    _width = width;
    _spin = sp;
    _maxRange = maxRange;

    double maxdelta = width;

    _massMax = mass + maxdelta;
    _massMin = mass - maxdelta;

    if ( _massMin < 0. )
        _massMin = 0.;
}

EvtManyDeltaFuncLineShape::EvtManyDeltaFuncLineShape(
    const EvtManyDeltaFuncLineShape& x ) :
    EvtAbsLineShape( x )
{
    _mass = x._mass;
    _width = x._width;
    _spin = x._spin;
    _massMax = x._massMax;
    _massMin = x._massMin;
    _maxRange = x._maxRange;
}

EvtManyDeltaFuncLineShape& EvtManyDeltaFuncLineShape::operator=(
    const EvtManyDeltaFuncLineShape& x )
{
    _mass = x._mass;
    _massMax = x._massMax;
    _massMin = x._massMin;
    _width = x._width;
    _maxRange = x._maxRange;
    _spin = x._spin;
    return *this;
}

EvtAbsLineShape* EvtManyDeltaFuncLineShape::clone()
{
    return new EvtManyDeltaFuncLineShape( *this );
}

double EvtManyDeltaFuncLineShape::getMassProb( double mass, double massPar,
                                               int nDaug, double* massDau )
{
    double dTotMass = 0.;

    int i;
    for ( i = 0; i < nDaug; i++ ) {
        dTotMass += massDau[i];
    }
    if ( ( mass < dTotMass ) )
        return 0.;

    if ( massPar > 0.0000000001 ) {
        if ( mass > massPar )
            return 0.;
    }

    return 1.;
}

double EvtManyDeltaFuncLineShape::getRandMass( EvtId*, int, EvtId*, EvtId*,
                                               double, double* )
{
    int nDelta = int( ( _massMax - _massMin ) / _width );
    nDelta++;
    double rand = EvtRandom::Flat( 0., float( nDelta ) );
    int randI = int( rand );
    return _massMin + randI * _width;
}
