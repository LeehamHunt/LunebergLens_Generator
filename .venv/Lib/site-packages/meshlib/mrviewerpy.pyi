from __future__ import annotations
import meshlib.mrmeshpy
import typing
__all__: list[str] = ['KeyMod', 'MouseButton', 'UiEntry', 'UiEntryType', 'UiValueInt', 'UiValueReal', 'UiValueString', 'UiValueUint', 'Viewer', 'ViewerLaunchParams', 'ViewerLaunchParamsMode', 'ViewerSetup', 'Viewport', 'ViewportFitDataParams', 'ViewportFitMode', 'addDistanceMapToScene', 'addLinesToScene', 'addMeshToScene', 'addPointCloudToScene', 'addVoxelsToScene', 'clearScene', 'getSelectedDistanceMaps', 'getSelectedMeshEdges', 'getSelectedMeshFaces', 'getSelectedMeshes', 'getSelectedObjects', 'getSelectedPointCloudPoints', 'getSelectedPointClouds', 'getSelectedPolylines', 'getSelectedVoxels', 'launch', 'modifySelectedMesh', 'runFromGUIThread', 'selectByName', 'selectByType', 'setSelectedMeshEdges', 'setSelectedMeshFaces', 'setSelectedPointCloudPoints', 'uiListEntries', 'uiPressButton', 'uiReadValueInt', 'uiReadValueReal', 'uiReadValueString', 'uiReadValueUint', 'uiWriteValue', 'uiWriteValueInt', 'uiWriteValueReal', 'uiWriteValueString', 'uiWriteValueUint', 'unselectAll']
class KeyMod:
    """
    Members:
    
      Empty
    
      Ctrl
    
      Super
    
      Shift
    
      Alt
    """
    Alt: typing.ClassVar[KeyMod]  # value = <KeyMod.Alt: 4>
    Ctrl: typing.ClassVar[KeyMod]  # value = <KeyMod.Ctrl: 2>
    Empty: typing.ClassVar[KeyMod]  # value = <KeyMod.Empty: 0>
    Shift: typing.ClassVar[KeyMod]  # value = <KeyMod.Shift: 1>
    Super: typing.ClassVar[KeyMod]  # value = <KeyMod.Super: 8>
    __members__: typing.ClassVar[dict[str, KeyMod]]  # value = {'Empty': <KeyMod.Empty: 0>, 'Ctrl': <KeyMod.Ctrl: 2>, 'Super': <KeyMod.Super: 8>, 'Shift': <KeyMod.Shift: 1>, 'Alt': <KeyMod.Alt: 4>}
    def __and__(self, arg0: KeyMod) -> KeyMod:
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __invert__(self) -> KeyMod:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __or__(self, arg0: KeyMod) -> KeyMod:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class MouseButton:
    """
    Members:
    
      Left
    
      Right
    
      Middle
    """
    Left: typing.ClassVar[MouseButton]  # value = <MouseButton.Left: 0>
    Middle: typing.ClassVar[MouseButton]  # value = <MouseButton.Middle: 2>
    Right: typing.ClassVar[MouseButton]  # value = <MouseButton.Right: 1>
    __members__: typing.ClassVar[dict[str, MouseButton]]  # value = {'Left': <MouseButton.Left: 0>, 'Right': <MouseButton.Right: 1>, 'Middle': <MouseButton.Middle: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class UiEntry:
    def __repr__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def type(self) -> UiEntryType:
        ...
class UiEntryType:
    """
    UI entry type enum.
    
    Members:
    
      button
    
      group
    
      valueInt
    
      valueUint
    
      valueReal
    
      valueString
    
      other
    """
    __members__: typing.ClassVar[dict[str, UiEntryType]]  # value = {'button': <UiEntryType.button: 0>, 'group': <UiEntryType.group: 1>, 'valueInt': <UiEntryType.valueInt: 2>, 'valueUint': <UiEntryType.valueUint: 3>, 'valueReal': <UiEntryType.valueReal: 4>, 'valueString': <UiEntryType.valueString: 5>, 'other': <UiEntryType.other: 6>}
    button: typing.ClassVar[UiEntryType]  # value = <UiEntryType.button: 0>
    group: typing.ClassVar[UiEntryType]  # value = <UiEntryType.group: 1>
    other: typing.ClassVar[UiEntryType]  # value = <UiEntryType.other: 6>
    valueInt: typing.ClassVar[UiEntryType]  # value = <UiEntryType.valueInt: 2>
    valueReal: typing.ClassVar[UiEntryType]  # value = <UiEntryType.valueReal: 4>
    valueString: typing.ClassVar[UiEntryType]  # value = <UiEntryType.valueString: 5>
    valueUint: typing.ClassVar[UiEntryType]  # value = <UiEntryType.valueUint: 3>
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class UiValueInt:
    @property
    def max(self) -> int:
        ...
    @property
    def min(self) -> int:
        ...
    @property
    def value(self) -> int:
        ...
