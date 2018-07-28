#!/bin/bash

NAME_ROOT=electrum-actinium
PYTHON_VERSION=3.5.4

# These settings probably don't need any change
export WINEPREFIX=/opt/wine64
export PYTHONDONTWRITEBYTECODE=1
export PYTHONHASHSEED=22

PYHOME=c:/python$PYTHON_VERSION
PYTHON="wine $PYHOME/python.exe -OO -B"


# Let's begin!
cd `dirname $0`
set -e

cd tmp

for repo in electrum-actinium electrum-actinium-locale electrum-actinium-icons; do
    if [ -d $repo ]; then
	cd $repo
	git pull
	git checkout master
	cd ..
    else
	URL=https://github.com/zcoinofficial/$repo.git
	git clone -b master $URL $repo
    fi
done

pushd electrum-actinium-locale
for i in ./locale/*; do
    dir=$i/LC_MESSAGES
    mkdir -p $dir
    msgfmt --output-file=$dir/electrum.mo $i/electrum.po || true
done
popd

pushd electrum-actinium
if [ ! -z "$1" ]; then
    git checkout $1
fi

VERSION=`git describe --tags`
echo "Last commit: $VERSION"
find -exec touch -d '2000-11-11T11:11:11+00:00' {} +
popd

rm -rf $WINEPREFIX/drive_c/electrum-actinium
cp -r electrum-actinium $WINEPREFIX/drive_c/electrum-actinium
cp electrum-actinium/LICENCE .
cp -r electrum-actinium-locale/locale $WINEPREFIX/drive_c/electrum-actinium/lib/
cp electrum-actinium-icons/icons_rc.py $WINEPREFIX/drive_c/electrum-actinium/gui/qt/

# Install frozen dependencies
$PYTHON -m pip install -r ../../deterministic-build/requirements.txt

# Workaround until they upload binary wheels themselves:
wget 'https://ci.appveyor.com/api/buildjobs/bwr3yfghdemoryy8/artifacts/dist%2Fpyblake2-1.1.0-cp35-cp35m-win32.whl' -O pyblake2-1.1.0-cp35-cp35m-win32.whl
$PYTHON -m pip install ./pyblake2-1.1.0-cp35-cp35m-win32.whl


$PYTHON -m pip install -r ../../deterministic-build/requirements-hw.txt

pushd $WINEPREFIX/drive_c/electrum-actinium
$PYTHON setup.py install
popd

cd ..

rm -rf dist/

# build standalone and portable versions
wine "C:/python$PYTHON_VERSION/scripts/pyinstaller.exe" --noconfirm --ascii --name $NAME_ROOT-$VERSION -w deterministic.spec

# set timestamps in dist, in order to make the installer reproducible
pushd dist
find -exec touch -d '2000-11-11T11:11:11+00:00' {} +
popd

# build NSIS installer
# $VERSION could be passed to the electrum.nsi script, but this would require some rewriting in the script iself.
wine "$WINEPREFIX/drive_c/Program Files (x86)/NSIS/makensis.exe" /DPRODUCT_VERSION=$VERSION electrum.nsi

cd dist
mv electrum-actinium-setup.exe $NAME_ROOT-$VERSION-setup.exe
cd ..

echo "Done."
md5sum dist/electrum*exe
