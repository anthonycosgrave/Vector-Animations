import anki_vector
from anki_vector.util import degrees
from anki_vector.behavior import MIN_HEAD_ANGLE

import time
import sys

try:
    from PIL import Image, ImageDraw, ImageFont  # imported by me
except ImportError:
    sys.exit("Cannot import from PIL: Do `pip3 install --user Pillow` to install")


def make_text_image(text_to_draw, x, y, font=None):

    # make a blank image for the text, initialized to opaque black
    text_image = Image.new('RGBA', (184, 96), (0, 0, 0, 255))

    dc = ImageDraw.Draw(text_image)

    font = ImageFont.truetype(
        "arial.ttf", 85, encoding="unic")  # 46 is not enough

    dc.text((x, y), text_to_draw, fill=(34, 177, 76, 255), font=font)

    return text_image

def convert_image_for_screen(path_to_image):
	the_image = Image.open(path_to_image)
	return anki_vector.screen.convert_image_to_screen_data(the_image)

def walk_screen_animation_and_speech_async_steps_or_distance():
    with anki_vector.AsyncRobot() as robot:
        left_foot_image = Image.open('footsteps-green-left.png')
        right_foot_image = Image.open('footsteps-green-right.png')
        left_foot_screen_data = anki_vector.screen.convert_image_to_screen_data(
            left_foot_image)
        right_foot_screen_data = anki_vector.screen.convert_image_to_screen_data(
            right_foot_image)

        eyes = robot.anim.play_animation('anim_eyepose_awe')
        h1 = robot.behavior.set_head_angle(degrees(25), duration=0.20)
        h1.result()
        eyes.result()

        t1 = robot.behavior.say_text(
            # phonetically spelled Irish to get it to sound right
            "Mo carra, Wow! Your boots were definitely made for walking, 8500 steps a day so far! Keep that up!")
        time.sleep(0.5)
        for i in range(0, 5): # higher max value for longer speech
            # (image_data, duration_sec, interrupt_running)
            l = robot.screen.set_screen_with_image_data(
                left_foot_screen_data, 1.0, True)
            time.sleep(1.0)
            r = robot.screen.set_screen_with_image_data(
                right_foot_screen_data, 1.0, True)
            time.sleep(1.0)
            l.result()
            r.result()
        t1.result()

        # to reset the display
        h = robot.anim.play_animation("anim_eyepose_happy")
        h.result()
        time.sleep(0.5)
    return False

def walk_forwards_with_screen_animation_and_speech_async_not_very_active():
    with anki_vector.AsyncRobot() as robot:

        if robot.status.is_on_charger:
            d = robot.behavior.drive_off_charger()
            d.result()

        left_foot_image = Image.open('footsteps-green-left.png')
        right_foot_image = Image.open('footsteps-green-right.png')
        left_foot_screen_data = anki_vector.screen.convert_image_to_screen_data(
            left_foot_image)
        right_foot_screen_data = anki_vector.screen.convert_image_to_screen_data(
            right_foot_image)

        eyes = robot.anim.play_animation('anim_eyepose_concerned')
        t1 = robot.behavior.say_text(
            "Hey chief, you've haven't been very active lately")
        h1 = robot.behavior.set_head_angle(degrees(25), duration=0.20)
        h1.result()
        eyes.result()
        time.sleep(0.5)
        t1.result()
        t2 = robot.behavior.say_text(" it's really important to get some daily exercise.")
        t2.result()
        t3 = robot.behavior.say_text(" What about putting on a podcast and going for a wander?")
        time.sleep(0.33)
        # don't result this or it will block the execution of the for loop!
        for i in range(0, 4):
            left_img = robot.screen.set_screen_with_image_data(
                left_foot_screen_data, 2.0, True)
            left_img.result()
            l = robot.motors.set_wheel_motors(50, -8)
            l.result()
            # the longer these are the longer walking continues
            # after text has finished
            time.sleep(0.5)

            right_img = robot.screen.set_screen_with_image_data(
                right_foot_screen_data, 2.0, True)
            right_img.result()
            r = robot.motors.set_wheel_motors(-8, 50)
            r.result()
            time.sleep(0.5)

        # without this Vector will keep going until another motor command has been issued
        stop = robot.motors.stop_all_motors()
        stop.result()
        t3.result()
        h = robot.anim.play_animation("anim_eyepose_happy")
        h.result()

    return False