class UiValueReal:
    @property
    def max(self) -> float:
        ...
    @property
    def min(self) -> float:
        ...
    @property
    def value(self) -> float:
        ...
class UiValueString:
    @property
    def allowed(self) -> list[str] | None:
        ...
    @property
    def value(self) -> str:
        ...
class UiValueUint:
    @property
    def max(self) -> int:
        ...
    @property
    def min(self) -> int:
        ...
    @property
    def value(self) -> int:
        ...
class Viewer:
    """
    GLFW-based mesh viewer
    """
    def __init__(self) -> None:
        ...
    def captureScreenShot(self, path: str) -> None:
        """
        Captures part of window (redraw 3d scene over UI (without redrawing UI))
        """
    def captureUIScreenShot(self, path: str) -> None:
        """
        Captures full window screenshot with UI
        """
    def getMousePos(self) -> meshlib.mrmeshpy.Vector2f:
        """
        Get the current mouse position.
        """
    def incrementForceRedrawFrames(self, num: int = 1, swapOnLastOnly: bool = False) -> None:
        """
        Increment number of forced frames to redraw in event loop
        if `swapOnLastOnly` only last forced frame will be present on screen and all previous will not
        """
    def mouseDown(self, button: MouseButton, modifier: KeyMod = ...) -> None:
        """
        Simulate mouse down event.
        """
    def mouseMove(self, x: int, y: int) -> None:
        """
        Simulate mouse move event.
        NOTE: Some plugins need at least TWO `mouseMove()`s in a row (possibly with the same position). If you're having issues, try sending two events.
        """
    def mouseUp(self, button: MouseButton, modifier: KeyMod = ...) -> None:
        """
        Simulate mouse up event.
        """
    def preciseFitDataViewport(self, vpList: meshlib.mrmeshpy.ViewportMask = ..., params: ViewportFitDataParams = ...) -> None:
        """
        Calls fitData and change FOV to match the screen size then
        params - params fit data
        """
    def showSceneTree(self, show: bool) -> None:
        """
        Shows or hide scene tree
        """
    def shutdown(self) -> None:
        """
        sets stop event loop flag (this flag is glfwShouldWindowClose equivalent)
        """
    def skipFrames(self, frames: int) -> None:
        ...
    def viewport(self, viewportId: meshlib.mrmeshpy.ViewportId = ...) -> Viewport:
        """
        Return the current viewport, or the viewport corresponding to a given unique identifier
        	viewportId - unique identifier corresponding to the desired viewport (current viewport if 0)
        """
    def viewportToScreen(self, arg0: meshlib.mrmeshpy.Vector3f, arg1: meshlib.mrmeshpy.ViewportId) -> meshlib.mrmeshpy.Vector3f:
        """
        Convert viewport coordinates to to screen coordinates
        """
class ViewerLaunchParams:
    """
    This struct contains rules for viewer launch
    """
    height: int
    width: int
    windowMode: ViewerLaunchParamsMode
    def __init__(self) -> None:
        ...
    @property
    def animationMaxFps(self) -> int:
        """
        max fps if animating
        """
    @animationMaxFps.setter
    def animationMaxFps(self, arg0: int) -> None:
        ...
    @property
    def fullscreen(self) -> bool:
        """
        if true starts fullscreen
        """
    @fullscreen.setter
    def fullscreen(self, arg0: bool) -> None:
        ...
    @property
    def isAnimating(self) -> bool:
        """
        if true - calls render without system events
        """
    @isAnimating.setter
    def isAnimating(self, arg0: bool) -> None:
        ...
    @property
    def name(self) -> str:
        """
        Window name
        """
    @name.setter
    def name(self, arg0: str) -> None:
        ...
class ViewerLaunchParamsMode:
    """
    Members:
    
      Hide : Don't show window
    
      HideInit : Show window after init
    
      Show : Show window immediately
    
      TryHidden : Launches in "Hide" mode if OpenGL is present and "NoWindow" if it is not
    
      NoWindow : Don't initialize GL window (don't call GL functions)(force `isAnimating`)
    """
    Hide: typing.ClassVar[ViewerLaunchParamsMode]  # value = <ViewerLaunchParamsMode.Hide: 2>
    HideInit: typing.ClassVar[ViewerLaunchParamsMode]  # value = <ViewerLaunchParamsMode.HideInit: 1>
    NoWindow: typing.ClassVar[ViewerLaunchParamsMode]  # value = <ViewerLaunchParamsMode.NoWindow: 4>
    Show: typing.ClassVar[ViewerLaunchParamsMode]  # value = <ViewerLaunchParamsMode.Show: 0>
    TryHidden: typing.ClassVar[ViewerLaunchParamsMode]  # value = <ViewerLaunchParamsMode.TryHidden: 3>
    __members__: typing.ClassVar[dict[str, ViewerLaunchParamsMode]]  # value = {'Hide': <ViewerLaunchParamsMode.Hide: 2>, 'HideInit': <ViewerLaunchParamsMode.HideInit: 1>, 'Show': <ViewerLaunchParamsMode.Show: 0>, 'TryHidden': <ViewerLaunchParamsMode.TryHidden: 3>, 'NoWindow': <ViewerLaunchParamsMode.NoWindow: 4>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class ViewerSetup:
    def __init__(self) -> None:
        ...
