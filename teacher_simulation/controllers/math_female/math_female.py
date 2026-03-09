"""
ECE 787 - Gender Bias in Robotic Educators
Controller: Female Math (Communal/Supportive Style)
Subject: Mathematics - The Pythagorean Theorem
Gesture Style: Smooth/B-Spline-like transitions, fluid open gestures

This controller plays the female-voice math lesson audio and
performs synchronized gestures using LOW motor velocities to
create smooth, flowing, communal teaching persona movements.
"""

from controller import Robot, Speaker

# ---------------------------------------------------------------------------
#  Configuration
# ---------------------------------------------------------------------------

AUDIO_FILE = "../../audio/math_female.mp3"
VOLUME     = 5.0

# Motor speed profiles — female style uses LOW velocity for smooth, fluid moves
SMOOTH_SPEED = 0.8   # rad/s – gentle, flowing motion
MEDIUM_SPEED = 1.2   # rad/s – slightly quicker for transitions
PHALANX_MAX  = 8

# ---------------------------------------------------------------------------
#  Gesture timing (seconds from start of audio)
#  TODO: Fine-tune after reviewing your final MP3 recording.
# ---------------------------------------------------------------------------
T_GREETING    =  0.0   # "Hello everyone!"
T_HAPPY       =  2.0   # "I'm so happy to help you..."
T_EXPLORE     =  6.0   # "explore a really helpful math..."
T_WONDERFUL   = 12.0   # "It's a wonderful way for us..."
T_PATTERN     = 18.0   # "we can see a special pattern..."
T_TOGETHER    = 24.0   # "We can write this together..."
T_HYPOTENUSE  = 30.0   # "'c' is the hypotenuse..."
T_SHORTER     = 36.0   # "'a' and 'b' are the two shorter..."
T_MISSING     = 42.0   # "find a missing side..."
T_RELIABLE    = 48.0   # "a very reliable method..."
T_COMFORTABLE = 54.0   # "I hope you feel comfortable..."
T_NEXT_STEP   = 60.0   # "Let's take a look... together."
T_END         = 68.0   # End of lesson / cooldown


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

def smooth_move(motor, position):
    """Set motor to target with LOW velocity — gentle, flowing (female style)."""
    motor.setVelocity(SMOOTH_SPEED)
    motor.setPosition(position)


def medium_move(motor, position):
    """Set motor with MEDIUM velocity for slightly quicker transitions."""
    motor.setVelocity(MEDIUM_SPEED)
    motor.setPosition(position)


def set_hand(phalanx_list, angle):
    """Open / close a hand with smooth motion."""
    for motor in phalanx_list:
        if motor:
            motor.setVelocity(SMOOTH_SPEED)
            motor.setPosition(angle)


def set_neutral_pose():
    """Arms relaxed, slightly open — approachable resting posture."""
    smooth_move(RShoulderPitch,  1.3)
    smooth_move(RShoulderRoll,  -0.25)
    smooth_move(RElbowYaw,       1.2)
    smooth_move(RElbowRoll,      0.4)
    smooth_move(LShoulderPitch,  1.3)
    smooth_move(LShoulderRoll,   0.25)
    smooth_move(LElbowYaw,      -1.2)
    smooth_move(LElbowRoll,     -0.4)
    smooth_move(HeadYaw,         0.0)
    smooth_move(HeadPitch,      -0.05)   # slightly up – engaged
    set_hand(rphalanx, 0.3)             # loosely open – relaxed
    set_hand(lphalanx, 0.3)


# ---------------------------------------------------------------------------
#  Gesture choreography
#
#  Female-Communal style:
#    - All movements use SMOOTH_SPEED (0.8 rad/s) for flowing motion.
#    - Gestures are open and inclusive: palms out, welcoming sweeps,
#      gentle head tilts, both arms used symmetrically.
#    - Hands stay open / relaxed throughout.
# ---------------------------------------------------------------------------

triggered = set()

