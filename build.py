"""Builds the project pages in projects/ from one shared template, so every page has the same head, nav and footer.

Run: python build.py   (edit the page text below, then rebuild; index.html is edited by hand)
"""
from pathlib import Path

ROOT = Path(__file__).parent
EMAIL = "Omar-swellam@aucegypt.edu"

# order = the "previous / next" chain at the bottom of each page
ORDER = ["s5", "fem", "drone", "pawl", "rov", "simulator", "launcher", "cad"]
TITLES = {
    "s5": "Five-axis 3D printer (S5)",
    "fem": "Resolving a sharp corner in 1,000 nodes",
    "drone": "Quadcopter modeling and control",
    "pawl": "Ratchet pawl design search",
    "rov": "Underwater robot (ROV)",
    "simulator": "Force-feedback driving simulator",
    "launcher": "Smart tennis ball launcher",
    "cad": "Personal CAD: F1 car, V10, GE90",
}


def page(slug, desc, body):
    i = ORDER.index(slug)
    prev, nxt = ORDER[i - 1], ORDER[(i + 1) % len(ORDER)]
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLES[slug]} | Omar Swellam</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../style.css">
</head>
<body>

<header class="nav">
  <div class="wrap nav-in">
    <a class="brand" href="../index.html">Omar Swellam</a>
    <nav class="links" style="display:flex">
      <a href="../index.html#projects">All projects</a>
      <a class="btn small" href="../Omar_Swellam_CV.pdf" target="_blank" rel="noopener">CV</a>
    </nav>
  </div>
</header>

<main class="wrap narrow">
<a class="back" href="../index.html#projects">&larr; All projects</a>
{body.strip()}
<nav class="next">
  <a href="{prev}.html">&larr; Previous<b>{TITLES[prev]}</b></a>
  <a href="{nxt}.html">Next &rarr;<b>{TITLES[nxt]}</b></a>
</nav>
</main>

<footer class="foot">
  <div class="wrap foot-in">
    <p>&copy; 2026 Omar Swellam &middot; <a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <p>Built with the help of Claude (Anthropic). All projects and results are my own work.</p>
  </div>
</footer>

<div class="lightbox" hidden><img alt=""><button aria-label="Close">&times;</button></div>
<script src="../script.js"></script>
</body>
</html>
"""
    (ROOT / "projects").mkdir(exist_ok=True)
    (ROOT / "projects" / f"{slug}.html").write_text(html, encoding="utf-8", newline="\n")


def fig(src, cap, alt=None):
    return f'<figure><img src="../img/{src}" alt="{alt or cap}" loading="lazy"><figcaption>{cap}</figcaption></figure>'


def kpis(*items):
    return '<div class="kpis">' + "".join(f"<div><b>{b}</b><span>{s}</span></div>" for b, s in items) + "</div>"


def ba(name, title, text):
    """before/after pair: flat print (left) vs S5 (right)"""
    return f"""<div class="pair">
  <div class="ba">
    <figure><img src="../img/s5_{name}_flat.jpg" alt="{title}, flat layers" loading="lazy"><span class="tag l">Flat</span></figure>
    <figure><img src="../img/s5_{name}_s5.jpg" alt="{title}, S5 curved layers" loading="lazy"><span class="tag l">S5</span></figure>
  </div>
  <h3>{title}</h3><p>{text}</p>
</div>"""


def hero(kicker, title, lead, facts):
    f = "".join(f"<span>{k} <b>{v}</b></span>" for k, v in facts)
    return f"""<section class="p-hero">
  <p class="kicker">{kicker}</p>
  <h1>{title}</h1>
  <p class="lead">{lead}</p>
  <div class="facts">{f}</div>
</section>"""


# ------------------------------------------------------------------ S5
page("s5", "Senior thesis: a five-axis 3D printer and the slicer that curves its layers for less support or more strength.", f"""
{hero("Senior thesis &middot; 2026&ndash;2027", TITLES["s5"],
      "A 3D printer whose bed tilts, and the software that curves each layer, so a part needs less support material or comes out stronger where it is pulled.",
      [("Role", "Thesis Coordinator"), ("Team", "5"), ("Tools", "Python, FEA, CuraEngine, RepRapFirmware")])}
