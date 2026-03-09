"""
ECE 787 - Gender Bias in Robotic Educators
Controller: Female English (Expressive/Relational Style)
Subject: English - Literary Device: Personification
Gesture Style: Smooth/B-Spline-like transitions, fluid open gestures

This controller plays the female-voice English lesson audio and
performs synchronized gestures using LOW motor velocities to
create expressive, relational, flowing movements.
"""

from controller import Robot, Speaker

# ---------------------------------------------------------------------------
#  Configuration
# ---------------------------------------------------------------------------

AUDIO_FILE   = "../../audio/english_female.mp3"
VOLUME       = 5.0
SMOOTH_SPEED = 0.8   # rad/s – gentle, flowing motion
MEDIUM_SPEED = 1.2   # rad/s – slightly quicker for emphasis
PHALANX_MAX  = 8

# ---------------------------------------------------------------------------
#  Gesture timing (seconds from start of audio)
#  TODO: Fine-tune after reviewing your final MP3 recording.
# ---------------------------------------------------------------------------
T_TODAY     =  0.0   # "Today, we're going to look at..."
T_BEAUTIFUL =  3.0   # "a beautiful way that writers..."
T_LOVELY    =  8.0   # "This is a lovely literary device..."
T_FEELINGS  = 13.0   # "give human feelings or traits..."
T_CONNECTED = 18.0   # "help us feel more connected..."
T_INSTANCE  = 24.0   # "For instance, think about..."
T_WIND      = 28.0   # "'The wind howled in the night.'"
T_KNOW      = 33.0   # "We know that the wind doesn't..."
T_IMAGINE   = 38.0   # "helps us imagine how lonely..."
T_CREATIVE  = 43.0   # "It's a creative way to bring..."
T_LOVE      = 49.0   # "I'd love for you to think..."
T_SHARE     = 55.0   # "Let's share a few more..."
T_END       = 64.0   # End of lesson / cooldown


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
    """LOW velocity — gentle, flowing (female-expressive style)."""
    motor.setVelocity(SMOOTH_SPEED)
    motor.setPosition(position)


def medium_move(motor, position):
    """MEDIUM velocity for slightly quicker transitions."""
    motor.setVelocity(MEDIUM_SPEED)
    motor.setPosition(position)


def set_hand(phalanx_list, angle):
    for motor in phalanx_list:
        if motor:
            motor.setVelocity(SMOOTH_SPEED)
            motor.setPosition(angle)


def set_neutral_pose():
    """Arms relaxed, slightly open — warm, approachable posture."""
    smooth_move(RShoulderPitch,  1.3)
    smooth_move(RShoulderRoll,  -0.25)
    smooth_move(RElbowYaw,       1.2)
    smooth_move(RElbowRoll,      0.4)
    smooth_move(LShoulderPitch,  1.3)
    smooth_move(LShoulderRoll,   0.25)
    smooth_move(LElbowYaw,      -1.2)
    smooth_move(LElbowRoll,     -0.4)
    smooth_move(HeadYaw,         0.0)
    smooth_move(HeadPitch,      -0.05)
    set_hand(rphalanx, 0.3)
    set_hand(lphalanx, 0.3)


# ---------------------------------------------------------------------------
#  Gesture choreography
#
#  Female-Expressive style:
#    - Slow, flowing movements (SMOOTH_SPEED = 0.8 rad/s).
#    - Open, inclusive gestures; soft head tilts conveying warmth.
#    - Hands stay relaxed and open throughout.
#    - Evocative gestures for the wind / emotion beats.
# ---------------------------------------------------------------------------

triggered = set()

