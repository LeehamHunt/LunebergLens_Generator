
# gui_qt.py
# Qt-based GUI for gyroidal sphere generator with full features

import sys
import numpy as np
import pyvista as pv
from pyvistaqt import QtInteractor
from PyQt5 import QtWidgets, QtCore, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from gyroid_generator import GyroidalSphere


class GyroidGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gyroidal Sphere Generator")
        self.resize(1600, 1000)

        self.generator = GyroidalSphere()
        
        self._build_ui()
        self._setup_statusbar()

    def _build_ui(self):
        # ==== MAIN LAYOUT ====
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QtWidgets.QHBoxLayout(central_widget)
        
        # ==== LEFT CONTROL PANEL ====
        control_panel = self._create_control_panel()
        main_layout.addWidget(control_panel, stretch=1)
        
        # ==== RIGHT VISUALIZATION PANEL ====
        viz_panel = self._create_viz_panel()
        main_layout.addWidget(viz_panel, stretch=3)

    def _create_control_panel(self):
        """Create left control panel with all parameters."""
        panel = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(panel)
        
        # --- Parameters Group ---
        param_group = QtWidgets.QGroupBox("Parameters")
        param_layout = QtWidgets.QFormLayout()
        
        # Radius
        self.radius_spin = QtWidgets.QDoubleSpinBox()
        self.radius_spin.setRange(25.0, 150.0)
        self.radius_spin.setValue(50.0)
        self.radius_spin.setSingleStep(5.0)
        self.radius_spin.setSuffix(" mm")
        param_layout.addRow("Sphere Radius:", self.radius_spin)
        
        # Resolution
        self.resolution_spin = QtWidgets.QSpinBox()
        self.resolution_spin.setRange(30, 450)
        self.resolution_spin.setValue(200)
        self.resolution_spin.setSingleStep(10)
        param_layout.addRow("Resolution:", self.resolution_spin)
        
        res_note = QtWidgets.QLabel("(Higher = better quality, slower)")
        res_note.setStyleSheet("color: gray; font-size: 9px;")
        param_layout.addRow("", res_note)
        
        # Unit Cell Size
        self.unit_cell_spin = QtWidgets.QDoubleSpinBox()
        self.unit_cell_spin.setRange(2.0, 50.0)
        self.unit_cell_spin.setValue(5.0)
        self.unit_cell_spin.setSingleStep(1.0)
        self.unit_cell_spin.setSuffix(" mm")
        param_layout.addRow("Unit Cell Size:", self.unit_cell_spin)
        
        cell_note = QtWidgets.QLabel("(Size of one gyroid cube)")
        cell_note.setStyleSheet("color: gray; font-size: 9px;")
        param_layout.addRow("", cell_note)
        
        # Infill Percentage
        infill_layout = QtWidgets.QHBoxLayout()
        self.infill_spin = QtWidgets.QDoubleSpinBox()
        self.infill_spin.setRange(10.0, 100.0)
        self.infill_spin.setValue(68.95)
        self.infill_spin.setSingleStep(5.0)
        self.infill_spin.setSuffix(" %")
        self.infill_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.infill_slider.setRange(10, 100)
        self.infill_slider.setValue(69)
        infill_layout.addWidget(self.infill_spin)
        infill_layout.addWidget(self.infill_slider)
        
        # Sync slider and spinbox
        self.infill_spin.valueChanged.connect(lambda v: self.infill_slider.setValue(int(v)))
        self.infill_slider.valueChanged.connect(lambda v: self.infill_spin.setValue(float(v)))
        
        param_layout.addRow("Infill %:", infill_layout)
        
        infill_note = QtWidgets.QLabel("(Higher = more material)")
        infill_note.setStyleSheet("color: gray; font-size: 9px;")
        param_layout.addRow("", infill_note)
        
        #core radius and holowing
        self.core_radius_spin = QtWidgets.QDoubleSpinBox()
        self.core_radius_spin.setRange(0.0, 0.9)
        self.core_radius_spin.setValue(0.5)
        self.core_radius_spin.setSingleStep(0.05)
        self.core_radius_spin.setSuffix(" × R")
        param_layout.addRow("Core Radius:", self.core_radius_spin)

        core_note = QtWidgets.QLabel("(0 = no core, 0.5 = R/2)")
        core_note.setStyleSheet("color: gray; font-size: 9px;")
        param_layout.addRow("", core_note)

        # Thickness Equation
        self.thickness_edit = QtWidgets.QLineEdit("np.sqrt(2 - np.square(r / radius))")
        param_layout.addRow("Thickness Eq:", self.thickness_edit)
        
        param_group.setLayout(param_layout)
        layout.addWidget(param_group)
        
        # --- Preset Buttons ---
        preset_group = QtWidgets.QGroupBox("Thickness Presets")
        preset_layout = QtWidgets.QGridLayout()
        
        presets = [
            ("Constant", "0.5"),
            ("Thick Center", "0.4 + 0.4 * (1 - r / radius)"),
            ("Thick Edge", "0.2 + 0.6 * (r / radius)"),
            ("Sinusoidal", "0.5 + 0.3 * np.sin(r * np.pi / radius)"),
            ("LL Linear Mixing", "np.sqrt(2 - np.square(r / radius))"),
            ("LL Bruggeman Mixing", "")]
        
        for i, (name, eq) in enumerate(presets):
            btn = QtWidgets.QPushButton(name)
            btn.clicked.connect(lambda checked, e=eq: self.thickness_edit.setText(e))
            preset_layout.addWidget(btn, i // 2, i % 2)
        
        preset_group.setLayout(preset_layout)
        layout.addWidget(preset_group)
        
        # --- Generation Buttons ---
        gen_layout = QtWidgets.QHBoxLayout()
        
        self.preview_btn = QtWidgets.QPushButton("Quick Preview")
        self.preview_btn.clicked.connect(self.generate_preview)
        
        self.generate_btn = QtWidgets.QPushButton("Generate Full")
        self.generate_btn.clicked.connect(self.generate_full)
        
        gen_layout.addWidget(self.preview_btn)
        gen_layout.addWidget(self.generate_btn)
        layout.addLayout(gen_layout)
        
        # --- Cross-Section Controls ---
        cross_group = QtWidgets.QGroupBox("Cross-Section")
        cross_layout = QtWidgets.QFormLayout()
        
        self.axis_combo = QtWidgets.QComboBox()
        self.axis_combo.addItems(['X', 'Y', 'Z'])
        self.axis_combo.setCurrentText('Z')
        cross_layout.addRow("Axis:", self.axis_combo)
        
        self.position_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.position_slider.setRange(-50, 50)
        self.position_slider.setValue(0)
        self.position_label = QtWidgets.QLabel("0.0")
        
        pos_layout = QtWidgets.QHBoxLayout()
        pos_layout.addWidget(self.position_slider)
        pos_layout.addWidget(self.position_label)
        cross_layout.addRow("Position:", pos_layout)
        
        self.position_slider.valueChanged.connect(
            lambda v: self.position_label.setText(f"{v/5.0:.1f}")
        )
        
        update_cross_btn = QtWidgets.QPushButton("Update Cross-Section")
        update_cross_btn.clicked.connect(self.update_cross_section)
        cross_layout.addRow(update_cross_btn)
        
        cross_group.setLayout(cross_layout)
        layout.addWidget(cross_group)
        
        # --- Export Options ---
        export_group = QtWidgets.QGroupBox("Export")
        export_layout = QtWidgets.QVBoxLayout()
        
        # Repair checkbox
        self.repair_check = QtWidgets.QCheckBox("Repair for CAD/CST (Recommended)")
        self.repair_check.setChecked(True)
        export_layout.addWidget(self.repair_check)
        
        # Simplify options
        simplify_layout = QtWidgets.QHBoxLayout()
        self.simplify_check = QtWidgets.QCheckBox("Simplify mesh")
        self.simplify_spin = QtWidgets.QSpinBox()
        self.simplify_spin.setRange(10, 90)
        self.simplify_spin.setValue(50)
        self.simplify_spin.setSuffix(" % keep")
        simplify_layout.addWidget(self.simplify_check)
        simplify_layout.addWidget(self.simplify_spin)
        export_layout.addLayout(simplify_layout)
        
        # Export buttons
        export_btn_layout = QtWidgets.QGridLayout()
        
        export_btns = [
            ("STL Binary", 'stl'),
            ("STL ASCII", 'stl_ascii'),
            ("OBJ", 'obj'),
            ("IGES", 'iges'),
            ("STEP", 'step')
        ]
        
        for i, (name, fmt) in enumerate(export_btns):
            btn = QtWidgets.QPushButton(name)
            btn.clicked.connect(lambda checked, f=fmt: self.export_file(f))
            export_btn_layout.addWidget(btn, i // 2, i % 2)
        
        export_layout.addLayout(export_btn_layout)
        export_group.setLayout(export_layout)
        layout.addWidget(export_group)
        
        # Add stretch to push everything to top
        layout.addStretch()
        
        return panel

    def _create_viz_panel(self):
        """Create right visualization panel with 3D view and cross-section."""
        panel = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(panel)

        # --- 3D View ---
        view_3d_group = QtWidgets.QGroupBox("3D Preview (Rotate: Left Click, Zoom: Scroll)")
        view_3d_layout = QtWidgets.QVBoxLayout()

        self.plotter = QtInteractor(view_3d_group)
        self.plotter.add_axes()
        self.plotter.set_background("white")

        self.plotter.enable_parallel_projection()

        view_3d_layout.addWidget(self.plotter)
        view_3d_group.setLayout(view_3d_layout)

        # --- Cross-Section View ---
        cross_view_group = QtWidgets.QGroupBox("Cross-Section View")
        cross_view_layout = QtWidgets.QVBoxLayout()

        self.fig = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.fig)
        self.ax_2d_slice = self.fig.add_subplot(111)
        self.fig.tight_layout()

        cross_view_layout.addWidget(self.canvas)
        cross_view_group.setLayout(cross_view_layout)

        # --- Draggable divider between 3D and 2D views ---
        splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        splitter.addWidget(view_3d_group)
        splitter.addWidget(cross_view_group)
        splitter.setSizes([800, 400])  # initial ratio

        layout.addWidget(splitter)


        return panel


    def _setup_statusbar(self):
        """Setup status bar."""
        self.statusbar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Ready. Note: Install 'meshlib' for proper volume generation.")

    # ========== GENERATION ==========
    
    def generate_preview(self):
        """Generate quick preview."""
        self.preview_btn.setEnabled(False)
        self.statusbar.showMessage("Generating preview...")
        QtWidgets.QApplication.processEvents()
        
        try:
            self.generator = GyroidalSphere(
                radius=self.radius_spin.value(),
                resolution=self.resolution_spin.value()
            )
            
            self.generator.generate_mesh(
                thickness_eq=self.thickness_edit.text(),
                unit_cell_size=self.unit_cell_spin.value(),
                infill_percent=self.infill_spin.value(),
                core_radius_ratio=self.core_radius_spin.value(),
                preview_mode=True
            )
            
            self.update_3d()
            self.update_cross_section()
            self.statusbar.showMessage("Preview ready")
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Preview generation failed:\n{str(e)}")
            self.statusbar.showMessage(f"Error: {str(e)}")
        
        finally:
            self.preview_btn.setEnabled(True)

    def generate_full(self):
        """Generate full resolution model."""
        self.generate_btn.setEnabled(False)
        self.statusbar.showMessage("Generating full resolution model...")
        QtWidgets.QApplication.processEvents()
        
        try:
            self.generator = GyroidalSphere(
                radius=self.radius_spin.value(),
                resolution=self.resolution_spin.value()
            )
            
            self.generator.generate_mesh(
                thickness_eq=self.thickness_edit.text(),
                unit_cell_size=self.unit_cell_spin.value(),
                infill_percent=self.infill_spin.value(),
                core_radius_ratio=self.core_radius_spin.value(),
                preview_mode=False
            )
            
            self.update_3d()
            self.update_cross_section()
            self.statusbar.showMessage("Full model ready. Ready to export.")
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Generation failed:\n{str(e)}")
            self.statusbar.showMessage(f"Error: {str(e)}")
        
        finally:
            self.generate_btn.setEnabled(True)

    # ========== 3D VIEW ==========
    
    def update_3d(self):
        """Update 3D visualization using PyVista."""
        self.plotter.clear()
        
        if self.generator.vertices is None or self.generator.faces is None:
            return
        
        # Sample faces for display
        max_faces = 50000000
        if len(self.generator.faces) > max_faces:
            step = len(self.generator.faces) // max_faces
            display_faces = self.generator.faces[::step]
        else:
            display_faces = self.generator.faces
        
        # Create PyVista mesh
        faces_with_count = np.hstack([
            np.full((len(display_faces), 1), 3),
            display_faces
        ]).flatten()
        
        mesh = pv.PolyData(self.generator.vertices, faces_with_count)
        
        self.plotter.add_mesh(
            mesh,
            color='steelblue',
            smooth_shading=True,
            show_edges=True,
            edge_color='black',
            line_width=0.25,
            opacity=1,
            # split_sharp_edges=True,
            metallic=1,
            roughness=0.5
        )
        
        self.plotter.reset_camera()
        self.plotter.render()
        
        
        
    # ========== CROSS-SECTION ==========
    
    def update_cross_section(self):
        """Update cross-section view."""
        self.ax_2d_slice.clear()
        
        if self.generator.vertices is None or self.generator.faces is None:
            self.canvas.draw()
            return
        
        axis = self.axis_combo.currentText().lower()
        position = self.position_slider.value() / 5.0
        
        # Get 2D slice data
        slice_data, extent, labels = self.generator.get_cross_section(axis, position)
        
        if slice_data is not None:
            self.ax_2d_slice.imshow(
                slice_data.T,
                origin='lower',
                extent=extent,
                cmap='RdBu_r',
                aspect='equal'
            )
            self.ax_2d_slice.contour(
                slice_data.T,
                levels=[0],
                colors='black',
                linewidths=1.5,
                extent=extent
            )
            self.ax_2d_slice.set_xlabel(labels[0] + ' (mm)')
            self.ax_2d_slice.set_ylabel(labels[1] + ' (mm)')
            self.ax_2d_slice.set_title(f'2D Cross-Section at {axis.upper()}={position:.2f} mm')
            self.ax_2d_slice.grid(True, alpha=0.3)
        
        self.fig.tight_layout()
        self.canvas.draw()
        
    # ========== EXPORT ==========
    
    def export_file(self, format_type):
        """Export mesh to file."""
        if self.generator.mesh is None:
            QtWidgets.QMessageBox.warning(
                self,
                "Warning",
                "Please generate a model first!"
            )
            return
        
        # File dialog
        filters = {
            'stl': "STL Binary (*.stl)",
            'stl_ascii': "STL ASCII (*.stl)",
            'obj': "OBJ Files (*.obj)",
            'iges': "IGES Files (*.igs *.iges)",
            'step': "STEP Files (*.step *.stp)"
        }
        
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Export Mesh",
            f"gyroidal_sphere.{format_type.replace('_ascii', '')}",
            filters.get(format_type, "All Files (*)")
        )
        
        if not filename:
            return
        
        # Apply repairs/simplification
        if self.repair_check.isChecked():
            self.statusbar.showMessage("Repairing mesh for CAD/CST...")
            QtWidgets.QApplication.processEvents()
            self.generator.repair_mesh_for_cad()
            self.update_3d()
        
        if self.simplify_check.isChecked():
            self.statusbar.showMessage("Simplifying mesh...")
            QtWidgets.QApplication.processEvents()
            self.generator.simplify_mesh(percent=self.simplify_spin.value())
            self.update_3d()
        
        # Export
        self.statusbar.showMessage(f"Exporting {format_type.upper()}...")
        QtWidgets.QApplication.processEvents()
        
        export_func = {
            'stl': self.generator.export_stl,
            'stl_ascii': self.generator.export_stl_ascii,
            'obj': self.generator.export_obj,
            'iges': self.generator.export_iges,
            'step': self.generator.export_step
        }
        
        success = export_func[format_type](filename)
        
        if success:
            is_watertight = self.generator.mesh.is_watertight if self.generator.mesh else False
            
            QtWidgets.QMessageBox.information(
                self,
                "Export Successful",
                f"File exported successfully!\n\n"
                f"Format: {format_type.upper()}\n"
                f"Faces: {len(self.generator.faces):,}\n"
                f"Vertices: {len(self.generator.vertices):,}\n"
                f"Watertight: {'Yes ✓' if is_watertight else 'No ⚠'}\n\n"
                f"CST Studio Suite Import Tips:\n"
                f"1. Use 'Import' → 'SAT' or 'ACIS'\n"
                f"2. If issues: Enable 'Repair for CAD/CST'\n"
                f"3. Try STL ASCII format\n"
                f"4. Increase resolution or unit cell size\n"
                f"5. Check that mesh is watertight (above)"
            )
            self.statusbar.showMessage(f"Exported to {filename}")
        else:
            QtWidgets.QMessageBox.critical(
                self,
                "Export Failed",
                f"Failed to export {format_type.upper()} file.\n\n"
                f"Troubleshooting:\n"
                f"1. Enable 'Repair for CAD/CST'\n"
                f"2. Try STL ASCII format\n"
                f"3. Enable simplification\n"
                f"4. Check console for error details"
            )
            self.statusbar.showMessage("Export failed")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = GyroidGUI()
    window.show()
    
    sys.exit(app.exec_())