class Viewport:
    """
    Viewport is a rectangular area, in which the objects of interest are going to be rendered.
    An application can have a number of viewports each with its own ID.
    """
    def cameraLookAlong(self, dir: meshlib.mrmeshpy.Vector3f, up: meshlib.mrmeshpy.Vector3f) -> None:
        """
        Set camera look direction and up direction (they should be perpendicular)
        this function changes camera position and do not change camera spot (0,0,0) by default
        to change camera position use setCameraTranslation after this function
        """
    def cameraRotateAround(self, axis: meshlib.mrmeshpy.Line3f, angle: float) -> None:
        """
        Rotates camera around axis +direction applied to axis point
        note: this can make camera clip objects (as far as distance to scene center is not fixed)
        """
    def projectToViewportSpace(self, arg0: meshlib.mrmeshpy.Vector3f) -> meshlib.mrmeshpy.Vector3f:
        """
        Project world space point to viewport coordinates (in pixels), (0,0) will be at the top-left corner of the viewport.
        """
    @property
    def id(self) -> meshlib.mrmeshpy.ViewportId:
        ...
class ViewportFitDataParams:
    def __init__(self) -> None:
        ...
    @property
    def factor(self) -> float:
        """
        part of the screen for scene location
        """
    @factor.setter
    def factor(self, arg0: float) -> None:
        ...
    @property
    def mode(self) -> ViewportFitMode:
        """
        fit mode
        """
    @mode.setter
    def mode(self, arg0: ViewportFitMode) -> None:
        ...
    @property
    def snapView(self) -> bool:
        """
        snapView - to snap camera angle to closest canonical quaternion
        """
    @snapView.setter
    def snapView(self, arg0: bool) -> None:
        ...
class ViewportFitMode:
    """
    Fit mode ( types of objects for which the fit is applied )
    
    Members:
    
      Visible : fit all visible objects
    
      SelectedObjects : fit only selected objects
    
      SelectedPrimitives : fit only selected primitives
    """
    SelectedObjects: typing.ClassVar[ViewportFitMode]  # value = <ViewportFitMode.SelectedObjects: 2>
    SelectedPrimitives: typing.ClassVar[ViewportFitMode]  # value = <ViewportFitMode.SelectedPrimitives: 1>
    Visible: typing.ClassVar[ViewportFitMode]  # value = <ViewportFitMode.Visible: 0>
    __members__: typing.ClassVar[dict[str, ViewportFitMode]]  # value = {'Visible': <ViewportFitMode.Visible: 0>, 'SelectedObjects': <ViewportFitMode.SelectedObjects: 2>, 'SelectedPrimitives': <ViewportFitMode.SelectedPrimitives: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
def addDistanceMapToScene(distancemap: meshlib.mrmeshpy.DistanceMap, name: str, dmap_to_local_xf: meshlib.mrmeshpy.AffineXf3f) -> None:
    """
    Add given distance map to scene tree.
    """
def addLinesToScene(lines: meshlib.mrmeshpy.Polyline3, name: str) -> None:
    """
    Add given lines to scene tree.
    """
def addMeshToScene(mesh: meshlib.mrmeshpy.Mesh, name: str) -> None:
    """
    Add given mesh to scene tree.
    """
def addPointCloudToScene(points: meshlib.mrmeshpy.PointCloud, name: str) -> None:
    """
    Add given point cloud to scene tree.
    """
def addVoxelsToScene(voxels: meshlib.mrmeshpy.VdbVolume, name: str) -> None:
    """
    Add given voxels to scene tree.
    """
def clearScene() -> None:
    """
    remove all objects from scene tree
    """
def getSelectedDistanceMaps() -> meshlib.mrmeshpy.std_vector_DistanceMap:
    """
    Get copies of all selected voxel grids in the scene.
    """
def getSelectedMeshEdges() -> meshlib.mrmeshpy.std_vector_TypedBitSet_Id_UndirectedEdgeTag:
    """
    Get selected edge bitsets of the selected mesh objects.
    """
def getSelectedMeshFaces() -> meshlib.mrmeshpy.std_vector_TypedBitSet_Id_FaceTag:
    """
    Get selected face bitsets of the selected mesh objects.
    """
