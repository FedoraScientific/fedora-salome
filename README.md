Salome Fedora Packaging
=======================

Initial setup:
--------------
```
    git clone --recursive git@github.com:fedora-scientific/fedora-salome.git
    cd fedora-salome
    ./add-upstream-origins.sh
```

Layout:
-------

* Each `salome-<name>` directory contains a spec file and a clone of the
  respective source tree.
* The clone of the source tree contains two branches, `master` and `fedora`.
  The `fedora` branch carries all the patches needed for the fedora package
* Each source tree clone has two remotes, `master` (the github repo) and
  `upstream` (the upstream repo at git.salome-platform.org)

Workflow:
---------

* Updating an existing module/plugin
    ```
    cd salome-<name>/<name>
    ../../salome_gensources.sh <tag>
    ```
  Tag is i.e. `7_5_0b1`. This script will generate a tarball for the specified
  tag, rebase the commits in the `fedora` branch and generate the patches.
  Patches and tarball are created in the directory above the source tree.

* Adding a new module
    ```
    mkdir salome-<name>
    cd salome-<name>
    git clone http://git.salome-platform.org/gitpub/modules/<name>.git
    cd <name>

    # Create github repo on github.com called salome-<name>
    git remote rename origin upstream
    git remote add origin git@github.com:fedora-scientific/salome-<name>.git

    git checkout -b fedora /V<tag>
    # Fedora specific patching

    git push -u origin master
    git push -u origin fedora
    ```
* Adding a new plugin: similar as for module, but clone as
    ```
    git clone http://git.salome-platform.org/gitpub/plugins/<name>.git
    ```
  and use `salome-<module>-plugin-<name>` as github repo name.

Status:
-------
* salome-geom:
    - fails to build due to bad linking flags
* salome-gui:
    - 7.5.0b1 builds, untested
    - 7.4.1 appeared to work
* salome-hexablock:
    - cannot build 7.5.0b1 due to missing geom
    - 7.4.1 appeared to work
* salome-homard:
    - cannot build 7.5.0b1 due to missing geom
    - in 7.4.1 it failed to appear in the gui
* salome-jobmanager:
    - 7.5.0b1 not built
    - in 7.4.1 it failed to appear in gui
* salome-kernel:
    - 7.5.0b1 builds, untested
    - 7.4.1 appeared to work, except new-style runner appliskel/salome does not work
* salome-med:
    - 7.5.0b1 not built
    - 7.4.1 appeared to work
* salome-paravis:
    - 7.5.0b1 not built
    - 7.4.1 crashes
* salome-smesh:
    - cannot build 7.5.0b1 due to missing geom
    - 7.4.1 appeared to work
* salome-smesh-plugin-hexablock:
    - 7.5.0b1 not built
    - 7.4.1 untested
* salome-smesh-plugin-hexotic:
    - 7.5.0b1 not built
    - 7.4.1 untested
* salome-smesh-plugin-netgen:
    - 7.5.0b1 not built
    - 7.4.1 untested
* salome-yacs:
    - 7.5.0b1 not built
    - 7.4.1 appeared to work, build complained about
    ```
    /builddir/build/BUILD/YACS_SRC_7.4.0rc1/doc/yacsgen.rst:1493: WARNING: autodoc: failed to import module u'module_generator'; the following exception was raised:
    Traceback (most recent call last):
      File "/usr/lib/python2.7/site-packages/sphinx/ext/autodoc.py", line 335, in import_object
        __import__(self.modname)
    ImportError: No module named module_generator
    ```
 