# Makefile for source rpm: xorg-x11-xinit
# $Id$
NAME := xorg-x11-xinit
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