<div class="pairs">
{ba("mushroom", "Mushroom cap", "Flat: the underside of the cap (red) hangs out past 45&deg; and needs about 2.2 g of support. S5: the layers follow the cap, the overhang area drops from 724 to 1 mm&sup2;, and no support is printed.")}
{ba("capital", "Column capital", "Flat: the flared top needs support all round. S5: the overhang area drops from 452 to 0 mm&sup2;, so it prints with no support at all.")}
</div>
<section class="p-body">
<h2>The problem</h2>
<p>A normal printer stacks flat layers. Anything that hangs out more than about 45&deg; has nothing under it, so the slicer adds support material that is printed and then thrown away. Flat layers are also weak in one direction: a part pulled across its layers breaks along them.</p>
<p>A five-axis printer can tilt the part while it prints (our bed tilts up to 60&deg;), so the layers don't have to be flat. The hard part is the software: deciding how the layers should curve and making sure the nozzle never hits the part or the bed.</p>

<h2>What the slicer does</h2>
<p>Each part on the plate gets one of two modes:</p>
<ul>
  <li><b>Low support:</b> the layers curve around the overhangs, so less of the part hangs over air.</li>
  <li><b>Strength:</b> a finite element analysis (FEA) of the part under its loads finds where it is pulled hardest, and the layers curve so the pull runs along them, not across.</li>
</ul>
<p>Then it checks every move for collisions with the tilted bed, fixes the ones it finds, and hands the curved layers to CuraEngine for the actual toolpaths. The printer runs RepRapFirmware 3.6.3 on a Duet 3, and I added the machine's five-axis kinematics to it, so the slicer and the printer use the same maths. Saving G-code refuses any file the printer would stop on, and lists the moves that would cause it.</p>

<h2>Results: support</h2>
<p>We compare S5 against normal flat slicing on a benchmark of 40 test parts, same print settings, same printer profile.</p>
{kpis(("&minus;35%", "support material, 32.1 &rarr; 21.0 g over 40 parts"), ("14", "parts that need no support at all"), ("&minus;57%", "overhang area that needs support"), ("0", "collisions in the final toolpaths"))}
<p>The parts that gained the most:</p>
<div class="table-wrap"><table>
  <thead><tr><th>Part</th><th class="num">Flat support (g)</th><th class="num">S5 support (g)</th></tr></thead>
  <tbody>
    <tr><td>Flared vase</td><td class="num">3.52</td><td class="num">0</td></tr>
    <tr><td>Wide cone</td><td class="num">3.09</td><td class="num">0</td></tr>
    <tr><td>Flat mushroom</td><td class="num">2.13</td><td class="num">0</td></tr>
    <tr><td>Round mushroom cap</td><td class="num">1.44</td><td class="num">0</td></tr>
    <tr><td>Big T</td><td class="num">1.34</td><td class="num">0</td></tr>
    <tr><td>Flag cantilever</td><td class="num">0.98</td><td class="num">0</td></tr>
    <tr><td>Goblet (45&deg; flare)</td><td class="num">0.93</td><td class="num">0</td></tr>
    <tr><td>Spiral ramp tower</td><td class="num">0.87</td><td class="num">0.01</td></tr>
    <tr><td>T shape</td><td class="num">0.70</td><td class="num">0</td></tr>
    <tr><td>Tree branches</td><td class="num">0.53</td><td class="num">0</td></tr>
  </tbody>
</table></div>
<p>Not every part improves. On a few (an umbrella, a shelf bracket) flat slicing still needs less support, and the 40-part totals above include them.</p>

<h2>Results: strength</h2>
<div class="pairs">{ba("hook", "Wall hook", "Flat layers (left) cross the hook's bend, its weakest point. In Strength mode (right) the layers follow the pull.")}</div>
<p>On 8 strength test parts, the stress pulling across the layers (the direction prints break in) went down on 7, by up to 56%.</p>