def run_gestures(t):

    # ---- GREETING: gentle head tilt + small wave ----
    if t >= T_GREETING and "greeting" not in triggered:
        triggered.add("greeting")
        set_neutral_pose()
        smooth_move(HeadYaw, 0.1)           # slight tilt right
        smooth_move(HeadPitch, -0.1)        # chin slightly up
        smooth_move(RShoulderPitch, 0.6)    # welcoming wave
        smooth_move(RShoulderRoll, -0.2)
        smooth_move(RElbowRoll, 0.3)
        set_hand(rphalanx, 0.8)             # open hand

    # ---- HAPPY: both arms open outward (welcoming) ----
    if t >= T_HAPPY and "happy" not in triggered:
        triggered.add("happy")
        smooth_move(HeadYaw, -0.05)
        smooth_move(RShoulderPitch, 0.9)
        smooth_move(RShoulderRoll, -0.4)
        smooth_move(RElbowRoll, 0.2)
        smooth_move(LShoulderPitch, 0.9)
        smooth_move(LShoulderRoll, 0.4)
        smooth_move(LElbowRoll, -0.2)
        set_hand(rphalanx, 0.8)
        set_hand(lphalanx, 0.8)

    # ---- EXPLORE: gentle sweep, head tilts to other side ----
    if t >= T_EXPLORE and "explore" not in triggered:
        triggered.add("explore")
        smooth_move(HeadYaw, -0.1)
        smooth_move(RShoulderPitch, 1.0)
        smooth_move(RElbowRoll, 0.4)
        smooth_move(LShoulderPitch, 0.7)
        smooth_move(LShoulderRoll, 0.3)
        smooth_move(LElbowRoll, -0.3)
        set_hand(lphalanx, 0.9)            # open, presenting

    # ---- WONDERFUL: both arms rise gently, palms out ----
    if t >= T_WONDERFUL and "wonderful" not in triggered:
        triggered.add("wonderful")
        smooth_move(HeadYaw, 0.0)
        smooth_move(HeadPitch, -0.1)
        smooth_move(RShoulderPitch, 0.7)
        smooth_move(RShoulderRoll, -0.35)
        smooth_move(RElbowRoll, 0.15)
        smooth_move(LShoulderPitch, 0.7)
        smooth_move(LShoulderRoll, 0.35)
        smooth_move(LElbowRoll, -0.15)
        set_hand(rphalanx, 0.9)
        set_hand(lphalanx, 0.9)

    # ---- PATTERN: right hand gestures toward "board" ----
    if t >= T_PATTERN and "pattern" not in triggered:
        triggered.add("pattern")
        smooth_move(RShoulderPitch, 0.5)
        smooth_move(RShoulderRoll, -0.2)
        smooth_move(RElbowYaw, 0.9)
        smooth_move(RElbowRoll, 0.1)
        smooth_move(LShoulderPitch, 1.2)
        smooth_move(LElbowRoll, -0.4)
        smooth_move(HeadYaw, 0.05)

    # ---- TOGETHER (write formula): both arms forward, collaborative ----
    if t >= T_TOGETHER and "together" not in triggered:
        triggered.add("together")
        smooth_move(RShoulderPitch, 0.6)
        smooth_move(RShoulderRoll, -0.15)
        smooth_move(LShoulderPitch, 0.6)
        smooth_move(LShoulderRoll, 0.15)
        smooth_move(RElbowRoll, 0.3)
        smooth_move(LElbowRoll, -0.3)
        smooth_move(HeadYaw, 0.0)

    # ---- HYPOTENUSE: right arm traces upward arc ----
    if t >= T_HYPOTENUSE and "hypotenuse" not in triggered:
        triggered.add("hypotenuse")
        smooth_move(RShoulderPitch, 0.3)
        smooth_move(RElbowYaw, 1.0)
        smooth_move(RElbowRoll, 0.05)
        smooth_move(LShoulderPitch, 1.1)
        smooth_move(HeadPitch, -0.05)
        smooth_move(HeadYaw, 0.08)

    # ---- SHORTER SIDES: left arm joins ----
    if t >= T_SHORTER and "shorter" not in triggered:
        triggered.add("shorter")
        smooth_move(LShoulderPitch, 0.7)
        smooth_move(LShoulderRoll, 0.25)
        smooth_move(LElbowRoll, -0.2)
        smooth_move(RShoulderPitch, 0.7)
        smooth_move(RElbowRoll, 0.3)
        smooth_move(HeadYaw, -0.08)

    # ---- MISSING SIDE: gentle encouraging nod ----
    if t >= T_MISSING and "missing" not in triggered:
        triggered.add("missing")
        set_neutral_pose()
        smooth_move(HeadPitch, 0.1)        # nod down

    if t >= T_MISSING + 1.5 and "missing_up" not in triggered:
        triggered.add("missing_up")
        smooth_move(HeadPitch, -0.05)       # nod back up

    # ---- RELIABLE: hands together, then open (togetherness) ----
    if t >= T_RELIABLE and "reliable" not in triggered:
        triggered.add("reliable")
        smooth_move(RShoulderPitch, 0.9)
        smooth_move(RShoulderRoll, -0.05)
        smooth_move(LShoulderPitch, 0.9)
        smooth_move(LShoulderRoll, 0.05)
        smooth_move(RElbowRoll, 0.1)
        smooth_move(LElbowRoll, -0.1)

    if t >= T_RELIABLE + 2.0 and "reliable_open" not in triggered:
        triggered.add("reliable_open")
        smooth_move(RShoulderRoll, -0.35)
        smooth_move(LShoulderRoll, 0.35)
        smooth_move(RElbowRoll, 0.2)
        smooth_move(LElbowRoll, -0.2)

    # ---- COMFORTABLE: head tilts warmly, palms toward audience ----
    if t >= T_COMFORTABLE and "comfortable" not in triggered:
        triggered.add("comfortable")
        smooth_move(HeadYaw, 0.1)
        smooth_move(HeadPitch, -0.08)
        smooth_move(RShoulderPitch, 0.8)
        smooth_move(RShoulderRoll, -0.3)
        smooth_move(LShoulderPitch, 0.8)
        smooth_move(LShoulderRoll, 0.3)
        set_hand(rphalanx, 0.9)
        set_hand(lphalanx, 0.9)

    # ---- NEXT STEP TOGETHER: gentle sweep back to centre ----
    if t >= T_NEXT_STEP and "next_step" not in triggered:
        triggered.add("next_step")
        smooth_move(HeadYaw, 0.0)
        smooth_move(HeadPitch, -0.05)
        set_neutral_pose()

    # ---- END: hold relaxed neutral ----
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

# Neutral blue LEDs (consistent across all conditions)
for i in range(5):
    leds[i].set(0x0033cc)

# Start audio playback
if speaker:
    Speaker.playSound(speaker, speaker, AUDIO_FILE, VOLUME, 1.0, 0.0, False)
else:
    print("WARNING: Skipping audio — no Speaker device. Gestures will still run.")

# Run the lesson
elapsed = 0.0
while robot.step(timestep) != -1:
    elapsed += timestep / 1000.0
    run_gestures(elapsed)
    if elapsed >= T_END + 3.0:
        break

# Final neutral hold
set_neutral_pose()
for _ in range(40):
    robot.step(timestep)