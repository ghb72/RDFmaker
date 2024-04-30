# RDFmaker
This repository contains some functions to make RDFs (radial pair distribution functions) and other tools to operate with atomic models for nanoparticles in .xyz files.

OK, THIS JOB IS ONLY FOR NANOPARTICLES IN .XYZ FILES

The tools I present are:

-A RDF python program to make radial pair distribution functions

-Python functions: Read .xyz file, write .xyz file, change elements labels of .xyz files , show percentes of composition in .xyz files, cut spheres from a model, delete atoms (in a random way, or radial but random way), change atoms in a percent (random, or radial random)

-Graph RDFs, and the fraction of a selected element radiously, the number of atoms in some radius

-Check lines of a .xyz file to discover atoms in the same coordinates

-From a .xyz file make a LAMMPS coords file for a model

-Create Janus, Sandwich, core-shell dispositions for .xyz models

You'll need numpy, random, matplotlib, collections, sys and os libraries

At 29/04/2024 this is not the final version.
