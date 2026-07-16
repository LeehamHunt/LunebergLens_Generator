#Lüneburg Lens Generator

![Application Screenshot](images/application.png)

## Overview

The Lüneburg Lens Generator is a desktop application developed to automate the design and generation of gradient-index (GRIN) Lüneburg lenses for microwave and millimeter-wave applications. The software provides an intuitive graphical interface for creating parametrically defined lens geometries using gyroid unit cells suitable for electromagnetic simulation and additive manufacturing.

The objective of the project was to reduce the time required to generate complex lens geometries while providing flexibility for rapid design iteration and optimization.

---

## Features

* Interactive graphical user interface
* Parametric lens generation
* Adjustable lens diameter and discretization
* Configurable refractive index profiles
* Gyroid unit cell generation
* Exportable 3D geometry for simulation and fabrication

---

## Engineering Objectives

* Automate the generation of gradient-index lens geometries
* Reduce manual CAD modeling effort
* Support rapid design iteration
* Enable electromagnetic simulation workflows
* Produce geometries compatible with additive manufacturing

---

## Software Architecture

The application consists of four primary modules:

* User Interface
* Lens Geometry Generator
* Refractive Index Calculator
* Model Export Engine

![Software Architecture](images/architecture.png)

---

## Design Methodology

The lens generation process follows a fully parametric workflow:

1. Define lens dimensions
2. Calculate refractive index distribution
3. Generate gyroid unit cell geometry
4. Assemble the complete lens model
5. Export geometry for simulation or fabrication

The modular design allows rapid evaluation of alternative lens configurations while minimizing repetitive manual modeling.

---

## Graphical User Interface

The application was developed using PyQt6 to provide a user-friendly workflow for engineering design.

The interface allows users to:

* Configure lens parameters
* Preview generated geometries
* Adjust generation settings
* Export completed models

![GUI](images/gui.png)

---

## Applications

Potential applications include:

* Microwave antenna systems
* Gradient-index (GRIN) lenses
* Millimeter-wave communication
* Electromagnetic research
* Additive manufacturing of RF components

---

## Lessons Learned

This project strengthened experience in:

* Python application development
* Computational geometry
* GUI development
* Parametric design
* Engineering software development
* RF system design workflows

---

## Technologies Used

### Programming

* Python

### Libraries

* PyQt6
* NumPy

### Engineering

* Computational Geometry
* Parametric Design
* Gradient-Index Optics
* Electromagnetic Design