<h2>My role</h2>
<ul>
  <li>Coordinate the team of five since September 2026: split the tasks, set the weekly priorities and keep the progress log.</li>
  <li>Built the slicer and the firmware kinematics. I worked with several AI coding agents on a shared task board: they claim tasks and log results, and I review and test their work before it is accepted.</li>
  <li>Used agentic AI to build a simple mass-spring-damper model of the printer that predicts its vibration in seconds; its loads feed the FEA checks of the critical brackets.</li>
</ul>
</section>
""")

# ------------------------------------------------------------------ FEM
page("fem", "MENG 4553 Finite Element Methods: a three-tier submodel chain that resolves a sharp corner within a 1,000-node license, plus thermo-plastic necking.", f"""
{hero("MENG 4553 Finite Element Methods &middot; Fall 2026", TITLES["fem"],
      "Our Abaqus license only allows 1,000 nodes per model. So to see the stress at a sharp corner, I zoomed in three times, each model feeding the next.",
      [("Software", "Abaqus + Python"), ("Load", "10 kN"), ("Status", "final project in progress")])}
<div class="cover contain"><img src="../img/fem_1.jpg" alt="Von Mises stress in the three submodel tiers"></div>
<section class="p-body">
<h2>The problem</h2>
<p>The part is a stepped plate under 10 kN, about 200 MPa away from the step. Where the two widths meet there is a sharp 270&deg; inside corner. In theory the stress there is infinite (the Williams singularity), so it keeps rising as the mesh gets finer. The question is what number you can honestly report, when the free Learning Edition caps every model at 1,000 nodes.</p>

<h2>The approach: three tiers</h2>
<ul>
  <li><b>Tier 1</b> models the whole plate coarsely (915 nodes).</li>
  <li><b>Tier 2</b> cuts out the region round the corner and takes its edge displacements from tier 1 (996 nodes).</li>
  <li><b>Tier 3</b> zooms in again on the corner itself (996 nodes).</li>
</ul>
<p>Each model stays under the limit, but together they reach a mesh far finer than one 1,000-node model could.</p>
{fig("fem_4.jpg", "The three meshes at true scale: each tier zooms into the corner of the one before.")}

<h2>Results</h2>
{kpis(("436", "MPa, tier 1 peak"), ("1,155", "MPa, tier 2 peak"), ("1,555", "MPa, tier 3 peak"), ("2,057", "MPa, extrapolated"))}
<p>I checked mesh convergence with Richardson extrapolation, as set out in ASME V&amp;V 10. The extrapolated peak is 2,057 MPa, but the grid convergence index (GCI) is 40%. That doesn't mean the models are wrong. It is what a singular corner should do: the stress never settles. The useful conclusion is that you can't design to the peak at a sharp corner. You add a fillet, or you judge the part on the stress a short distance away.</p>
{fig("fem_2.jpg", "Peak stress against mesh size: it keeps climbing, as a singularity should.")}
{fig("fem_3.jpg", "The extrapolated stress field, mapped back onto the mesh with an Abaqus Python script.")}

<h2>Lab: thermo-plastic necking</h2>
<p>A notched bar pulled until it necks, once slowly and once fast. Plastic work turns into heat, and how hot the neck gets depends on how fast you pull, because the heat has less time to escape.</p>
{kpis(("20.0 &deg;C", "peak temperature, slow pull"), ("444.5 &deg;C", "fast pull"), ("607 &deg;C", "adiabatic (no heat escapes)"), ("6.78 kN", "peak force"))}
<div class="figs">
  {fig("fem_5.jpg", "Notched bar: mesh, plastic strain and temperature at the neck.")}
  {fig("fem_6.jpg", "Peak temperature against displacement.")}
</div>

