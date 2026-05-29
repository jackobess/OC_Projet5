#!/bin/bash
VERSION=$(python -c "from app.__version__ import __version__; print(__version__)")
echo "Tagging v$VERSION..."
git tag "v$VERSION"
git push origin "v$VERSION"
echo "Done."