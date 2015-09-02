//--------------------------------------------------------------------------
//
// Environment:
//      This software is part of the EvtGen package developed jointly
//      for the BaBar and CLEO collaborations.  If you use all or part
//      of it, please give an appropriate acknowledgement.
//
// Copyright Information: See EvtGen/COPYRIGHT
//      Copyright (C) 2000      Caltech, UCSB
//
// Module: EvtGen/EvtbTosllBall.hh
//
// Description:Implementation of the b->sll decays according to Ball et al.
//
// Modification history:
//
//    Ryd     January 5, 2000         Module created
//
//------------------------------------------------------------------------

#ifndef EVTBTOSLLBALL_HH
#define EVTBTOSLLBALL_HH


#include "EvtGenBase/EvtDecayAmp.hh"

class EvtbTosllFF;
class EvtbTosllAmp;
class EvtParticle;

class EvtbTosllBall:public  EvtDecayAmp  {

public:

  EvtbTosllBall() {}
  virtual ~EvtbTosllBall();

  void getName(std::string& name);
  EvtDecayBase* clone();

  void decay(EvtParticle *p);
  void init();
  void initProbMax();

private:
  EvtbTosllFF *_ballffmodel;
  EvtbTosllAmp *_calcamp;
  double _poleSize;
};

#endif

