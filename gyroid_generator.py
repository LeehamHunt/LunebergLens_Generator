# gyroid_generator.py
# Core gyroidal sphere generation logic using meshlib approach

import numpy as np
from skimage import measure
import trimesh
import tempfile
import os
import meshlib.mrmeshpy as mr

class GyroidalSphere:
    def __init__(self, radius=10, resolution=100):
        """
        Initialize the gyroidal sphere generator.
        
        Parameters:
        -----------
        radius : float
            Radius of the sphere
        resolution : int
            Grid resolution for marching cubes algorithm
        """
        self.radius = radius
        self.resolution = resolution
        self.vertices = None
        self.faces = None
        self.mesh = None
        self.volume_data = None
        self.grid_coords = None
        self.use_meshlib = self._check_meshlib()


    def _check_meshlib(self):
        """Check if meshlib is available."""
        try:
            import meshlib.mrmeshpy as mr
            return True
        except ImportError:
            print("Note: meshlib not available. Install with: pip install meshlib")
            print("Using fallback mesh generation method.")
            return False
        
    def thickness_function(self, r, equation_str):
        """
        Evaluate thickness as a function of radial distance.
        
        Parameters:
        -----------
        r : float or np.ndarray
            Radial distance from center
        equation_str : str
            Python expression for thickness (use 'r' as variable)
        """
        radius = self.radius
        try:
            thickness = eval(equation_str)
            return np.clip(thickness, 0.01, 10.0)
        except Exception as e:
            print(f"Error evaluating thickness equation: {e}")
            return 0.5
    
    def gyroid_function(self, x, y, z, scale=2.0):
        """Gyroid implicit surface function."""
        return np.sin(x*scale)*np.cos(y*scale) + \
               np.sin(y*scale)*np.cos(z*scale) + \
               np.sin(z*scale)*np.cos(x*scale)
    
    def gyroid_function(self, x, y, z, scale=2.0):
        """Gyroid implicit surface function."""
        return np.sin(x*scale)*np.cos(y*scale) + \
               np.sin(y*scale)*np.cos(z*scale) + \
               np.sin(z*scale)*np.cos(x*scale)
    
    def unit_cell_to_scale(self, unit_cell_size_mm):
        """
        Convert unit cell size (mm) to gyroid scale parameter.
        
        The gyroid has a natural period of 2π. To get a specific unit cell size,
        we need to calculate the appropriate scaling factor.
        
        Parameters:
        -----------
        unit_cell_size_mm : float
            Desired unit cell size in millimeters
            
        Returns:
        --------
        scale : float
            Gyroid scale parameter
        """
        # The gyroid repeats every 2π in each direction
        # scale = 2π / unit_cell_size
        scale = (2 * np.pi) / unit_cell_size_mm
        return scale
    
    def generate_mesh(self, thickness_eq, unit_cell_size=10.0, infill_percent=50.0, core_radius_ratio=0.5, preview_mode=False):
        """
        Generate the gyroidal sphere mesh.
        
        Parameters:
        -----------
        thickness_eq : str
            Equation for thickness as function of radius
        unit_cell_size : float
            Size of one gyroid unit cell in millimeters (e.g., 10.0 for 10mm cubes)
        infill_percent : float
            Percentage of infill (0-100%). Higher = more material, lower = more voids
        preview_mode : bool
            If True, use lower resolution for faster preview
        """
        # Convert unit cell size to gyroid scale
        gyroid_scale = self.unit_cell_to_scale(unit_cell_size)
        # Use lower resolution for preview
        res = self.resolution // 2 if preview_mode else self.resolution
        
        # Create 3D grid
        margin = 1.2
        x = np.linspace(-self.radius*margin, self.radius*margin, res)
        y = np.linspace(-self.radius*margin, self.radius*margin, res)
        z = np.linspace(-self.radius*margin, self.radius*margin, res)
        
        X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
        
        # Calculate radial distance from center
        R = np.sqrt(X**2 + Y**2 + Z**2)
        
        # Evaluate thickness function
        thickness_value = self.thickness_function(R, thickness_eq)
        
        # Calculate gyroid value
        gyroid = self.gyroid_function(X, Y, Z, gyroid_scale)
        
        # Convert infill percentage to threshold
        # The gyroid function oscillates between approximately -1.73 and +1.73
        # At 0% infill: threshold → 0 (almost no material)
        # At 50% infill: threshold ≈ 0.87 (roughly half material, half void)
        # At 100% infill: threshold → 1.73 (almost all material)
        
        # Map infill percentage to gyroid threshold
        # infill_percent 0-100 maps to threshold 0 to ~1.73
        max_gyroid_value = 1.73  # Approximate max value of gyroid function
        threshold = (infill_percent / 100.0) * max_gyroid_value
        
        # Adjust thickness based on threshold
        # Material exists where |gyroid| < threshold
        adjusted_thickness = thickness_value * (threshold / (max_gyroid_value / 2))
        
        # Create signed distance field
        sphere_sdf = self.radius - R
        gyroid_sdf = adjusted_thickness/2 - np.abs(gyroid)
        
        # Combine: material exists where both conditions are met
        combined_sdf = np.minimum(sphere_sdf, gyroid_sdf)

        # Carve out the hollow core         <-- ADD THESE LINES HERE
        if core_radius_ratio > 0:
            core_radius = self.radius * core_radius_ratio
            core_sdf = core_radius - R
            combined_sdf = np.maximum(combined_sdf, core_sdf)

        # Store volume data for cross-section
        self.volume_data = combined_sdf
        self.grid_coords = (x, y, z)
        
        # Use marching cubes to extract surface
        print("Running marching cubes...")
        vertices, faces, normals, values = measure.marching_cubes(
            combined_sdf, 
            level=0,
            spacing=(x[1]-x[0], y[1]-y[0], z[1]-z[0])
        )
        
        # Adjust vertices to actual coordinates
        vertices[:, 0] += x[0]
        vertices[:, 1] += y[0]
        vertices[:, 2] += z[0]
        
        print(f"Marching cubes complete: {len(vertices)} vertices, {len(faces)} faces")
        
        # Create initial surface mesh
        surface_mesh = trimesh.Trimesh(vertices=vertices, faces=faces, 
                                       vertex_normals=normals)
        
        # Remove disconnected floating bodies
        print("Removing floating bodies...")
        surface_mesh = self._remove_floating_bodies(surface_mesh)
        
        # Apply thickness using meshlib or fallback method
        if self.use_meshlib and not preview_mode:
            print("Applying thickness with meshlib...")
            self.mesh = self._apply_thickness_meshlib(surface_mesh, thickness_value)
        else:
            print("Using surface mesh (no thickness applied)...")
            self.mesh = surface_mesh

        # Update vertices and faces
        self.vertices = self.mesh.vertices
        self.faces = self.mesh.faces
        
        print(f"Final mesh: {len(self.vertices)} vertices, {len(self.faces)} faces")
        
        return self.vertices, self.faces
    
    def _remove_floating_bodies(self, mesh):
        """Remove small disconnected components, keeping only the largest body."""
        try:
            # Split mesh into connected components
            components = mesh.split(only_watertight=False)
            
            if len(components) > 1:
                print(f"Found {len(components)} separate components")
                
                # Sort by number of vertices (largest first)
                components_sorted = sorted(components, key=lambda m: len(m.vertices), reverse=True)
                
                # Keep only the largest component
                largest = components_sorted[0]
                
                # Report what was removed
                removed_vertices = sum(len(c.vertices) for c in components_sorted[1:])
                print(f"Removed {len(components)-1} floating bodies ({removed_vertices} vertices)")
                print(f"Kept main body: {len(largest.vertices)} vertices, {len(largest.faces)} faces")
                
                return largest
            else:
                print("No floating bodies detected")
                return mesh
                
        except Exception as e:
            print(f"Could not remove floating bodies: {e}")
            return mesh
    
    def _apply_thickness_meshlib(self, surface_mesh, thickness):
        """Apply thickness to surface using meshlib's offsetMesh."""
        try:
            import meshlib.mrmeshpy as mr
            
            # Save surface to temporary STL
            temp_file = tempfile.NamedTemporaryFile(suffix='.stl', delete=False)
            temp_file.close()
            surface_mesh.export(temp_file.name)
            
            # Load with meshlib
            mr_mesh = mr.loadMesh(temp_file.name)
            
            # Get average thickness value
            if isinstance(thickness, np.ndarray):
                avg_thickness = float(np.mean(thickness))
            else:
                avg_thickness = float(thickness)
            
            # Ensure thickness is reasonable (in mm)
            avg_thickness = max(0.5, min(avg_thickness, 5.0))
            offset = avg_thickness / 2
            
            print(f"Applying offset of {offset:.3f}mm...")
            
            # Calculate appropriate voxel size (should be ~1/10 of offset)
            voxel_size = offset / 10.0
            if voxel_size < 0.01:
                voxel_size = 0.01  # Minimum voxel size
            
            print(f"Using voxel size: {voxel_size:.4f}mm")
            
            # Create OffsetParameters object (correct API)
            params = mr.OffsetParameters()
            params.voxelSize = voxel_size
            
            # Apply offset with parameters object
            offset_mesh = mr.offsetMesh(mr_mesh, offset, params)
            
            # Save offset mesh to temp file
            temp_offset_file = tempfile.NamedTemporaryFile(suffix='.stl', delete=False)
            temp_offset_file.close()
            mr.saveMesh(offset_mesh, temp_offset_file.name)
            
            # Load back with trimesh
            final_mesh = trimesh.load(temp_offset_file.name)
            
            # Clean up temp files
            os.unlink(temp_file.name)
            os.unlink(temp_offset_file.name)
            
            print("Thickness applied successfully with meshlib")
            return final_mesh
            
        except Exception as e:
            print(f"Meshlib thickness application failed: {e}")
            print("Falling back to surface mesh only")
            return surface_mesh
        
    def get_cross_section(self, axis='z', position=0):
        """
        Get a 2D cross-section of the volume.
        
        Parameters:
        -----------
        axis : str
            'x', 'y', or 'z'
        position : float
            Position along the axis for the cross-section
        """
        if self.volume_data is None:
            return None, None, None
        
        x, y, z = self.grid_coords
        
        # Find closest index to position
        if axis == 'x':
            idx = np.argmin(np.abs(x - position))
            slice_data = self.volume_data[idx, :, :]
            extent = [y[0], y[-1], z[0], z[-1]]
            labels = ('Y', 'Z')
        elif axis == 'y':
            idx = np.argmin(np.abs(y - position))
            slice_data = self.volume_data[:, idx, :]
            extent = [x[0], x[-1], z[0], z[-1]]
            labels = ('X', 'Z')
        else:  # z
            idx = np.argmin(np.abs(z - position))
            slice_data = self.volume_data[:, :, idx]
            extent = [x[0], x[-1], y[0], y[-1]]
            labels = ('X', 'Y')
        
        return slice_data, extent, labels
    
    def export_stl(self, filename="gyroidal_sphere.stl"):
        """Export mesh to STL format."""
        if self.mesh is None:
            print("No mesh generated yet.")
            return False
        
        try:
            # Export as binary STL for better compatibility
            self.mesh.export(filename, file_type='stl')
            print(f"Successfully exported to {filename}")
            print(f"Mesh stats: {len(self.vertices)} vertices, {len(self.faces)} faces")
            print(f"Watertight: {self.mesh.is_watertight}")
            return True
        except Exception as e:
            print(f"Error exporting: {e}")
            return False
    
    def export_obj(self, filename="gyroidal_sphere.obj"):
        """Export mesh to OBJ format."""
        if self.mesh is None:
            return False
        try:
            self.mesh.export(filename)
            print(f"Exported to {filename}")
            return True
        except Exception as e:
            print(f"Error exporting OBJ: {e}")
            return False
    
    def export_step(self, filename="gyroidal_sphere.step"):
        """Export mesh to STEP format (if supported)."""
        if self.mesh is None:
            return False
        try:
            self.mesh.export(filename)
            print(f"Exported to {filename}")
            return True
        except Exception as e:
            print(f"STEP export not supported. Try STL or OBJ format.")
            print(f"You can convert STL to STEP using FreeCAD or SolidWorks.")
            return False
    # Add these methods to your GyroidalSphere class in gyroid_generator.py

    def export_stl_ascii(self, filename="gyroidal_sphere.stl"):
        """Export mesh to ASCII STL format."""
        if self.mesh is None:
            print("No mesh generated yet.")
            return False
        
        try:
            with open(filename, 'w') as f:
                f.write('solid gyroidal_sphere\n')
                for face in self.faces:
                    v0, v1, v2 = self.vertices[face]
                    normal = np.cross(v1 - v0, v2 - v0)
                    norm = np.linalg.norm(normal)
                    if norm > 1e-10:
                        normal = normal / norm
                    else:
                        normal = np.array([0, 0, 1])
                    
                    f.write(f'  facet normal {normal[0]:.6e} {normal[1]:.6e} {normal[2]:.6e}\n')
                    f.write('    outer loop\n')
                    f.write(f'      vertex {v0[0]:.6e} {v0[1]:.6e} {v0[2]:.6e}\n')
                    f.write(f'      vertex {v1[0]:.6e} {v1[1]:.6e} {v1[2]:.6e}\n')
                    f.write(f'      vertex {v2[0]:.6e} {v2[1]:.6e} {v2[2]:.6e}\n')
                    f.write('    endloop\n')
                    f.write('  endfacet\n')
                f.write('endsolid gyroidal_sphere\n')
            
            print(f"Successfully exported ASCII STL to {filename}")
            return True
        except Exception as e:
            print(f"Error exporting ASCII STL: {e}")
            return False

    def export_iges(self, filename="gyroidal_sphere.igs"):
        """Export mesh to IGES format."""
        if self.mesh is None:
            return False
        try:
            self.mesh.export(filename, file_type='iges')
            print(f"Exported to {filename}")
            return True
        except Exception as e:
            print(f"IGES export failed: {e}")
            print("IGES export may require additional CAD libraries.")
            print("Recommendation: Export as STL ASCII with simplification enabled.")
            return False

    def simplify_mesh(self, target_faces=None, percent=None):
        """Simplify mesh to reduce complexity."""
        if self.mesh is None:
            print("No mesh to simplify")
            return False
        
        try:
            original_faces = len(self.faces)
            
            if percent is not None:
                target_faces = int(original_faces * percent / 100.0)
            elif target_faces is None:
                target_faces = original_faces // 2
            
            print(f"Simplifying mesh from {original_faces} to ~{target_faces} faces...")
            
            simplified = self.mesh.simplify_quadric_decimation(target_faces)
            
            if simplified is not None and len(simplified.faces) > 0:
                self.mesh = simplified
                self.vertices = self.mesh.vertices
                self.faces = self.mesh.faces
                
                print(f"Simplified to {len(self.faces)} faces ({100*len(self.faces)/original_faces:.1f}% of original)")
                return True
            else:
                print("Simplification failed")
                return False
                
        except Exception as e:
            print(f"Error simplifying mesh: {e}")
            return False

    def repair_mesh_for_cad(self):
        """
        Aggressively repair mesh for CAD/CST import.
        Ensures watertight, manifold geometry with consistent normals.
        """
        if self.mesh is None:
            print("No mesh to repair")
            return False
        
        try:
            print("Performing aggressive mesh repair for CAD/CST...")
            
            # 1. Fill holes
            trimesh.Trimesh.fill_holes(self.mesh)

            # 2. Fix normals
            trimesh.Trimesh.fix_normals(self.mesh)

            # 3. Fix face winding / inversion
            trimesh.repair.fix_inversion(self.mesh)

            # 4. Remove duplicate faces (method on mesh)
            if hasattr(self.mesh, "remove_duplicate_faces"):
                self.mesh.remove_duplicate_faces()

            # 5. Merge vertices (new location in 4.x)
            trimesh.Trimesh.merge_vertices(self.mesh)

            # 6. Remove unreferenced vertices
            trimesh.Trimesh.remove_unreferenced_vertices(self.mesh)

            # 7. Run trimesh's built-in cleanup pipeline
            trimesh.Trimesh.process(self.mesh)

            # 8. Recompute normals
            trimesh.Trimesh.fix_normals(self.mesh)

            
            # Update arrays
            self.vertices = self.mesh.vertices
            self.faces = self.mesh.faces
            
            # Check final state
            is_watertight = trimesh.Trimesh.is_watertight(self.mesh)
            is_winding = trimesh.Trimesh.is_winding_consistent(self.mesh)
            
            print(f"\nRepair Results:")
            print(f"  Watertight: {is_watertight}")
            print(f"  Consistent winding: {is_winding}")
            print(f"  Final: {len(self.vertices)} vertices, {len(self.faces)} faces")
            
            if not is_watertight:
                print("\n⚠ Warning: Mesh still not watertight after repair")
                print("  This may cause issues in CST Studio Suite")
                print("  Try: Higher resolution, larger unit cell size, or different infill %")
            else:
                print("\n✓ Mesh is watertight and ready for CST import")
            
            return is_watertight
            
        except Exception as e:
            print(f"Error during mesh repair: {e}")
            return False