def run_gestures(t):

    # ---- TODAY: warm head tilt + slight wave ----
    if t >= T_TODAY and "today" not in triggered:
        triggered.add("today")
        set_neutral_pose()
        smooth_move(HeadYaw, 0.1)
        smooth_move(HeadPitch, -0.1)
        smooth_move(RShoulderPitch, 0.8)
        smooth_move(RElbowRoll, 0.2)
        set_hand(rphalanx, 0.8)

    # ---- BEAUTIFUL: both arms open outward (expressive wonder) ----
    if t >= T_BEAUTIFUL and "beautiful" not in triggered:
        triggered.add("beautiful")
        smooth_move(HeadYaw, -0.05)
        smooth_move(RShoulderPitch, 0.7)
        smooth_move(RShoulderRoll, -0.4)
        smooth_move(RElbowRoll, 0.15)
        smooth_move(LShoulderPitch, 0.7)
        smooth_move(LShoulderRoll, 0.4)
        smooth_move(LElbowRoll, -0.15)
        set_hand(rphalanx, 0.9)
        set_hand(lphalanx, 0.9)

    # ---- LOVELY: head tilts other way, left hand gestures ----
    if t >= T_LOVELY and "lovely" not in triggered:
        triggered.add("lovely")
        smooth_move(HeadYaw, -0.1)
        smooth_move(RShoulderPitch, 1.1)
        smooth_move(RElbowRoll, 0.4)
        smooth_move(LShoulderPitch, 0.6)
        smooth_move(LShoulderRoll, 0.3)
        smooth_move(LElbowRoll, -0.2)
        set_hand(lphalanx, 0.9)

    # ---- FEELINGS: hands to heart / chest area (emotional) ----
    if t >= T_FEELINGS and "feelings" not in triggered:
        triggered.add("feelings")
        smooth_move(HeadYaw, 0.0)
        smooth_move(HeadPitch, -0.08)
        smooth_move(RShoulderPitch, 1.0)
        smooth_move(RShoulderRoll, -0.05)
        smooth_move(RElbowRoll, 0.8)
        smooth_move(LShoulderPitch, 1.0)
        smooth_move(LShoulderRoll, 0.05)
        smooth_move(LElbowRoll, -0.8)
        set_hand(rphalanx, 0.5)
        set_hand(lphalanx, 0.5)

    # ---- CONNECTED: arms open outward from chest (reaching out) ----
    if t >= T_CONNECTED and "connected" not in triggered:
        triggered.add("connected")
        smooth_move(RShoulderPitch, 0.8)
        smooth_move(RShoulderRoll, -0.35)
        smooth_move(RElbowRoll, 0.2)
        smooth_move(LShoulderPitch, 0.8)
        smooth_move(LShoulderRoll, 0.35)
        smooth_move(LElbowRoll, -0.2)
        set_hand(rphalanx, 0.9)
        set_hand(lphalanx, 0.9)
        smooth_move(HeadYaw, 0.08)

    # ---- INSTANCE: settle, right hand presents ----
    if t >= T_INSTANCE and "instance" not in triggered:
        triggered.add("instance")
        smooth_move(LShoulderPitch, 1.2)
        smooth_move(LElbowRoll, -0.4)
        smooth_move(RShoulderPitch, 0.6)
        smooth_move(RShoulderRoll, -0.25)
        smooth_move(RElbowRoll, 0.2)
        smooth_move(HeadYaw, 0.0)
        smooth_move(HeadPitch, -0.05)

    # ---- WIND HOWLED: evocative — both arms sweep like wind ----
    if t >= T_WIND and "wind" not in triggered:
        triggered.add("wind")
        smooth_move(LShoulderPitch, 0.5)
        smooth_move(LShoulderRoll, 0.4)
        smooth_move(LElbowYaw, -0.7)
        smooth_move(LElbowRoll, -0.15)
        set_hand(lphalanx, 0.9)
        smooth_move(RShoulderPitch, 0.5)
        smooth_move(RShoulderRoll, -0.4)
        smooth_move(RElbowYaw, 0.7)
        smooth_move(RElbowRoll, 0.15)
        set_hand(rphalanx, 0.9)
        smooth_move(HeadYaw, -0.15)    # look aside – dramatic

    # Slow sweep continuation
    if t >= T_WIND + 2.0 and "wind_cont" not in triggered:
        triggered.add("wind_cont")
        smooth_move(LShoulderRoll, 0.2)
        smooth_move(RShoulderRoll, -0.2)
        smooth_move(HeadYaw, 0.15)     # head follows the "wind"

    # ---- KNOW: settle back, gentle nod ----
    if t >= T_KNOW and "know" not in triggered:
        triggered.add("know")
        set_neutral_pose()
        smooth_move(HeadPitch, 0.08)
        smooth_move(HeadYaw, 0.05)

    # ---- IMAGINE: arms rise softly (painting a picture) ----
    if t >= T_IMAGINE and "imagine" not in triggered:
        triggered.add("imagine")
        smooth_move(HeadPitch, -0.08)
        smooth_move(HeadYaw, -0.05)
        smooth_move(RShoulderPitch, 0.7)
        smooth_move(RShoulderRoll, -0.3)
        smooth_move(RElbowRoll, 0.15)
        smooth_move(LShoulderPitch, 0.7)
        smooth_move(LShoulderRoll, 0.3)
        smooth_move(LElbowRoll, -0.15)
        set_hand(rphalanx, 0.9)
        set_hand(lphalanx, 0.9)

    # ---- CREATIVE: hands together then bloom outward ----
    if t >= T_CREATIVE and "creative" not in triggered:
        triggered.add("creative")
        smooth_move(RShoulderRoll, -0.05)
        smooth_move(LShoulderRoll, 0.05)
        smooth_move(RElbowRoll, 0.6)
        smooth_move(LElbowRoll, -0.6)
        smooth_move(HeadYaw, 0.0)

    if t >= T_CREATIVE + 2.0 and "creative_bloom" not in triggered:
        triggered.add("creative_bloom")
        smooth_move(RShoulderRoll, -0.4)
        smooth_move(LShoulderRoll, 0.4)
        smooth_move(RElbowRoll, 0.15)
        smooth_move(LElbowRoll, -0.15)

    # ---- LOVE: warm head tilt, open posture toward audience ----
    if t >= T_LOVE and "love" not in triggered:
        triggered.add("love")
        smooth_move(HeadYaw, 0.12)
        smooth_move(HeadPitch, -0.1)
        smooth_move(RShoulderPitch, 0.9)
        smooth_move(RShoulderRoll, -0.3)
        smooth_move(LShoulderPitch, 0.9)
        smooth_move(LShoulderRoll, 0.3)
        set_hand(rphalanx, 0.8)
        set_hand(lphalanx, 0.8)

    # ---- SHARE: return to warm neutral ----
    if t >= T_SHARE and "share" not in triggered:
        triggered.add("share")
        smooth_move(HeadYaw, 0.0)
        set_neutral_pose()

    # ---- END: hold relaxed neutral ----
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