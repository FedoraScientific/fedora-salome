#!/bin/sh

(
cd ./salome-smesh-plugin-hexablock/hexablockplugin
git checkout master
git remote add upstream http://git.salome-platform.org/gitpub/plugins/hexablockplugin.git
)
(
cd ./salome-gui/gui
git checkout master
git remote add upstream http://git.salome-platform.org/gitpub/modules/gui.git
)
(
cd ./salome-smesh-plugin-hexotic/hexoticplugin
git checkout master
git remote add upstream http://git.salome-platform.org/gitpub/plugins/hexoticplugin.git
)
(
cd ./salome-hexablock/hexablock
git checkout master
git remote add upstream http://git.salome-platform.org/gitpub/modules/hexablock.git
)
(
cd ./salome-yacs/yacs
git checkout master
git remote add upstream http://git.salome-platform.org/gitpub/modules/yacs.git
)
(
cd ./salome-smesh/smesh
git checkout master
git remote add upstream http://git.salome-platform.org/gitpub/modules/smesh.git
)
(
cd ./salome-jobmanager/jobmanager
git checkout master
git remote add upstream http://git.salome-platform.org/gitpub/modules/jobmanager.git
)
(
cd ./salome-paravis/paravis
git checkout master
git remote add upstream http://git.salome-platform.org/gitpub/modules/paravis.git
)
(
cd ./salome-smesh-plugin-netgen/netgenplugin
git checkout master
git remote add upstream http://git.salome-platform.org/gitpub/plugins/netgenplugin.git
)
(
cd ./salome-med/med
git checkout master
git remote add upstream http://git.salome-platform.org/gitpub/modules/med.git
)
(
cd ./salome-kernel/kernel
git checkout master
git remote add upstream http://git.salome-platform.org/gitpub/modules/kernel.git
)
(
cd ./salome-geom/geom
git checkout master
git remote add upstream http://git.salome-platform.org/gitpub/modules/geom.git
)
(
cd ./salome-homard/homard
git checkout master
git remote add upstream http://git.salome-platform.org/gitpub/modules/homard.git
)