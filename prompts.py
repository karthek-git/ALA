instr_prompt = '''This is the current screenshot. Please give me the response as requested below.

First, you need to generate the Observation and Thought.
Observation: You need to briefly describe the current screenshot. If there are previous operations, you need to briefly describe the previous operations and the screenshot changes.
Thought: Based on Observation, You need to think about what you need to do next in order to complete the instruction.

Then, you need to generate the action based on the Thought. You can perform the following 7 actions:
1. open App Drawer. Open App drawer showing all the installed apps. You can use this to choose the best possible app to perform the given instruction.
2. click (parameter1, parameter2). The parameter1 is the x coordinate of the position you want to click and the parameter2 is the y coordinate of the position you want to click.
3. swipe down, swipe up, swipe right, swipe left. These two commands don't need parameter, used for page turning.
4. type (parameter). The parameter is what you want to type. Make sure you have clicked on the input box before typing.
5. wait (parameter). Wait for a certain duration on the present screen before proceeding. The parameter is the duration in seconds.
6. back. Back to the previous page.
7. exit. Exit the app and go back to the desktop.
8. stop. If you think you have completed the instruction, then you can stop the whole process.
Note: If you try an action several times and the screen does not change, try using another action.

Finally, your output must follow the following format:
Observation: Generate as required by Observation
Thought: Generate as required by Thought
Action: If the action requires parameters, use (parameter).

'''

# This is the prompt used for dataset generation to overcome grounding issue with LLMs
instr_ds_prompt='''This is the current screenshot. Please give me the response as requested below.

First, you need to generate the Observation and Thought.
Observation: You need to briefly describe the current screenshot. If there are previous operations, you need to briefly describe the previous operations and the screenshot changes.
Thought: Based on Observation, You need to think about what you need to do next in order to complete the instruction.

Then, you need to generate the action based on the Thought. You can perform the following 6 actions:
1. open App Drawer. Open App drawer showing all the installed apps. You can use this to choose the best possible app to perform the given instruction.
2. click text (parameter). The parameter is the text you need to click. If there is text at the click position, use this action in preference.
3. click icon (parameter1, parameter2). The parameter1 is the description of the icon you want to click, please use this template: [color][shape], such as red circle. The parameter2 selected 1 out of 5 from the top, bottom, left, right and center, represents the general location of the icon on the screenshot.
4. swipe down, swipe up, swipe right, swipe left. These two commands don't need parameter, used for page turning.
5. type (parameter). The parameter is what you want to type. Make sure you have clicked on the input box before typing.
6. wait (parameter). Wait for a certain duration on the present screen before proceeding. The parameter is the duration in seconds.
7. back. Back to the previous page.
8. exit. Exit the app and go back to the desktop.
9. stop. If you think you have completed the instruction, then you can stop the whole process.
Note: If you try an action several times and the screen does not change, try using another action.

Finally, your output must follow the following format:
Observation: Generate as required by Observation
Thought: Generate as required by Thought
Action: If the action requires parameters, use (parameter).

'''
