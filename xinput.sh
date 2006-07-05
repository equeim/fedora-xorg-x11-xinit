#!/bin/bash
# Copyright (C) 1999 - 2004 Red Hat, Inc. All rights reserved. This
# copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the
# GNU General Public License version 2.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
# X Input method setup script

USER_XINPUTRC="$HOME/.xinputrc"
SYS_XINPUTRC="/etc/X11/xinit/xinputrc"

# Load up the user and system locale settings
oldterm=$TERM
unset TERM
if [ -r /etc/profile.d/lang.sh ]; then
    source /etc/profile.d/lang.sh
fi
[ -n "$oldterm" ] && export TERM=$oldterm

tmplang=${LC_CTYPE:-${LANG:-"en_US.UTF-8"}}

# unset env vars to be safe
unset XIM XIM_PROGRAM XIM_ARGS XMODIFIERS GTK_IM_MODULE QT_IM_MODULE

if [ -r "$USER_XINPUTRC" ]; then
    source "$USER_XINPUTRC"
elif [ -r "$SYS_XINPUTRC" ]; then
    source "$SYS_XINPUTRC"
fi

[ -n "$GTK_IM_MODULE" ] && export GTK_IM_MODULE
[ -n "$QT_IM_MODULE" ] && export QT_IM_MODULE

# setup XMODIFIERS
[ -z "$XMODIFIERS" -a -n "$XIM" ] && XMODIFIERS="@im=$XIM"
[ -n "$XMODIFIERS" ] && export XMODIFIERS

# execute XIM_PROGRAM
[ -n "$XIM_PROGRAM" ] && which "$XIM_PROGRAM" > /dev/null 2>&1 && LANG="$tmplang" "$XIM_PROGRAM" $XIM_ARGS &
