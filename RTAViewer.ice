/***************************************************************************
    begin                : Mar 21 2014
    copyright            : (C) 2014 Andrea Zoli
    email                : zoli@iasfbo.inaf.it
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software for non commercial purpose              *
 *   and for public research institutes; you can redistribute it and/or    *
 *   modify it under the terms of the GNU General Public License.          *
 *   For commercial purpose see appropriate license terms                  *
 *                                                                         *
 ***************************************************************************/

#pragma once

module CTA
{

sequence<int> IntSeq;

interface RTAViewer
{
    idempotent void update(IntSeq telescopes, int evtnum);
};

};
