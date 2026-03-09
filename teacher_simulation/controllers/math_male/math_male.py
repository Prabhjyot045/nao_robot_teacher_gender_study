"""
ECE 787 - Gender Bias in Robotic Educators
Controller: Male Math (Agentic/Authoritative Style)
Subject: Mathematics - The Pythagorean Theorem
Gesture Style: Linear transitions, direct/rigid arm movements

This controller plays the male-voice math lesson audio and
performs synchronized gestures using HIGH motor velocities to
create sharp, direct, authoritative teaching movements.
"""

from controller import Robot, Speaker

# ---------------------------------------------------------------------------
#  Configuration
# ---------------------------------------------------------------------------

# Path to the recorded MP3 audio file (relative to this controller's folder)
AUDIO_FILE = "../../audio/math_male.mp3"

# Volume for audio playback (0.0 - 1.0)
VOLUME = 1.0

# Motor speed profiles — male style uses HIGH velocity for sharp, linear moves
DIRECT_SPEED = 2.0   # rad/s – brisk, decisive motion
PHALANX_MAX  = 8

# ---------------------------------------------------------------------------
#  Gesture timing (seconds from start of audio)
#  TODO: Fine-tune these values after reviewing your final MP3 recording.
# ---------------------------------------------------------------------------
T_INTRO         =  0.0   # "Good morning. Let's get straight..."
T_OBJECTIVE     =  3.0   # "Today's objective is to master..."
T_FORMULA_INTRO =  9.0   # "the square of the hypotenuse..."
T_WRITE_FORMULA = 16.0   # "A squared plus B squared..."
T_DEFINE_C      = 22.0   # "C represents the hypotenuse..."
T_DEFINE_AB     = 28.0   # "A and B are the shorter legs"
T_SOLVE         = 34.0   # "isolate the variable..."
T_PRECISE       = 42.0   # "a precise system..."
T_FOCUS         = 50.0   # "Focus on the structure..."
T_PRACTICE      = 58.0   # "Let's move on to the practice..."
T_END           = 68.0   # End of lesson / cooldown


# ---------------------------------------------------------------------------
#  Robot Setup
# ---------------------------------------------------------------------------

robot    = Robot()
timestep = int(robot.getBasicTimeStep())

# --- Head motors ---
HeadYaw   = robot.getDevice("HeadYaw")
HeadPitch = robot.getDevice("HeadPitch")

# --- Right arm motors ---
RShoulderPitch = robot.getDevice("RShoulderPitch")
RShoulderRoll  = robot.getDevice("RShoulderRoll")
RElbowYaw      = robot.getDevice("RElbowYaw")
RElbowRoll     = robot.getDevice("RElbowRoll")
RWristYaw      = robot.getDevice("RWristYaw")

# --- Left arm motors ---
LShoulderPitch = robot.getDevice("LShoulderPitch")
LShoulderRoll  = robot.getDevice("LShoulderRoll")
LElbowYaw      = robot.getDevice("LElbowYaw")
LElbowRoll     = robot.getDevice("LElbowRoll")
LWristYaw      = robot.getDevice("LWristYaw")

# --- Hand phalanx motors (2x8 in Webots) ---
rphalanx = []
lphalanx = []
for i in range(PHALANX_MAX):
    rphalanx.append(robot.getDevice("RPhalanx%d" % (i + 1)))
    lphalanx.append(robot.getDevice("LPhalanx%d" % (i + 1)))

# --- Speaker for audio playback ---
# IMPORTANT: The NAO does not include a Speaker by default.
# You must add a Speaker node to the NAO's children in the world file
# with the name "Speaker". See SPEAKER_SETUP.md for instructions.
speaker = robot.getDevice("Speaker")
if speaker is None:
    print("ERROR: Speaker device not found on NAO.")
    print("  You must add a Speaker node to the NAO robot in the world file.")
    print("  In the scene tree: Nao > children > Add > Speaker (set name to 'Speaker')")
    print("  See SPEAKER_SETUP.md for detailed instructions.")

