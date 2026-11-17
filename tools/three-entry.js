// The parts of three.js the viewer (skills/fdm-minimal-design/scripts/viewer/fdm-viewer.js) uses,
// bundled into one IIFE (window.THREE) by tools/build_three.sh.
export {
  WebGLRenderer, Scene, PerspectiveCamera, MOUSE, Color, Group, MeshStandardMaterial, HemisphereLight,
  DirectionalLight, Vector2, Vector3, Box3, Sphere, Raycaster, SRGBColorSpace, EdgesGeometry, LineSegments,
  LineBasicMaterial, GridHelper,
} from "three";
export { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
export { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
