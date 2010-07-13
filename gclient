#!/bin/bash
# Copyright (c) 2009 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# This script will try to sync the bootstrap directories and then defer control.

base_dir=$(dirname "$0")

# Test git and git --version.
function test_git {
  local GITV="$(git --version)" || {
    echo "git isn't installed, please install it"
    exit 1
  }

  GITV="${GITV##* }"          # Only examine last word (i.e. version number)
  local GITD=( ${GITV//./ } ) # Split version number into decimals
  if ((GITD[0] < 1 || (GITD[0] == 1 && GITD[1] < 6) )); then
    echo "git version is ${GITV}, please update to a version later than 1.6"
    exit 1
  fi
}

# Test git svn and git svn --version.
function test_git_svn {
  local GITV="$(git svn --version)" || {
    echo "git-svn isn't installed, please install it"
    exit 1
  }

  GITV="${GITV#* version }"   # git svn --version has extra output to remove.
  GITV="${GITV% (svn*}"
  local GITD=( ${GITV//./ } ) # Split version number into decimals
  if ((GITD[0] < 1 || (GITD[0] == 1 && GITD[1] < 6) )); then
    echo "git version is ${GITV}, please update to a version later than 1.6"
    exit 1
  fi
}


# Update git checkouts prior the cygwin check, we don't want to use msysgit.
if [ "X$DEPOT_TOOLS_UPDATE" != "X0" -a -e "$base_dir/.git" ]
then
  cd $base_dir
  test_git_svn
  # work around a git-svn --quiet bug
  OUTPUT=`git svn rebase -q -q`
  if [[ ! "$OUTPUT" =~ Current.branch ]]; then
    echo $OUTPUT
  fi
  cd - > /dev/null
fi

# Use the batch file as an entry point if on cygwin.
if [ "${OSTYPE}" = "cygwin" -a "${TERM}" != "xterm" ]; then
   ${base_dir}/gclient.bat "$@"
   exit
fi


# We're on POSIX (not cygwin). We can now safely look for svn checkout.
if [ "X$DEPOT_TOOLS_UPDATE" != "X0" -a -e "$base_dir/.svn" ]
then
  # Update the bootstrap directory to stay up-to-date with the latest
  # depot_tools.
  svn -q up "$base_dir"
fi

exec python "$base_dir/gclient.py" "$@"
