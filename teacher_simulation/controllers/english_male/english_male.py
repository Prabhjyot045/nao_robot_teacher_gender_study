"""
ECE 787 - Gender Bias in Robotic Educators
Controller: Male English (Analytical/Structural Style)
Subject: English - Literary Device: Personification
Gesture Style: Linear transitions, direct/rigid arm movements

This controller plays the male-voice English lesson audio and
performs synchronized gestures using HIGH motor velocities to
create sharp, analytical, structural teaching movements.
"""

from controller import Robot, Speaker

# ---------------------------------------------------------------------------
#  Configuration
# ---------------------------------------------------------------------------

AUDIO_FILE   = "../../audio/english_male.mp3"
VOLUME       = 5.0
DIRECT_SPEED = 2.0   # rad/s – brisk, decisive motion
PHALANX_MAX  = 8

# ---------------------------------------------------------------------------
#  Gesture timing (seconds from start of audio)
#  TODO: Fine-tune after reviewing your final MP3 recording.
# ---------------------------------------------------------------------------
T_SESSION     =  0.0   # "In this session, we will analyze..."
T_DEVICE      =  4.0   # "personification. This is a..."
T_ATTRIBUTE   =  9.0   # "systematically attribute human..."
T_WRITER      = 14.0   # "a writer forces the reader..."
T_IMPACT      = 19.0   # "heighten the narrative's impact"
T_EXAMPLE     = 23.0   # "Consider this standard example..."
T_WIND        = 28.0   # "'The wind howled in the night.'"
T_TECHNICALLY = 33.0   # "Technically, wind does not..."
T_APPLYING    = 39.0   # "by applying this human action..."
T_CALCULATED  = 45.0   # "a calculated choice..."
T_IDENTIFY    = 51.0   # "Identify this device..."
T_EXAMINE     = 57.0   # "We will now examine further..."
T_END         = 66.0   # End of lesson / cooldown


# ---------------------------------------------------------------------------
#  Robot Setup
# ---------------------------------------------------------------------------

robot    = Robot()
timestep = int(robot.getBasicTimeStep())

# Head
HeadYaw   = robot.getDevice("HeadYaw")
HeadPitch = robot.getDevice("HeadPitch")

# Right arm
RShoulderPitch = robot.getDevice("RShoulderPitch")
RShoulderRoll  = robot.getDevice("RShoulderRoll")
RElbowYaw      = robot.getDevice("RElbowYaw")
RElbowRoll     = robot.getDevice("RElbowRoll")
RWristYaw      = robot.getDevice("RWristYaw")

# Left arm
LShoulderPitch = robot.getDevice("LShoulderPitch")
LShoulderRoll  = robot.getDevice("LShoulderRoll")
LElbowYaw      = robot.getDevice("LElbowYaw")
LElbowRoll     = robot.getDevice("LElbowRoll")
LWristYaw      = robot.getDevice("LWristYaw")

# Hands
rphalanx = []
lphalanx = []
for i in range(PHALANX_MAX):
    rphalanx.append(robot.getDevice("RPhalanx%d" % (i + 1)))
    lphalanx.append(robot.getDevice("LPhalanx%d" % (i + 1)))

# Speaker — requires a Speaker node added to the NAO in the world file
# See SPEAKER_SETUP.md for instructions.
speaker = robot.getDevice("Speaker")
if speaker is None:
    print("ERROR: Speaker device not found. Add a Speaker node to the NAO (name='Speaker').")

# LEDs
leds = []
for name in ["ChestBoard/Led", "RFoot/Led", "LFoot/Led",
             "Face/Led/Right", "Face/Led/Left",
             "Ears/Led/Right", "Ears/Led/Left"]:
    leds.append(robot.getDevice(name))


# ---------------------------------------------------------------------------
#  Helper functions
# ---------------------------------------------------------------------------

def direct_move(motor, position):
    """HIGH velocity — sharp, decisive (male-analytical style)."""
    motor.setVelocity(DIRECT_SPEED)
    motor.setPosition(position)


def set_hand(phalanx_list, angle):
    for motor in phalanx_list:
        if motor:
            motor.setPosition(angle)


def set_neutral_pose():
    """Arms at sides, attentive — authoritative resting posture."""
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
#  Male-Analytical style:
#    - Crisp, angular movements (DIRECT_SPEED = 2.0 rad/s).
#    - Counting / enumerating gestures, deliberate pointing.
#    - Closed hands (fists) for emphasis; minimal idle motion.
# ---------------------------------------------------------------------------

triggered = set()