<h2>Final project (in progress)</h2>
<p>A notched shaft followed end to end in Abaqus: from manufacturing through to service loads, with plasticity, damage and thermal effects. The submodeling method above is how it gets enough detail at the notch.</p>
</section>
""")

# ------------------------------------------------------------------ drone
page("drone", "MENG 3705 System Dynamics: nonlinear quadcopter model and cascaded PID control in MATLAB/Simulink.", f"""
{hero("MENG 3705 System Dynamics &middot; Fall 2025", TITLES["drone"],
      "We modeled a quadcopter from first principles, showed that without control it is unstable, then designed a controller that flies it along a 3D spiral.",
      [("Role", "Project Coordinator"), ("Team", "5"), ("Tools", "MATLAB, Simulink")])}
<div class="cover contain"><img src="../img/drone_2.jpg" alt="Spiral trajectory: reference vs actual, 3D, top and side views"></div>
<section class="p-body">
<h2>The model</h2>
<p>A 1.2 kg quadcopter with 0.23 m arms. We derived its nonlinear equations of motion with Newtonian mechanics (thrust, drag, and an offset centre of gravity), then linearised them about hover. The state-space model is controllable and observable, and open loop it is unstable, so it can't fly without a controller.</p>

<h2>The controller</h2>
<p>A cascaded PID: an outer loop turns position errors in X, Y and Z into the roll and pitch angles and thrust needed; an inner loop holds those angles. I added angle and input limits with anti-windup, and the motor dynamics.</p>
{fig("drone_1.jpg", "The full Simulink model: outer loop, inner loop, motor dynamics and the plant.")}
{fig("drone_5.jpg", "Inside the outer loop: three PIDs turn position errors into pitch, roll and thrust commands.")}

<h2>Results</h2>
<p>Every axis follows a unit step with under 10% overshoot and stays stable:</p>
<div class="table-wrap"><table>
  <thead><tr><th>Axis</th><th class="num">Rise (s)</th><th class="num">Settling (s)</th><th class="num">Overshoot</th></tr></thead>
  <tbody>
    <tr><td>X</td><td class="num">1.26</td><td class="num">6.26</td><td class="num">8.5%</td></tr>
    <tr><td>Y</td><td class="num">1.20</td><td class="num">5.69</td><td class="num">9.0%</td></tr>
    <tr><td>Z (altitude)</td><td class="num">0.76</td><td class="num">3.00</td><td class="num">5.9%</td></tr>
    <tr><td>Yaw</td><td class="num">1.16</td><td class="num">3.65</td><td class="num">~0%</td></tr>
    <tr><td>Pitch</td><td class="num">0.68</td><td class="num">2.85</td><td class="num">7.4%</td></tr>
    <tr><td>Roll</td><td class="num">0.77</td><td class="num">3.23</td><td class="num">~0%</td></tr>
  </tbody>
</table></div>
<p>Steps in X, Y and Z at the same time behave almost exactly like separate ones, so the axes are well decoupled. On the spiral it drifts wide on the first loop, then tracks the reference closely.</p>
{fig("drone_3.jpg", "Unit steps in X, Y, Z and yaw, with MATLAB's step metrics.")}

<h2>What if the centre of gravity moves?</h2>
<p>We swept the centre of gravity &plusmn;0.3 m in X and Y: 61 &times; 61 = 3,721 cases. The matrix that splits commands between the four rotors stayed well-conditioned in every one (condition number about 10 to 10.8, none ill-conditioned). Performance does get worse at large offsets, and at the extremes the drone goes partly unstable. The gains were tuned by hand, so there is room to optimise them.</p>
{fig("drone_4.jpg", "Condition number of the rotor-mixing matrix across the centre-of-gravity sweep.")}

<h2>My role</h2>
<p>Project coordinator for the team of five. I updated the mathematical model and built the MATLAB and Simulink simulation.</p>
</section>
""")

# ------------------------------------------------------------------ pawl
page("pawl", "Research assistant: an automated Abaqus search over 3,000+ ratchet-pawl geometries for 3D-printed resin micro actuators.", f"""
{hero("Research Assistant, Micro Linear Actuators &middot; AUC &middot; 2026&ndash;", TITLES["pawl"],
      "A tiny 3D-printed resin pawl has to lock the actuator and survive the load. I automated the search: over 3,000 designs tested by FEA, and 20 that pass every check.",
      [("Software", "Abaqus + Python"), ("Material", "3D-printed resin"), ("Designs tested", "3,000+")])}