# --- LEDs (for consistent visual appearance across conditions) ---
leds = []
leds.append(robot.getDevice("ChestBoard/Led"))
leds.append(robot.getDevice("RFoot/Led"))
leds.append(robot.getDevice("LFoot/Led"))
leds.append(robot.getDevice("Face/Led/Right"))
leds.append(robot.getDevice("Face/Led/Left"))
leds.append(robot.getDevice("Ears/Led/Right"))
leds.append(robot.getDevice("Ears/Led/Left"))


# ---------------------------------------------------------------------------
#  Helper functions
# ---------------------------------------------------------------------------

def direct_move(motor, position):
    """Set motor to target with HIGH velocity — sharp, decisive (male style)."""
    motor.setVelocity(DIRECT_SPEED)
    motor.setPosition(position)


def set_hand(phalanx_list, angle):
    """Open / close a hand (list of 8 phalanx motors)."""
    for motor in phalanx_list:
        if motor:
            motor.setPosition(angle)


def set_neutral_pose():
    """Arms at sides, attentive but still — authoritative resting posture."""
    direct_move(RShoulderPitch,  1.4)
    direct_move(RShoulderRoll,  -0.15)
    direct_move(RElbowYaw,       1.4)
    direct_move(RElbowRoll,      0.5)
    direct_move(LShoulderPitch,  1.4)
    direct_move(LShoulderRoll,   0.15)
    direct_move(LElbowYaw,      -1.4)
    direct_move(LElbowRoll,     -0.5)
    direct_move(HeadYaw,         0.0)
    direct_move(HeadPitch,       0.0)
    set_hand(rphalanx, 0.0)
    set_hand(lphalanx, 0.0)


# ---------------------------------------------------------------------------
#  Gesture choreography
#
#  Male-Authoritative style:
#    - All movements use DIRECT_SPEED (2.0 rad/s) for crisp, snappy motion.
#    - Gestures are purposeful: pointing, presenting, returning to neutral.
#    - Hands mostly closed or flat; minimal idle sway.
# ---------------------------------------------------------------------------

# Track which gestures have already been triggered
triggered = set()