def weight_lifting_screen_animation_with_speech_async():
	
	image_1 = convert_image_for_screen('1.png')
	image_2 = convert_image_for_screen('2.png')
	image_3 = convert_image_for_screen('3.png')
	image_question_mark = convert_image_for_screen('question.png')
	image_99 = convert_image_for_screen('99.png')
	image_100 = convert_image_for_screen('100.png')
	images = [image_1, image_2, image_3, image_question_mark, image_100]

	args = anki_vector.util.parse_command_args()

	with anki_vector.AsyncRobot(args.serial) as robot:

		f = robot.anim.play_animation('anim_eyepose_bothered') # Now I need a quick workout to keep up with you
		g = robot.behavior.say_text("Yo, did you die or something? You've barely moved recently! Follow along with me")
		
		g.result()
		f.result()
		time.sleep(0.2)
		d = robot.anim.play_animation('anim_eyepose_determined')
		time.sleep(0.1)
		d.result()
		# do_this = robot.behavior.say_text("LET'S DO THIS!")
		do_this = robot.behavior.say_text("LET'S GO!!!")
		lookup = robot.behavior.set_head_angle(degrees(25), duration=0.20)
		lookup.result()

		do_this.result()
		h1 = robot.behavior.set_head_angle(MIN_HEAD_ANGLE, duration=0.25)
		h1.result()
		rep_text = ["One!", "Two!", "Three!", "Eh...", "One Hundred!"]
		for i in range(len(rep_text)):
			if i == 3:
				partial_curl_up = robot.behavior.set_lift_height(
					0.2, max_speed=5.0, duration=0.33)
				partial_curl_up.result()
				img = robot.screen.set_screen_with_image_data(images[i], 1.0, True)
				img.result()
				rep = robot.behavior.say_text(rep_text[i])
				lookup = robot.behavior.set_head_angle(
					degrees(15), duration=0.20)
				lookup.result()
				rep.result()
				time.sleep(0.33)

				# 99 image
				img = robot.screen.set_screen_with_image_data(image_99, 1.0, True)
				rep = robot.behavior.say_text("99")
				img.result()
				h1 = robot.behavior.set_head_angle(
					MIN_HEAD_ANGLE, duration=0.25)
				h1.result()
				curl_up = robot.behavior.set_lift_height(
					0.5, max_speed=5.0, duration=0.33)
				curl_up.result()
				rep.result()
				curl_down = robot.behavior.set_lift_height(0.0)
				curl_down.result()
			else:
				img = robot.screen.set_screen_with_image_data(images[i], 1.0, True)
				rep = robot.behavior.say_text(rep_text[i])
				img.result()
				curl_up = robot.behavior.set_lift_height(
					0.5, max_speed=5.0, duration=0.33)
				curl_up.result()
				rep.result()
				curl_down = robot.behavior.set_lift_height(0.0)
				curl_down.result()

		happy = robot.anim.play_animation("anim_eyepose_happy")
		happy.result()
		lookup = robot.behavior.set_head_angle(degrees(25), duration=0.1)
		lookup.result()

		happy = robot.anim.play_animation("anim_eyepose_happy")
		
		swole = robot.behavior.say_text(
			"What are you laughing at, it's more than you've done... Welcome to the gun show baby!")
		swole.result()
		happy.result()

		# default max_speed = 10.0, duration = 0.5
		lift_up = robot.behavior.set_lift_height(
			0.9, max_speed=15.0, duration=0.20)
		lift_up.result()
		time.sleep(0.5)
		lift_reset = robot.behavior.set_lift_height(0.0)
		lift_reset.result() 

def main():
    try:

        # walk_screen_animation_and_speech_async_steps_or_distance()
        #walk_forwards_with_screen_animation_and_speech_async_not_very_active()
        weight_lifting_screen_animation_with_speech_async()

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
