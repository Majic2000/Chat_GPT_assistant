# Chat_GPT_assistant

Proof-of-concept (PoC) application called "Task-GPT" within the Django framework, integrating it with ChatGPT 3.5 and utilizing prompt engineering techniques. 

Here are some key features of Task-GPT:
1. Assign tasks effortlessly through the user-friendly GUI of the system, allowing Task-GPT to remember and reflect upon them.
2. Interact with Task-GPT using the convenient "/chat" command.
3. Discover valuable tips and tricks to enhance your productivity and effectively tackle your daily tasks.
4. Track your task progress and mark tasks as complete, ensuring you stay organized and on top of your responsibilities.
And much more! 
To keep things lightweight and efficient, the system employs functional views, server-local session data, and avoids the need for a comprehensive SQL backend. After all, simplicity is key when it comes to managing daily tasks. 

IMPROVEMENTS:
1. Move session-related operations to a separate function: Instead of checking session variables using if statements in multiple places, should create a separate function to handle session operations. This will make the code cleaner and more maintainable.
2. Refactor the POST request handling: Use a single conditional block to handle the different POST requests. This will reduce code duplication and make it easier to manage different scenarios.
3. Utilize helper functions: Extract common functionalities into helper functions to improve code readability and maintainability. For example, you can create a function to process chatbot responses and another function to render the chat template.
4. Remove unnecessary print statements: Clean up the code by removing debugging print statements that are no longer needed.
5. Change style: Use JS to change the button style once user has completed a task.