def getSelectedMeshes() -> meshlib.mrmeshpy.std_vector_Mesh:
    """
    Get copies of all selected meshes in the scene.
    """
def getSelectedObjects() -> meshlib.mrmeshpy.std_vector_std_shared_ptr_Object:
    ...
def getSelectedPointCloudPoints() -> meshlib.mrmeshpy.std_vector_TypedBitSet_Id_VertTag:
    """
    Get selected point bitsets of the selected point cloud objects.
    """
def getSelectedPointClouds() -> meshlib.mrmeshpy.std_vector_PointCloud:
    """
    Get copies of all selected point clouds in the scene.
    """
def getSelectedPolylines() -> meshlib.mrmeshpy.std_vector_Polyline_Vector3_float:
    """
    Get copies of all selected polylines in the scene.
    """
def getSelectedVoxels() -> meshlib.mrmeshpy.std_vector_VoxelsVolumeMinMax_FloatGrid:
    """
    Get copies of all selected voxel grids in the scene.
    """
def launch(params: ViewerLaunchParams = ..., setup: ViewerSetup = ...) -> None:
    """
    starts default viewer with given params and setup
    """
def modifySelectedMesh(mesh: meshlib.mrmeshpy.Mesh) -> None:
    """
    Assign a new mesh to the selected mesh object. Exactly one object must be selected.
    """
def runFromGUIThread(lambda: typing.Callable) -> None:
    """
    Executes given function from GUI thread, and returns after it is done
    """
def selectByName(objectName: str) -> None:
    """
    select objects in scene tree with given name, unselect others
    """
def selectByType(typeName: str) -> None:
    """
    string typeName: {"Meshes", "Points", "Voxels"}
    objects in scene tree with given type, unselect others
    """
def setSelectedMeshEdges(arg0: meshlib.mrmeshpy.std_vector_TypedBitSet_Id_UndirectedEdgeTag) -> None:
    """
    Set selected edge bitsets of the selected mesh objects.
    """
def setSelectedMeshFaces(arg0: meshlib.mrmeshpy.std_vector_TypedBitSet_Id_FaceTag) -> None:
    """
    Set selected face bitsets of the selected mesh objects.
    """
def setSelectedPointCloudPoints(arg0: meshlib.mrmeshpy.std_vector_TypedBitSet_Id_VertTag) -> None:
    """
    Set selected point bitsets of the selected point cloud objects.
    """
def uiListEntries(arg0: list[str]) -> list[UiEntry]:
    """
    List existing UI entries at the specified path.
    Pass an empty list to see top-level groups.
    Add group name to the end of the vector to see its contents.
    When you find the button you need, pass it to `uiPressButton()`.
    """
def uiPressButton(arg0: list[str]) -> None:
    """
    Simulate a button click. Use `uiListEntries()` to find button names.
    """
def uiReadValueInt(arg0: list[str]) -> UiValueInt:
    """
    Read a value from a drag/slider widget. This function is for signed integers.
    """
def uiReadValueReal(arg0: list[str]) -> UiValueReal:
    """
    Read a value from a drag/slider widget. This function is for real numbers.
    """
def uiReadValueString(arg0: list[str]) -> UiValueString:
    """
    Read a value from a drag/slider widget. This function is for strings.
    """
def uiReadValueUint(arg0: list[str]) -> UiValueUint:
    """
    Read a value from a drag/slider widget. This function is for unsigned integers.
    """
@typing.overload
def uiWriteValue(arg0: list[str], arg1: int) -> None:
    """
    Write a value to a drag/slider widget. This overload is for signed integers.
    """
@typing.overload
def uiWriteValue(arg0: list[str], arg1: int) -> None:
    """
    Write a value to a drag/slider widget. This overload is for unsigned integers.
    """
@typing.overload
def uiWriteValue(arg0: list[str], arg1: float) -> None:
    """
    Write a value to a drag/slider widget. This overload is for real numbers.
    """
@typing.overload
def uiWriteValue(arg0: list[str], arg1: str) -> None:
    """
    Write a value to a drag/slider widget. This overload is for strings.
    """
def uiWriteValueInt(arg0: list[str], arg1: int) -> None:
    """
    Write a value to a drag/slider widget. This overload is for signed integers.
    """
def uiWriteValueReal(arg0: list[str], arg1: float) -> None:
    """
    Write a value to a drag/slider widget. This overload is for real numbers.
    """
def uiWriteValueString(arg0: list[str], arg1: str) -> None:
    """
    Write a value to a drag/slider widget. This overload is for strings.
    """
def uiWriteValueUint(arg0: list[str], arg1: int) -> None:
    """
    Write a value to a drag/slider widget. This overload is for unsigned integers.
    """
def unselectAll() -> None:
    """
    unselect all objects in scene tree
    """
