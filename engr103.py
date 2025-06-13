###########################################################
#Program Filename:Track Workout Generator
#Author: Kaylee Ho
#Date: 5/29/2025
#Description: Getting User Input and Validating Event
#Parameters: List of strings representing valid track events
#Return Values: String containing valid event entered
#Pre-Conditions:Must be 400m, 800m, 1500m, or 5k
#Post-Conditions: User is continuously prompted until valid event is entered.
#############################################################
print("Welcome to the Track Workout Generator!")
valid_events=["400m","800m","1500m","5k"]
valid_goals=["speed","endurance"]
while True:
    event = input("Enter your event (400m, 800m, 1500m, 5k):").strip().lower()
    if event in valid_events:
        break
    print("Invalid event. Please try again.")
###########################################################
#Description: Validating Goal Given User Input
#Parameters:List of strings representing valid goal of endurance or speed
#Return Values: A string containing valid goal entered
#Pre-Conditions: Must be endurance or speed
#Post-Conditions: User is continuously prompted until valid event is entered
#############################################################
while True:
    goal= input("Enter your training goal (speed or endurance):").strip().lower()
    if goal in valid_goals:
        break
    print ("Invalid goal. Please enter 'speed or 'endurance.")
###########################################################
#Description: Generates a track workout given input
#Parameters: Track event and training goal
#Return Values: A workout given selected event and goal
#Pre-Conditions: Event and goal should be strings and valid values
#Post-Conditions: Returns a list of a string describing a workout. If input is
#invalid, user is prompted again.
#############################################################
def gen_workout(event,goal):
    event=event.lower()
    goal=goal.lower()
    if event == "400m":
        if goal=="speed":
            return["6x100m sprints","Full recovery between reps"]
        elif goal=="endurance":
            return["4x300m at race pace", "60 seconds rest"]
    elif event == "800m":
        if goal == "speed":
            return["5x200m fast", "90 sec rest"]
        elif goal == "endurance":
            return ["4x600m at race pace", "2 minutes rest"]
elif event == "1500m":
if goal== "speed":
return ["5x400m fast", "90 seconds rest"]
elif goal=="endurance":
return ["3x800m tempo", "2 minute rest"]
elif event == "5k":
if goal=="speed":
return ["4x1km at race pace", "2-3 minute rest"]
elif goal == "endurance":
return ["3x1600m tempo", "3 minute rest"]
return ["No workout found."]
###########################################################
#Description: Prints Workout
#Parameters: Selected event and goal already validated
#Return Values: None
#Pre-Conditions: gen_workout must be defined and event and goal must be valid
#Post-Conditions: Personalized workout is displayed
#############################################################
workout= gen_workout(event,goal)
print("\n Your personalized workout:")
for w in workout:
print("-"+w)