def run_gestures(t):

    # ---- SESSION INTRO: small authoritative nod ----
    if t >= T_SESSION and "session" not in triggered:
        triggered.add("session")
        set_neutral_pose()
        direct_move(HeadPitch, 0.15)

    # ---- DEVICE (define personification): right hand rises, palm flat ----
    if t >= T_DEVICE and "device" not in triggered:
        triggered.add("device")
        direct_move(HeadPitch, 0.0)
        direct_move(RShoulderPitch, 0.7)
        direct_move(RShoulderRoll, -0.2)
        direct_move(RElbowRoll, 0.3)
        set_hand(rphalanx, 0.5)        # flat hand – presenting a term

    # ---- ATTRIBUTE: left hand rises to "count off" the definition ----
    if t >= T_ATTRIBUTE and "attribute" not in triggered:
        triggered.add("attribute")
        direct_move(LShoulderPitch, 0.8)
        direct_move(LShoulderRoll, 0.2)
        direct_move(LElbowRoll, -0.3)
        set_hand(lphalanx, 0.5)

    # ---- WRITER: both arms retract, right points forward ----
    if t >= T_WRITER and "writer" not in triggered:
        triggered.add("writer")
        direct_move(LShoulderPitch, 1.4)
        direct_move(LElbowRoll, -0.5)
        set_hand(lphalanx, 0.0)
        direct_move(RShoulderPitch, 0.5)
        direct_move(RElbowYaw, 1.0)
        direct_move(RElbowRoll, 0.1)
        set_hand(rphalanx, 0.6)        # pointing

    # ---- IMPACT: firm right-arm chop downward (emphasis) ----
    if t >= T_IMPACT and "impact" not in triggered:
        triggered.add("impact")
        direct_move(RShoulderPitch, 0.9)
        direct_move(RElbowRoll, 0.5)
        set_hand(rphalanx, 0.0)        # fist – deliberate

    # ---- EXAMPLE: return to neutral, then present ----
    if t >= T_EXAMPLE and "example" not in triggered:
        triggered.add("example")
        set_neutral_pose()

    if t >= T_EXAMPLE + 1.0 and "example_present" not in triggered:
        triggered.add("example_present")
        direct_move(RShoulderPitch, 0.6)
        direct_move(RShoulderRoll, -0.3)
        direct_move(RElbowRoll, 0.2)
        set_hand(rphalanx, 0.5)

    # ---- WIND HOWLED: left arm sweeps across (evoking the wind) ----
    if t >= T_WIND and "wind" not in triggered:
        triggered.add("wind")
        direct_move(LShoulderPitch, 0.5)
        direct_move(LShoulderRoll, 0.4)
        direct_move(LElbowYaw, -0.8)
        direct_move(LElbowRoll, -0.2)
        set_hand(lphalanx, 0.7)
        direct_move(HeadYaw, -0.1)     # glance toward "the wind"

    # ---- TECHNICALLY: head returns centre, analytical finger-raise ----
    if t >= T_TECHNICALLY and "technically" not in triggered:
        triggered.add("technically")
        direct_move(HeadYaw, 0.0)
        direct_move(LShoulderPitch, 1.4)
        direct_move(LElbowRoll, -0.5)
        set_hand(lphalanx, 0.0)
        direct_move(RShoulderPitch, 0.4)
        direct_move(RShoulderRoll, -0.15)
        direct_move(RElbowRoll, 0.05)
        set_hand(rphalanx, 0.7)        # index-finger raise

    # ---- APPLYING: right arm extends outward ----
    if t >= T_APPLYING and "applying" not in triggered:
        triggered.add("applying")
        direct_move(RShoulderPitch, 0.6)
        direct_move(RShoulderRoll, -0.35)
        direct_move(RElbowYaw, 1.2)
        direct_move(RElbowRoll, 0.15)

    # ---- CALCULATED CHOICE: both arms chop together (precision) ----
    if t >= T_CALCULATED and "calculated" not in triggered:
        triggered.add("calculated")
        direct_move(RShoulderPitch, 0.9)
        direct_move(RElbowRoll, 0.4)
        direct_move(LShoulderPitch, 0.9)
        direct_move(LElbowRoll, -0.4)
        set_hand(rphalanx, 0.0)
        set_hand(lphalanx, 0.0)

    # ---- IDENTIFY: point at audience ----
    if t >= T_IDENTIFY and "identify" not in triggered:
        triggered.add("identify")
        set_neutral_pose()
        direct_move(RShoulderPitch, 0.5)
        direct_move(RElbowRoll, 0.1)
        set_hand(rphalanx, 0.6)

    # ---- EXAMINE: return neutral, concluding nod ----
    if t >= T_EXAMINE and "examine" not in triggered:
        triggered.add("examine")
        set_neutral_pose()

    if t >= T_EXAMINE + 1.0 and "examine_nod" not in triggered:
        triggered.add("examine_nod")
        direct_move(HeadPitch, 0.15)

    # ---- END: hold neutral ----
    if t >= T_END and "end" not in triggered:
        triggered.add("end")
        set_neutral_pose()


# ---------------------------------------------------------------------------
#  Main loop
# ---------------------------------------------------------------------------

set_neutral_pose()
for _ in range(20):
    robot.step(timestep)

for i in range(5):
    leds[i].set(0x0033cc)

if speaker:
    Speaker.playSound(speaker, speaker, AUDIO_FILE, VOLUME, 1.0, 0.0, False)
else:
    print("WARNING: Skipping audio — no Speaker device. Gestures will still run.")

elapsed = 0.0
while robot.step(timestep) != -1:
    elapsed += timestep / 1000.0
    run_gestures(elapsed)
    if elapsed >= T_END + 3.0:
        break

set_neutral_pose()
for _ in range(40):
    robot.step(timestep)