<div class="cover contain"><img src="../img/pawl_mises.jpg" alt="Abaqus von Mises stress in a ratchet pawl"></div>
<section class="p-body">
<h2>The problem</h2>
<p>The lab builds small linear actuators driven by shape memory alloys (SMA), wires that shorten when heated. A ratchet and pawl holds the position between strokes. Printed in resin, the pawl is small and brittle, so it has to be stiff enough to lock and strong enough not to crack. Changing one dimension changes both.</p>

<h2>The approach</h2>
<ul>
  <li><b>Geometry:</b> a curved pawl arm built from up to five arcs, plus the rack teeth. The variables are arm thickness, arc curvatures and lengths, end radius, root fillets, base size, tooth pitch (0.8&ndash;2.2 mm), tooth height and ramp angle.</li>
  <li><b>Each design:</b> a Python script builds it in Abaqus (grey resin, E = 2,800 MPa, 4 mm thick), meshes it within the 1,000-node limit, and simulates locking forward, reverse and travel.</li>
  <li><b>Checks:</b> resin tension &le; 20 MPa and compression &le; 40 MPa; the lock must hold 4.5 N even at the weakest print corner; push force &le; 1.5 N; no buckling; fits in 10 &times; 10 mm.</li>
  <li><b>Search:</b> a surrogate model picks which designs to simulate next, then a stress-guided step refines the best ones.</li>
</ul>

<h2>Results</h2>
{kpis(("4,600+", "designs simulated over six search runs"), ("20", "designs pass every check"), ("2.22", "safety factor of the best design"), ("7 &times; 5 mm", "size of the best design"))}
<p>The first runs found nothing that passed. The spec was tight, and printed resin is weak. Shrinking the pawl and tightening the print tolerance to &plusmn;0.05 mm is what made 20 designs pass. The best one locks at all 8 worst-case print corners with a forward stress around 28 MPa.</p>
</section>
""")

# ------------------------------------------------------------------ ROV
page("rov", "AUC Aquavaders: mechanical team lead for an underwater robot in the MATE ROV competition.", f"""
{hero("AUC Aquavaders &middot; MATE ROV Competition", TITLES["rov"],
      "An underwater robot built by students for the MATE competition. I joined the mechanical team in 2025 and have led it since June 2026.",
      [("Role", "Mechanical Team Lead"), ("Since", "June 2025"), ("Tools", "SolidWorks, ANSYS CFD and FEA")])}
<div class="figs">
  {fig("rov_team.jpg", "The team with our ROV at the competition.")}
  {fig("rov_poster.jpg", "AUC Aquavaders at the Arab Academy.")}
</div>
<section class="p-body">
<h2>What the mechanical team does</h2>
<ul>
  <li><b>Propulsion:</b> where the thrusters go and how they point, so the robot can move and turn in every direction.</li>
  <li><b>Buoyancy and stability:</b> placing the components so the robot floats level and stays steady.</li>
  <li><b>Structure:</b> the frame, designed in CAD and checked with FEA; CFD to cut drag.</li>
  <li>Fabrication, 3D printing and pool testing.</li>
</ul>

<h2>My role</h2>
<p>In my first year I designed the propulsion and buoyancy layout and ran the CFD. As team lead, I split the work, manage the timeline, and coordinate with the software and electronics teams, so that the mechanics, wiring and controls fit together.</p>
</section>
""")

# ------------------------------------------------------------------ simulator
page("simulator", "MENG 4778 Microcontrollers and Mechatronics: a force-feedback steering wheel for a driving simulator.", f"""
{hero("MENG 4778 Microcontrollers &amp; Mechatronics &middot; Fall 2026", TITLES["simulator"],
      "A steering wheel that pushes back like a real car: at least 2.5 Nm of force feedback from a DC motor, run by an Arduino.",
      [("Team", "5"), ("Status", "in progress"), ("My part", "CAM / CNC, assembly, electronics")])}