def run_gestures(t):
    """Dispatch gesture keyframes based on elapsed simulation time `t`."""

    # ---- INTRO: slight head-down nod, hands at sides ----
    if t >= T_INTRO and "intro" not in triggered:
        triggered.add("intro")
        set_neutral_pose()
        direct_move(HeadPitch, 0.15)   # small nod

    # ---- OBJECTIVE: right arm points forward/up (to board) ----
    if t >= T_OBJECTIVE and "objective" not in triggered:
        triggered.add("objective")
        direct_move(HeadPitch, 0.0)
        direct_move(RShoulderPitch,  0.4)
        direct_move(RShoulderRoll,  -0.2)
        direct_move(RElbowRoll,      0.1)
        set_hand(rphalanx, 0.5)       # flat / pointing hand

    # ---- FORMULA INTRO: both arms slightly raised, palms out ----
    if t >= T_FORMULA_INTRO and "formula_intro" not in triggered:
        triggered.add("formula_intro")
        direct_move(RShoulderPitch, 0.8)
        direct_move(LShoulderPitch, 0.8)
        direct_move(RElbowRoll,     0.4)
        direct_move(LElbowRoll,    -0.4)

    # ---- WRITE FORMULA: right arm sweeps across (writing on board) ----
    if t >= T_WRITE_FORMULA and "write_formula" not in triggered:
        triggered.add("write_formula")
        direct_move(RShoulderPitch,  0.3)
        direct_move(RShoulderRoll,  -0.5)
        direct_move(RElbowYaw,       0.8)
        direct_move(RElbowRoll,      0.2)
        set_hand(rphalanx, 0.7)       # extended finger
        direct_move(LShoulderPitch,  1.4)
        direct_move(LElbowRoll,     -0.5)

    # Sweep right arm across after short pause
    if t >= T_WRITE_FORMULA + 2.0 and "write_sweep" not in triggered:
        triggered.add("write_sweep")
        direct_move(RShoulderRoll, 0.1)

    # ---- DEFINE C: point right arm upward (hypotenuse) ----
    if t >= T_DEFINE_C and "define_c" not in triggered:
        triggered.add("define_c")
        direct_move(RShoulderPitch, 0.2)
        direct_move(RShoulderRoll, -0.15)
        direct_move(RElbowYaw,      1.2)
        direct_move(RElbowRoll,     0.05)
        set_hand(rphalanx, 0.5)

    # ---- DEFINE AB: left arm joins, indicating two shorter sides ----
    if t >= T_DEFINE_AB and "define_ab" not in triggered:
        triggered.add("define_ab")
        direct_move(LShoulderPitch, 0.6)
        direct_move(LShoulderRoll,  0.15)
        direct_move(LElbowRoll,    -0.2)
        set_hand(lphalanx, 0.5)
        direct_move(RShoulderPitch, 0.6)

    # ---- SOLVE: deliberate right-arm chop (emphasis) ----
    if t >= T_SOLVE and "solve" not in triggered:
        triggered.add("solve")
        direct_move(LShoulderPitch, 1.4)
        direct_move(LElbowRoll,    -0.5)
        set_hand(lphalanx, 0.0)
        direct_move(RShoulderPitch, 0.5)
        direct_move(RElbowRoll,     0.9)
        direct_move(RWristYaw,      0.0)
        set_hand(rphalanx, 0.0)       # closed fist – decisive

    # ---- PRECISE SYSTEM: small firm nod ----
    if t >= T_PRECISE and "precise" not in triggered:
        triggered.add("precise")
        set_neutral_pose()
        direct_move(HeadPitch, 0.2)    # nod down

    if t >= T_PRECISE + 0.8 and "precise_up" not in triggered:
        triggered.add("precise_up")
        direct_move(HeadPitch, 0.0)    # nod back up

    # ---- FOCUS: right arm points forward at audience ----
    if t >= T_FOCUS and "focus" not in triggered:
        triggered.add("focus")
        direct_move(RShoulderPitch, 0.5)
        direct_move(RShoulderRoll, -0.1)
        direct_move(RElbowYaw,      1.0)
        direct_move(RElbowRoll,     0.05)
        set_hand(rphalanx, 0.6)

    # ---- PRACTICE SET: return to neutral, brief nod ----
    if t >= T_PRACTICE and "practice" not in triggered:
        triggered.add("practice")
        set_neutral_pose()

    if t >= T_PRACTICE + 1.0 and "practice_nod" not in triggered:
        triggered.add("practice_nod")
        direct_move(HeadPitch, 0.15)   # concluding nod

    # ---- END: hold neutral ----
    if t >= T_END and "end" not in triggered:
        triggered.add("end")
        set_neutral_pose()


# ---------------------------------------------------------------------------
#  Main loop
# ---------------------------------------------------------------------------

# Settle into neutral pose
set_neutral_pose()
for _ in range(20):
    robot.step(timestep)

# Set LED colour – neutral blue (consistent across all four conditions)
for i in range(5):
    leds[i].set(0x0033cc)

# Start audio playback
if speaker:
    # Speaker.playSound(left, right, sound, volume, pitch, balance, loop)
    Speaker.playSound(speaker, speaker, AUDIO_FILE, VOLUME, 1.0, 0.0, False)
else:
    print("WARNING: Skipping audio — no Speaker device. Gestures will still run.")

# Run the lesson
elapsed = 0.0
while robot.step(timestep) != -1:
    elapsed += timestep / 1000.0
    run_gestures(elapsed)

    # Stop after the lesson finishes + a brief hold
    if elapsed >= T_END + 3.0:
        break

# Final neutral hold
set_neutral_pose()
for _ in range(40):
    robot.step(timestep)