<div class="figs">
  {fig("sim_cad.jpg", "CAD of the wheel base.")}
  {fig("sim_cad2.jpg", "The drive: DC motor and 5:1 belt reduction.")}
</div>
<section class="p-body">
<h2>How it works</h2>
<ul>
  <li>A DC motor drives the steering shaft through a 5:1 belt, so a small motor gives enough torque.</li>
  <li>A 600-pulse encoder reads the wheel angle; an Arduino and motor driver set the torque.</li>
  <li>The game sends the effects over USB: centering, damping and vibration.</li>
</ul>

<h2>My role</h2>
<p>I did the CAM and CNC machining of the wheel's main frame. Next I'm helping with assembly and the electronics.</p>
</section>
""")

# ------------------------------------------------------------------ launcher
page("launcher", "MENG 4779 Electromechanical Systems: a 3D-printed counter-rotating tennis ball launcher with PLC control.", f"""
{hero("MENG 4779 Electromechanical Systems &middot; Spring 2026", TITLES["launcher"],
      "A tennis ball launcher we designed, printed, wired and programmed: two wheels spinning in opposite directions fire the ball, and a PLC runs it.",
      [("Role", "Project Coordinator"), ("Team", "5"), ("Tools", "SolidWorks, RSLogix")])}
<div class="cover"><img src="../img/launcher.jpg" alt="The printed launcher with its electronics"></div>
<section class="p-body">
<h2>Design</h2>
<p>Two wheels spin in opposite directions and grip the ball between them, so it leaves at the wheels' surface speed. I led the mechanical hardware: designed in SolidWorks and 3D printed.</p>

<h2>Control</h2>
<p>PLC ladder logic, written and verified in RSLogix:</p>
<ul>
  <li>start and stop,</li>
  <li>a timed auto-shutdown,</li>
  <li>a counter for the balls fired.</li>
</ul>
</section>
""")

# ------------------------------------------------------------------ CAD
def gallery(pics):
    return '<div class="figs">' + "".join(fig(s, c) for s, c in pics) + "</div>"


page("cad", "Personal Fusion 360 projects: a Formula 1 car, a V10 hybrid engine and a GE90 jet engine.", f"""
{hero("Personal projects &middot; Fusion 360 &middot; 2024&ndash;2025", TITLES["cad"],
      "I taught myself Fusion 360 to model an F1 car, and it went from there: an engine for it, and then a jet engine.",
      [("Hours", "100+ on the car alone"), ("Tool", "Fusion 360"), ("Self-taught", "yes")])}
<section class="p-body">
<h2 id="f1">Formula 1 car</h2>
<p class="tile-meta">January&ndash;May 2024</p>
<p>Modeled from scratch over 20 versions and 100+ hours: diffusers, Venturi tunnels, multi-element wings and suspension.</p>
{gallery([("f1car_side2.jpg", "Side"), ("f1car_front.jpg", "Front"), ("f1car_top.jpg", "Top"), ("f1car_nose.jpg", "Nose and cockpit")])}

<h2 id="v10">F1 V10 hybrid engine</h2>
<p class="tile-meta">July&ndash;November 2024</p>
<p>A naturally aspirated V10 with an MGU-K, as my answer to the 2026 rules: over 1,000 components, about 20,000 RPM and about 950 hp as a concept. Joints simulate the engine's motion.</p>
{gallery([("v10_car.jpg", "The engine in the car"), ("v10_block.jpg", "Pistons and gears"), ("v10_mguk.jpg", "MGU-K motor"), ("v10_top.jpg", "From above")])}

<h2 id="ge90">GE90 jet engine</h2>
<p class="tile-meta">December 2024&ndash;January 2025</p>
<p>The Boeing 777's engine, from fan to nozzle: the multi-stage compressor and turbine, the bypass ratio and the combustor.</p>
{gallery([("ge90_section.jpg", "Section"), ("ge90_nacelle.jpg", "Nacelle and fan"), ("ge90_core.jpg", "Core"), ("ge90_cutaway.jpg", "Cutaway")])}
</section>
""")

print("built", ", ".join(ORDER))
